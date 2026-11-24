/* ==========================================================================
   ROSTO + CAPACETE — entrada do site
   Um cardume de gotas de vidro (a lógica do CandyShoal, em 2D e sem cores):
   as gotas flutuam, respiram e se fundem como xarope (smooth-min de círculos).
   Dentro delas aparece o capacete, refratado como por uma lente; fora, o rosto.
   · sozinhas: deriva + respiração, sempre deixando parte do rosto à vista;
   · cursor/dedo: empurra as gotas (molas, com um balanço de gelatina);
     apertar e segurar junta as gotas próximas numa só;
   · setFull(0..1): as gotas crescem e se fundem até vestir o capacete inteiro.
   Sem WebGL, fica só a fotografia do rosto.
   ========================================================================== */
function capacete(stage,o){
 const cv=stage.querySelector("canvas"),gl=cv.getContext("webgl",{premultipliedAlpha:true,alpha:true,antialias:false,powerPreference:"low-power"});
 const api={setFull(){},hint(){},ok:false};if(!gl)return api;
 const N=14,VS="attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}";
 const FS=`precision highp float;varying vec2 v;
uniform sampler2D uF,uH;uniform vec4 uHR;uniform vec3 uB[${N}];uniform float uA,uK,uFull,uPx,uIn;
float smin(float a,float b,float k){float h=max(k-abs(a-b),0.)/k;return min(a,b)-h*h*k*.25;}
float sdf(vec2 q){float d=1e3;
 for(int i=0;i<${N};i++){vec3 b=uB[i];if(b.z>0.)d=smin(d,length(q-b.xy)-b.z,uK);}
 float w=q.y-(uFull*1.45-.3)+.06*sin(q.x*9.+uFull*6.);
 return uFull>0.?smin(d,w,uK*1.6):d;}
vec4 helm(vec2 uv){vec2 hu=(uv-uHR.xy)/uHR.zw;if(hu.x<0.||hu.x>1.||hu.y<0.||hu.y>1.)return vec4(0.);return texture2D(uH,hu);}
void main(){vec2 k=vec2(uA,1.),q=v*k;
 float d=sdf(q),e=.004;
 vec2 g=vec2(sdf(q+vec2(e,0.))-sdf(q-vec2(e,0.)),sdf(q+vec2(0.,e))-sdf(q-vec2(0.,e)))/(2.*e);
 float inside=1.-smoothstep(-uPx,uPx,d);
 float dep=clamp(-d/.055,0.,1.),edge=1.-dep;
 vec3 n=normalize(vec3(g*edge*edge*1.7,.35+dep));
 float fade=smoothstep(1.,.9,v.y);
 /* fora: o rosto, com a sombra das gotas */
 vec4 f=texture2D(uF,v);f.a*=fade;f.rgb*=f.a;
 float ds=sdf(q-vec2(.008,-.016));
 f.rgb*=1.-.22*(1.-smoothstep(-.01,.05,ds))*(1.-inside);
 /* dentro: capacete sobre o rosto, refratados pela gota */
 vec2 rv=v-n.xy*.03*edge/k;
 vec4 h=helm(rv),fr=texture2D(uF,rv);h.a*=mix(1.,fade,.6);fr.a*=fade;
 vec3 c=h.rgb*h.a+fr.rgb*fr.a*(1.-h.a);float a=h.a+fr.a*(1.-h.a);
 c*=.8+.2*dep;
 float spec=pow(max(dot(n,normalize(vec3(-.45,.62,.64))),0.),42.);
 float fres=pow(1.-n.z,2.5);
 c+=vec3(1.)*(spec*.6+fres*.12)*a;
 vec3 col=mix(f.rgb,c,inside);float al=mix(f.a,a,inside);
 col*=1.-.35*(1.-smoothstep(0.,uPx*1.6,abs(d)))*al;
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

 /* o cardume: casas espalhadas sobre a cabeça, em 4 tamanhos (como o CandyShoal) */
 const reduce=matchMedia("(prefers-reduced-motion:reduce)").matches;
 let A=.8;const head=o.head||[.5,.4,.27];
 const rnd=(s=>()=>{s=(s+0x6d2b79f5)|0;let t=Math.imul(s^(s>>>15),1|s);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296})(7);
 const SIZES=[.088,.062,.042,.024],CLS=[0,0,0,1,1,1,1,2,2,2,2,3,3,3];
 const B=CLS.map((c,i)=>{let x,y;do{x=rnd()*2-1;y=rnd()*2-1}while(x*x+y*y>1);
  return{hx:x,hy:y,r:SIZES[c]*(.88+rnd()*.24),ph:[0,1,2,3].map(()=>rnd()*TAU),fr:[0,1,2,3].map(k=>TAU*(k%2?.16+rnd()*.24:.09+rnd()*.18)),bp:rnd()*TAU,ox:0,oy:0,vx:0,vy:0,tx:0,ty:0,born:.15+i*.07}});
 const P=new Float32Array(N*3),ptr={x:0,y:0,in:false,down:false};
 let full=0,t=0,acc=0,ready=false,vis=true,last=performance.now(),W=0,H=0,introT=0,qual=1,slow=0;
 function size(){const r=stage.getBoundingClientRect();if(!r.width)return;const D=Math.min(1.5,devicePixelRatio||1)*qual,w=Math.round(r.width*D),h=Math.round(r.height*D);
  if(w!==W||h!==H){W=cv.width=w;H=cv.height=h;gl.viewport(0,0,w,h);A=r.width/r.height;gl.uniform1f(uA,A);gl.uniform1f(uPx,1.6/h)}}
 const at=e=>{const r=stage.getBoundingClientRect();ptr.x=(e.clientX-r.left)/r.height;ptr.y=(e.clientY-r.top)/r.height};
 stage.addEventListener("pointermove",e=>{at(e);ptr.in=true},{passive:true});
 stage.addEventListener("pointerdown",e=>{at(e);ptr.in=true;ptr.down=true},{passive:true});
 stage.addEventListener("pointerleave",()=>{ptr.in=false;ptr.down=false},{passive:true});
 addEventListener("pointerup",e=>{ptr.down=false;if(e.pointerType==="touch")ptr.in=false},{passive:true});
 addEventListener("pointercancel",()=>{ptr.down=false;ptr.in=false},{passive:true});
 new IntersectionObserver(es=>{vis=es[0].isIntersecting},{rootMargin:"100px"}).observe(stage);
 function step(dt){t+=reduce?0:dt;introT+=dt;
  const cx=head[0]*A,cy=head[1],R=head[2],grow=1+full*1.6,pull=1-full*.45;
  B.forEach((b,i)=>{const w=.045,wx=w*(.62*Math.sin(b.fr[0]*t+b.ph[0])+.38*Math.sin(b.fr[1]*t+b.ph[1])),wy=w*(.62*Math.sin(b.fr[2]*t+b.ph[2])+.38*Math.sin(b.fr[3]*t+b.ph[3]));
   const hx=cx+(b.hx*R*.95+wx)*pull,hy=cy+(b.hy*R*1.05+wy)*pull;b.x0=hx;b.y0=hy;
   let tx=0,ty=0;if(ptr.in&&!reduce){const dx=hx-ptr.x,dy=hy-ptr.y,d2=dx*dx+dy*dy;
    if(ptr.down){const k=.85*Math.exp(-d2/(.3*.3));tx=-dx*k;ty=-dy*k}else{const d=Math.sqrt(d2)||1e-4,k=.07*Math.exp(-d2/(.16*.16));tx=dx/d*k;ty=dy/d*k}}
   b.tx=tx;b.ty=ty});
  acc=Math.min(acc+dt,8/120);while(acc>=1/120){acc-=1/120;B.forEach(b=>{b.vx+=(70*(b.tx-b.ox)-5.4*b.vx)/120;b.vy+=(70*(b.ty-b.oy)-5.4*b.vy)/120;b.ox+=b.vx/120;b.oy+=b.vy/120})}
  B.forEach((b,i)=>{const br=.5+.5*Math.cos(TAU*t/2.85+b.bp),bi=EO(cl((introT-b.born)/.9));
   P[i*3]=b.x0+b.ox;P[i*3+1]=b.y0+b.oy;P[i*3+2]=b.r*(1-.16*br)*grow*bi})}
 function frame(now){requestAnimationFrame(frame);const ms=now-last,dt=Math.min(.05,ms/1000);last=now;if(!ready||!vis||document.hidden)return;
  if(ms>28){if((slow+=ms)>700&&qual>.6){qual*=.85;slow=0;W=0}}else slow=Math.max(0,slow-ms*.5);
  size();step(dt);gl.uniform3fv(uB,P);gl.uniform1f(uK,.07+full*.05);gl.uniform1f(uFull,full);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)}
 api.ready=Promise.all([load(o.face),load(o.helmet)]).then(([f,h])=>{tex(f,0);tex(h,1);ready=true;api.ok=true;stage.classList.add("gl");size();requestAnimationFrame(frame)}).catch(e=>console.warn(e));
 api.setFull=v=>{full=cl(v)};
 api.hint=()=>{introT=0};
 return api}
