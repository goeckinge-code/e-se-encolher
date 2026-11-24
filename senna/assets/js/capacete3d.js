/* ==========================================================================
   CAPACETE 3D — modelado no Blender (blender/capacete.py), desenhado com three.js
   · casco de vidro: transparente no centro, opaco nas bordas (Fresnel), com a
     pintura do Senna calculada no shader (amarelo, faixas verde/branca/azul,
     faixa da viseira) e reflexos de estúdio;
   · viseira fumê; "lente" que segue o cursor e deixa o casco transparente;
   · o loop é do main.js: chame frame(t) a cada quadro e set({...}) para mover.
   ========================================================================== */
function capacete3d(canvas,o={}){
 const api={ready:Promise.resolve(false),set(){},frame(){},size(){},ok:false};
 if(!window.THREE)return api;let R;try{R=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,premultipliedAlpha:true,powerPreference:"low-power"})}catch(e){return api}
 R.setClearColor(0,0);const scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(22,1,.1,50);cam.position.set(0,0,10);
 const root=new THREE.Group();scene.add(root);
 const U={uGlass:{value:o.glass?1:0},uMinA:{value:o.minA??.16},uOp:{value:1},uLens:{value:new THREE.Vector3(-1e4,-1e4,0)},uT:{value:0},uIn:{value:0}};
 const VS=`varying vec3 vP;varying vec3 vN;varying vec3 vV;varying vec3 vWN;
 void main(){vP=position;vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);vWN=normalize(mat3(modelMatrix)*normal);gl_Position=projectionMatrix*mv;}`;
 const ENV=`vec3 env(vec3 r){float y=r.y;vec3 c=mix(vec3(.16,.15,.14),vec3(.95,.93,.9),smoothstep(-.3,.9,y));
  float box=smoothstep(.55,.62,y)*(1.-smoothstep(.86,.9,y))*(1.-smoothstep(.5,.56,abs(r.x)));
  float side=smoothstep(.75,.8,abs(r.x))*(1.-smoothstep(.2,.3,abs(y)));return c+vec3(box*1.4+side*.6);}`;
 const FS_SHELL=`uniform float uMinA,uOp,uIn,uGlass;uniform vec3 uLens;varying vec3 vP;varying vec3 vN;varying vec3 vV;varying vec3 vWN;
 ${ENV}
 float band(float y,float a,float b,float aa){return smoothstep(a-aa,a+aa,y)-smoothstep(b-aa,b+aa,y);}
 void main(){vec3 p=vP;float ang=atan(p.x,p.z),side=clamp(abs(ang)/1.25,0.,1.),top=.14-.05*side*side,y=p.y,aa=max(fwidth(y)*1.2,.002);
  float fr=(1.-smoothstep(1.0,1.1,abs(ang)))*smoothstep(.12,.22,p.z);
  vec3 col=vec3(.98,.78,.02);
  float w1=band(y,top+.05,top+.07,aa)+band(y,top+.15,top+.17,aa),g1=band(y,top+.07,top+.15,aa),b1=band(y,top-.12,top-.02,aa)*(1.-fr),n1=band(y,top-.005,top+.05,aa)*fr;
  col=mix(col,vec3(.96,.96,.94),w1);col=mix(col,vec3(.02,.5,.22),g1);col=mix(col,vec3(.05,.17,.52),b1);col=mix(col,vec3(.03,.05,.14),n1);
  float stripe=clamp(w1+g1+b1+n1,0.,1.);
  vec3 n=normalize(vN);if(!gl_FrontFacing)n=-n;vec3 v=normalize(vV);
  float ndv=abs(dot(n,v)),fres=pow(1.-ndv,2.2);if(dot(n,v)<0.)n=-n;
  vec3 L=normalize(vec3(-.45,.75,.6)),H=normalize(L+v);
  float dif=clamp(dot(n,L)*.5+.5,0.,1.),spec=pow(max(dot(n,H),0.),90.);
  vec3 r=reflect(-v,n);vec3 e=env(r);
  vec3 c=col*(.35+.75*dif);c=mix(c,e*col*1.1,.18+.4*fres);c+=vec3(1.)*spec*.9+e*fres*.35;
  float a=mix(uMinA,1.,pow(fres,1.4))+spec*.6;
  if(uGlass>.5){a=mix(uMinA,.7,pow(fres,2.2))+stripe*.32+spec*.75;c=mix(c,col*1.1+e*.3,.3);}
  if(!gl_FrontFacing){c*=.45;a*=uGlass>.5?.08:.55;}
  float d=length(gl_FragCoord.xy-uLens.xy);a*=mix(1.,smoothstep(uLens.z*.55,uLens.z,d),step(1.,uLens.z));
  a=clamp(a,0.,1.)*uOp;gl_FragColor=vec4(c*a,a);}`;
 const FS_VISOR=`uniform float uOp;uniform vec3 uLens;varying vec3 vP;varying vec3 vN;varying vec3 vV;varying vec3 vWN;
 ${ENV}
 void main(){vec3 n=normalize(vN);if(!gl_FrontFacing)n=-n;vec3 v=normalize(vV);float ndv=abs(dot(n,v)),fres=pow(1.-ndv,3.);if(dot(n,v)<0.)n=-n;
  vec3 r=reflect(-v,n);vec3 e=env(r);vec3 c=vec3(.03,.035,.04)+e*(.25+.6*fres);
  float a=.5+.45*fres;float d=length(gl_FragCoord.xy-uLens.xy);a*=mix(1.,smoothstep(uLens.z*.55,uLens.z,d),step(1.,uLens.z));
  a=clamp(a,0.,1.)*uOp;gl_FragColor=vec4(c*a,a);}`;
 const mat=(fs,side)=>{const m=new THREE.ShaderMaterial({uniforms:U,vertexShader:VS,fragmentShader:fs,transparent:true,depthWrite:false,side,blending:THREE.CustomBlending,blendSrc:THREE.OneFactor,blendDst:THREE.OneMinusSrcAlphaFactor});m.extensions={derivatives:true};return m};
 api.ready=fetch(o.base+".json").then(r=>r.json()).then(meta=>{const bin=atob(meta.data),buf=new ArrayBuffer(bin.length),u8=new Uint8Array(buf);for(let i=0;i<bin.length;i++)u8[i]=bin.charCodeAt(i);
  meta.parts.forEach(pt=>{const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.BufferAttribute(new Float32Array(buf,pt.pos,pt.count*3),3));
   g.setAttribute("normal",new THREE.BufferAttribute(new Float32Array(buf,pt.nor,pt.count*3),3));g.setIndex(new THREE.BufferAttribute(new Uint16Array(buf,pt.idx,pt.index),1));
   const fs=pt.name==="viseira"?FS_VISOR:FS_SHELL;const back=new THREE.Mesh(g,mat(fs,THREE.BackSide)),front=new THREE.Mesh(g,mat(fs,THREE.FrontSide));
   back.renderOrder=pt.name==="viseira"?1:0;front.renderOrder=pt.name==="viseira"?3:2;root.add(back,front)});
  api.ok=true;canvas.classList.add("on");return true}).catch(e=>{console.warn(e);return false});
 let W=0,H=0,D=1,dirty=true;const S={x:0,y:0,s:1,yaw:0,pitch:0,roll:0,op:1,lens:null};
 api.size=(w,h)=>{const d=Math.min(1.75,devicePixelRatio||1);if(w===W&&h===H&&d===D)return;W=w;H=h;D=d;R.setPixelRatio(d);R.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix();dirty=true};
 /* x,y em fração da tela (0..1), s = largura do capacete em fração da largura */
 api.set=st=>{Object.assign(S,st);dirty=true};
 api.frame=t=>{if(!api.ok||!W)return;U.uT.value=t;
  const vh=2*cam.position.z*Math.tan(cam.fov*Math.PI/360),vw=vh*cam.aspect;
  root.position.set((S.x-.5)*vw,(.5-S.y)*vh,0);const sc=S.s*vw/1.85;root.scale.setScalar(sc);
  root.rotation.set(S.pitch,S.yaw,S.roll,"YXZ");U.uOp.value=S.op;
  if(S.lens)U.uLens.value.set(S.lens[0]*W*D,(1-S.lens[1])*H*D,S.lens[2]*W*D);else U.uLens.value.set(-1e4,-1e4,0);
  R.render(scene,cam)};
 return api}
