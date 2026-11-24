/* ==========================================================================
   CAPACETE 3D — feito com as fotografias reais do capacete (9 vistas)
   · o molde é gerado aqui mesmo: uma esfera deformada em casco fechado, com
     queixeira e o corte do pescoço inclinado;
   · cada vista (frente, laterais, traseira, topo…) é projetada no molde a partir
     do ângulo em que foi fotografada; cada ponto do casco mistura as fotos
     tiradas na direção para onde ele aponta. Assim a pintura, os logos, a faixa
     da viseira e a assinatura são os do capacete de verdade, girando em 3D;
   · modo vidro (entrada): transparente no centro, com lente no cursor;
   · o laço é do main.js: chame frame(t) a cada quadro e set({...}) para mover.
   ========================================================================== */
const CAPACETE_VISTAS=[ /* ângulo (graus) e inclinação da câmera de cada foto do atlas, na ordem das células */
 {yaw:0,pitch:6},{yaw:-28,pitch:6},{yaw:-74,pitch:4},
 {yaw:-142,pitch:2},{yaw:180,pitch:4},{yaw:160,pitch:2},
 {yaw:62,pitch:-4},{yaw:30,pitch:-10},{top:true}];
function capacete3d(canvas,o={}){
 const api={ready:Promise.resolve(false),set(){},frame(){},size(){},ok:false};
 if(!window.THREE)return api;let R;try{R=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,premultipliedAlpha:true,powerPreference:"low-power"})}catch(e){return api}
 R.setClearColor(0,0);const scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(22,1,.1,50);cam.position.set(0,0,10);
 const root=new THREE.Group();scene.add(root);

 /* molde do casco: x direita, y cima, z frente */
 const CUT=(z)=>-.66-.404*Math.max(0,z)+.1*Math.max(0,-z);
 const geo=new THREE.SphereGeometry(1,144,108),P=geo.attributes.position;
 for(let i=0;i<P.count;i++){let x=P.getX(i),y=P.getY(i),z=P.getZ(i);
  x*=.9;z*=z>0?1.06:1.14;y*=1.02;
  if(y<0){const k=Math.pow(Math.max(0,z),1.2);z+=.24*k*(-y);y*=1+.2*k;x*=1+.05*(-y)*(1-k)}
  P.setXYZ(i,x,Math.max(y,CUT(z)-.02),z)}
 geo.computeVertexNormals();

 /* vistas: direção da câmera, eixos da imagem e caixa da projeção de cada foto */
 const NV=CAPACETE_VISTAS.length,D=[],RG=[],UP=[],BB=[];
 const vtmp=new THREE.Vector3();
 CAPACETE_VISTAS.forEach(v=>{let d,u;
  if(v.top){d=new THREE.Vector3(0,1,0);u=new THREE.Vector3(0,0,-1)}
  else{const a=v.yaw*Math.PI/180,p=v.pitch*Math.PI/180;d=new THREE.Vector3(-Math.sin(a)*Math.cos(p),Math.sin(p),Math.cos(a)*Math.cos(p));u=new THREE.Vector3(Math.sin(a)*Math.sin(p),Math.cos(p),-Math.cos(a)*Math.sin(p))}
  const r=new THREE.Vector3().crossVectors(u,d).normalize();
  let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;for(let i=0;i<P.count;i++){vtmp.fromBufferAttribute(P,i);if(vtmp.y<CUT(vtmp.z)-.01)continue;
   const px=vtmp.dot(r),py=vtmp.dot(u);x0=Math.min(x0,px);x1=Math.max(x1,px);y0=Math.min(y0,py);y1=Math.max(y1,py)}
  D.push(d);RG.push(r);UP.push(u);BB.push(new THREE.Vector4(x0,y0,x1,y1))});

 const U={uAtlas:{value:null},uD:{value:D},uR:{value:RG},uU:{value:UP},uBB:{value:BB},uGlass:{value:o.glass?1:0},uMinA:{value:o.minA??.06},uOp:{value:1},uLens:{value:new THREE.Vector3(-1e4,-1e4,0)}};
 const VS=`varying vec3 vP;varying vec3 vON;varying vec3 vN;varying vec3 vV;
 void main(){vP=position;vON=normal;vec4 mv=modelViewMatrix*vec4(position,1.);vN=normalize(normalMatrix*normal);vV=normalize(-mv.xyz);gl_Position=projectionMatrix*mv;}`;
 const FS=`uniform sampler2D uAtlas;uniform vec3 uD[${NV}];uniform vec3 uR[${NV}];uniform vec3 uU[${NV}];uniform vec4 uBB[${NV}];
 uniform float uGlass,uMinA,uOp,uBack;uniform vec3 uLens;varying vec3 vP;varying vec3 vON;varying vec3 vN;varying vec3 vV;
 void main(){vec3 p=vP;if(p.y<-.66-.404*max(0.,p.z)+.1*max(0.,-p.z)+.003)discard;
  vec3 on=normalize(vON),acc=vec3(0.);float ws=0.,best=-1.;float dd[${NV}];vec2 tt[${NV}];
  for(int i=0;i<${NV};i++){vec4 b=uBB[i];vec2 t=(vec2(dot(p,uR[i]),dot(p,uU[i]))-b.xy)/(b.zw-b.xy);tt[i]=t;
   float d=dot(on,uD[i]);if(t.x<0.||t.x>1.||t.y<0.||t.y>1.)d=-2.;dd[i]=d;best=max(best,d);}
  for(int i=0;i<${NV};i++){if(dd[i]<-1.)continue;vec2 t=tt[i];
   float w=exp(22.*(dd[i]-best))*(.15+.85*smoothstep(0.,.06,min(min(t.x,1.-t.x),min(t.y,1.-t.y))));
   float fi=float(i);vec2 cell=vec2(mod(fi,3.),floor(fi/3.));
   vec2 uv=(cell+vec2(.008+t.x*.984,.008+(1.-t.y)*.984))/3.;
   acc+=texture2D(uAtlas,uv).rgb*w;ws+=w;}
  vec3 col=ws>1e-4?acc/ws:vec3(.97,.76,.05);
  vec3 n=normalize(vN),v=normalize(vV);if(dot(n,v)<0.)n=-n;
  float ndv=abs(dot(n,v)),fres=pow(1.-ndv,2.4);
  vec3 L=normalize(vec3(-.45,.75,.6)),H=normalize(L+v);float spec=pow(max(dot(n,H),0.),70.);
  vec3 c=col*(.9+.18*clamp(dot(n,L),0.,1.))+vec3(1.)*spec*.45+fres*.12;
  float a=1.;
  if(uGlass>.5){float lum=dot(col,vec3(.3,.59,.11));a=mix(uMinA,.92,pow(fres,1.5))+(1.-smoothstep(.08,.35,lum))*.45+spec*.6;}
  if(uBack>.5){c=vec3(.05,.05,.055)+fres*.05;a=uGlass>.5?a*.15:1.;}
  float d=length(gl_FragCoord.xy-uLens.xy);a*=mix(1.,smoothstep(uLens.z*.55,uLens.z,d),step(1.,uLens.z));
  a=clamp(a,0.,1.)*uOp;gl_FragColor=vec4(c*a,a);}`;
 const mat=side=>new THREE.ShaderMaterial({uniforms:Object.assign({},U,{uBack:{value:side===THREE.BackSide?1:0}}),vertexShader:VS,fragmentShader:FS,transparent:true,depthWrite:!o.glass,side,blending:THREE.CustomBlending,blendSrc:THREE.OneFactor,blendDst:THREE.OneMinusSrcAlphaFactor});
 const back=new THREE.Mesh(geo,mat(THREE.BackSide)),front=new THREE.Mesh(geo,mat(THREE.FrontSide));back.renderOrder=0;front.renderOrder=1;if(o.glass)root.add(front);else root.add(back,front);

 api.ready=new Promise(ok=>{new THREE.TextureLoader().load(o.atlas,tx=>{tx.flipY=false;tx.anisotropy=Math.min(8,R.capabilities.getMaxAnisotropy());tx.needsUpdate=true;
  U.uAtlas.value=tx;api.ok=true;canvas.classList.add("on");ok(true)},undefined,()=>ok(false))});
 let W=0,H=0,DPR=1;const S={x:0,y:0,s:1,yaw:0,pitch:0,roll:0,op:1,lens:null};
 api.size=(w,h)=>{const d=Math.min(1.75,devicePixelRatio||1);if(w===W&&h===H&&d===DPR)return;W=w;H=h;DPR=d;R.setPixelRatio(d);R.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()};
 /* x,y em fração da tela (0..1), s = largura do capacete em fração da largura */
 api.set=st=>{Object.assign(S,st)};
 api.frame=()=>{if(!api.ok||!W)return;
  const vh=2*cam.position.z*Math.tan(cam.fov*Math.PI/360),vw=vh*cam.aspect;
  root.position.set((S.x-.5)*vw,(.5-S.y)*vh,0);root.scale.setScalar(S.s*vw/1.85);
  root.rotation.set(S.pitch,S.yaw,S.roll,"YXZ");U.uOp.value=S.op;
  if(S.lens)U.uLens.value.set(S.lens[0]*W*DPR,(1-S.lens[1])*H*DPR,S.lens[2]*W*DPR);else U.uLens.value.set(-1e4,-1e4,0);
  R.render(scene,cam)};
 return api}
