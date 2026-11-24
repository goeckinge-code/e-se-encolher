/* Ayrton Senna — documentário interativo
   Depende de assinatura.js ($, $$, cl, EO, ES, fill, write, sigWrite, abertura). */
if("scrollRestoration" in history)history.scrollRestoration="manual";
scrollTo(0,0);
const reduce=matchMedia("(prefers-reduced-motion:reduce)").matches,touch=matchMedia("(hover:none)").matches;
if(reduce)document.body.classList.add("reduce");
let started=false,vw=innerWidth,vh=innerHeight,cy=0,vel=0,svel=0;

/* rolagem suave com inércia (roda do mouse e trackpad). Toque, teclado e barra
   de rolagem continuam nativos; a posição real da página é sempre a do navegador,
   então o palco fixo (position: sticky) e os links continuam funcionando. */
const smooth=(()=>{if(reduce||touch)return null;let target=scrollY,cur=scrollY,on=false;
 const max=()=>document.documentElement.scrollHeight-innerHeight;
 addEventListener("wheel",e=>{if(e.ctrlKey||document.body.classList.contains("lock"))return;e.preventDefault();
  if(!on){target=cur=scrollY}const d=e.deltaY*(e.deltaMode===1?36:e.deltaMode===2?innerHeight:1)*1.05;target=cl(target+d,0,max());on=true},{passive:false});
 addEventListener("scroll",()=>{if(!on)target=cur=scrollY},{passive:true});
 addEventListener("keydown",()=>{on=false},{passive:true});
 addEventListener("pointerdown",()=>{on=false},{passive:true});
 return{tick(dt){if(!on)return;cur+=(target-cur)*(1-Math.pow(1-.075,dt*60));if(Math.abs(target-cur)<.25){cur=target;on=false}scrollTo(0,cur)},
  to(y){if(!on)cur=scrollY;target=cl(y,0,max());on=true}}})();

/* grão animado (mesmo canvas do Plazza) */
(()=>{const c=$("#grain"),g=c.getContext("2d");c.width=c.height=160;const d=g.createImageData(160,160);for(let i=0;i<d.data.length;i+=4){const v=Math.random()*255|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255}g.putImageData(d,0,0);c.style.backgroundImage="url("+c.toDataURL()+")";c.style.backgroundSize="160px";g.clearRect(0,0,160,160);c.width=c.height=1})();

/* assinaturas */
fill($("#sigMini"),{pen:true});
const sigHero=$("#sigHero");fill(sigHero);
sigWrite("#sigFt",2.8);sigWrite("#sigCar",2.4);

/* hero: "SENNA" ajustado à largura da composição (como na primeira fotografia) */
const plate=$("#plate"),senna=$("#senna"),lts=$$("#senna .lt"),sigWrap=$("#plate .sig-wrap");
function fitHero(){const pw=plate.offsetWidth;senna.style.fontSize="100px";const w=lts.reduce((a,l)=>a+l.getBoundingClientRect().width,0);senna.style.fontSize=(100*pw*.777/(w*1.07)).toFixed(2)+"px"}

/* entrada do carro: da direita para a esquerda, desacelerando até o centro */
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

/* go(): fim da abertura — libera a página (mesmo papel do go() do Plazza) */
function go(){if(started)return;started=true;document.body.classList.remove("lock");document.body.classList.add("ready");measure();if(!reduce)setTimeout(()=>helm.hint(),1500)}

/* entrada: rosto + capacete (capacete.js). O retângulo do capacete e o centro da viseira
   estão em coordenadas da foto do rosto (0..1). */
const fhStage=$("#fhStage"),fhName=$(".fh-name"),fhSides=$$(".fh-side"),fhSig=$(".fh-sig");
const helm=capacete(fhStage,{face:"assets/img/rosto.webp",helmet:"assets/img/capacete.webp",helm:[-.135,-.085,1.29,1.03],head:[.5,.33,.3]});
const garage=$("#garage");
new IntersectionObserver((es,ob)=>{if(es[0].isIntersecting){ob.disconnect();garage.classList.add("on");setTimeout(carIn,reduce?0:180)}},{threshold:.35}).observe(garage);

/* história: palco fixo, fotografias empilhadas como num álbum */
const steps=$$(".step"),prints=$$(".print"),P=prints.map(p=>({el:p,img:p.querySelector("img"),dev:p.querySelector(".dev"),sh:p.querySelector(".shade"),r:parseFloat(p.style.getPropertyValue("--r"))||0}));
const first=[],span=[];steps.forEach((s,i)=>{const k=+s.dataset.photo;if(first[k]===undefined)first[k]=i;span[k]=i-first[k]+1});
const yearBox=$("#year"),railFill=$("#railFill"),railLabels=$$("#rail span"),pos=steps.map(s=>+s.dataset.pos);
const navA=$$("nav a"),navT=navA.map(a=>document.getElementById(a.dataset.go));
const pq=$("#pq");pq.innerHTML=pq.textContent.trim().split(/\s+/).map(w=>`<span class="w">${w}</span>`).join(" ");const pw=$$("#pq .w");
const ult=$("#cap-6"),trackLine=$("#trackLine"),track=$(".track"),pass=$("#pass"),passCar=$("#passCar"),passWheels=$$("#passCar .wheel");
let M=[],NT=[],R={},lcy=-1,dirty=true;
const docTop=el=>el.getBoundingClientRect().top+scrollY;
function measure(){vw=innerWidth;vh=innerHeight;dirty=true;fitHero();
 M=steps.map(s=>({t:docTop(s),h:s.offsetHeight}));NT=navT.map(docTop);
 R={gar:docTop(garage),pq:docTop(pq),pqh:pq.offsetHeight,ult:docTop(ult),ulth:ult.offsetHeight,track:docTop(track),pass:docTop(pass),passh:pass.offsetHeight,passw:passCar.offsetWidth,wc:Math.PI*(passWheels[0].offsetWidth||60),hc:Math.PI*(heroWheels[0].offsetWidth||60)}}
let active=-1;
function setYear(i){if(i===active)return;active=i;const old=yearBox.querySelector(".y-in");if(old){old.className="y-out";setTimeout(()=>old.remove(),800)}const s=document.createElement("span");s.className="y-in";s.textContent=steps[i].dataset.year;yearBox.appendChild(s)}
function stepProgress(y){const a=y+vh*.5;if(!M.length)return-1;if(a<M[0].t)return(a-M[0].t)/M[0].h;let p=0;for(let i=0;i<M.length;i++)if(a>=M[i].t)p=i+Math.min(1,(a-M[i].t)/M[i].h);return p}

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

/* revelações e contadores (IntersectionObserver, como no Plazza) */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target;el.classList.add("in");io.unobserve(el);if(el.matches(".chap,.eyebrow"))scramble(el);
 el.querySelectorAll&&el.querySelectorAll("[data-n]").forEach(b=>{const n=+b.dataset.n,len=String(n).length,t0=performance.now();if(reduce){b.textContent=n;return}(function f(t){const k=EO((t-t0)/1800);b.textContent=String(Math.round(n*k)).padStart(len,"0");if(k<1)requestAnimationFrame(f)})(t0)})}),{threshold:.2,rootMargin:"0px 0px -8% 0px"});
$$("[data-r],.title,.epi-title,.helmet-rule,.chap,.eyebrow").forEach(el=>io.observe(el));

/* navegação */
$$("[data-go]").forEach(a=>a.addEventListener("click",e=>{e.preventDefault();const el=document.getElementById(a.dataset.go);if(!el)return;let y=docTop(el);if(el.classList.contains("step"))y+=Math.max(0,(el.offsetHeight-vh)/2)+vh*.1;const ty=a.dataset.go==="top"?0:y;if(smooth)smooth.to(ty);else scrollTo({top:ty,behavior:reduce?"auto":"smooth"})}));

/* laço de animação: valores suavizados pelo mesmo lerp de rolagem do Plazza */
const cards=$$(".card");let last=performance.now();
function loop(now){requestAnimationFrame(loop);const dt=Math.min(.05,(now-last)/1000);last=now;
 smooth&&smooth.tick(dt);
 const ty=scrollY,prev=cy;if(reduce||smooth)cy=ty;else{const k=1-Math.pow(.00006,dt);cy+=(ty-cy)*k;if(Math.abs(ty-cy)<.05)cy=ty}
 vel=dt>0?(cy-prev)/(dt*60):0;svel+=(vel-svel)*.12;if(Math.abs(svel)<.01)svel=0;
 if(!dirty&&Math.abs(cy-lcy)<.02&&!svel)return;lcy=cy;dirty=false;
 /* a velocidade da rolagem vira "vento": cartões e fotos inclinam levemente */
 const sk=reduce?0:cl(-svel*.05,-2.2,2.2);cards.forEach(c=>c.style.transform=sk?`skewY(${sk.toFixed(3)}deg)`:"");
 const maxS=Math.max(1,document.documentElement.scrollHeight-vh);$("#prog").style.transform=`scaleX(${(cy/maxS).toFixed(4)})`;
 document.body.classList.toggle("past",cy>vh*.8);
 /* hero: parallax — letras mais lentas, carro sai pela esquerda */
 if(started&&cy<vh*1.2){const h=cl(cy/vh,0,1.2);helm.setFull(reduce?0:EIO(cl((h-.04)/.62)));
  if(!reduce){fhStage.style.transform=`translate3d(-50%,${(-h*vh*.08).toFixed(1)}px,0) scale(${(1+h*.06).toFixed(4)})`;fhName.style.transform=`translate3d(0,calc(-50% + ${(h*vh*.32).toFixed(1)}px),0)`;
   fhSig.style.opacity=(1-h*2.2).toFixed(3);fhSides.forEach(s=>s.style.translate=`0 ${(-h*vh*.2).toFixed(1)}px`)}}
 const gy=cy-(R.gar||0);if(started&&gy>-vh&&gy<vh*1.3){const h=cl(gy/vh,0,1.3),dx=reduce?0:-h*vw*.6;
  senna.style.transform=`translate3d(0,${(h*vh*.28).toFixed(1)}px,0)`;
  carDrive.style.transform=`translate3d(${dx.toFixed(1)}px,${(h*vh*.05).toFixed(1)}px,0)`;
  heroWheels.forEach(w=>w.style.transform=`rotate(${(dx/R.hc*360).toFixed(1)}deg)`);
  if(sigWrap){sigWrap.style.transform=`translate3d(0,${(h*vh*.12).toFixed(1)}px,0)`;sigWrap.style.opacity=(1-h*1.4).toFixed(3)}}
 /* prólogo: palavras acendem conforme a leitura */
 if(R.pq){const tp=R.pq-cy;if(tp<vh*1.1&&tp>-R.pqh){const pr=cl((vh*.82-tp)/(R.pqh*.9+vh*.2)),n=pw.length;pw.forEach((w,i)=>{w.style.opacity=reduce?1:(.14+.86*cl(pr*n*1.15-i)).toFixed(2)})}}
 /* história */
 if(M.length){const p=stepProgress(cy),n=P.length;
  const ent=P.map((_,k)=>cl((p-first[k]+(k?.3:.35))/(k?.5:.6)));
  P.forEach((o,k)=>{const t=ent[k];if(t<=0||(k+2<n&&ent[k+2]>=1)){if(o.vis!==0){o.el.style.visibility="hidden";o.vis=0}return}
   if(o.vis!==1){o.el.style.visibility="visible";o.vis=1}
   const e=EO(t),d=k+1<n?EO(ent[k+1]):0,lp=cl((p-first[k]+.3)/(span[k]+.3));
   let y=(1-e)*vh*.07-d*vh*.035,rot=o.r+(1-e)*(k%2?-3.5:3.5)+d*(k%2?-2.2:2.2)+sk*.6*(1-d),s=(1+(1-e)*.05)*(1-d*.05);
   if(reduce){y=0;rot=o.r;s=1}
   o.el.style.transform=`translate3d(0,${y.toFixed(1)}px,0) rotate(${rot.toFixed(2)}deg) scale(${s.toFixed(4)})`;
   o.el.style.clipPath=reduce||e>=1?"":`inset(-40px -80px calc(${((1-e)*100).toFixed(2)}% + ${(e*-80).toFixed(1)}px) -80px)`;
   o.el.style.opacity=reduce?cl(t*2).toFixed(3):"";
   o.img.style.transform=reduce?"scale(1)":`translate3d(0,${((.5-lp)*3).toFixed(2)}%,0) scale(${(1.13-.1*lp+(1-e)*.22).toFixed(4)})`;
   o.dev.style.opacity=(.85*(1-EO(cl((p-first[k]+(k?.2:.25))/.35)))).toFixed(3);
   o.sh.style.opacity=(d*.3).toFixed(3)});
  setYear(cl(Math.floor(p+.12),0,steps.length-1));
  let pc=pos[0];for(let i=1;i<pos.length;i++)pc+=(pos[i]-pos[i-1])*ES(cl((p-i+.3)/.45));
  railFill.style.transform=`scaleX(${pc.toFixed(4)})`;railLabels.forEach(l=>l.classList.toggle("on",+l.style.getPropertyValue("--p")<=pc+.001))}
 /* navegação ativa */
 let on=-1;NT.forEach((t,i)=>{if(t-cy<=vh*.55)on=i});if(cy<vh*.6)on=-1;navA.forEach((a,i)=>a.classList.toggle("on",i===on));
 /* capítulo VI: escurece, a linha da pista se desenha e para */
 if(R.ult){const hy=cy+34;document.body.classList.toggle("dark",hy>R.ult+vh*.4&&hy<R.ult+R.ulth-vh*.4);
  const q=cl((cy+vh*.75-R.track)/(vh*.45));trackLine.style.transform=`scaleX(${(reduce?1:EO(q)).toFixed(4)})`;track.style.setProperty("--dot",q>=1?1:0)}
 /* epílogo: o carro atravessa a página com a rolagem */
 if(R.pass){const q=cl((cy+vh-R.pass)/Math.max(1,maxS+vh-R.pass)),tx=(1-EO(q))*(vw*.5+R.passw)-R.passw/2;passCar.style.transform=`translate3d(${tx.toFixed(1)}px,0,0)`;passWheels.forEach(w=>w.style.transform=`rotate(${(tx/R.wc*360).toFixed(1)}deg)`)}
}

addEventListener("resize",()=>{measure()});
document.fonts&&document.fonts.ready.then(measure);addEventListener("load",measure);
measure();requestAnimationFrame(loop);
abertura(sigHero,go);
