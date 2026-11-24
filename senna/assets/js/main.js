/* Ayrton Senna — documentário interativo
   Depende de: assinatura.js ($, $$, cl, EO, EIO, ES, TAU, fill, write, sigWrite, abertura),
   three.min.js + capacete3d.js (capacete 3D) e pistas.js (traçados). */
if("scrollRestoration" in history)history.scrollRestoration="manual";
scrollTo(0,0);
const reduce=matchMedia("(prefers-reduced-motion:reduce)").matches,touch=matchMedia("(hover:none)").matches;
const sc=$("#sc"),native=reduce;
if(native)document.body.classList.add("native","reduce");
let started=false,vw=innerWidth,vh=innerHeight,cy=0,vel=0,svel=0,docH=1;

/* ---------------------------------------------------------------------------
   ROLAGEM CONTÍNUA (igual ao Plazza): o conteúdo vive no #sc fixo; o body rola
   de verdade com a altura do #sc, e cada quadro aproxima cy de scrollY.
   --------------------------------------------------------------------------- */
const setH=()=>{if(!native&&started)document.body.style.height=sc.offsetHeight+"px"};
let roQ=0;new ResizeObserver(()=>{if(roQ)return;roQ=requestAnimationFrame(()=>{roQ=0;setH();measure()})}).observe(sc);

/* grão animado (mesmo canvas do Plazza) */
(()=>{const c=$("#grain"),g=c.getContext("2d");c.width=c.height=160;const d=g.createImageData(160,160);for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0);c.style.backgroundImage="url("+c.toDataURL()+")";c.style.backgroundSize="160px";g.clearRect(0,0,160,160);c.width=c.height=1})();

/* assinaturas */
fill($("#sigMini"),{pen:true});
const sigHero=$("#sigHero");fill(sigHero);
sigWrite("#sigFt",2.8);sigWrite("#sigCar",2.4);

/* carro: "SENNA" ajustado à largura da composição (primeira fotografia) */
const plate=$("#plate"),senna=$("#senna"),lts=$$("#senna .lt"),sigWrap=$("#plate .sig-wrap");
function fitHero(){const pw=plate.offsetWidth;senna.style.fontSize="100px";const w=lts.reduce((a,l)=>a+l.offsetWidth,0);senna.style.fontSize=(100*pw*.777/(w*1.07)).toFixed(2)+"px"}
const carEnter=$("#carEnter"),carBody=$("#carBody"),carDrive=$("#carDrive"),heroWheels=$$("#carEnter .wheel");
function carIn(){
 if(reduce){carEnter.classList.add("done");return}
 const r=carEnter.getBoundingClientRect(),cur=new DOMMatrix(getComputedStyle(carEnter).transform).m41,left=r.left-cur;
 const dx=vw-left+40,D=2100,E="cubic-bezier(.12,.74,.2,1)",circ=Math.PI*heroWheels[0].offsetWidth,turns=dx/circ*360;
 const a=carEnter.animate([{transform:`translate3d(${dx}px,0,0)`},{transform:"translate3d(0,0,0)"}],{duration:D,easing:E,fill:"forwards"});
 a.onfinish=()=>{carEnter.classList.add("done");a.cancel()};
 heroWheels.forEach(w=>w.firstElementChild.animate([{transform:`rotate(${turns}deg)`},{transform:"rotate(0deg)"}],{duration:D,easing:E}));
 $$("#carEnter .car-ghost").forEach((g,i)=>g.animate([{transform:`translate3d(${dx*(.1+.12*i)}px,0,0)`,opacity:.34-.14*i},{opacity:.2-.08*i,offset:.45},{transform:"translate3d(0,0,0)",opacity:0}],{duration:D*.9,easing:E,fill:"forwards"}));
 $$("#carEnter .speed").forEach((s,i)=>s.animate([{transform:"scaleX(1.8)",opacity:0},{opacity:.85,offset:.12},{transform:"scaleX(0)",opacity:0}],{duration:D*.8,delay:i*40,easing:"cubic-bezier(.3,.6,.3,1)",fill:"forwards"}));
 carBody.animate([{transform:"rotate(0)"},{transform:"rotate(0)",offset:.55},{transform:"rotate(-.9deg)",offset:.8},{transform:"rotate(.3deg)",offset:.92},{transform:"rotate(0)"}],{duration:D+250,easing:"ease-in-out"});
}
const garage=$("#garage");
new IntersectionObserver((es,ob)=>{if(es[0].isIntersecting){ob.disconnect();garage.classList.add("on");setTimeout(carIn,reduce?0:180)}},{threshold:.35}).observe(garage);

/* escrita barata: só toca no estilo quando o valor muda */
const T=(el,v)=>{if(el._t!==v){el._t=v;el.style.transform=v}},O=(el,v)=>{if(el._o!==v){el._o=v;el.style.opacity=v}};

/* go(): fim da abertura — libera a rolagem e define a altura do body (como no Plazza) */
let heroIn=-1;
function go(){if(started)return;started=true;document.body.classList.remove("lock");document.body.classList.add("ready");setH();measure();heroIn=performance.now();helm.hint()}

/* ---------------------------------------------------------------------------
   ENTRADA: rosto + capacete 3D (fotos reais projetadas, three.js), transparente, com lente no cursor
   --------------------------------------------------------------------------- */
const fh=$("#top"),fhStage=$("#fhStage"),fhName=$(".fh-name"),fhSides=$$(".fh-side"),fhSig=$(".fh-sig");
const helm=capacete(fhStage,{face:"assets/img/rosto.webp",helmet:"assets/img/capacete.webp",helm:[-.135,-.085,1.29,1.03],head:[.5,.34,.3]});
const ptr={x:0,y:0,in:false,down:false};
const toStage=e=>{const S=R.fs;ptr.x=(e.clientX-S.l)/S.h;ptr.y=(e.clientY+(native?0:cy)-S.t)/S.h};
fh.addEventListener("pointermove",e=>{toStage(e);ptr.in=true},{passive:true});
fh.addEventListener("pointerdown",e=>{toStage(e);ptr.in=true;ptr.down=true},{passive:true});
fh.addEventListener("pointerleave",()=>{ptr.in=false;ptr.down=false},{passive:true});
addEventListener("pointerup",e=>{ptr.down=false;if(e.pointerType==="touch")ptr.in=false},{passive:true});

/* ---------------------------------------------------------------------------
   HISTÓRIA: palco preso + fotografias empilhadas como num álbum
   --------------------------------------------------------------------------- */
const steps=$$(".step"),prints=$$(".print"),P=prints.map(p=>({el:p,img:p.querySelector("img"),dev:p.querySelector(".dev"),sh:p.querySelector(".shade"),r:parseFloat(p.style.getPropertyValue("--r"))||0}));
const first=[],span=[];steps.forEach((s,i)=>{const k=+s.dataset.photo;if(first[k]===undefined)first[k]=i;span[k]=i-first[k]+1});
const yearBox=$("#year"),railFill=$("#railFill"),railLabels=$$("#rail span"),pos=steps.map(s=>+s.dataset.pos);
const navA=$$("nav a"),navT=navA.map(a=>document.getElementById(a.dataset.go));
const pq=$("#pq");pq.innerHTML=pq.textContent.trim().split(/\s+/).map(w=>`<span class="w">${w}</span>`).join(" ");const pw=$$("#pq .w");
const ult=$("#cap-6"),trackLine=$("#trackLine"),track=$(".track"),pass=$("#pass"),passCar=$("#passCar"),passWheels=$$("#passCar .wheel");
const pins=[{sec:$("#historia"),st:$("#historia .stage")},{sec:$("#pistas"),st:$(".pz-stage")}];

/* NAS PISTAS */
const races=$$(".race"),pzLine=$("#pzLine"),pzGhost=$("#pzGhost"),pzCar=$("#pzCar"),pzName=$("#pzName"),pzNum=$("#pzNum");
let pzIdx=-1,pzL=1,pzPts=[],lap=0;
const pzOld=$("#pzOld"),pzStrip=$("#pzStrip");
const minis=races.map((r,j)=>{const b=document.createElement("button");b.type="button";b.className="pz-mini";b.setAttribute("aria-label",r.dataset.name+" "+r.querySelector(".chap b").textContent);
 b.innerHTML=`<svg viewBox="0 0 1000 1000" aria-hidden="true"><path d="${PISTAS[r.dataset.track].d}"/><path d="${PISTAS[r.dataset.track].d}"/></svg><span>${r.querySelector(".chap b").textContent.split(" ")[0]}</span>`;
 pzStrip.appendChild(b);const L=b.querySelector("path+path").getTotalLength();b.style.setProperty("--l",L.toFixed(0));
 b.addEventListener("click",()=>scrollTo(0,docTop(r)+Math.max(0,(r.offsetHeight-vh)/2)));return{el:b}});
function setRace(i){if(i===pzIdx)return;const prevD=pzIdx>=0?pzLine.getAttribute("d"):null;pzIdx=i;const r=races[i],tr=PISTAS[r.dataset.track];
 if(prevD&&!reduce){pzOld.setAttribute("d",prevD);pzOld.classList.remove("go");void pzOld.getBBox();pzOld.classList.add("go")}
 minis.forEach((mm,j)=>mm.el.classList.toggle("on",j===i));
 pzLine.setAttribute("d",tr.d);pzGhost.setAttribute("d",tr.d);pzL=pzLine.getTotalLength();pzLine.style.strokeDasharray=pzL+" "+pzL;
 pzPts=[];for(let k=0;k<=400;k++){const p=pzLine.getPointAtLength(pzL*k/400);pzPts.push([p.x,p.y])}
 const old=pzName.querySelector("span:not(.out)");if(old){old.className="out";setTimeout(()=>old.remove(),650)}
 const s=document.createElement("span");s.textContent=r.dataset.name;pzName.appendChild(s);pzNum.textContent=String(i+1).padStart(2,"0")}

/* faixas de texto (Plazza): correm, aceleram e inclinam com a velocidade */
const MQ=$$(".mq-row").map((el,j)=>{const W=el.dataset.words.split("|");el.innerHTML=[...W,...W].map((w,i)=>`<span class="${(i+j)%2?"o":""}">${w}</span><i></i>`).join("");return{el,x:0,j,w:1,top:0,h:0}});

/* medidas: lidas uma vez (e a cada mudança de tamanho), nunca dentro do quadro */
let M=[],RM=[],NT=[],R={fhH:innerHeight};
function docTop(el){let y=0;while(el&&el!==sc&&el!==document.body){y+=el.offsetTop;el=el.offsetParent}return y}
function measure(){vw=innerWidth;vh=innerHeight;fitHero();docH=sc.offsetHeight;
 M=steps.map(s=>({t:docTop(s),h:s.offsetHeight}));RM=races.map(s=>({t:docTop(s),h:s.offsetHeight}));NT=navT.map(docTop);
 pins.forEach(p=>{p.top=docTop(p.sec);p.h=p.sec.offsetHeight});
 MQ.forEach(m=>{m.w=m.el.scrollWidth/2;m.top=docTop(m.el.parentNode);m.h=m.el.parentNode.offsetHeight});
 R={fhH:fh.offsetHeight,fs:{l:fhStage.offsetLeft-fhStage.offsetWidth/2,t:fhStage.offsetTop,w:fhStage.offsetWidth,h:fhStage.offsetHeight},
  gar:docTop(garage),pq:docTop(pq),pqh:pq.offsetHeight,ult:docTop(ult),ulth:ult.offsetHeight,track:docTop(track),pass:docTop(pass),passh:pass.offsetHeight,passw:passCar.offsetWidth,
  wc:Math.PI*(passWheels[0].offsetWidth||60),hc:Math.PI*(heroWheels[0].offsetWidth||60),pz:pins[1].top,pzh:pins[1].h};
 helm.size(R.fs.w,R.fs.h)}
let active=-1;
function setYear(i){if(i===active)return;active=i;const old=yearBox.querySelector(".y-in");if(old){old.className="y-out";setTimeout(()=>old.remove(),800)}const s=document.createElement("span");s.className="y-in";s.textContent=steps[i].dataset.year;yearBox.appendChild(s)}
const progressOf=(L,y)=>{const a=y+vh*.5;if(!L.length)return-1;if(a<L[0].t)return(a-L[0].t)/L[0].h;let p=0;for(let i=0;i<L.length;i++)if(a>=L[i].t)p=i+Math.min(1,(a-L[i].t)/L[i].h);return p};

/* textos: títulos letra a letra, parágrafos palavra a palavra, rótulos "decodificando" */
function splitWords(el){let i=0;const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3){const f=document.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(w=>{if(!w)return;if(/^\s+$/.test(w)){f.appendChild(document.createTextNode(w));return}const s=document.createElement("span");s.className="wd";s.innerHTML=`<i style="--i:${i++}">${w}</i>`;f.appendChild(s)});c.replaceWith(f)}else if(c.nodeType===1)walk(c)})};walk(el);el.classList.add("split")}
function splitChars(line,base){const t=line.textContent;line.innerHTML=[...t].map((ch,i)=>ch===" "?" ":`<span class="ch" style="--i:${base+i}">${ch}</span>`).join("");return base+t.length}
if(!reduce){
 $$(".title,.epi-title").forEach(ti=>{let b=0;ti.querySelectorAll(".ln>span").forEach(l=>{b=splitChars(l,b)+2})});
 $$(".card p[data-r]:not(.note),.note,.epi-text,.ultimo p[data-r]:not(.chap)").forEach(splitWords);
}
const GL="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789·—/";
function scramble(el){if(reduce||el._s)return;el._s=1;const nodes=[];const w=n=>[...n.childNodes].forEach(c=>c.nodeType===3?nodes.push([c,c.textContent]):w(c));w(el);const t0=performance.now();
 (function f(now){const k=cl((now-t0)/700);nodes.forEach(([n,txt])=>{n.textContent=[...txt].map((ch,i)=>ch===" "||i/txt.length<k*1.15-.15?ch:GL[(Math.random()*GL.length)|0]).join("")});if(k<1)requestAnimationFrame(f);else nodes.forEach(([n,txt])=>n.textContent=txt)})(t0)}

/* revelações: IntersectionObserver com threshold 0.2 adiciona "in" (como no Plazza) */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target;el.classList.add("in");io.unobserve(el);if(el.matches(".chap,.eyebrow"))scramble(el);
 el.querySelectorAll&&el.querySelectorAll("[data-n]").forEach(b=>{const n=+b.dataset.n,len=String(n).length,t0=performance.now();if(reduce){b.textContent=n;return}(function f(t){const k=EO((t-t0)/1800);b.textContent=String(Math.round(n*k)).padStart(len,"0");if(k<1)requestAnimationFrame(f)})(t0)})}),{threshold:.2});
$$("[data-r],.title,.epi-title,.helmet-rule,.chap,.eyebrow").forEach(el=>io.observe(el));

/* links internos: preventDefault + scrollTo; a rolagem suave faz a animação */
$$("[data-go]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();const el=document.getElementById(a.dataset.go);if(!el)return;
 let y=a.dataset.go==="top"?0:docTop(el);if(el.matches(".step,.race"))y+=Math.max(0,(el.offsetHeight-vh)/2);scrollTo(0,y)}));

/* ---------------------------------------------------------------------------
   LAÇO ÚNICO: lê scrollY, suaviza, depois só escreve (transform/opacity)
   --------------------------------------------------------------------------- */
const prog=$("#prog");let last=performance.now();
function loop(now){requestAnimationFrame(loop);const dt=Math.min(.05,(now-last)/1000);last=now;const t=now/1000;
 /* leitura */
 const target=scrollY,prev=cy;
 if(native)cy=target;else{const k=1-Math.pow(touch?.00006:.0006,dt);cy+=(target-cy)*k;if(Math.abs(target-cy)<.05)cy=target}
 vel=cy-prev;svel+=(vel-svel)*.15;
 /* escrita */
 if(!native)T(sc,`translate3d(0,${(-cy).toFixed(2)}px,0)`);
 const maxS=Math.max(1,docH-vh);T(prog,`scaleX(${cl(cy/maxS).toFixed(4)})`);
 document.body.classList.toggle("past",cy>vh*.8);
 if(!native)pins.forEach(p=>T(p.st,`translate3d(0,${cl(cy-p.top,0,Math.max(0,p.h-vh)).toFixed(2)}px,0)`));
 /* faixas de texto: a de cima corre para a esquerda, a de baixo para a direita */
 if(!reduce)MQ.forEach(m=>{m.x+=(m.j%2?(.12+svel*.08):-(.15+svel*.1))*dt*60;if(m.top-cy>vh||m.top+m.h-cy<0)return;
  const w=m.w||1;m.x=((m.x%w)-w)%w;T(m.el,`translate3d(${m.x.toFixed(1)}px,0,0) skewX(${cl(-svel*.2,-6,6).toFixed(2)}deg)`)});
 /* entrada: rosto + capacete 3D */
 if(cy<R.fhH*1.1){const h=started?cl(cy/vh,0,1.3):0;
  if(started&&!reduce){T(fhStage,`translate3d(-50%,${(-h*vh*.08).toFixed(1)}px,0) scale(${(1+h*.06).toFixed(4)})`);T(fhName,`translate3d(0,calc(-50% + ${(h*vh*.32).toFixed(1)}px),0)`);
   O(fhSig,(1-h*2.2).toFixed(3));fhSides.forEach(s=>T(s,`translate3d(0,${(-h*vh*.2).toFixed(1)}px,0)`))}
  helm.pointer(ptr.x,ptr.y,ptr.in,ptr.down);helm.setFull(reduce?0:EIO(cl((h-.06)/.65)));helm.frame(dt)}
 /* carro (seção 2): letras mais lentas, o carro sai pela esquerda */
 const gy=cy-(R.gar||0);if(started&&gy>-vh&&gy<vh*1.3){const h=cl(gy/vh,0,1.3),dx=reduce?0:-h*vw*.6;
  T(senna,`translate3d(0,${(h*vh*.28).toFixed(1)}px,0)`);T(carDrive,`translate3d(${dx.toFixed(1)}px,${(h*vh*.05).toFixed(1)}px,0)`);
  heroWheels.forEach(w=>T(w,`rotate(${(dx/R.hc*360).toFixed(1)}deg)`));
  if(sigWrap){T(sigWrap,`translate3d(0,${(h*vh*.12).toFixed(1)}px,0)`);O(sigWrap,(1-h*1.4).toFixed(3))}}
 /* prólogo */
 if(R.pq){const tp=R.pq-cy;if(tp<vh*1.1&&tp>-R.pqh){const pr=cl((vh*.82-tp)/(R.pqh*.9+vh*.2)),n=pw.length;pw.forEach((w,i)=>O(w,reduce?"1":(.14+.86*cl(pr*n*1.15-i)).toFixed(2)))}}
 /* história */
 if(M.length&&cy>M[0].t-vh*1.5&&cy<M[M.length-1].t+M[M.length-1].h){const p=progressOf(M,cy),n=P.length;
  const ent=P.map((_,k)=>cl((p-first[k]+(k?.3:.35))/(k?.5:.6)));
  P.forEach((o,k)=>{const tt=ent[k];if(tt<=0||(k+2<n&&ent[k+2]>=1)){if(o.vis!==0){o.el.style.visibility="hidden";o.vis=0}return}
   if(o.vis!==1){o.el.style.visibility="visible";o.vis=1}
   const e=EO(tt),d=k+1<n?EO(ent[k+1]):0,lp=cl((p-first[k]+.3)/(span[k]+.3));
   let y=(1-e)*vh*.07-d*vh*.035,rot=o.r+(1-e)*(k%2?-3.5:3.5)+d*(k%2?-2.2:2.2),s=(1+(1-e)*.05)*(1-d*.05);
   if(reduce){y=0;rot=o.r;s=1}
   T(o.el,`translate3d(0,${y.toFixed(1)}px,0) rotate(${rot.toFixed(2)}deg) scale(${s.toFixed(4)})`);
   const cp=reduce||e>=1?"":`inset(-40px -80px calc(${((1-e)*100).toFixed(1)}% + ${(e*-80).toFixed(0)}px) -80px)`;if(o._c!==cp){o._c=cp;o.el.style.clipPath=cp}
   T(o.img,reduce?"scale(1)":`translate3d(0,${((.5-lp)*3).toFixed(2)}%,0) scale(${(1.13-.1*lp+(1-e)*.22).toFixed(4)})`);
   O(o.dev,(.85*(1-EO(cl((p-first[k]+(k?.2:.25))/.35)))).toFixed(2));
   O(o.sh,(d*.3).toFixed(2))});
  setYear(cl(Math.floor(p+.12),0,steps.length-1));
  let pc=pos[0];for(let i=1;i<pos.length;i++)pc+=(pos[i]-pos[i-1])*ES(cl((p-i+.3)/.45));
  T(railFill,`scaleX(${pc.toFixed(4)})`);railLabels.forEach(l=>l.classList.toggle("on",+l.style.getPropertyValue("--p")<=pc+.001))}
 /* nas pistas: o traçado se desenha, o carrinho dá voltas e as miniaturas mostram todas as corridas */
 if(R.pz!==undefined&&cy>R.pz-vh&&cy<R.pz+R.pzh){const p=progressOf(RM,cy),i=cl(Math.floor(p+.12),0,races.length-1);setRace(i);
  const draw=reduce?1:EO(cl((p-i+.25)/.5));pzLine.style.strokeDashoffset=(pzL*(1-draw)).toFixed(1);
  lap=(lap+dt*(.05+Math.min(.25,Math.abs(svel)*.01)))%1;const at=draw<.999?draw:lap,q=pzPts[Math.round(at*400)]||[0,0];
  pzCar.setAttribute("cx",q[0].toFixed(1));pzCar.setAttribute("cy",q[1].toFixed(1));
  minis.forEach((mm,j)=>{const k=(reduce?(j<=i?1:0):cl(p-j+.75)).toFixed(3);if(mm._k!==k){mm._k=k;mm.el.style.setProperty("--k",k)}})}
 /* menu ativo e cabeçalho claro sobre fundo escuro */
 let on=-1;NT.forEach((tp,i)=>{if(tp-cy<=vh*.55)on=i});if(cy<vh*.6)on=-1;navA.forEach((a,i)=>a.classList.toggle("on",i===on));
 if(R.ult){const hy=cy+34;document.body.classList.toggle("dark",(hy>R.pz&&hy<R.pz+R.pzh)||(hy>R.ult+vh*.4&&hy<R.ult+R.ulth-vh*.4));
  const q=cl((cy+vh*.75-R.track)/(vh*.45));trackLine.style.transform=`scaleX(${(reduce?1:EO(q)).toFixed(4)})`;track.style.setProperty("--dot",q>=1?1:0)}
 /* epílogo: o carro atravessa a página e estaciona */
 if(R.pass){const q=cl((cy+vh-R.pass)/Math.max(1,maxS+vh-R.pass)),tx=(1-EO(q))*(vw*.5+R.passw)-R.passw/2;passCar.style.transform=`translate3d(${tx.toFixed(1)}px,0,0)`;passWheels.forEach(w=>w.style.transform=`rotate(${(tx/R.wc*360).toFixed(1)}deg)`)}
}

addEventListener("resize",()=>{measure();setH()});
document.fonts&&document.fonts.ready.then(()=>{measure();setH()});addEventListener("load",()=>{measure();setH()});
measure();requestAnimationFrame(loop);
abertura(sigHero,go);
