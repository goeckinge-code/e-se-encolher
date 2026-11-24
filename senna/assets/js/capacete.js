/* ==========================================================================
   ROSTO + CAPACETE — entrada do site
   O capacete aparece sobre o rosto por uma máscara líquida (metaballs) que
   segue o rastro do cursor/dedo; a borda ondula com ruído, refrata um pouco a
   imagem e ganha um brilho amarelo. setFull(0..1) veste o capacete inteiro
   (usado pela rolagem). Sem WebGL, fica só a fotografia do rosto.
   ========================================================================== */
function capacete(stage,o){
 const cv=stage.querySelector("canvas"),gl=cv.getContext("webgl",{premultipliedAlpha:true,alpha:true,antialias:false});
 const api={setFull(){},hint(){},ok:false};if(!gl)return api;
 const N=24,VS="attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;v.y=1.-v.y;gl_Position=vec4(p,0.,1.);}";
 const FS=`precision highp float;varying vec2 v;uniform sampler2D uF,uH;uniform vec4 uHR;uniform vec3 uP[${N}];uniform float uA,uT,uFull;uniform vec2 uC;
float h1(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float ns(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h1(i),h1(i+vec2(1.,0.)),f.x),mix(h1(i+vec2(0.,1.)),h1(i+1.),f.x),f.y);}
void main(){vec2 k=vec2(uA,1.),q=v*k;float fl=0.;
 for(int i=0;i<${N};i++){vec2 d=q-uP[i].xy*k;fl+=uP[i].z*uP[i].z/(dot(d,d)+1e-4);}
 fl+=clamp((uFull*1.32-.16-v.y+(uC.x-v.x)*(uC.x-v.x)*.35)*7.,0.,4.);
 float n=ns(v*6.+vec2(uT*.35,-uT*.5))*.6+ns(v*17.-uT*.8)*.4;
 float e=fl*(.7+n*.6);
 float m=smoothstep(.88,1.12,e);
 float rim=smoothstep(.45,1.,e)*(1.-smoothstep(1.,1.7,e));
 vec2 w=(n-.5)*vec2(.018,.012)*rim;
 vec2 hu=(v+w-uHR.xy)/uHR.zw;
 vec4 hc=texture2D(uH,hu);if(hu.x<0.||hu.x>1.||hu.y<0.||hu.y>1.)hc=vec4(0.);
 vec4 fc=texture2D(uF,v+w*.6);float fade=smoothstep(1.,.9,v.y);fc*=fade;hc*=mix(1.,fade,.7);
 float hm=hc.a*m;
 float a=hm+fc.a*(1.-hm);
 vec3 c=hc.rgb*hm+fc.rgb*fc.a*(1.-hm);
 c+=vec3(.98,.8,.2)*rim*.16*a*(1.-m*.7);
 gl_FragColor=vec4(c,a);}`;
 const sh=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(x);return x};
 let pg;try{pg=gl.createProgram();gl.attachShader(pg,sh(gl.VERTEX_SHADER,VS));gl.attachShader(pg,sh(gl.FRAGMENT_SHADER,FS));gl.linkProgram(pg);gl.useProgram(pg)}catch(e){return api}
 const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
 const lp=gl.getAttribLocation(pg,"p");gl.enableVertexAttribArray(lp);gl.vertexAttribPointer(lp,2,gl.FLOAT,false,0,0);
 const U=n=>gl.getUniformLocation(pg,n),uP=U("uP"),uA=U("uA"),uT=U("uT"),uFull=U("uFull");
 gl.uniform4fv(U("uHR"),o.helm);gl.uniform2fv(U("uC"),o.center);gl.uniform1i(U("uF"),0);gl.uniform1i(U("uH"),1);
 const tex=(img,unit)=>{const t=gl.createTexture();gl.activeTexture(gl.TEXTURE0+unit);gl.bindTexture(gl.TEXTURE_2D,t);gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL,false);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);[gl.TEXTURE_WRAP_S,gl.TEXTURE_WRAP_T].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,gl.CLAMP_TO_EDGE));
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR)};
 const load=s=>new Promise((ok,no)=>{const i=new Image();i.decoding="async";i.onload=()=>ok(i);i.onerror=no;i.src=s});
 const P=new Float32Array(N*3),trail=[];let head={x:.5,y:.45,r:0,tr:0},tgt=null,full=0,dirty=true,ready=false,hintT=-1,last=performance.now(),W=0,H=0;
 const R0=o.radius||.12;
 function size(){const r=stage.getBoundingClientRect(),D=Math.min(1.6,devicePixelRatio||1),w=Math.round(r.width*D),h=Math.round(r.height*D);if(w!==W||h!==H){W=cv.width=w;H=cv.height=h;gl.viewport(0,0,w,h);gl.uniform1f(uA,r.width/r.height);dirty=true}}
 const at=e=>{const r=stage.getBoundingClientRect();return{x:(e.clientX-r.left)/r.width,y:(e.clientY-r.top)/r.height}};
 stage.addEventListener("pointermove",e=>{if(e.pointerType==="touch"&&!e.buttons&&e.pressure===0)return;tgt=at(e);head.tr=R0;hintT=-1},{passive:true});
 stage.addEventListener("pointerdown",e=>{tgt=at(e);head.x=tgt.x;head.y=tgt.y;head.tr=R0;hintT=-1},{passive:true});
 stage.addEventListener("pointerleave",()=>{head.tr=0},{passive:true});
 stage.addEventListener("pointerup",e=>{if(e.pointerType==="touch")head.tr=0},{passive:true});
 function frame(now){requestAnimationFrame(frame);if(!ready)return;const dt=Math.min(.05,(now-last)/1000);last=now;size();
  if(hintT>=0){hintT+=dt;const k=hintT/2.4;if(k>=1){hintT=-1;head.tr=0}else{tgt={x:.95-1.0*ES(k),y:.42+.08*Math.sin(k*TAU)};head.tr=R0*Math.sin(Math.PI*cl(k*1.15))}}
  if(tgt){const px=head.x,py=head.y;head.x+=(tgt.x-head.x)*(1-Math.pow(.82,dt*60));head.y+=(tgt.y-head.y)*(1-Math.pow(.82,dt*60));
   const sp=Math.hypot(head.x-px,head.y-py);if(sp>.0015&&head.r>.01)trail.unshift({x:head.x,y:head.y,r:head.r*.85,a:0});}
  head.r+=(head.tr-head.r)*(1-Math.pow(.86,dt*60));
  trail.forEach(p=>p.a+=dt);while(trail.length>N-1||(trail.length&&trail[trail.length-1].a>.75))trail.pop();
  const live=head.r>.002||trail.length||(full>0&&full<1)||(head.r>.002||trail.length);if(!live&&!dirty)return;dirty=false;
  P.fill(0);P[0]=head.x;P[1]=head.y;P[2]=head.r;trail.forEach((p,i)=>{const k=1-p.a/.75;P[(i+1)*3]=p.x;P[(i+1)*3+1]=p.y;P[(i+1)*3+2]=p.r*k*k});
  gl.uniform3fv(uP,P);gl.uniform1f(uT,now/1000);gl.uniform1f(uFull,full);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)}
 api.ready=Promise.all([load(o.face),load(o.helmet)]).then(([f,h])=>{tex(f,0);tex(h,1);ready=true;api.ok=true;stage.classList.add("gl");size();requestAnimationFrame(frame)}).catch(()=>{});
 api.setFull=v=>{v=cl(v);if(Math.abs(v-full)>.0005){full=v;dirty=true}};
 api.hint=()=>{hintT=0};
 addEventListener("resize",()=>{dirty=true},{passive:true});
 return api}
