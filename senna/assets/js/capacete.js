/* ==========================================================================
   ROSTO + CAPACETE — entrada do site
   · parado: só o rosto;
   · toque/clique (ou o cursor passando): surgem gotas de vidro no ponto de
     contato, que mostram o capacete por dentro, se fundem entre si e somem;
   · rolagem (setFull 0..1): o capacete aparece descendo do alto da cabeça
     até cobrir o rosto.
   O laço é do main.js: size(w,h) quando muda o tamanho, frame(dt) a cada quadro.
   Sem WebGL, fica só a fotografia do rosto.
   ========================================================================== */
function capacete(stage,o){
 const cv=stage.querySelector("canvas"),gl=cv.getContext("webgl",{premultipliedAlpha:true,alpha:true,antialias:false,powerPreference:"low-power"});
 const api={setFull(){},hint(){},frame(){},size(){},pointer(){},splash(){},trail(){},ok:false};if(!gl)return api;
 const N=16,VS="attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}";
 const FS=`precision highp float;varying vec2 v;
uniform sampler2D uF,uH;uniform vec4 uHR;uniform vec3 uB[${N}];uniform float uA,uK,uFull,uPx;
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.)/k;return min(a,b)-h*h*k*.25;}
float field(vec2 q){float d=1e3;for(int i=0;i<${N};i++){vec3 b=uB[i];if(b.z>0.)d=smin(d,length(q-b.xy)-b.z,uK);}
 if(uFull>0.){float x=q.x/uA-.5;d=smin(d,q.y-(uFull*1.15-.08)+.24*x*x,uK*1.4);}return d;}
vec4 helm(vec2 uv){vec2 hu=(uv-uHR.xy)/uHR.zw;if(hu.x<0.||hu.x>1.||hu.y<0.||hu.y>1.)return vec4(0.);return texture2D(uH,hu);}
void main(){vec2 k=vec2(uA,1.),q=v*k;float fade=smoothstep(1.,.9,v.y);
 vec4 f=texture2D(uF,v);f.a*=fade;f.rgb*=f.a;
 float d=field(q);
 if(d>.05){gl_FragColor=f;return;}
 f.rgb*=1.-.14*(1.-smoothstep(-.01,.045,field(q-vec2(.006,-.012))));
 float e=.004;vec2 g=vec2(field(q+vec2(e,0.))-d,field(q+vec2(0.,e))-d)/e;
 float inside=1.-smoothstep(-uPx,uPx,d),dep=clamp(-d/.05,0.,1.),edge=1.-dep;
 vec3 n=normalize(vec3(g*edge*edge*1.5,.4+dep));
 vec2 rv=v-(n.xy*.03*edge)/k;
 vec4 h=helm(rv),fr=texture2D(uF,rv);h.a*=mix(.78,1.,uFull)*mix(1.,fade,.6);fr.a*=fade;
 vec3 c=h.rgb*h.a+fr.rgb*fr.a*(1.-h.a);float a=h.a+fr.a*(1.-h.a);
 c*=.88+.12*dep;
 float spec=pow(max(dot(n,normalize(vec3(-.45,.62,.64))),0.),40.),fres=pow(1.-n.z,2.4);
 c+=vec3(1.)*(spec*.5+fres*.1)*a;
 vec3 col=mix(f.rgb,c,inside);float al=mix(f.a,a,inside);
 col*=1.-.3*(1.-smoothstep(0.,uPx*1.8,abs(d)))*al;
 gl_FragColor=vec4(col,al);}`;
 const sh=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(x);return x};
 let pg;try{pg=gl.createProgram();gl.attachShader(pg,sh(gl.VERTEX_SHADER,VS));gl.attachShader(pg,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(pg);gl.useProgram(pg)}catch(e){console.warn(e);return api}
 const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
 const lp=gl.getAttribLocation(pg,"p");gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
 const U=n=>gl.getUniformLocation(pg,n),uB=U("uB"),uA=U("uA"),uK=U("uK"),uFull=U("uFull"),uPx=U("uPx");
 gl.uniform4fv(U("uHR"),o.helm);gl.uniform1i(U("uF"),0);gl.uniform1i(U("uH"),1);
 const tex=(img,unit)=>{const t=gl.createTexture();gl.activeTexture(gl.TEXTURE0+unit);gl.bindTexture(gl.TEXTURE_2D,t);gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,false);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.CLAMP_TO_EDGE));
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR)};
 const load=s=>new Promise((ok,no)=>{const i=new Image();i.decoding="async";i.onload=()=>ok(i);i.onerror=no;i.src=s});

 /* gotas: nascem no ponto de contato, crescem, flutuam um pouco e somem */
 const reduce=matchMedia("(prefers-reduced-motion:reduce)").matches;
 const D=[];for(let i=0;i<N;i++)D.push({x:0,y:0,vx:0,vy:0,r:0,age:9,life:1});
 let slot=0,A=.8,full=0,ready=false,W=0,H=0,qual=1,slow=0,cssW=0,cssH=0,idle=0,lastT=-1,clock=0;
 const P=new Float32Array(N*3);
 function drop(x,y,r,life,vx=0,vy=0){const d=D[slot++%N];d.x=x;d.y=y;d.r=r;d.age=0;d.life=life;d.vx=vx;d.vy=vy;idle=0}
 api.size=(w,h)=>{cssW=w;cssH=h;const s=Math.min(1.25,devicePixelRatio||1)*qual,pw=Math.round(w*s),ph=Math.round(h*s);
  if(pw!==W||ph!==H){W=cv.width=pw;H=cv.height=ph;gl.viewport(0,0,pw,ph);A=w/h;gl.uniform1f(uA,A);gl.uniform1f(uPx,1.6/ph);idle=0}};
 /* toque/clique: um pequeno grupo de gotas no ponto */
 api.splash=(x,y)=>{if(reduce)return;drop(x,y,.075,1.9);for(let i=0;i<4;i++){const a=Math.random()*TAU,s=.04+Math.random()*.05;drop(x+Math.cos(a)*s,y+Math.sin(a)*s,.025+Math.random()*.03,1.4+Math.random()*.6,Math.cos(a)*.03,Math.sin(a)*.03)}};
 /* cursor ou dedo arrastando: uma gota a cada pedacinho do caminho */
 api.trail=(x,y)=>{if(reduce||clock-lastT<.07)return;lastT=clock;drop(x,y,.045+Math.random()*.02,1.2+Math.random()*.4)};
 function step(dt){clock+=dt;let alive=0;
  D.forEach((d,i)=>{d.age+=dt;const k=d.age/d.life;let r=0;
   if(k<1){alive++;r=d.r*EO(cl(k/.22))*(1-ES(cl((k-.55)/.45)));d.x+=d.vx*dt;d.y+=d.vy*dt-.012*dt;d.vx*=.96;d.vy*=.96}
   P[i*3]=d.x;P[i*3+1]=d.y;P[i*3+2]=r});
  return alive}
 api.frame=dt=>{if(!ready||!cssW||document.hidden)return;
  const alive=step(dt);
  /* nada se movendo: desenha uma última vez e para (não gasta a placa de vídeo) */
  if(!alive){if(idle++>1)return}else idle=0;
  if(dt>.028){if((slow+=dt)>.7&&qual>.6){qual*=.85;slow=0;W=0;api.size(cssW,cssH)}}else slow=Math.max(0,slow-dt*.5);
  gl.uniform3fv(uB,P);gl.uniform1f(uK,.06);gl.uniform1f(uFull,full);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)};
 api.ready=Promise.all([load(o.face),load(o.helmet)]).then(([f,h])=>{tex(f,0);tex(h,1);ready=true;api.ok=true;stage.classList.add("gl")}).catch(e=>console.warn(e));
 api.setFull=v=>{v=cl(v);if(Math.abs(v-full)>1e-4){full=v;idle=0}};
 return api}
