/* ==========================================================================
   ROSTO + CAPACETE — entrada do site
   Bolhas de água sobre o rosto (a lógica do CandyShoal, em 2D e sem cores):
   as bolhas flutuam, respiram e se fundem (smooth-min de círculos); as bordas
   ondulam como água, por dentro a superfície tem ondinhas que correm e
   cáusticas, e o capacete aparece refratado, translúcido, deixando o rosto
   visível por baixo.
   · toque/clique: um anel de onda se espalha pelo rosto e pela água e as bolhas
     são empurradas; arrastar o cursor deixa ondinhas; segurar junta as bolhas;
   · setFull(0..1): a água cresce e veste o capacete inteiro (rolagem);
   · o laço é do main.js: size(w,h) quando muda o tamanho, frame(dt) a cada quadro.
   Sem WebGL, fica só a fotografia do rosto.
   ========================================================================== */
function capacete(stage,o){
 const cv=stage.querySelector("canvas"),gl=cv.getContext("webgl",{premultipliedAlpha:true,alpha:true,antialias:false,powerPreference:"low-power"});
 const api={setFull(){},hint(){},frame(){},size(){},pointer(){},splash(){},trail(){},ok:false};if(!gl)return api;
 const N=12,VS="attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}";
 const FS=`precision highp float;varying vec2 v;
uniform sampler2D uF,uH;uniform vec4 uHR;uniform vec3 uB[${N}];uniform vec4 uRp[4];uniform float uA,uK,uFull,uPx,uT;
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.)/k;return min(a,b)-h*h*k*.25;}
float h1(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float ns(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h1(i),h1(i+vec2(1.,0.)),f.x),mix(h1(i+vec2(0.,1.)),h1(i+1.),f.x),f.y);}
float field(vec2 q){float d=1e3;for(int i=0;i<${N};i++){vec3 b=uB[i];if(b.z>0.)d=smin(d,length(q-b.xy)-b.z,uK);}
 if(uFull>0.)d=smin(d,q.y-(uFull*1.45-.3)+.05*sin(q.x*9.+uT*1.3),uK*1.6);return d;}
vec4 helm(vec2 uv){vec2 hu=(uv-uHR.xy)/uHR.zw;if(hu.x<0.||hu.x>1.||hu.y<0.||hu.y>1.)return vec4(0.);return texture2D(uH,hu);}
void main(){vec2 k=vec2(uA,1.),q=v*k;
 /* toques: anéis de onda que se espalham pelo rosto e pela água */
 vec2 disp=vec2(0.);float ring=0.;
 for(int i=0;i<4;i++){vec4 r=uRp[i];if(r.w<=0.)continue;vec2 dq=q-r.xy;float dist=length(dq),front=r.z*.55,x=dist-front;
  float env=exp(-x*x/.0018)*exp(-r.z*1.6)*r.w;disp+=dq/(dist+1e-4)*sin(x*90.)*env*.012;ring+=env*(.5+.5*sin(x*90.));}
 q+=disp;
 /* as bordas fluem como água: o deslocamento é calculado uma vez por pixel */
 vec2 wq=q+.024*vec2(ns(q*4.+vec2(uT*.5,0.))-.5,ns(q*4.+vec2(5.2,-uT*.45))-.5)*2.;
 float d=field(wq);
 float fade=smoothstep(1.,.9,v.y);
 vec2 vv=v+disp/k;
 vec4 f=texture2D(uF,vv);f.a*=fade;f.rgb*=f.a;f.rgb+=vec3(1.)*ring*.06*f.a;
 if(d>.06){gl_FragColor=f;return;}   /* longe da água: só o rosto (a maior parte dos pixels) */
 f.rgb*=1.-.12*(1.-smoothstep(-.01,.05,field(wq-vec2(.006,-.012))));
 float e=.006;vec2 g=vec2(field(wq+vec2(e,0.))-d,field(wq+vec2(0.,e))-d)/e;
 float inside=1.-smoothstep(-uPx,uPx,d);
 float dep=clamp(-d/.06,0.,1.),edge=1.-dep;
 vec2 rip=vec2(sin(q.y*34.+uT*2.4+ns(q*6.)*5.),cos(q.x*30.-uT*2.+ns(q*7.+3.)*5.))*.07*(.35+.65*dep);
 vec3 n=normalize(vec3(g*edge*edge*1.4+rip+disp*30.,.42+dep));
 vec2 rv=vv-(n.xy*.034*(.4+.6*edge))/k;
 vec4 h=helm(rv),fr=texture2D(uF,rv);h.a*=.62*mix(1.,fade,.6);fr.a*=fade;
 vec3 c=h.rgb*h.a+fr.rgb*fr.a*(1.-h.a);float a=h.a+fr.a*(1.-h.a);
 c*=.9+.1*dep;
 float ca=pow(1.-abs(sin(q.x*21.+uT*1.2+sin(q.y*16.-uT)*1.6)*sin(q.y*18.-uT*1.05+sin(q.x*12.+uT*.8)*1.6)),14.);
 float spec=pow(max(dot(n,normalize(vec3(-.45,.62,.64))),0.),36.);
 float fres=pow(1.-n.z,2.2);
 c+=vec3(1.)*(spec*.45+fres*.1+ca*.16)*a;
 vec3 col=mix(f.rgb,c,inside);float al=mix(f.a,a,inside);
 col+=vec3(1.)*.28*(1.-smoothstep(0.,uPx*2.5,abs(d)))*al;
 gl_FragColor=vec4(col,al);}`;
 const sh=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(x);return x};
 let pg;try{pg=gl.createProgram();gl.attachShader(pg,sh(gl.VERTEX_SHADER,VS));gl.attachShader(pg,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(pg);gl.useProgram(pg)}catch(e){console.warn(e);return api}
 const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
 const lp=gl.getAttribLocation(pg,"p");gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
 const U=n=>gl.getUniformLocation(pg,n),uB=U("uB"),uA=U("uA"),uK=U("uK"),uFull=U("uFull"),uPx=U("uPx"),uT=U("uT"),uRp=U("uRp");
 gl.uniform4fv(U("uHR"),o.helm);gl.uniform1i(U("uF"),0);gl.uniform1i(U("uH"),1);
 const tex=(img,unit)=>{const t=gl.createTexture();gl.activeTexture(gl.TEXTURE0+unit);gl.bindTexture(gl.TEXTURE_2D,t);gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,false);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.CLAMP_TO_EDGE));
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR)};
 const load=s=>new Promise((ok,no)=>{const i=new Image();i.decoding="async";i.onload=()=>ok(i);i.onerror=no;i.src=s});

 /* as bolhas: casas espalhadas sobre a cabeça, em 4 tamanhos (como o CandyShoal) */
 const reduce=matchMedia("(prefers-reduced-motion:reduce)").matches;
 let A=.8;const head=o.head||[.5,.4,.27];
 const rnd=(s=>()=>{s=(s+0x6d2b79f5)|0;let t=Math.imul(s^(s>>>15),1|s);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296})(7);
 const SIZES=[.072,.05,.034,.02],CLS=[0,0,1,1,1,1,2,2,2,3,3,3];
 const B=CLS.map((c,i)=>{let x,y;do{x=rnd()*2-1;y=rnd()*2-1}while(x*x+y*y>1);
  return{hx:x,hy:y,r:SIZES[c]*(.88+rnd()*.24),ph:[0,1,2,3].map(()=>rnd()*TAU),fr:[0,1,2,3].map(k=>TAU*(k%2?.12+rnd()*.18:.07+rnd()*.14)),bp:rnd()*TAU,ox:0,oy:0,vx:0,vy:0,tx:0,ty:0,born:.15+i*.08}});
 const P=new Float32Array(N*3),ptr={x:0,y:0,in:false,down:false};
 let full=0,t=0,acc=0,ready=false,W=0,H=0,introT=0,qual=1,slow=0,cssW=0,cssH=0;
 api.size=(w,h)=>{cssW=w;cssH=h;const D=Math.min(1.25,devicePixelRatio||1)*qual,pw=Math.round(w*D),ph=Math.round(h*D);
  if(pw!==W||ph!==H){W=cv.width=pw;H=cv.height=ph;gl.viewport(0,0,pw,ph);A=w/h;gl.uniform1f(uA,A);gl.uniform1f(uPx,1.6/ph)}};
 /* ponteiro em coordenadas do palco: x e y divididos pela altura do palco */
 api.pointer=(x,y,inside,down)=>{ptr.x=x;ptr.y=y;ptr.in=inside;ptr.down=down};
 /* toque/clique: um anel de onda e um empurrão nas bolhas; arrastar deixa ondinhas */
 const RP=new Float32Array(16);let rpi=0,lastRip=0;
 api.splash=(x,y,amp=1)=>{if(reduce)return;const j=rpi++%4;RP[j*4]=x;RP[j*4+1]=y;RP[j*4+2]=0;RP[j*4+3]=amp;
  if(amp<.6)return;B.forEach(b=>{const dx=(b.x0+b.ox)-x,dy=(b.y0+b.oy)-y,d=Math.hypot(dx,dy)||1e-4,k=1.6*amp*Math.exp(-d*d/(.22*.22));b.vx+=dx/d*k;b.vy+=dy/d*k})};
 api.trail=(x,y)=>{if(t-lastRip>.18){lastRip=t;api.splash(x,y,.35)}};
 function step(dt){t+=reduce?0:dt;introT+=dt;
  const cx=head[0]*A,cy=head[1],R=head[2],grow=1+full*1.9,pull=1-full*.45;
  B.forEach(b=>{const w=.05,wx=w*(.62*Math.sin(b.fr[0]*t+b.ph[0])+.38*Math.sin(b.fr[1]*t+b.ph[1])),wy=w*(.62*Math.sin(b.fr[2]*t+b.ph[2])+.38*Math.sin(b.fr[3]*t+b.ph[3]));
   const hx=cx+(b.hx*R+wx)*pull,hy=cy+(b.hy*R*1.08+wy)*pull;b.x0=hx;b.y0=hy;
   let tx=0,ty=0;if(ptr.in&&!reduce){const dx=hx-ptr.x,dy=hy-ptr.y,d2=dx*dx+dy*dy;
    if(ptr.down){const k=.85*Math.exp(-d2/(.3*.3));tx=-dx*k;ty=-dy*k}else{const d=Math.sqrt(d2)||1e-4,k=.07*Math.exp(-d2/(.16*.16));tx=dx/d*k;ty=dy/d*k}}
   b.tx=tx;b.ty=ty});
  acc=Math.min(acc+dt,8/120);while(acc>=1/120){acc-=1/120;B.forEach(b=>{b.vx+=(70*(b.tx-b.ox)-5.4*b.vx)/120;b.vy+=(70*(b.ty-b.oy)-5.4*b.vy)/120;b.ox+=b.vx/120;b.oy+=b.vy/120})}
  B.forEach((b,i)=>{const br=.5+.5*Math.cos(TAU*t/3.2+b.bp),bi=EO(cl((introT-b.born)/.9));
   P[i*3]=b.x0+b.ox;P[i*3+1]=b.y0+b.oy;P[i*3+2]=b.r*(1-.18*br)*grow*bi})}
 api.frame=dt=>{if(!ready||!cssW||document.hidden)return;
  if(dt>.028){if((slow+=dt)>.7&&qual>.6){qual*=.85;slow=0;W=0;api.size(cssW,cssH)}}else slow=Math.max(0,slow-dt*.5);
  step(dt);for(let j=0;j<4;j++)if(RP[j*4+3]>0){RP[j*4+2]+=dt;if(RP[j*4+2]>2.2)RP[j*4+3]=0}gl.uniform4fv(uRp,RP);gl.uniform3fv(uB,P);gl.uniform1f(uK,.075+full*.05);gl.uniform1f(uFull,full);gl.uniform1f(uT,t);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)};
 api.ready=Promise.all([load(o.face),load(o.helmet)]).then(([f,h])=>{tex(f,0);tex(h,1);ready=true;api.ok=true;stage.classList.add("gl")}).catch(e=>console.warn(e));
 api.setFull=v=>{full=cl(v)};
 api.hint=()=>{introT=0};
 return api}
