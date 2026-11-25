/* 구조 먼저 그리기 연구실 · 웃음 편 2 · 베리에이션 — 실험 패널 모음 (외부 라이브러리 없음) */
(function(){
'use strict';
var NS='http://www.w3.org/2000/svg';
var C={teal:'#0f8f84',orange:'#e8731a',navy:'#1e2f6e',blue:'#2458d6',green:'#13733a',red:'#c9302c',purple:'#6b4fb0',grid:'#e3e8ee',muted:'#5b6874',ink:'#16212b'};
var KFONT='"IBM Plex Sans KR","Malgun Gothic","Noto Sans KR",sans-serif';
var RM=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var P={};

/* ---------- 공용 도구 ---------- */
function el(tag,a,parent){var e=document.createElementNS(NS,tag);for(var k in a){if(a[k]!=null)e.setAttribute(k,a[k]);}if(parent)parent.appendChild(e);return e;}
function ktxt(p,x,y,s,a){a=a||{};var t=el('text',{x:x,y:y,'font-size':a.size||13,fill:a.fill||C.muted,'font-family':KFONT,'text-anchor':a.anchor||'start','font-weight':a.weight||'normal'},p);t.textContent=s;return t;}
function svgOf(h,W,H,label){h.innerHTML='';return el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':'실험 그림: '+(label||noteOf(h))},h);}
function noteOf(h){var n=h.parentNode&&h.parentNode.querySelector('.ph small');return n?n.textContent:'';}
function canvasOf(h,W,H,mw){h.innerHTML='';var c=document.createElement('canvas');c.width=W;c.height=H;c.style.width='100%';c.style.maxWidth=(mw||W*1.2)+'px';c.style.margin='0 auto';c.style.height='auto';c.style.display='block';c.style.borderRadius='10px';c.setAttribute('role','img');c.setAttribute('aria-label','실험 그림: '+noteOf(h));h.appendChild(c);return c;}
function out(h){return h.parentNode.querySelector('.readout');}
function ctl(h){return h.parentNode.querySelector('.ctrl');}
function f2(v,d){d=d==null?2:d;if(d===0)return String(Math.round(v));var m=Math.pow(10,d);var s=(Math.round(v*m)/m).toFixed(d);s=s.replace(/\.?0+$/,'');if(s==='-0')s='0';return s;}
function num(v,d){return v<0?'−'+f2(-v,d):f2(v,d);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
function hex(c){c=c.replace('#','');return[parseInt(c.substr(0,2),16),parseInt(c.substr(2,2),16),parseInt(c.substr(4,2),16)];}
function rgb(a){return 'rgb('+a.map(function(v){return Math.round(clamp(v,0,255));}).join(',')+')';}
function mix(c1,c2,t){var a=hex(c1),b=hex(c2);return rgb([lerp(a[0],b[0],t),lerp(a[1],b[1],t),lerp(a[2],b[2],t)]);}
function shade(c,k){var a=hex(c);return rgb([a[0]*k,a[1]*k,a[2]*k]);}
function rad(d){return d*Math.PI/180;}
function seg(h,sel,cb){var bs=ctl(h).querySelectorAll(sel);bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b);});});}
function rng(seed){var s=seed>>>0||1;return function(){s=(s*1664525+1013904223)>>>0;return s/4294967296;};}
function onIn(inp,f){inp.addEventListener('input',f);}
function svgPt(s,e){var m=s.getScreenCTM().inverse();var q=s.createSVGPoint();q.x=e.clientX;q.y=e.clientY;return q.matrixTransform(m);}

function board(el_,items){el_.innerHTML=items.map(function(it){return '<div class="'+(it[2]?'good':'bad')+'"><span>'+it[0]+'</span><b>'+it[1]+'</b></div>';}).join('');}
function say(el_,lines){el_.innerHTML=lines.map(function(l){return '<div class="line"><img src="../assets/chars/'+l[0]+'_'+l[1]+'.webp" alt="" width="48" height="48"><div class="bub"><b>'+l[2]+'</b>'+l[3]+'</div></div>';}).join('');}
function missions(el_,state,touched){el_.querySelectorAll('li').forEach(function(li,i){if(touched&&state[i])li.classList.add('done');});}
var DONE={};
/* ===================== 공용 도구 ===================== */
function pick(h,sel){return ctl(h).querySelector(sel);}
function rv(h,name){var e=pick(h,'[name='+name+']');return e?(e.type==='checkbox'?e.checked:+e.value):null;}
function allIn(h,f){ctl(h).querySelectorAll('input,select').forEach(function(i){i.addEventListener(i.tagName==='SELECT'||i.type==='checkbox'?'change':'input',f);});}
function bg(s,W,H){el('rect',{x:0,y:0,width:W,height:H,fill:'#fbfcfd'},s);}
function seg2(h,cb){var bs=ctl(h).querySelectorAll('button[data-v]');bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on');});b.classList.add('on');cb(b.dataset.v);});});}
function verdict(ok,txt){return '<span style="color:'+(ok?C.green:C.red)+';font-weight:700">'+(ok?'✔ ':'⚠ ')+txt+'</span>';}
function P2(x,y){return x.toFixed(1)+','+y.toFixed(1);}
function toHsl(c){var a=hex(c).map(function(v){return v/255;});var mx=Math.max(a[0],a[1],a[2]),mn=Math.min(a[0],a[1],a[2]),h=0,s=0,l=(mx+mn)/2;
  if(mx!==mn){var d=mx-mn;s=l>.5?d/(2-mx-mn):d/(mx+mn);if(mx===a[0])h=(a[1]-a[2])/d+(a[1]<a[2]?6:0);else if(mx===a[1])h=(a[2]-a[0])/d+2;else h=(a[0]-a[1])/d+4;h*=60;}return [h,s,l];}
function fromHsl(h,s,l){h=((h%360)+360)%360;var c=(1-Math.abs(2*l-1))*s,x=c*(1-Math.abs((h/60)%2-1)),m=l-c/2,r,g,b;
  if(h<60){r=c;g=x;b=0;}else if(h<120){r=x;g=c;b=0;}else if(h<180){r=0;g=c;b=x;}else if(h<240){r=0;g=x;b=c;}else if(h<300){r=x;g=0;b=c;}else{r=c;g=0;b=x;}return rgb([(r+m)*255,(g+m)*255,(b+m)*255]);}
function gray(c){var a=hex(c);return 0.299*a[0]+0.587*a[1]+0.114*a[2];}
/* 색보정: hue(도), sat(배), light(배), sepia(0~1), mono(흑백) */
function grade(c,G){if(!G||c==='none')return c;var a=hex(c);
  if(G.mono){var y=clamp(gray(c)*(G.light||1),0,255);return rgb([y,y,y]);}
  var q=toHsl(c);var out=fromHsl(q[0]+(G.hue||0),clamp(q[1]*(G.sat==null?1:G.sat),0,1),clamp(q[2]*(G.light||1),0,1));
  if(G.sepia){var b=out.match(/\d+/g).map(Number),t=G.sepia;out=rgb([lerp(b[0],b[0]*0.85+45,t),lerp(b[1],b[1]*0.8+32,t),lerp(b[2],b[2]*0.62+8,t)]);}return out;}
var SKIN='#F8E3D3',INK='#2a2230',UID=0;
var CHAR={haru:{name:'하루',hair:'#E88AAA',hair2:'#1E2F6E',eye:'#3B6FD8',cloth:'#BEAAE1',cloth2:'#FFFFFF',style:'buns'},
 sia:{name:'시아',hair:'#1E1B22',eye:'#8A8F99',cloth:'#2E2E34',cloth2:'#FFFFFF',style:'long',acc:'earring'},
 moa:{name:'모아',hair:'#C9B79C',eye:'#D9922E',cloth:'#C8A27A',cloth2:'#FFFFFF',style:'wavy',acc:'band'},
 doctor:{name:'박사',hair:'#33343C',eye:'#2f2f38',cloth:'#FFFFFF',cloth2:'#1d1d22',style:'spiky',acc:'glasses',male:true}};
var GENERIC={hair:'#7a6250',eye:'#6b5a4a',style:'short'};
function defsOf(s){var d=s.querySelector('defs');if(!d){d=el('defs',{},null);s.insertBefore(d,s.firstChild);}return d;}
function pattern(s,kind,dens,col){var id='pt'+(++UID),d=defsOf(s),p;
  if(kind==='dots'){var a=8,r=1.25+0.25*dens;p=el('pattern',{id:id,width:a,height:a,patternUnits:'userSpaceOnUse'},d);el('rect',{width:a,height:a,fill:'#fff'},p);el('circle',{cx:a/2,cy:a/2,r:r,fill:col||INK},p);}
  else if(kind==='big'){var b=14,rb=2.5+0.5*dens;p=el('pattern',{id:id,width:b,height:b,patternUnits:'userSpaceOnUse'},d);el('rect',{width:b,height:b,fill:'#fff'},p);el('circle',{cx:b/2,cy:b/2,r:rb,fill:col||'#d23a3a'},p);}
  else if(kind==='hatch'){var sp=10-1.5*dens;p=el('pattern',{id:id,width:sp,height:sp,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},d);el('rect',{width:sp,height:sp,fill:'#fff'},p);el('line',{x1:0,y1:0,x2:0,y2:sp,stroke:col||INK,'stroke-width':1.1},p);}
  else if(kind==='check'){p=el('pattern',{id:id,width:12,height:12,patternUnits:'userSpaceOnUse'},d);el('rect',{width:12,height:12,fill:col||'#2f8f86'},p);el('rect',{width:6,height:12,fill:'rgba(255,255,255,.35)'},p);el('rect',{width:12,height:4,y:4,fill:'rgba(0,0,0,.25)'},p);}
  else if(kind==='argyle'){p=el('pattern',{id:id,width:18,height:24,patternUnits:'userSpaceOnUse'},d);el('rect',{width:18,height:24,fill:'#f3b8c8'},p);el('path',{d:'M9,0 L18,12 L9,24 L0,12Z',fill:'#9fd6c0'},p);}
  return 'url(#'+id+')';}
function blurF(s,sd){var id='bl'+(++UID),f=el('filter',{id:id,x:'-20%',y:'-20%',width:'140%',height:'140%'},defsOf(s));el('feGaussianBlur',{stdDeviation:sd},f);return 'url(#'+id+')';}
function radial(s,c){var id='rg'+(++UID),g=el('radialGradient',{id:id,cx:'38%',cy:'32%',r:'75%'},defsOf(s));el('stop',{offset:'0%','stop-color':mix('#ffffff',toHex(c),0.55)},g);el('stop',{offset:'60%','stop-color':c},g);el('stop',{offset:'100%','stop-color':shadeC(c,0.72)},g);return 'url(#'+id+')';}
function toHex(c){if(c.charAt(0)==='#')return c;var b=c.match(/\d+/g).map(Number);return '#'+b.map(function(v){return ('0'+Math.round(clamp(v,0,255)).toString(16)).slice(-2);}).join('');}
function shadeC(c,k){return shade(toHex(c),k);}

/* ===================== 캐릭터 그리기 도구 =====================
 o: cx, cy(머리 중심), R(머리 반지름), who, keep(고정값), G(색보정), lw(가장 가는 선), ratio(굵기 비), steps(그림자 단계), soft(부드러운 경계), hi(머리 하이라이트),
 tone(cel|dots|big|hatch|ink), dens, eye(눈 배율), hl(하이라이트 개수), lash(0~1), strands(가닥 선), simp(0 사실~1 카툰), brush(선 끊김 0~1), inkW, render(cel|soft|ink),
 exp, collapse(0~4), exE·exM·exS(과장 배율), sym{}, lines{}, outfit, headOnly, eyeDrop, beret */
function chara(s,o){o=o||{};var who=o.who||'haru',D=CHAR[who],keep=o.keep!==false;var id=keep?D:{hair:GENERIC.hair,eye:GENERIC.eye,style:o.lostStyle||'short',cloth:D.cloth,cloth2:D.cloth2,male:D.male};
  var cx=o.cx||200,cy=o.cy||170,R=o.R||80,G=o.G,simp=o.simp==null?0.4:o.simp,lw=o.lw||2.4,ratio=o.ratio||1.6,render=o.render||'cel',col=o.collapse||0;
  var ink=render==='ink',soft3=render==='soft';var g=el('g',{},s);
  function c(x){return grade(x,G);}
  var skin=ink?'#ffffff':c(SKIN),hairC=ink?INK:c(id.hair);var lineC=ink?INK:(soft3?shadeC(c(id.hair),0.55):INK);
  var lwMin=soft3?Math.max(0.6,lw*0.35):lw;
  var dash=o.brush?(function(b){var on=30-20*b,off=4+22*b;return on.toFixed(1)+' '+off.toFixed(1);})(o.brush):null;
  function line(d,w,a){a=a||{};return el('path',{d:d,fill:a.fill||'none',stroke:a.stroke||lineC,'stroke-width':w==null?lwMin:w,'stroke-linecap':'round','stroke-linejoin':'round','stroke-dasharray':a.nodash?null:dash,opacity:a.op},a.p||g);}
  var chin=cy+R*(1.0+0.22*(1-simp)),w=R*(0.92-0.06*(1-simp));
  var faceD=id.male?('M'+P2(cx,cy-R)+' C'+P2(cx-R*0.6,cy-R)+' '+P2(cx-w,cy-R*0.55)+' '+P2(cx-w,cy+R*0.05)+' L'+P2(cx-w*0.92,cy+R*0.62)+' L'+P2(cx-R*0.32,chin-R*0.02)+' L'+P2(cx+R*0.32,chin-R*0.02)+' L'+P2(cx+w*0.92,cy+R*0.62)+' L'+P2(cx+w,cy+R*0.05)+' C'+P2(cx+w,cy-R*0.55)+' '+P2(cx+R*0.6,cy-R)+' '+P2(cx,cy-R)+'Z')
    :('M'+P2(cx,cy-R)+' C'+P2(cx-R*0.56,cy-R)+' '+P2(cx-w,cy-R*0.55)+' '+P2(cx-w,cy+R*0.05)+' C'+P2(cx-w,cy+R*(0.35+0.3*simp))+' '+P2(cx-R*(0.42+0.3*simp),chin-R*0.08)+' '+P2(cx,chin)+' C'+P2(cx+R*(0.42+0.3*simp),chin-R*0.08)+' '+P2(cx+w,cy+R*(0.35+0.3*simp))+' '+P2(cx+w,cy+R*0.05)+' C'+P2(cx+w,cy-R*0.55)+' '+P2(cx+R*0.56,cy-R)+' '+P2(cx,cy-R)+'Z');
  if(col>=4){var jit=rng(7),pts=[];for(var i=0;i<=24;i++){var t=i/24*Math.PI*2,rr=R*(1+(jit()-.5)*0.12);pts.push(P2(cx+Math.sin(t)*w*rr/R,cy+(-Math.cos(t))*(t>Math.PI/2&&t<Math.PI*1.5?(chin-cy):R)*rr/R));}faceD='M'+pts.join(' L')+'Z';}
  /* 배경 기호(금 간 배경) */
  if(o.sym&&o.sym.crack){var cg=el('g',{},g);for(var k=0;k<9;k++){var a=k/9*Math.PI*2+0.3,x1=cx+Math.cos(a)*R*1.25,y1=cy-R*0.1+Math.sin(a)*R*1.25,x2=cx+Math.cos(a)*R*2.3,y2=cy-R*0.1+Math.sin(a)*R*2.3;el('path',{d:'M'+P2(x1,y1)+' L'+P2((x1+x2)/2+8,(y1+y2)/2-6)+' L'+P2(x2,y2),stroke:'#5b4a3a','stroke-width':2.4,fill:'none'},cg);}}
  /* 뒷머리 */
  var st=id.style;var hb;
  if(st==='spiky'){hb='M'+P2(cx-R*1.02,cy+R*0.2)+' L'+P2(cx-R*1.15,cy-R*0.6)+' L'+P2(cx-R*0.8,cy-R*1.05)+' L'+P2(cx-R*0.5,cy-R*1.32)+' L'+P2(cx-R*0.1,cy-R*1.18)+' L'+P2(cx+R*0.3,cy-R*1.38)+' L'+P2(cx+R*0.6,cy-R*1.12)+' L'+P2(cx+R*1.1,cy-R*1.1)+' L'+P2(cx+R*1.05,cy-R*0.5)+' L'+P2(cx+R*1.02,cy+R*0.2)+'Z';}
  else if(st==='short'){hb='M'+P2(cx-R*1.05,cy+R*0.55)+' C'+P2(cx-R*1.25,cy-R*0.8)+' '+P2(cx-R*0.6,cy-R*1.25)+' '+P2(cx,cy-R*1.2)+' C'+P2(cx+R*0.6,cy-R*1.25)+' '+P2(cx+R*1.25,cy-R*0.8)+' '+P2(cx+R*1.05,cy+R*0.55)+'Z';}
  else{var bot=cy+R*(o.headOnly?1.5:2.3),wv=st==='wavy';hb='M'+P2(cx-R*1.08,bot)+(wv?' Q'+P2(cx-R*1.35,cy+R*1.4)+' '+P2(cx-R*1.12,cy+R*0.8)+' Q'+P2(cx-R*1.35,cy+R*0.2)+' '+P2(cx-R*1.12,cy-R*0.3):' L'+P2(cx-R*1.15,cy+R*0.2))+' C'+P2(cx-R*1.2,cy-R*1.0)+' '+P2(cx-R*0.6,cy-R*1.22)+' '+P2(cx,cy-R*1.2)+' C'+P2(cx+R*0.6,cy-R*1.22)+' '+P2(cx+R*1.2,cy-R*1.0)+' '+(wv?P2(cx+R*1.12,cy-R*0.3)+' Q'+P2(cx+R*1.35,cy+R*0.2)+' '+P2(cx+R*1.12,cy+R*0.8)+' Q'+P2(cx+R*1.35,cy+R*1.4)+' '+P2(cx+R*1.08,bot):P2(cx+R*1.15,cy+R*0.2)+' L'+P2(cx+R*1.08,bot))+'Z';}
  var hairFill=soft3?radial(s,hairC):hairC;
  line(hb,ink?(o.inkW||6)*0.6:lwMin,{fill:hairFill,stroke:ink?INK:lineC});
  if(keep&&st==='buns'){[-1,1].forEach(function(d){el('circle',{cx:cx+d*R*0.58,cy:cy-R*1.05,r:R*0.3,fill:hairFill,stroke:lineC,'stroke-width':lwMin},g);});}
  /* 몸 */
  if(!o.headOnly&&!o.noBody){drawBody(s,g,o,id,cx,cy,R,c,lineC,lwMin,ink,soft3);}
  /* 목 */
  el('rect',{x:cx-R*0.22,y:chin-R*0.15,width:R*0.44,height:R*0.45,fill:skin},g);
  if(!o.headOnly&&!o.noBody)line('M'+P2(cx-R*0.22,chin-R*0.1)+' L'+P2(cx-R*0.22,chin+R*0.28)+' M'+P2(cx+R*0.22,chin-R*0.1)+' L'+P2(cx+R*0.22,chin+R*0.28),lwMin);
  /* 얼굴 */
  var faceFill=soft3?radial(s,toHex(skin)):skin;
  el('path',{d:faceD,fill:faceFill},g);
  /* 그림자 */
  var steps=o.steps==null?1:o.steps;if(steps>0&&!(ink&&!o.tone)){var sg=el('g',{filter:o.soft?blurF(s,R*0.05):null},g);var tone=o.tone||'cel';
    function sfill(k){if(tone==='cel')return shadeC(skin,k===1?0.87:k===2?0.77:0.68);if(tone==='ink')return INK;return pattern(s,tone,o.dens||3,tone==='big'?'#e0606a':INK);}
    var clipId='cf'+(++UID);var cp=el('clipPath',{id:clipId},defsOf(s));el('path',{d:faceD},cp);sg.setAttribute('clip-path','url(#'+clipId+')');
    el('path',{d:'M'+P2(cx-R*1.1,cy-R*0.5)+' L'+P2(cx+R*1.1,cy-R*0.5)+' L'+P2(cx+R*1.1,cy-R*0.18)+' Q'+P2(cx,cy-R*0.02)+' '+P2(cx-R*1.1,cy-R*0.18)+'Z',fill:sfill(1)},sg);
    el('path',{d:'M'+P2(cx+w*0.55,cy-R*0.2)+' Q'+P2(cx+w*1.05,cy+R*0.4)+' '+P2(cx+R*0.25,chin+2)+' L'+P2(cx+w*1.2,chin)+' L'+P2(cx+w*1.2,cy-R*0.2)+'Z',fill:sfill(1)},sg);
    if(steps>=2)el('path',{d:'M'+P2(cx+w*0.8,cy+R*0.05)+' Q'+P2(cx+w*1.05,cy+R*0.5)+' '+P2(cx+R*0.45,chin-R*0.05)+' L'+P2(cx+w*1.2,chin)+' L'+P2(cx+w*1.2,cy)+'Z',fill:sfill(2)},sg);
    if(steps>=3)el('path',{d:'M'+P2(cx-R*1.1,cy-R*0.5)+' L'+P2(cx+R*1.1,cy-R*0.5)+' L'+P2(cx+R*1.1,cy-R*0.32)+' Q'+P2(cx,cy-R*0.2)+' '+P2(cx-R*1.1,cy-R*0.32)+'Z',fill:sfill(3)},sg);
    if(!o.headOnly&&!o.noBody){el('path',{d:'M'+P2(cx-R*0.22,chin-R*0.1)+' Q'+P2(cx,chin+R*0.15)+' '+P2(cx+R*0.22,chin-R*0.1)+' L'+P2(cx+R*0.22,chin+R*0.12)+' L'+P2(cx-R*0.22,chin+R*0.12)+'Z',fill:sfill(1)},g);}}
  /* 얼굴 윤곽(굵기 비) */
  if(!soft3){line(faceD,lwMin);if(ratio>1.05){var jw=lwMin*ratio;line('M'+P2(cx-w,cy+R*0.25)+' C'+P2(cx-w,cy+R*(0.5+0.2*simp))+' '+P2(cx-R*(0.42+0.3*simp),chin-R*0.06)+' '+P2(cx,chin)+' C'+P2(cx+R*(0.42+0.3*simp),chin-R*0.06)+' '+P2(cx+w,cy+R*(0.5+0.2*simp))+' '+P2(cx+w,cy+R*0.25),jw);}}
  /* 선 더하기(감정 자리) */
  var L=o.lines||{},ey=cy+R*(0.18+(o.eyeDrop||0)),ex=R*0.4;
  if(L.under)[-1,1].forEach(function(d){line('M'+P2(cx+d*ex-R*0.16,ey+R*0.34)+' Q'+P2(cx+d*ex,ey+R*0.42)+' '+P2(cx+d*ex+R*0.16,ey+R*0.34),lwMin*0.9);});
  if(L.brow)line('M'+P2(cx-R*0.06,ey-R*0.42)+' L'+P2(cx-R*0.03,ey-R*0.22)+' M'+P2(cx+R*0.06,ey-R*0.42)+' L'+P2(cx+R*0.03,ey-R*0.22),lwMin*0.9);
  if(L.cheek){[-1,1].forEach(function(d){el('path',{d:'M'+P2(cx+d*w*0.55,cy+R*0.35)+' Q'+P2(cx+d*w*0.85,cy+R*0.6)+' '+P2(cx+d*w*0.45,chin-R*0.15),fill:'none',stroke:shadeC(skin,0.72),'stroke-width':R*0.08,opacity:.6},g);});}
  var ex2=L.extra||0;for(var e2=0;e2<ex2;e2++){var side=e2%2?1:-1,yy=cy-R*0.62+(e2>>1)*R*0.06;line(e2<4?'M'+P2(cx-R*0.3,yy)+' Q'+P2(cx,yy-R*0.03)+' '+P2(cx+R*0.3,yy):'M'+P2(cx+side*w*0.6,cy+R*(0.1+0.07*e2))+' l'+P2(side*R*0.12,R*0.06),lwMin*0.7);}
  /* 눈 */
  var eS=(o.eye||1)*(o.exE||1),ew=R*0.3*eS,eh=ew*(id.male?0.62:1.1)*(simp>0.85?0.9:1),hl=o.hl==null?2:o.hl,lash=o.lash==null?0.3:o.lash;
  var glow=o.sym&&o.sym.glow;
  [-1,1].forEach(function(d){var x=cx+d*ex,y=ey;var eg=el('g',{},g);
    if(col>=4&&!glow){line('M'+P2(x-ew*0.4,y+eh*0.2)+' L'+P2(x+d*ew*0.2,y+eh*0.45)+' L'+P2(x-ew*0.4,y+eh*0.7),lw*1.6,{p:eg});return;}
    if(col===3&&!glow){el('ellipse',{cx:x,cy:y+eh*0.45,rx:ew*0.5,ry:eh*0.55,fill:'#fff',stroke:lineC,'stroke-width':lw*1.2},eg);el('circle',{cx:x,cy:y+eh*0.5,r:ew*0.08,fill:INK},eg);return;}
    if(col===2&&!glow){el('circle',{cx:x,cy:y+eh*0.45,r:ew*0.13,fill:INK},eg);return;}
    if(simp>0.85){el('ellipse',{cx:x,cy:y+eh*0.5,rx:ew*0.22,ry:eh*0.36,fill:ink?INK:c(id.eye===GENERIC.eye?'#3a3030':'#2a2230')},eg);if(hl>0&&!ink)el('circle',{cx:x-ew*0.07,cy:y+eh*0.36,r:ew*0.07,fill:'#fff'},eg);return;}
    var irisC=glow?'#ff3d9a':(ink?'#ffffff':c(id.eye));
    el('ellipse',{cx:x,cy:y+eh*0.55,rx:ew*0.36,ry:eh*0.45,fill:irisC,stroke:ink?INK:null,'stroke-width':ink?lwMin*0.8:null},eg);
    if(!ink)el('ellipse',{cx:x,cy:y+eh*0.6,rx:ew*0.16,ry:eh*0.22,fill:glow?'#fff':'#1d1622'},eg);
    var hp=[[-0.12,0.3,0.1],[0.12,0.75,0.06],[0.18,0.38,0.05]];for(var q=0;q<Math.min(hl,3)&&!ink&&col<1;q++)el('circle',{cx:x+hp[q][0]*ew*d*-1,cy:y+eh*hp[q][1],r:ew*hp[q][2],fill:'#fff'},eg);
    if(col===1&&!ink)el('circle',{cx:x-ew*0.1,cy:y+eh*0.32,r:ew*0.09,fill:'#fff'},eg);
    var uw=lwMin*(1.1+lash*1.9)*(col>=1?0.7:1);line('M'+P2(x-ew*0.5,y+eh*0.22)+' Q'+P2(x,y-eh*0.08)+' '+P2(x+ew*0.5,y+eh*0.14),uw,{p:eg});
    if(lash>0.5&&col<1)for(var z=0;z<3;z++)line('M'+P2(x+d*ew*(0.32+z*0.08),y+eh*(0.08+z*0.03))+' l'+P2(d*ew*0.14,-eh*0.12),lwMin*0.9,{p:eg});
    if(col<1)line('M'+P2(x-ew*0.3,y+eh*1.02)+' Q'+P2(x,y+eh*1.08)+' '+P2(x+ew*0.3,y+eh*1.0),lwMin*0.6,{p:eg,op:.8});
    if(glow){el('line',{x1:x-ew*0.2,y1:y+eh*0.55,x2:x+d*R*1.8,y2:y+eh*0.5,stroke:'#ff3d6e','stroke-width':R*0.05,opacity:.85},eg);}});
  /* 눈썹 */
  [-1,1].forEach(function(d){var x=cx+d*ex,by=ey-R*(id.male?0.16:0.2);var raise=L.brow?-0.04:0;line('M'+P2(x-d*ew*0.45,by+R*(0.03+raise))+' Q'+P2(x,by-R*0.05)+' '+P2(x+d*ew*0.55,by+R*0.02),id.male?lwMin*2.2:lwMin*0.9);});
  /* 코 */
  var ny=cy+R*(0.55+(o.eyeDrop||0)*0.6);
  if(simp<0.85&&col<2){if(simp<0.3)line('M'+P2(cx+R*0.02,ey+R*0.12)+' L'+P2(cx+R*0.06,ny)+' Q'+P2(cx,ny+R*0.05)+' '+P2(cx-R*0.07,ny),lwMin*0.8);else line('M'+P2(cx+R*0.02,ny-R*0.06)+' Q'+P2(cx-R*0.03,ny)+' '+P2(cx+R*0.03,ny+R*0.01),lwMin*0.8);}
  /* 입 */
  var my=cy+R*(0.78+(o.eyeDrop||0)*0.5),mS=(o.exM||1),exp=o.exp||'smile',mw=R*0.13*mS;
  if(col>=2){el('ellipse',{cx:cx,cy:my+R*0.02,rx:R*0.2*mS,ry:R*0.16*mS,fill:ink?'#fff':'#a23a4a',stroke:lineC,'stroke-width':lwMin*1.2},g);}
  else if(L.teeth){el('rect',{x:cx-R*0.16,y:my-R*0.05,width:R*0.32,height:R*0.1,rx:R*0.03,fill:'#fff',stroke:lineC,'stroke-width':lwMin},g);line('M'+P2(cx-R*0.16,my)+' L'+P2(cx+R*0.16,my)+' M'+P2(cx,my-R*0.05)+' L'+P2(cx,my+R*0.05),lwMin*0.6);}
  else if(exp==='open'||mS>1.05){el('ellipse',{cx:cx,cy:my,rx:mw*0.7,ry:mw*0.85,fill:ink?'#fff':'#a23a4a',stroke:lineC,'stroke-width':lwMin},g);}
  else if(exp==='neutral')line('M'+P2(cx-mw*0.6,my)+' L'+P2(cx+mw*0.6,my),lwMin);
  else line('M'+P2(cx-mw,my-R*0.02)+' Q'+P2(cx,my+R*0.06)+' '+P2(cx+mw,my-R*0.02),lwMin);
  if(col>=1&&!ink)[-1,1].forEach(function(d){el('ellipse',{cx:cx+d*ex*1.15,cy:ey+R*0.42,rx:R*0.11,ry:R*0.05,fill:'#f2a0a8',opacity:.6},g);});
  /* 앞머리 */
  var bangTop=cy-R*1.15,bl=cy-R*(st==='spiky'?0.42:0.3);var n=st==='spiky'?6:8,bd='M'+P2(cx-R*1.06,cy+R*0.15)+' C'+P2(cx-R*1.15,cy-R*0.9)+' '+P2(cx-R*0.55,bangTop)+' '+P2(cx,bangTop)+' C'+P2(cx+R*0.55,bangTop)+' '+P2(cx+R*1.15,cy-R*0.9)+' '+P2(cx+R*1.06,cy+R*0.15);
  for(var i2=n;i2>=0;i2--){var xx=cx-R*0.98+R*1.96*i2/n,tip=i2%2===1,yy2=tip?bl+R*(0.06+0.06*((i2*5)%3)):bl-R*0.22;if(i2===n)yy2=cy+R*0.1;if(i2===0)yy2=cy+R*0.1;bd+=' L'+P2(xx,yy2);}
  bd+='Z';line(bd,ink?(o.inkW||6)*0.5:lwMin,{fill:hairFill,stroke:ink?INK:lineC});
  if(o.hi&&!ink)el('path',{d:'M'+P2(cx-R*0.6,cy-R*0.78)+' Q'+P2(cx,cy-R*0.95)+' '+P2(cx+R*0.6,cy-R*0.78),stroke:'rgba(255,255,255,.65)','stroke-width':R*0.07,fill:'none','stroke-linecap':'round'},g);
  var sn=o.strands==null?5:o.strands;for(var j=0;j<sn;j++){var t2=(j+0.5)/sn,x0=cx-R*0.85+R*1.7*t2,top=cy-R*1.05+Math.abs(t2-0.5)*R*0.35;line('M'+P2(x0,top)+' Q'+P2(x0+R*0.06,(top+bl)/2)+' '+P2(x0-R*0.02,bl-R*0.05),Math.max(0.6,lwMin*0.55),{stroke:ink?'#ffffff':shadeC(hairC,0.55)});}
  /* 고정 장식 */
  if(keep){if(st==='buns'){el('path',{d:'M'+P2(cx-R*0.08,bangTop+2)+' L'+P2(cx+R*0.08,bangTop+2)+' L'+P2(cx+R*0.05,bl)+' L'+P2(cx-R*0.05,bl)+'Z',fill:ink?'#fff':c(D.hair2)},g);}
    if(D.acc==='band'){line('M'+P2(cx-R*0.95,cy-R*0.6)+' Q'+P2(cx,cy-R*1.35)+' '+P2(cx+R*0.95,cy-R*0.6),R*0.12,{stroke:ink?'#fff':'#ffffff',nodash:true});line('M'+P2(cx-R*0.95,cy-R*0.6)+' Q'+P2(cx,cy-R*1.35)+' '+P2(cx+R*0.95,cy-R*0.6),lwMin*0.7,{stroke:INK,op:.5});
      var rx=cx+R*1.0,ry=cy-R*0.45;el('path',{d:'M'+P2(rx,ry)+' l'+P2(R*0.28,-R*0.16)+' l0,'+(R*0.34).toFixed(1)+'Z M'+P2(rx,ry)+' l'+P2(-R*0.05,R*0.32)+' l'+P2(R*0.2,R*0.05)+'Z',fill:'#ffffff',stroke:INK,'stroke-width':lwMin*0.8},g);}
    if(D.acc==='earring'){[-1,1].forEach(function(d){el('circle',{cx:cx+d*w*1.02,cy:cy+R*0.42,r:R*0.05,fill:ink?'#fff':'#c8ccd4',stroke:INK,'stroke-width':lwMin*0.6},g);});}
    if(D.acc==='glasses'){[-1,1].forEach(function(d){el('rect',{x:cx+d*ex-ew*0.65,y:ey-eh*0.15,width:ew*1.3,height:eh*1.3,rx:3,fill:'none',stroke:ink?INK:'#0f8f84','stroke-width':lwMin*1.2},g);});line('M'+P2(cx-ex+ew*0.65,ey+eh*0.3)+' L'+P2(cx+ex-ew*0.65,ey+eh*0.3),lwMin,{stroke:ink?INK:'#0f8f84'});
      el('path',{d:'M'+P2(cx-R*0.25,bangTop+R*0.05)+' L'+P2(cx-R*0.05,bangTop+R*0.02)+' L'+P2(cx-R*0.12,bl-R*0.1)+'Z',fill:'#ffffff'},g);}}
  if(o.beret){el('ellipse',{cx:cx-R*0.15,cy:cy-R*1.05,rx:R*1.0,ry:R*0.38,fill:c('#E8DCC8'),stroke:lineC,'stroke-width':lwMin},g);el('circle',{cx:cx-R*0.15,cy:cy-R*1.4,r:R*0.06,fill:c('#E8DCC8'),stroke:lineC,'stroke-width':lwMin},g);}
  /* 무너짐 3단계 이상: 얼굴 위 세로 그림자 선 */
  if(col>=3){var vg=el('g',{opacity:.75},g);for(var v=0;v<7;v++){var vx=cx-R*0.6+v*R*0.2;el('line',{x1:vx,y1:cy-R*0.55,x2:vx,y2:cy-R*(0.15+0.05*(v%2)),stroke:'#4a5bb5','stroke-width':lwMin*0.9},vg);}}
  /* 기호 */
  var Sy=o.sym||{},sS=o.exS||1;
  if(Sy.sweat||sS>1.05){var sx=cx+w*0.95,sy=cy-R*0.55,sr=R*0.09*sS;el('path',{d:'M'+P2(sx,sy-sr*2.2)+' Q'+P2(sx+sr*1.2,sy)+' '+P2(sx,sy+sr)+' Q'+P2(sx-sr*1.2,sy)+' '+P2(sx,sy-sr*2.2)+'Z',fill:'#bfe3ff',stroke:'#2f6fb5','stroke-width':1.6},g);}
  if(Sy.heart){var hx=cx-R*1.25,hy=cy-R*0.9,hs=R*0.16;el('path',{d:'M'+P2(hx,hy+hs)+' C'+P2(hx-hs*1.6,hy-hs*0.2)+' '+P2(hx-hs*0.6,hy-hs*1.4)+' '+P2(hx,hy-hs*0.4)+' C'+P2(hx+hs*0.6,hy-hs*1.4)+' '+P2(hx+hs*1.6,hy-hs*0.2)+' '+P2(hx,hy+hs)+'Z',fill:'#ff5f8f'},g);}
  if(Sy.note){var nx=cx+R*1.25,ny2=cy-R*1.0;el('ellipse',{cx:nx,cy:ny2+R*0.2,rx:R*0.08,ry:R*0.06,fill:INK},g);el('line',{x1:nx+R*0.07,y1:ny2+R*0.2,x2:nx+R*0.07,y2:ny2-R*0.15,stroke:INK,'stroke-width':2},g);el('path',{d:'M'+P2(nx+R*0.07,ny2-R*0.15)+' q'+P2(R*0.12,R*0.05)+' '+P2(R*0.1,R*0.18),stroke:INK,'stroke-width':2,fill:'none'},g);}
  if(Sy.vein){var vx2=cx+R*0.45,vy=cy-R*0.75,vs=R*0.09;el('path',{d:'M'+P2(vx2-vs,vy-vs*0.2)+' Q'+P2(vx2,vy)+' '+P2(vx2-vs*0.2,vy-vs)+' M'+P2(vx2+vs,vy-vs*0.2)+' Q'+P2(vx2,vy)+' '+P2(vx2+vs*0.2,vy-vs)+' M'+P2(vx2-vs,vy+vs*0.2)+' Q'+P2(vx2,vy)+' '+P2(vx2-vs*0.2,vy+vs)+' M'+P2(vx2+vs,vy+vs*0.2)+' Q'+P2(vx2,vy)+' '+P2(vx2+vs*0.2,vy+vs),stroke:'#d0303a','stroke-width':2.4,fill:'none'},g);}
  if(Sy.sparkle){[[-1.3,-0.5],[1.35,-0.2]].forEach(function(p){var sx2=cx+p[0]*R,sy2=cy+p[1]*R,k2=R*0.1;el('path',{d:'M'+P2(sx2,sy2-k2)+' L'+P2(sx2+k2*0.25,sy2-k2*0.25)+' L'+P2(sx2+k2,sy2)+' L'+P2(sx2+k2*0.25,sy2+k2*0.25)+' L'+P2(sx2,sy2+k2)+' L'+P2(sx2-k2*0.25,sy2+k2*0.25)+' L'+P2(sx2-k2,sy2)+' L'+P2(sx2-k2*0.25,sy2-k2*0.25)+'Z',fill:'#ffd34d'},g);});}
  return {g:g,chin:chin,ey:ey,w:w};}
function drawBody(s,g,o,id,cx,cy,R,c,lineC,lw,ink,soft3){var top=cy+R*1.28,bot=cy+R*2.7,sw=R*(id.male?1.75:1.5);var who=o.who||'haru',of=o.outfit||'default';
  var T='M'+P2(cx-sw,bot)+' Q'+P2(cx-sw*0.98,top+R*0.12)+' '+P2(cx-R*0.45,top)+' L'+P2(cx+R*0.45,top)+' Q'+P2(cx+sw*0.98,top+R*0.12)+' '+P2(cx+sw,bot)+'Z';
  var bg_=el('g',{},g);function fillOf(x){return ink?'#ffffff':(soft3?radial(s,c(x)):c(x));}
  function part(d,f,w){el('path',{d:d,fill:f,stroke:lineC,'stroke-width':w==null?lw:w,'stroke-linejoin':'round'},bg_);}
  var main=CHAR[who].cloth;
  if(of==='punk')main='#26262b';else if(of==='preppy')main='#ffffff';else if(of==='y2k')main='#ff7fb8';else if(of==='autumn')main='#EFE3CF';else if(of==='hood')main='#4f7ed6';
  part(T,fillOf(main));
  var V='M'+P2(cx-R*0.38,top)+' L'+P2(cx,top+R*0.55)+' L'+P2(cx+R*0.38,top)+'Z';
  if(of==='default'){
    if(who==='haru'){part('M'+P2(cx-sw,bot)+' Q'+P2(cx-sw*0.98,top+R*0.12)+' '+P2(cx-R*0.6,top+R*0.02)+' L'+P2(cx-R*0.75,bot)+'Z',fillOf('#ffffff'));part('M'+P2(cx+sw,bot)+' Q'+P2(cx+sw*0.98,top+R*0.12)+' '+P2(cx+R*0.6,top+R*0.02)+' L'+P2(cx+R*0.75,bot)+'Z',fillOf('#ffffff'));
      el('line',{x1:cx-R*0.12,y1:top+R*0.1,x2:cx-R*0.15,y2:top+R*0.55,stroke:ink?INK:'#fff','stroke-width':lw*1.2},bg_);el('line',{x1:cx+R*0.12,y1:top+R*0.1,x2:cx+R*0.15,y2:top+R*0.55,stroke:ink?INK:'#fff','stroke-width':lw*1.2},bg_);}
    else if(who==='sia'){part('M'+P2(cx-R*0.75,bot)+' L'+P2(cx-R*0.55,top+R*0.55)+' L'+P2(cx+R*0.55,top+R*0.55)+' L'+P2(cx+R*0.75,bot)+'Z',fillOf('#ffffff'));part('M'+P2(cx,top+R*0.12)+' l'+P2(-R*0.32,-R*0.12)+' l0,'+(R*0.3).toFixed(1)+'Z M'+P2(cx,top+R*0.12)+' l'+P2(R*0.32,-R*0.12)+' l0,'+(R*0.3).toFixed(1)+'Z',fillOf('#9aa0a8'));}
    else if(who==='moa'){part(V,fillOf('#ffffff'));part('M'+P2(cx,top+R*0.2)+' l'+P2(-R*0.25,-R*0.1)+' l0,'+(R*0.22).toFixed(1)+'Z M'+P2(cx,top+R*0.2)+' l'+P2(R*0.25,-R*0.1)+' l0,'+(R*0.22).toFixed(1)+'Z',ink?'#fff':pattern(s,'check',0,'#b8353d'));}
    else{part(V,fillOf('#ffffff'));part('M'+P2(cx-R*0.3,top+R*0.05)+' L'+P2(cx-R*0.45,bot)+' L'+P2(cx+R*0.45,bot)+' L'+P2(cx+R*0.3,top+R*0.05)+' L'+P2(cx,top+R*0.55)+'Z',fillOf('#1d1d22'));part('M'+P2(cx-R*0.07,top+R*0.12)+' L'+P2(cx+R*0.07,top+R*0.12)+' L'+P2(cx+R*0.1,bot-R*0.3)+' L'+P2(cx,bot-R*0.15)+' L'+P2(cx-R*0.1,bot-R*0.3)+'Z',fillOf('#26262b'));}}
  else if(of==='punk'){part('M'+P2(cx-R*0.08,top+R*0.05)+' L'+P2(cx+R*0.08,top+R*0.05)+' L'+P2(cx+R*0.12,bot-R*0.2)+' L'+P2(cx,bot)+' L'+P2(cx-R*0.12,bot-R*0.2)+'Z',ink?'#fff':'#c0303a');for(var k=0;k<5;k++)el('line',{x1:cx-R*0.12,y1:top+R*(0.25+k*0.22),x2:cx+R*0.12,y2:top+R*(0.15+k*0.22),stroke:'#111','stroke-width':lw*1.4},bg_);}
  else if(of==='preppy'){part('M'+P2(cx-sw*0.7,bot)+' L'+P2(cx-R*0.4,top+R*0.1)+' L'+P2(cx,top+R*0.6)+' L'+P2(cx+R*0.4,top+R*0.1)+' L'+P2(cx+sw*0.7,bot)+'Z',ink?'#fff':pattern(s,'argyle',0));part('M'+P2(cx-R*0.38,top)+' l'+P2(R*0.18,R*0.22)+' l'+P2(R*0.2,-R*0.18)+'Z M'+P2(cx+R*0.38,top)+' l'+P2(-R*0.18,R*0.22)+' l'+P2(-R*0.2,-R*0.18)+'Z',fillOf('#ffffff'));}
  else if(of==='y2k'){part(V,fillOf('#ffffff'));var sx=cx,sy=top+R*0.9,k2=R*0.18;part('M'+P2(sx,sy-k2)+' L'+P2(sx+k2*0.3,sy-k2*0.3)+' L'+P2(sx+k2,sy)+' L'+P2(sx+k2*0.3,sy+k2*0.3)+' L'+P2(sx,sy+k2)+' L'+P2(sx-k2*0.3,sy+k2*0.3)+' L'+P2(sx-k2,sy)+' L'+P2(sx-k2*0.3,sy-k2*0.3)+'Z',fillOf('#ffd34d'),lw*0.6);}
  else if(of==='autumn'){for(var a2=0;a2<4;a2++){var xx=cx-sw*0.6+a2*sw*0.4;el('path',{d:'M'+P2(xx,top+R*0.5)+' q'+P2(R*0.08,R*0.2)+' 0,'+(R*0.4).toFixed(1)+' q'+P2(-R*0.08,R*0.2)+' 0,'+(R*0.4).toFixed(1),stroke:shadeC(c('#EFE3CF'),0.75),'stroke-width':lw*1.3,fill:'none'},bg_);}
    part('M'+P2(cx-R*0.75,top-R*0.05)+' Q'+P2(cx,top+R*0.45)+' '+P2(cx+R*0.75,top-R*0.05)+' L'+P2(cx+R*0.7,top+R*0.25)+' Q'+P2(cx,top+R*0.7)+' '+P2(cx-R*0.7,top+R*0.25)+'Z',ink?'#fff':pattern(s,'check',0,c('#2f8f86')));part('M'+P2(cx+R*0.3,top+R*0.35)+' l'+P2(R*0.25,R*0.85)+' l'+P2(R*0.22,-R*0.1)+' l'+P2(-R*0.15,-R*0.8)+'Z',ink?'#fff':pattern(s,'check',0,c('#2f8f86')));}
  else if(of==='hood'){part('M'+P2(cx-R*0.6,top-R*0.05)+' Q'+P2(cx,top+R*0.3)+' '+P2(cx+R*0.6,top-R*0.05),'none');el('line',{x1:cx-R*0.1,y1:top+R*0.15,x2:cx-R*0.12,y2:top+R*0.7,stroke:'#fff','stroke-width':lw},bg_);el('line',{x1:cx+R*0.1,y1:top+R*0.15,x2:cx+R*0.12,y2:top+R*0.7,stroke:'#fff','stroke-width':lw},bg_);}}
/* 전신(등신 실험): o.heads, o.Htot, o.base, o.adapt, o.kick(0~1), o.exag */
function figure(s,o){var who=o.who||'haru',heads=o.heads,Ht=o.Htot,base=o.base,cx=o.cx,hh=Ht/heads,top=base-Ht;var g=el('g',{opacity:o.op==null?1:o.op},s);
  var R=hh/2.15,cy=top+R;var adapt=!!o.adapt,sdness=clamp((7-heads)/5,0,1);
  var rest=Ht-hh,neckY=top+hh,torsoL=rest*0.5,legL=rest*0.5,sw=hh*(heads>=5?0.85:lerp(0.55,0.85,(heads-2)/3)),lw=Math.max(1.2,hh*0.03);
  var hipY=neckY+torsoL,armW=Math.max(3,hh*(0.16+0.1*sdness)),legW=Math.max(4,hh*(0.2+0.12*sdness));
  var lineC=INK,D=CHAR[who];
  function seg(x1,y1,x2,y2,wd,col){el('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:lineC,'stroke-width':wd+lw*2,'stroke-linecap':'round'},g);el('line',{x1:x1,y1:y1,x2:x2,y2:y2,stroke:col,'stroke-width':wd,'stroke-linecap':'round'},g);}
  // 다리
  var kick=o.kick||0,ex=o.exag||1,ang=kick*Math.PI/180*80*ex;var lx=cx-sw*0.3,rx=cx+sw*0.3;
  seg(lx,hipY,lx,base-legW*0.3,legW,'#3b3b48');
  var kx=rx+Math.sin(ang)*legL*ex,ky=hipY+Math.cos(ang)*legL;seg(rx,hipY,kx,ky-legW*0.3,legW,'#3b3b48');
  [[lx,base],[kx,ky]].forEach(function(p){el('ellipse',{cx:p[0]+legW*0.25,cy:p[1]-legW*0.15,rx:legW*0.75,ry:legW*0.45,fill:'#5a4a40',stroke:lineC,'stroke-width':lw},g);});
  // 몸통
  el('path',{d:'M'+P2(cx-sw,neckY+hh*0.12)+' Q'+P2(cx,neckY-hh*0.02)+' '+P2(cx+sw,neckY+hh*0.12)+' L'+P2(cx+sw*0.85,hipY+hh*0.08)+' L'+P2(cx-sw*0.85,hipY+hh*0.08)+'Z',fill:D.cloth,stroke:lineC,'stroke-width':lw},g);
  el('path',{d:'M'+P2(cx-sw,neckY+hh*0.12)+' L'+P2(cx-sw*1.05,hipY+hh*0.3)+' L'+P2(cx-sw*0.55,hipY+hh*0.3)+' L'+P2(cx-sw*0.4,neckY+hh*0.05)+'Z M'+P2(cx+sw,neckY+hh*0.12)+' L'+P2(cx+sw*1.05,hipY+hh*0.3)+' L'+P2(cx+sw*0.55,hipY+hh*0.3)+' L'+P2(cx+sw*0.4,neckY+hh*0.05)+'Z',fill:'#ffffff',stroke:lineC,'stroke-width':lw},g);
  // 팔과 손
  var aL=torsoL*0.95;[-1,1].forEach(function(d){var ax=cx+d*sw*0.95,ay=neckY+hh*0.15,hx=ax+d*hh*0.15,hy=ay+aL;seg(ax,ay,hx,hy,armW,'#ffffff');
    var hr=Math.max(3,armW*0.62);if(adapt&&heads<4){el('circle',{cx:hx,cy:hy+hr*0.6,r:hr*1.05,fill:SKIN,stroke:lineC,'stroke-width':lw},g);}
    else{el('ellipse',{cx:hx,cy:hy+hr*0.7,rx:hr*0.7,ry:hr,fill:SKIN,stroke:lineC,'stroke-width':lw},g);for(var f=0;f<5;f++)el('line',{x1:hx-hr*0.55+f*hr*0.27,y1:hy+hr*1.1,x2:hx-hr*0.55+f*hr*0.27,y2:hy+hr*1.9,stroke:lineC,'stroke-width':Math.max(0.6,lw*0.6)},g);}});
  // 머리
  var drop=adapt?sdness*0.18:0;chara(g,{who:who,cx:cx,cy:cy,R:R,headOnly:true,eyeDrop:drop,simp:adapt?lerp(0.4,0.8,sdness):0.4,lw:Math.max(1,R*0.035),steps:1,strands:adapt&&heads<4?3:5,eye:adapt?1+sdness*0.25:1});
  return {hh:hh,top:top,R:R,eyeFrac:0.5+drop*0.5,legRatio:legL/Ht};}
function pixelate(svg,host,W,H,px){var xml=new XMLSerializer().serializeToString(svg);var img=new Image();
  img.onload=function(){var sc=document.createElement('canvas');sc.width=Math.ceil(W/px);sc.height=Math.ceil(H/px);var x=sc.getContext('2d');x.drawImage(img,0,0,sc.width,sc.height);
    var cv=canvasOf(host,W,H,W*1.1),y=cv.getContext('2d');y.imageSmoothingEnabled=false;y.drawImage(sc,0,0,W,H);};
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(xml);}
function offSvg(W,H){var s=document.createElementNS(NS,'svg');s.setAttribute('xmlns',NS);s.setAttribute('viewBox','0 0 '+W+' '+H);s.setAttribute('width',W);s.setAttribute('height',H);return s;}

/* ===================== 0 스타일 지도 ===================== */
var GCOL=['#0f8f84','#e8731a','#6b4fb0','#2458d6','#c9302c','#13733a','#b8860b','#d6378a'];
function stylePts(){var e=document.getElementById('style-pts');return e?JSON.parse(e.textContent):null;}
function dist(a,b,m){var s=0;for(var i=0;i<a.length;i++)if(!m||m[i])s+=(a[i]-b[i])*(a[i]-b[i]);return Math.sqrt(s);}
function kmeans(X,k,m){var n=X.length,d=X[0].length;var sums=X.map(function(x){return x.reduce(function(a,b){return a+b;},0);});var first=sums.indexOf(Math.max.apply(null,sums));var C=[X[first].slice()];
  while(C.length<k){var best=-1,bi=0;X.forEach(function(x,i){var md=Math.min.apply(null,C.map(function(c){return dist(x,c,m);}));if(md>best){best=md;bi=i;}});C.push(X[bi].slice());}
  var lab=new Array(n).fill(0);for(var it=0;it<40;it++){var ch=false;X.forEach(function(x,i){var bj=0,bd=1e9;C.forEach(function(c,j){var dd=dist(x,c,m);if(dd<bd){bd=dd;bj=j;}});if(lab[i]!==bj){lab[i]=bj;ch=true;}});
    C=C.map(function(c,j){var mem=X.filter(function(_,i){return lab[i]===j;});if(!mem.length)return c;var nc=new Array(d).fill(0);mem.forEach(function(x){for(var q=0;q<d;q++)nc[q]+=x[q]/mem.length;});return nc;});if(!ch)break;}
  var inert=X.reduce(function(a,x,i){var dd=dist(x,C[lab[i]],m);return a+dd*dd;},0);return {lab:lab,C:C,inert:inert};}
function pca2(X,m){var d=X[0].length,n=X.length,mu=new Array(d).fill(0);X.forEach(function(x){for(var i=0;i<d;i++)mu[i]+=x[i]/n;});
  var Y=X.map(function(x){return x.map(function(v,i){return m[i]?v-mu[i]:0;});});var cov=[];for(var i=0;i<d;i++){cov.push([]);for(var j=0;j<d;j++){var s=0;Y.forEach(function(y){s+=y[i]*y[j];});cov[i].push(s/n);}}
  function power(M,skip){var v=new Array(d).fill(0).map(function(_,i){return m[i]?1+i*0.1:0;});for(var t=0;t<80;t++){var w=new Array(d).fill(0);for(var i=0;i<d;i++)for(var j=0;j<d;j++)w[i]+=M[i][j]*v[j];
      if(skip){var dot=0;for(var q=0;q<d;q++)dot+=w[q]*skip[q];for(q=0;q<d;q++)w[q]-=dot*skip[q];}var nr=Math.sqrt(w.reduce(function(a,b){return a+b*b;},0))||1;v=w.map(function(x){return x/nr;});}return v;}
  var v1=power(cov),v2=power(cov,v1);if(v1[0]<0)v1=v1.map(function(x){return -x;});if(v2[2]<0)v2=v2.map(function(x){return -x;});
  return Y.map(function(y){return [y.reduce(function(a,b,i){return a+b*v1[i];},0),y.reduce(function(a,b,i){return a+b*v2[i];},0)];});}
P.p0_map=function(h){var D=stylePts();if(!D)return;var W=660,H=430;
  function draw(){var k=rv(h,'k'),human=rv(h,'human'),m=[0,1,2,3,4,5].map(function(i){return rv(h,'a'+i);});if(!m.some(Boolean)){m[0]=true;}
    var X=D.pts.map(function(p){return p.f;}),R=kmeans(X,k,m),Z=pca2(X,m);var xs=Z.map(function(z){return z[0];}),ys=Z.map(function(z){return z[1];});
    var x0=Math.min.apply(null,xs),x1=Math.max.apply(null,xs),y0=Math.min.apply(null,ys),y1=Math.max.apply(null,ys);
    function px(i){return 40+(Z[i][0]-x0)/((x1-x0)||1)*(W-80);}function py(i){return 30+(Z[i][1]-y0)/((y1-y0)||1)*(H-70);}
    var s=svgOf(h,W,H,'참고 그림 스타일 지도');bg(s,W,H);
    ktxt(s,W-12,H-10,'가로·세로: 선택한 특징을 2차원으로 펼친 축(주성분)',{size:11.5,anchor:'end'});
    var labs=human?D.pts.map(function(p){return p.g-1;}):R.lab;
    D.pts.forEach(function(p,i){var cc=GCOL[labs[i]%8];var cir=el('circle',{cx:px(i),cy:py(i),r:9,fill:cc,'fill-opacity':.85,stroke:p.alt?'#16212b':'#fff','stroke-width':p.alt?2.6:1.2,tabindex:0},s);
      var t=el('title',{},cir);t.textContent=p.d+' · 이 편의 군집: '+D.groups[p.g]+(p.alt?' / '+D.groups[p.alt]:'');
      cir.addEventListener('click',function(){out(h).querySelector('.pick').innerHTML='<b>고른 점</b> — '+p.d+' · 기계 군집 '+(R.lab[i]+1)+' · 이 편의 부: '+D.groups[p.g]+(p.alt?' / '+D.groups[p.alt]+'(경계)':'');});});
    // 군집 요약
    var rows=[],agree=0;for(var j=0;j<k;j++){var mem=D.pts.map(function(p,i){return i;}).filter(function(i){return R.lab[i]===j;});if(!mem.length)continue;
      var cnt={};mem.forEach(function(i){var g=D.pts[i].g;cnt[g]=(cnt[g]||0)+1;});var top=Object.keys(cnt).sort(function(a,b){return cnt[b]-cnt[a];})[0];agree+=cnt[top];
      var near=mem.slice().sort(function(a,b){return dist(X[a],R.C[j],m)-dist(X[b],R.C[j],m);}).slice(0,2).map(function(i){return D.pts[i].d;});
      rows.push('<span style="color:'+GCOL[j%8]+';font-weight:700">●</span> 군집 '+(j+1)+' ('+mem.length+'개) — 많이 겹치는 부: <b>'+D.groups[top]+'</b> · 예: '+near.join(' / '));}
    var agr=agree/D.pts.length*100;
    out(h).innerHTML='<div>'+rows.join('<br>')+'</div><div style="margin-top:6px">기계 군집과 이 편의 부가 겹치는 비율 <b>'+f2(agr,0)+'%</b> · 군집 안 거리 제곱합 <b>'+f2(R.inert,2)+'</b> '+(k<4?verdict(false,'너무 넓게 묶여 서로 다른 그림체가 한 군집에 섞입니다'):k>7?verdict(false,'잘게 나뉘어 군집마다 배울 축이 흐려집니다'):verdict(true,'넓게 묶되 축이 보이는 정도입니다'))+'</div><div class="pick muted" style="margin-top:6px">점을 누르면 설명이 여기에 나옵니다. 테두리가 두꺼운 점은 두 군집에 걸친 그림입니다.</div>';}
  allIn(h,draw);draw();};

/* ===================== 1부 시대 ===================== */
P.p1_cel=function(h){var W=460,H=430;function draw(){var st=rv(h,'steps'),hi=rv(h,'hi'),soft=rv(h,'soft');var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'moa',cx:230,cy:175,R:92,steps:st,soft:soft,hi:hi,lw:soft?1.8:2.6,hl:soft?2:1,lash:soft?0.25:0.6});
    var n=5*(1+st+hi),era=st<=1&&!soft?'80~90년대 셀화 인상':st>=2&&soft?'2010년대 이후 디지털 애니 인상':'2000년대 초 디지털 셀 인상(그 사이)';
    out(h).innerHTML='색 수 ≈ 5 × (1 + '+st+' + '+hi+') = <b>'+n+'색</b> · '+(st===0?'그림자 없음 — 평평한 카툰 인상':'<b>'+era+'</b>')+(soft&&st<=1?' · '+verdict(false,'단계가 적은데 경계만 부드러우면 흐릿해 보입니다'):'');}
  allIn(h,draw);draw();};
P.p1_eyes=function(h){var W=460,H=430;function draw(){var e=rv(h,'eye')/100,hl=rv(h,'hl'),la=rv(h,'lash')/100;var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'moa',cx:230,cy:175,R:92,eye:e,hl:hl,lash:la,steps:1});
    var era=hl<=1&&la>=0.5?'80년대 인상':hl>=2&&la<=0.4?'지금의 인상':'90년대~2000년대 인상';
    out(h).innerHTML='하이라이트 <b>'+hl+'개</b>, 속눈썹 무게 <b>'+f2(la*100,0)+'</b> → <b>'+era+'</b> · '+(e>1.3?verdict(false,'눈 크기 '+f2(e*100,0)+'% — 연대보다 나이가 먼저 바뀌어 보입니다(어려 보이는 쏠림)'):verdict(true,'눈 크기 '+f2(e*100,0)+'% — 나이는 그대로'));}
  allIn(h,draw);draw();};
P.p1_info=function(h){var W=460,H=430;function draw(){var sn=rv(h,'strands'),lw=rv(h,'lw');var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'moa',cx:230,cy:175,R:92,strands:sn,lw:lw,steps:1});
    var per=10+2*sn,sec=12*per;out(h).innerHTML='장마다 선 약 <b>'+per+'개</b>(기본 10 + 가닥·주름 '+(2*sn)+') → 1초 12장이면 <b>'+sec+'개</b> · '+(sn<=5?'단순하고 가벼운 TV 애니 인상':sn>=12?'정교한 극장판·일러스트 인상':'보통의 정보량')+(lw>=4&&sn>=12?' · '+verdict(false,'굵은 선에 가닥이 많아 답답합니다'):'');}
  allIn(h,draw);draw();};
P.p1_grade=function(h){var W=560,H=380;function draw(){var G={hue:rv(h,'hue'),sat:rv(h,'sat')/100,light:rv(h,'light')/100,sepia:rv(h,'sepia')?0.7:0};var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'moa',cx:140,cy:150,R:70,steps:1});chara(s,{who:'moa',cx:420,cy:150,R:70,steps:1,G:G});ktxt(s,140,370,'원판',{anchor:'middle',fill:C.ink});ktxt(s,420,370,'보정판',{anchor:'middle',fill:C.ink});
    var hc=grade(CHAR.moa.hair,G),tag=G.sepia||(G.sat<0.85&&G.hue>=0)?'오래된 인쇄물 인상':(G.sat>1.1&&G.hue<0)?'지금 화면 인상':'중간';
    out(h).innerHTML='보정판 머리색 <span style="display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:middle;background:'+hc+'"></span> · <b>'+tag+'</b> · '+(Math.abs(G.hue)>30?verdict(false,'색상 회전 '+G.hue+'° — 머리색(고정값)이 바뀌어 다른 사람처럼 보입니다'):verdict(true,'색상 회전 '+G.hue+'° — 같은 캐릭터의 보정'));}
  allIn(h,draw);draw();};

/* ===================== 2부 선과 지역 ===================== */
P.p2_weight=function(h){var W=460,H=430;function draw(){var r=rv(h,'ratio'),b=rv(h,'base');var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'sia',cx:230,cy:175,R:92,lw:b,ratio:r,steps:r<=1.2?0:1});
    out(h).innerHTML='가장 가는 곳 <b>'+f2(b,1)+'</b>, 가장 굵은 곳 <b>'+f2(b*r,1)+'</b> → 굵기 비 '+f2(b*r,1)+' ÷ '+f2(b,1)+' = <b>'+f2(r,1)+'</b> · '+(r<=1.2?'맑고 평평한 선(클리어 라인 계열)':r<3?'보통의 애니·만화 펜선':'힘 있는 붓 느낌의 펜선');}
  allIn(h,draw);draw();};
P.p3_gesture=function(h){var W=460,H=440;function draw(){var bd=rv(h,'bend')/100,cl=rv(h,'clean')/100,showL=rv(h,'line');var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#ffffff'},s);var r=rng(21);
    var A=[170,70],B=[290,410],L=Math.hypot(B[0]-A[0],B[1]-A[1]),nx=(B[1]-A[1])/L,ny=-(A[0]-B[0])/L;var dev=bd*L,Cp=[(A[0]+B[0])/2-nx*dev*2,(A[1]+B[1])/2-ny*dev*2];
    function bz(t){var u=1-t;return [u*u*A[0]+2*u*t*Cp[0]+t*t*B[0],u*u*A[1]+2*u*t*Cp[1]+t*t*B[1]];}
    if(showL)el('path',{d:'M'+P2(A[0],A[1])+' Q'+P2(Cp[0],Cp[1])+' '+P2(B[0],B[1]),stroke:'#e0337f','stroke-width':3,fill:'none','stroke-dasharray':'8 5'},s);
    var copies=Math.round(lerp(4,1,cl)),jit=lerp(4,0,cl),wd=lerp(1.2,2.6,cl),col=cl>0.6?INK:'#55505a';
    function st(d){for(var c=0;c<copies;c++){el('path',{d:d,fill:'none',stroke:col,'stroke-width':wd,'stroke-linecap':'round','stroke-linejoin':'round',opacity:cl>0.6?1:0.55,transform:'translate('+f2((r()-.5)*2*jit,1)+','+f2((r()-.5)*2*jit,1)+')'},s);}}
    var head=bz(0.06),neck=bz(0.16),chest=bz(0.3),hip=bz(0.55),knee=bz(0.78),foot=bz(1);
    st('M'+P2(head[0]-24,head[1])+' a24,26 0 1,0 48,0 a24,26 0 1,0 -48,0');
    st('M'+P2(head[0]+14,head[1]-24)+' l14,-8 l-2,16 Z');
    st('M'+P2(neck[0],neck[1])+' Q'+P2(chest[0],chest[1])+' '+P2(hip[0],hip[1]));
    st('M'+P2(chest[0]-26,chest[1]-6)+' L'+P2(hip[0]-20,hip[1])+' M'+P2(chest[0]+26,chest[1]-2)+' L'+P2(hip[0]+18,hip[1]+2));
    st('M'+P2(hip[0],hip[1])+' Q'+P2(knee[0],knee[1])+' '+P2(foot[0],foot[1])+' l22,0');
    st('M'+P2(hip[0],hip[1])+' L'+P2(hip[0]-60-bd*80,hip[1]+70)+' L'+P2(hip[0]-90-bd*120,hip[1]+130)+' l-18,0');
    var reach=90+bd*120;st('M'+P2(chest[0]+20,chest[1])+' L'+P2(chest[0]+reach*0.55,chest[1]+10)+' L'+P2(chest[0]+reach,chest[1]+4));
    st('M'+P2(chest[0]+reach,chest[1]+4)+' l70,-18');
    st('M'+P2(chest[0]-20,chest[1])+' L'+P2(chest[0]-60,chest[1]-40)+' L'+P2(chest[0]-80,chest[1]-90));
    var tag=bd<0.15?'차분한 자세':bd<=0.3?'힘이 실린 자세':'크게 휘어 과장된 동작';
    out(h).innerHTML='양 끝 직선 '+f2(L,0)+', 가장 먼 거리 '+f2(dev,0)+' → 휜 정도 '+f2(dev,0)+' ÷ '+f2(L,0)+' = <b>'+f2(bd,2)+'</b> · <b>'+tag+'</b> · '+(cl<0.5?'러프 선(겹친 선) — 동작을 먼저 확인하는 단계':'정리 선 — 동작이 정해진 뒤 한 번만 긋는 선')+(bd<0.08?' · '+verdict(false,'선이 너무 곧아 뻣뻣해 보입니다'):'');}
  allIn(h,draw);draw();};
P.p3_tone=function(h){var W=460,H=430,mode='cel';seg2(h,function(v){mode=v;draw();});
  function draw(){var dn=rv(h,'dens');var s=svgOf(h,W,H);bg(s,W,H);chara(s,{who:'sia',cx:230,cy:175,R:92,G:{mono:true},tone:mode,dens:dn,steps:mode==='ink'?1:2});
    var cov,txt;if(mode==='dots'){var r=1.25+0.25*dn;cov=Math.PI*r*r/64;txt='망점: 3.14 × '+f2(r,2)+'² ÷ 8² ≈ <b>'+f2(cov*100,0)+'%</b> 회색';}
    else if(mode==='big'){var rb=2.5+0.5*dn;cov=Math.PI*rb*rb/196;txt='큰 점: 3.14 × '+f2(rb,1)+'² ÷ 14² ≈ <b>'+f2(cov*100,0)+'%</b> — 옛 미국 코믹스 인상';}
    else if(mode==='hatch'){var sp=10-1.5*dn;cov=1.1/sp;txt='해칭: 선 굵기 1.1 ÷ 간격 '+f2(sp,1)+' ≈ <b>'+f2(cov*100,0)+'%</b> — 진지한 그래픽 노블 인상';}
    else if(mode==='ink'){cov=1;txt='먹칠: <b>100%</b> — 대비가 가장 강함';}else{cov=0.13;txt='단색 회색 1단계 — 평평한 애니 인상';}
    out(h).innerHTML=txt+(mode==='ink'?' · '+verdict(false,'얼굴 그림자를 먹칠하면 표정이 사라집니다. 머리·옷에 먼저 쓰세요'):'');}
  allIn(h,draw);draw();};
P.p2_simplify=function(h){var W=460,H=430;function draw(){var sp=rv(h,'simp')/100,k=rv(h,'keep');var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'sia',cx:230,cy:175,R:92,simp:sp,keep:k,steps:sp>0.8?0:1,strands:Math.round((1-sp)*10),lw:lerp(1.6,3.4,sp)});
    out(h).innerHTML='단순화 <b>'+f2(sp,2)+'</b> → '+(sp>=0.8?'<b>카툰</b>(기본 도형)':sp<=0.25?'<b>극화·그래픽 노블</b>(사실적)':'<b>애니</b>(가운데)')+' · '+(k?verdict(true,'고정값(검은 긴 머리·은 귀걸이)이 남아 시아로 보입니다'):verdict(false,'고정값이 없어 누구인지 알 수 없습니다'));}
  allIn(h,draw);draw();};
P.p3_brush=function(h){var W=460,H=430;function draw(){var gp=rv(h,'gap')/100,ik=rv(h,'ink'),pt=rv(h,'pattern');var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:'#fbf8f1'},s);
    if(pt){for(var i=0;i<7;i++){var x=30+i*70,y=i%2?60:380;el('path',{d:'M'+P2(x,y)+' q15,-22 30,0 q15,-22 30,0',stroke:'#c9b8a0','stroke-width':3,fill:'none'},s);el('circle',{cx:x+30,cy:y+8,r:10,fill:'none',stroke:'#c9b8a0','stroke-width':3},s);}}
    chara(s,{who:'sia',cx:230,cy:175,R:92,render:'ink',brush:gp,inkW:ik,steps:0,strands:3,lw:1.6});
    var ws=clamp(35+45*gp-1.5*(ik-6),10,95);out(h).innerHTML='선 끊김 <b>'+f2(gp*100,0)+'</b>, 머리 먹 두께 <b>'+ik+'</b> → 여백 약 <b>'+f2(ws,0)+'%</b> · '+(ws>=50&&ws<=70?verdict(true,'수묵 느낌 — 끊긴 자리를 눈이 잇습니다'):ws<50?verdict(false,'여백이 적어 붓을 쓴 일반 그림처럼 보입니다'):verdict(false,'여백이 너무 많아 형태가 무너집니다'))+(pt?' · 전통 무늬는 배경에만, 글씨·도장은 넣지 않습니다':'');}
  allIn(h,draw);draw();};

/* ----- 2부 새 단계: 칠 방식·배경 효과선 ----- */
P.p2_paint=function(h){var W=460,H=430;function draw(){var bl=rv(h,'bleed')/100,sa=rv(h,'sat')/100;var s=svgOf(h,W,H);el('rect',{x:0,y:0,width:W,height:H,fill:bl>0.3?'#fbf7ee':'#fbfcfd'},s);
    var r=chara(s,{who:'sia',cx:230,cy:175,R:92,G:{sat:sa},lw:lerp(2.4,1.0,bl),steps:bl>0.5?1:1,soft:bl>0.5});
    if(bl>0){var cl=r.g.cloneNode(true);cl.setAttribute('filter',blurF(s,bl*9));cl.setAttribute('opacity',(0.35+0.4*bl).toFixed(2));cl.querySelectorAll('[stroke]').forEach(function(e){e.setAttribute('stroke-opacity','0');});s.insertBefore(cl,r.g);r.g.setAttribute('opacity',(1-0.35*bl).toFixed(2));}
    var tag=bl<=0.2&&sa>=1.2?'진한 원색 코믹스·카툰 인상':bl<=0.2?'맑은 평면 색(클리어 라인 계열)':bl>=0.6&&sa<=0.8?'번지는 수채의 예술 만화·동화풍':'평면과 물감 사이';
    out(h).innerHTML='번짐 <b>'+f2(bl*100,0)+'</b>, 채도 <b>'+f2(sa*100,0)+'%</b> → <b>'+tag+'</b>'+(bl>=0.6&&sa>=1.2?' · '+verdict(false,'번지는 칠에 아주 진한 채도 — 탁해 보입니다'):'');}
  allIn(h,draw);draw();};
P.p2_speed=function(h){var W=460,H=430;function draw(){var f={focus:rv(h,'focus'),speed:rv(h,'speed'),flower:rv(h,'flower'),sparkle:rv(h,'sparkle')},n=rv(h,'n');var s=svgOf(h,W,H);bg(s,W,H);var cx=230,cy=190,r=rng(11);
    if(f.focus)for(var i=0;i<n;i++){var a=i/n*Math.PI*2+r()*0.1,R1=150+r()*30,R2=330;el('path',{d:'M'+P2(cx+Math.cos(a)*R1,cy+Math.sin(a)*R1)+' L'+P2(cx+Math.cos(a+0.02)*R2,cy+Math.sin(a+0.02)*R2)+' L'+P2(cx+Math.cos(a-0.02)*R2,cy+Math.sin(a-0.02)*R2)+'Z',fill:INK,opacity:.8},s);}
    if(f.speed)for(var j=0;j<n;j++){var y=20+r()*390,x=r()*200;el('line',{x1:x,y1:y,x2:x+120+r()*140,y2:y,stroke:'#5b6874','stroke-width':1+r()*2,opacity:.6},s);}
    if(f.flower)for(var k=0;k<Math.round(n/4);k++){var fx=30+r()*400,fy=20+r()*390;if(Math.abs(fx-cx)<110&&fy<330)continue;for(var q=0;q<5;q++){var aa=q/5*Math.PI*2;el('ellipse',{cx:fx+Math.cos(aa)*9,cy:fy+Math.sin(aa)*9,rx:7,ry:4.5,transform:'rotate('+(aa*57.3)+' '+(fx+Math.cos(aa)*9)+' '+(fy+Math.sin(aa)*9)+')',fill:'#f7b6c8'},s);}el('circle',{cx:fx,cy:fy,r:4,fill:'#ffd34d'},s);}
    if(f.sparkle)for(var m=0;m<Math.round(n/3);m++){var sx=20+r()*420,sy=20+r()*390,kk=5+r()*8;if(Math.abs(sx-cx)<100&&sy<320)continue;el('path',{d:'M'+P2(sx,sy-kk)+' L'+P2(sx+kk*0.2,sy-kk*0.2)+' L'+P2(sx+kk,sy)+' L'+P2(sx+kk*0.2,sy+kk*0.2)+' L'+P2(sx,sy+kk)+' L'+P2(sx-kk*0.2,sy+kk*0.2)+' L'+P2(sx-kk,sy)+' L'+P2(sx-kk*0.2,sy-kk*0.2)+'Z',fill:'#ffd34d'},s);}
    chara(s,{who:'sia',cx:cx,cy:cy-15,R:80,exp:f.focus||f.speed?'neutral':'smile',lines:f.focus?{brow:true}:{}});
    var act=f.focus||f.speed,love=f.flower||f.sparkle;
    out(h).innerHTML=(act&&love?verdict(false,'긴장(집중선·속도선)과 설렘(꽃·반짝임)이 섞여 장면이 흐려집니다'):act?'<b>긴장·속도</b> — 소년 만화 액션 장면 인상 · 효과선 '+n+'개':love?'<b>설렘</b> — 순정 만화 장면 인상':'배경 비움 — 일상 장면')+(act&&n>=40?' · 선이 많아 인물이 묻힐 수 있습니다':'');}
  allIn(h,draw);draw();};
/* ===================== 4부 등신 ===================== */
P.p4_heads=function(h){var W=460,H=470;function draw(){var hd=rv(h,'heads'),gr=rv(h,'grid');var s=svgOf(h,W,H);bg(s,W,H);var Ht=400,base=440;
    var F=figure(s,{who:'haru',heads:hd,Htot:Ht,base:base,cx:230,adapt:true});
    if(gr){for(var i=0;i<=Math.ceil(hd);i++){var y=base-Ht+i*F.hh;if(y>base+1)break;el('line',{x1:60,y1:y,x2:120,y2:y,stroke:C.teal,'stroke-width':1.5,'stroke-dasharray':'4 3'},s);if(i<Math.floor(hd)+1&&i<hd)ktxt(s,56,y+F.hh/2+4,String(i+1),{anchor:'end',size:12,fill:C.teal,weight:'bold'});}}
    var hh160=160/hd;out(h).innerHTML='키 160 ÷ '+f2(hd,1)+'등신 = 머리 높이 <b>'+f2(hh160,1)+'</b> · '+(hd>=7?'진지하고 멋있는 사실 비율':hd>=5?'애니 기본 비율':hd>=3.5?'가벼운 데포르메':'<b>SD 개그</b> — 그림체일 뿐 나이는 그대로 20대');}
  allIn(h,draw);draw();};
P.p4_parts=function(h){var W=460,H=470;function draw(){var hd=rv(h,'heads'),ad=rv(h,'adapt');var s=svgOf(h,W,H);bg(s,W,H);
    var F=figure(s,{who:'haru',heads:hd,Htot:400,base:440,cx:230,adapt:ad});var ef=F.eyeFrac*100;
    out(h).innerHTML='눈 높이: 머리의 위에서 <b>'+f2(ef,0)+'%</b> · 손: <b>'+(ad&&hd<4?'둥근 덩어리':'손가락 다섯')+'</b> · '+(hd<4?(ad?verdict(true,'SD답게 눈이 내려가고 손이 단순해졌습니다'):verdict(false,'큰 머리에 8등신 얼굴 — 이마가 넓고 손이 답답합니다(7부 f5)')):'사실에 가까운 비율에서는 기본 얼굴 그대로');}
  allIn(h,draw);draw();};
P.p4_mascot=function(h){var W=460,H=430;function draw(){var sz=rv(h,'size')/100,sy=rv(h,'sym'),sf=rv(h,'soft');var s=svgOf(h,W,H);bg(s,W,H);
    var R=80*sz,cx=230,cy=120+(1-sz)*120;var g=el('g',{},s);
    var bodyC=sy>=4?CHAR.haru.cloth:'#d9d9df';var bf=sf?radial(s,bodyC):bodyC;el('ellipse',{cx:cx,cy:cy+R*1.75,rx:R*0.85,ry:R*0.75,fill:bf,stroke:sf?'none':INK,'stroke-width':2},g);
    if(sy>=5){el('path',{d:'M'+P2(cx-R*0.85,cy+R*1.6)+' Q'+P2(cx-R*0.5,cy+R*1.05)+' '+P2(cx-R*0.25,cy+R*1.15)+' L'+P2(cx-R*0.35,cy+R*2.45)+'Z M'+P2(cx+R*0.85,cy+R*1.6)+' Q'+P2(cx+R*0.5,cy+R*1.05)+' '+P2(cx+R*0.25,cy+R*1.15)+' L'+P2(cx+R*0.35,cy+R*2.45)+'Z',fill:'#fff',stroke:sf?'none':INK,'stroke-width':1.5},g);}
    if(sy>=6&&sz>=0.6){for(var b=0;b<3;b++)el('circle',{cx:cx-R*0.32,cy:cy+R*(1.5+b*0.25),r:R*0.045,fill:'#9aa0a8'},g);}
    var savedHair=CHAR.haru.hair;if(sy<1)CHAR.haru.hair='#b9b0a8';
    chara(g,{who:'haru',cx:cx,cy:cy,R:R,headOnly:true,simp:0.9,render:sf?'soft':'cel',steps:sf?0:1,strands:sz>=0.7?3:0,eye:1.2,keep:true});
    if(sy<2)g.querySelectorAll('circle').forEach(function(cc){if(+cc.getAttribute('r')>R*0.25&&+cc.getAttribute('cy')<cy-R*0.8)cc.remove();});
    CHAR.haru.hair=savedHair;
    var list=['분홍 머리','정수리 번 2개','앞머리 남색 줄','라벤더 후드','흰 랩코트','코트 단추'],vis=list.slice(0,sy).filter(function(_,i){return !(i===5&&sz<0.6)&&!(i===2&&sz<0.4);});
    out(h).innerHTML='보이는 크기 <b>'+f2(sz*100,0)+'%</b> · 남긴 상징 '+sy+'개 중 보이는 것: <b>'+vis.join(', ')+'</b>'+(sz<0.6&&sy>=6?' · '+verdict(false,'작게 줄이니 단추가 뭉개집니다'):'')+' · '+(sy>=3&&sy<=4?verdict(true,'상징 세 개 안팎 — 작아도 하루로 읽힙니다'):sy<3?verdict(false,'상징이 너무 적어 누구인지 흐립니다'):'세부가 많아 작게 쓰면 뭉개질 수 있습니다')+(sf?' · 입체 명암으로 형태를 냅니다':'');}
  allIn(h,draw);draw();};
P.p4_motion=function(h){var W=520,H=440;function draw(){var hd=rv(h,'heads'),ex=rv(h,'exag'),gh=rv(h,'ghost');var s=svgOf(h,W,H);bg(s,W,H);var F;
    for(var i=0;i<gh;i++){var t=gh===1?1:i/(gh-1);F=figure(s,{who:'haru',heads:hd,Htot:300,base:410,cx:140+t*120*ex*0.9,adapt:true,kick:t,exag:ex,op:i===gh-1?1:0.18+0.12*i});}
    for(var j=0;j<5;j++)el('line',{x1:120+j*8,y1:300-j*22,x2:120+j*8+90*ex,y2:300-j*22-10,stroke:C.orange,'stroke-width':2,opacity:.45},s);
    var dd=120*ex,gap=dd/(gh-1),vis=ex*F.legRatio/0.43;
    out(h).innerHTML='이동 '+f2(dd,0)+' ÷ (잔상 '+gh+' − 1) = 간격 <b>'+f2(gap,0)+'</b> · 다리 길이/키 '+f2(F.legRatio,2)+' → 보이는 정도 <b>'+f2(vis,2)+'</b> · '+((vis>=0.85&&gap>=40&&gap<=70)?verdict(true,'동작이 또렷하게 읽힙니다'):vis<0.85?verdict(false,'짧은 다리라 동작이 작게 보입니다 — 과장을 늘리세요'):verdict(false,'잔상 간격이 '+(gap<40?'좁아 겹쳐':'넓어 끊겨')+' 보입니다'));}
  allIn(h,draw);draw();};

/* ===================== 5부 표정·과장 ===================== */
P.p5_collapse=function(h){var W=460,H=430;function draw(){var lv=rv(h,'lv'),k=rv(h,'keep');var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'sia',cx:230,cy:175,R:92,collapse:lv,keep:k||lv<3,lostStyle:'short',exp:'open',steps:lv>=2?0:1});
    var nm=['예쁜 작화','단순한 눈','점 눈·큰 입','얼굴 그림자 선','흔들린 윤곽'];
    out(h).innerHTML='무너짐 <b>'+lv+'단계 — '+nm[lv]+'</b> · '+((k||lv<3)?verdict(true,'검은 긴 머리·은 귀걸이가 남아 시아로 읽힙니다'):verdict(false,'고정값까지 무너져 누구인지 모릅니다'));}
  allIn(h,draw);draw();};
P.p5_one=function(h){var W=460,H=430;function draw(){var e=rv(h,'eye'),m=rv(h,'mouth'),sw=rv(h,'sweat');var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'sia',cx:230,cy:175,R:92,exE:e,exM:m,exS:sw,exp:'neutral',hl:2});
    var big=[['눈',e],['입',m],['땀',sw]].filter(function(x){return x[1]>1.05;});var emo={'눈':'놀람','입':'외침','땀':'당황'};
    out(h).innerHTML='과장한 곳 <b>'+big.length+'개</b>'+(big.length?' ('+big.map(function(x){return x[0]+' '+f2(x[1],2)+'배 → 넓이 '+f2(x[1]*x[1],2)+'배';}).join(', ')+')':'')+' · '+(big.length===1?verdict(true,'감정이 또렷합니다: '+emo[big[0][0]]):big.length===0?'아직 과장 없음':verdict(false,'여러 곳을 키워 감정이 흐려집니다(7부 f6)'));}
  allIn(h,draw);draw();};
P.p5_lines=function(h){var W=460,H=430;function draw(){var L={under:rv(h,'under'),brow:rv(h,'brow'),cheek:rv(h,'cheek'),teeth:rv(h,'teeth'),extra:rv(h,'extra')};var s=svgOf(h,W,H);bg(s,W,H);
    chara(s,{who:'doctor',cx:230,cy:175,R:90,lines:L,exp:'neutral',steps:L.cheek?2:1});
    var n=['under','brow','cheek','teeth'].filter(function(k){return L[k];}).length;
    out(h).innerHTML='감정 자리 선 <b>'+n+'개</b>, 잔주름 <b>'+L.extra+'개</b> → '+(n>=3?'<b>지친 베테랑 얼굴</b>':n>=1?'조금 피곤한 얼굴':'평소 얼굴')+' · '+(L.extra>4?verdict(false,'잔주름이 많아 감정보다 나이가 먼저 바뀌어 보입니다'):verdict(true,'나이는 그대로 30대'));}
  allIn(h,draw);draw();};
P.p5_symbols=function(h){var W=460,H=430;var EMO={sweat:'당황·곤란',glow:'위협·불타는 의욕',crack:'충격',heart:'좋아함',note:'기분 좋음',vein:'화남'};var BAD=[['heart','vein'],['note','sweat'],['heart','sweat'],['note','vein']];
  function draw(){var Sy={};Object.keys(EMO).forEach(function(k){Sy[k]=rv(h,k);});var s=svgOf(h,W,H);bg(s,W,H);chara(s,{who:'sia',cx:230,cy:185,R:88,sym:Sy,exp:'neutral'});
    var on=Object.keys(EMO).filter(function(k){return Sy[k];});var clash=BAD.filter(function(p){return Sy[p[0]]&&Sy[p[1]];});
    out(h).innerHTML=(on.length?'읽히는 감정: <b>'+on.map(function(k){return EMO[k];}).join(' + ')+'</b>':'기호 없음 — 무표정')+' · '+(clash.length?verdict(false,'서로 반대 감정의 기호가 함께 있어 흐립니다'):on.length>2?verdict(false,'기호가 많아 어지럽습니다'):on.length?verdict(true,'감정이 한눈에 읽힙니다'):'');}
  allIn(h,draw);draw();};

/* ===================== 6부 매체·옷 ===================== */
P.p6_render=function(h){var W=460,H=430,mode='cel';seg2(h,function(v){mode=v;draw();});
  function draw(){var px=rv(h,'px');var o={who:'haru',cx:230,cy:175,R:92,steps:1,hl:2};var note;
    if(mode==='soft'){o.render='soft';o.steps=0;note='부드러운 3D: 선 대신 둥근 명암, 질감이 매끈해집니다';}else if(mode==='ink'){o.render='ink';o.steps=1;o.tone='dots';o.G={mono:true};note='먹선: 색 대신 선과 망점';}else note='셀 애니: 선 + 또렷한 그림자';
    if(mode==='pixel'){var sv=offSvg(W,H);bg(sv,W,H);chara(sv,o);pixelate(sv,h,W,H,px);note='픽셀: 픽셀 '+px+' → 가는 선과 작은 하이라이트가 사라짐';}
    else{var s=svgOf(h,W,H);bg(s,W,H);chara(s,o);}
    out(h).innerHTML='<b>'+note+'</b> · '+verdict(true,'남는 것: 분홍 머리·번 2개·남색 줄·라벤더 후드(실루엣·색·장식)');}
  allIn(h,draw);draw();};
P.p3_mono=function(h){var W=460,H=430;function draw(){var mono=rv(h,'mono'),tn=rv(h,'tone'),adj=rv(h,'adj');var s=svgOf(h,W,H);bg(s,W,H);
    var hairG=gray(CHAR.haru.hair),clo=CHAR.haru.cloth,clG=gray(clo),k=(clG+adj)/clG;var clAdj=toHex(rgb(hex(clo).map(function(v){return v*k;})));
    var saved=CHAR.haru.cloth;CHAR.haru.cloth=clAdj;chara(s,{who:'haru',cx:230,cy:175,R:92,G:mono?{mono:true}:null,steps:1});CHAR.haru.cloth=saved;
    if(tn){var pat=pattern(s,'dots',4,INK);el('path',{d:'M'+P2(230-138,175+92*2.7)+' Q'+P2(230-135,175+92*1.4)+' '+P2(230-41,175+92*1.28)+' L'+P2(230+41,175+92*1.28)+' Q'+P2(230+135,175+92*1.4)+' '+P2(230+138,175+92*2.7)+'Z',fill:pat,opacity:.55},s);}
    var cg=clG+adj,diff=Math.abs(hairG-cg);
    out(h).innerHTML='분홍 머리 회색값 <b>'+f2(hairG,0)+'</b> · 라벤더 옷 회색값 <b>'+f2(cg,0)+'</b> → 차이 <b>'+f2(diff,0)+'</b> · '+(diff>=40||tn?verdict(true,tn?'망점 무늬로 머리와 옷이 구별됩니다':'밝기 차이로 구별됩니다'):verdict(false,'흑백에서 머리와 옷의 경계가 흐려집니다'));}
  allIn(h,draw);draw();};
P.p6_camera=function(h){var W=460,H=460;function draw(){var cam=rv(h,'cam')/100,wd=rv(h,'wide')/100;var s=svgOf(h,W,H);bg(s,W,H);
    var cx=230,top=60,bot=430,Hh=bot-top,k=cam*0.3*(1+wd);function sc(y){return 1+k*((Hh/2)-(y-top))/(Hh/2);}
    function P_(x,y){return [cx+(x-cx)*sc(y),y];}
    el('line',{x1:0,y1:cam<0?bot+10:cam>0?top+120:bot-40,x2:W,y2:cam<0?bot+10:cam>0?top+120:bot-40,stroke:'#d5dbe2','stroke-width':2},s);
    var hip=top+Hh*0.55,neck=top+Hh*0.24,sw=55;
    var leg=function(x0,x1){var a=P_(x0,hip),b=P_(x1,bot);el('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:'#3b3b48','stroke-width':22*sc(bot),'stroke-linecap':'round'},s);};leg(cx-18,cx-30);leg(cx+18,cx+30);
    var p1=P_(cx-sw,neck),p2=P_(cx+sw,neck),p3=P_(cx+sw*0.8,hip),p4=P_(cx-sw*0.8,hip);el('path',{d:'M'+P2(p1[0],p1[1])+' L'+P2(p2[0],p2[1])+' L'+P2(p3[0],p3[1])+' L'+P2(p4[0],p4[1])+'Z',fill:CHAR.haru.cloth,stroke:INK,'stroke-width':2},s);
    var hand=P_(cx+90,neck+40),hs=14*sc(neck)*(1+wd*1.6);var sh=P_(cx+sw,neck+8);el('line',{x1:sh[0],y1:sh[1],x2:hand[0],y2:hand[1],stroke:'#ffffff','stroke-width':18*sc(neck)*(1+wd*0.5),'stroke-linecap':'round'},s);el('line',{x1:sh[0],y1:sh[1],x2:hand[0],y2:hand[1],stroke:INK,'stroke-width':1.5},s);el('circle',{cx:hand[0],cy:hand[1],r:hs,fill:SKIN,stroke:INK,'stroke-width':2},s);
    var hc=P_(cx,top+Hh*0.12),R=Hh*0.105*sc(top+Hh*0.12);chara(s,{who:'haru',cx:hc[0],cy:hc[1],R:R,headOnly:true,steps:1});
    var tag=cam<=-0.4?'올려다보기 — 크고 당당한 영웅·광고 인상':cam>=0.4?'내려다보기 — 작고 귀엽고 친근한 인상':'눈높이 — 설명용 기본';
    out(h).innerHTML='<b>'+tag+'</b>'+(wd>=0.6?' · 넓은 렌즈 — 내민 손이 '+f2(1+wd*1.6,1)+'배로 커 보여 현장감이 생깁니다':'')+' · 옷과 고정값은 그대로';}
  allIn(h,draw);draw();};
P.p6_outfit=function(h){var W=520,H=430,th='lab';seg2(h,function(v){th=v;draw();});
  var NM={lab:'실험실',punk:'펑크',preppy:'프레피',y2k:'Y2K',autumn:'가을 코디'};
  function draw(){var k=rv(h,'keep'),po=rv(h,'poster');var s=svgOf(h,W,H);var bgc={lab:'#fbfcfd',punk:'#f2e6e6',preppy:'#eef6f1',y2k:'#fde8f3',autumn:'#fbefe0'}[th];el('rect',{x:0,y:0,width:W,height:H,fill:bgc},s);
    var of=th==='lab'?'default':th,lost={punk:'spiky',preppy:'short',y2k:'short',autumn:'short',lab:'short'}[th];
    if(po){chara(s,{who:'moa',cx:190,cy:170,R:105,keep:k,lostStyle:lost,outfit:of,beret:th==='autumn',steps:2,soft:true});var g=el('g',{transform:'translate(330,40) scale(0.45)'},s);chara(g,{who:'moa',cx:200,cy:200,R:90,keep:k,lostStyle:lost,outfit:of,beret:th==='autumn'});
      el('rect',{x:20,y:20,width:200,height:34,rx:6,fill:'none',stroke:C.muted,'stroke-dasharray':'6 4'},s);ktxt(s,120,42,'문구 자리(비워 둠)',{anchor:'middle',size:12});el('rect',{x:0,y:H-44,width:W,height:16,fill:'rgba(0,0,0,.08)'},s);}
    else chara(s,{who:'moa',cx:260,cy:170,R:92,keep:k,lostStyle:lost,outfit:of,beret:th==='autumn',steps:1});
    out(h).innerHTML='테마 <b>'+NM[th]+'</b>'+(po?' · 포스터 구성(큰 얼굴 + 전신 + 문구 자리)':'')+' · '+(k?verdict(true,'머리띠·왼쪽 리본·웨이브 머리가 남아 모아의 베리에이션으로 읽힙니다'):verdict(false,'머리와 장식까지 바꿔 다른 사람처럼 보입니다'));}
  allIn(h,draw);draw();};
P.p6_sheet=function(h){var W=620,H=300;var VER=[['시대',{steps:1,hl:1,lash:0.7,G:{sepia:0.5}}],['선',{ratio:3.5,lw:1.6,steps:0}],['등신',{simp:0.85,eye:1.25}],['표정',{collapse:2,exp:'open'}],['옷',{outfit:'autumn',beret:true}]];
  function draw(){var f={hair:rv(h,'hair'),color:rv(h,'color'),acc:rv(h,'acc'),face:rv(h,'face'),age:rv(h,'age')};var s=svgOf(h,W,H);bg(s,W,H);var r=rng(5);
    var saved={hair:CHAR.sia.hair,style:CHAR.sia.style,acc:CHAR.sia.acc,eye:CHAR.sia.eye};
    VER.forEach(function(v,i){var o={who:'sia',cx:62+i*124,cy:110,R:42};for(var kk in v[1])o[kk]=v[1][kk];
      CHAR.sia.style=f.hair?'long':['short','wavy','spiky','short','wavy'][i];CHAR.sia.hair=f.color?saved.hair:['#6a3d2a','#1E1B22','#3a4a8a','#7a6250','#1E1B22'][i];CHAR.sia.acc=f.acc?'earring':(i%2?null:'earring');
      if(!f.face)o.eyeDrop=[0.08,-0.04,0.12,0,0.06][i];if(!f.age&&v[0]==='등신'){o.eye=1.6;o.simp=0.95;}chara(s,o);ktxt(s,62+i*124,285,v[0],{anchor:'middle',fill:C.ink,size:13});});
    CHAR.sia.hair=saved.hair;CHAR.sia.style=saved.style;CHAR.sia.acc=saved.acc;
    var n=Object.keys(f).filter(function(k){return f[k];}).length;out(h).innerHTML='고정값 <b>'+n+' / 5</b> → 일관성 <b>'+(n*20)+'%</b> · '+(n===5?verdict(true,'화풍이 달라도 다섯 버전 모두 시아입니다'):verdict(false,'고정되지 않은 것: '+['머리 모양','머리·눈 색','장식','얼굴 기준선','성인 나이'].filter(function(_,i){return !f[['hair','color','acc','face','age'][i]];}).join(', ')));}
  allIn(h,draw);draw();};

/* ===================== 7부 진단 ===================== */
var DIAG_ITEMS=['① 정체성 고정값','② 바꾸는 축','③ 등신·나이','④ 과장','⑤ 매체·글자·출처'];
var DIAG_FIRST=[0,1,1,2,2,3,3,4];
var DIAG_FIX=['고정값 조각: 머리띠·왼쪽 리본·웨이브 머리를 적고 화풍만 바꾸기','축 하나만: Change only one thing','군집을 한쪽으로: clean cel shading only, no watercolor, no 3D','성인 명시: adult in her twenties drawn in SD style, not a child','SD 부위: eyes low in the large head, mitten-like hands','한 곳 과장: only the eyes are exaggerated','웃음의 방향: expression only, keep his face shape, no mocking','글자·출처: no text, no seals; describe style by features, no titles'];
P.p7_diag=function(h){var sel=pick(h,'select');var st=0;
  function draw(){var cs=+sel.value,first=DIAG_FIRST[cs];h.innerHTML='';var list=document.createElement('div');list.style.cssText='display:flex;flex-direction:column;gap:6px';h.appendChild(list);
    DIAG_ITEMS.forEach(function(t,i){var b=document.createElement('button');b.type='button';b.className='btn';b.style.textAlign='left';b.textContent=t+(i<st?(i===first?' — 걸림':' — 통과'):'');
      if(i<st)b.style.borderColor=i===first?C.red:C.green;b.disabled=i!==st||st>first;b.addEventListener('click',function(){st=i+1;draw();});list.appendChild(b);});
    out(h).innerHTML=st>first?verdict(false,'처음 걸린 항목: '+DIAG_ITEMS[first])+'<br>고치는 조각 — '+DIAG_FIX[cs]+'<br><span class="muted">걸린 곳을 고친 뒤 나머지 항목을 다시 봅니다.</span>':'위에서부터 차례로 눌러 점검하세요. 지금 볼 항목: <b>'+DIAG_ITEMS[st]+'</b>';}
  sel.addEventListener('change',function(){st=0;draw();});draw();};

/* ===================== 8부 실전 연습장 ===================== */
function practice(){var root=document.getElementById('practice');if(!root)return;var tabs=root.querySelectorAll('.tabs button'),scenes=root.querySelectorAll('.scene');
  function show(id){tabs.forEach(function(b){b.classList.toggle('on',b.dataset.t===id);});scenes.forEach(function(s){s.classList.toggle('on',s.id===id);});if(history.replaceState)history.replaceState(null,'','#'+id);}
  tabs.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t);});});var hsh=(location.hash||'').slice(1);show([].some.call(scenes,function(s){return s.id===hsh;})?hsh:'bench');
  bench();sortBoard();workshop();desk();}
function wire(S,f){S.querySelectorAll('.ctrl input,.ctrl select').forEach(function(i){i.addEventListener(i.tagName==='SELECT'||i.type==='checkbox'?'change':'input',f);});}
var TARGET={retro:['80년대 셀화',[0.1,0.5,0.55,0.2,0.1,0.7]],sd:['SD 개그',[0.85,0.35,0.05,0.75,0.1,0.85]],ink:['수묵 붓선',[0.8,0.9,0.6,0.1,0.5,0.0]],toy:['3D 마스코트',[0.95,0.1,0.05,0.1,0.95,0.8]],graphic:['흑백 그래픽 노블',[0.55,0.75,0.95,0.25,0.4,0.15]],sketch:['흑백 러프 선화',[0.85,0.35,0.6,0.4,0.0,0.0]],modern:['지금의 애니',[0.95,0.25,0.5,0.3,0.15,0.85]]};
function featStyle(f,who){var era=f[0],line=f[1],real=f[2],exag=f[3],media=f[4],color=f[5];
  var o={who:who,steps:era<0.4?1:2,soft:era>0.6,hl:era<0.4?1:era>0.75?3:2,lash:era<0.4?0.7:0.25,lw:lerp(1.6,3.2,line),ratio:lerp(1,4,line),simp:1-real,collapse:Math.round(clamp(exag-0.3,0,0.7)/0.7*3),strands:Math.round(lerp(3,12,real))};
  if(real<0.2){o.eye=1.2;o.eyeDrop=0.1;}
  if(media>0.7){o.render='soft';o.steps=0;}
  if(color<0.15){o.G={mono:true};if(line>0.8){o.render='ink';o.brush=0.4;o.tone=null;}else o.tone=line>0.6?'hatch':'dots';}
  else{o.G={sat:lerp(0.5,1.25,color),sepia:era<0.3?0.55:0};}
  return o;}
function bench(){var S=document.getElementById('bench');if(!S)return;var q=function(n){return S.querySelector('[name='+n+']');};var touched=false,hit={};
  function upd(e){if(e)touched=true;var tk=q('target').value,T=TARGET[tk][1];var f=['era','line','real','exag','media','color'].map(function(n){return +q(n).value/100;});var d=dist(f,T);
    if(d<=0.25&&touched)hit[tk]=1;var nm=['시대','선','사실','과장','재료','색'];var worst=f.map(function(v,i){return [Math.abs(v-T[i]),i];}).sort(function(a,b){return b[0]-a[0];})[0];
    board(S.querySelector('.board'),[['목표',TARGET[tk][0],true],['거리',f2(d,2),d<=0.25],['가장 먼 축',nm[worst[1]]+' ('+(f[worst[1]]<T[worst[1]]?'올리기':'내리기')+')',worst[0]<0.1],['완성한 목표',Object.keys(hit).length+' / 7',Object.keys(hit).length===7]]);
    var s=el('svg',{viewBox:'0 0 360 360',role:'img','aria-label':'베리에이션 작업대 그림'});var g1=S.querySelector('.g1');g1.innerHTML='';g1.appendChild(s);el('rect',{x:0,y:0,width:360,height:360,fill:'#fbfcfd'},s);
    var o=featStyle(f,q('who').value);o.cx=180;o.cy=140;o.R=72;chara(s,o);
    var s2=el('svg',{viewBox:'0 0 360 220',role:'img','aria-label':'목표까지 축별 거리'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s2);
    nm.forEach(function(t,i){var v=Math.abs(f[i]-T[i]);el('rect',{x:80,y:12+i*34,width:Math.max(4,250*v),height:22,rx:5,fill:v<0.1?C.green:C.orange},s2);ktxt(s2,74,28+i*34,t,{size:12.5,anchor:'end',fill:C.ink});});
    var M=[!!hit[tk],Object.keys(hit).length>=3,Object.keys(hit).length===7];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','목표 '+TARGET[tk][0]+'까지 거리 '+f2(d,2)+'. 0.25 이하면 완성.'],['haru','e10','조수','가장 먼 축은 '+nm[worst[1]]+'이에요. 하나씩 맞춰 봐요.'],['fruitfly','e09','초파리','고정값은 손잡이가 아니야. '+CHAR[q('who').value].name+'의 머리와 장식은 언제나 그대로.']]);}
  wire(S,upd);upd();}
function sortBoard(){var S=document.getElementById('sort');if(!S)return;var D=stylePts();if(!D)return;var r=rng(Date.now()%9973+3);var cur=null,right=0,edge=0,used={},touched=false,seen=0;
  function next(){var gs=[1,2,3,4,5,6,7],g=gs[Math.floor(r()*7)];var cand=D.pts.filter(function(p){return p.g===g||p.alt===g;});cur=cand[Math.floor(r()*cand.length)];
    S.querySelector('.sym').textContent='카드: '+cur.d+(cur.alt?'  [경계 카드]':'');var o=S.querySelector('.sortopts');o.innerHTML='';
    gs.forEach(function(k){var b=document.createElement('button');b.type='button';b.textContent=D.groups[k];b.addEventListener('click',function(){touched=true;var ok=k===cur.g||k===cur.alt;
      if(ok){right++;used[k]=1;if(cur.alt)edge++;b.classList.add('ok');setTimeout(next,380);}else b.classList.add('no');upd(ok,k);});o.appendChild(b);});}
  function upd(ok,k){var n=Object.keys(used).length;board(S.querySelector('.board'),[['맞힘',right,right>=5],['경계 카드',edge,edge>=2],['쓴 군집',n+' / 7',n===7],['지금 카드',cur&&cur.alt?'경계':'보통',true]]);
    var M=[right>=5,edge>=2,n===7];if(touched)missions(S.querySelector('.missions'),M,true);
    var s=el('svg',{viewBox:'0 0 360 290',role:'img','aria-label':'군집별 넣은 카드'});var g=S.querySelector('.g2');g.innerHTML='';g.appendChild(s);
    [1,2,3,4,5,6,7].forEach(function(k2,i){el('rect',{x:12+(i%3)*116,y:20+Math.floor(i/3)*90,width:106,height:70,rx:8,fill:used[k2]?'#e8f6ec':'#f2f4f7',stroke:used[k2]?C.green:'#d5dbe2'},s);ktxt(s,65+(i%3)*116,60+Math.floor(i/3)*90,D.groups[k2]+(used[k2]?' ✓':''),{size:12,anchor:'middle',fill:C.ink});});
    say(S.querySelector('.talk'),[['doctor','e10','박사',ok===undefined?'카드를 보고 가장 크게 바뀐 축을 떠올려 보자.':ok?'맞았다. '+(cur.alt?'경계 카드라 두 군집 모두 정답이다.':''):'다시. 이 그림에서 무엇이 가장 크게 바뀌었나?'],['sia','e10','시아',cur?'이 카드의 군집: '+D.groups[cur.g]+(cur.alt?' 또는 '+D.groups[cur.alt]:''):''],['jupanbot','e16','주판봇','그림마다 정답 하나씩이면 편할 텐데요…']]);}
  next();upd();}
function variationForm(host,onchange){var form=document.createElement('div');form.style.cssText='display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px 14px;width:100%';host.appendChild(form);
  var F=[['who','캐릭터',[['haru','하루'],['sia','시아'],['moa','모아']]],['axis','바꾸는 축',[['','(고르기)'],['retro','시대: 80년대 셀화'],['ink','선: 수묵 붓선'],['sd','등신: 2.5등신 SD'],['collapse','과장: 개그 무너짐'],['toy','재료: 3D 마스코트'],['outfit','옷: 가을 코디']]],
    ['axis2','두 번째 축',[['','없음'],['retro','시대'],['toy','재료'],['outfit','옷']]],['heads','등신',[['','(고르기)'],['std','기본 비율'],['sd','2.5등신 SD']]],['exag','과장',[['','(고르기)'],['none','과장 없음'],['one','한 곳만'],['many','여러 곳']]],['desc','화풍 적는 법',[['','(고르기)'],['feat','특징으로(선·명암·색·비율)'],['name','유명 작품 이름으로']]]];
  F.forEach(function(f){var l=document.createElement('label');l.textContent=f[1]+' ';var s=document.createElement('select');s.name=f[0];f[2].forEach(function(o){var op=document.createElement('option');op.value=o[0];op.textContent=o[1];s.appendChild(op);});s.addEventListener('change',onchange);l.appendChild(s);form.appendChild(l);});
  [['keep','고정값 문장 넣기'],['adult','성인 명시'],['notext','글자·도장 금지']].forEach(function(c){var l=document.createElement('label');var i=document.createElement('input');i.type='checkbox';i.name=c[0];i.addEventListener('change',onchange);l.appendChild(i);l.appendChild(document.createTextNode(' '+c[1]));form.appendChild(l);});
  return function(){var o={};form.querySelectorAll('select').forEach(function(s){o[s.name]=s.value;});form.querySelectorAll('input').forEach(function(i){o[i.name]=i.checked;});return o;};}
var KEEPTXT={haru:'keep exactly: long pink hair with navy streaks, two round buns on top, a navy streak down the center of the bangs, lavender hoodie',sia:'keep exactly: long straight black hair, no headdress, small silver earrings, gray eyes',moa:'keep exactly: ash-beige wavy hair, white frilled maid headband with a white ribbon over her LEFT ear, amber eyes'};
var AXTXT={retro:'change only the drawing style to a retro cel look: one hard-edged shadow tone, one eye highlight, heavy upper lashes, thick outlines',ink:'change only the drawing style to black ink brush painting: broken brush lines, large empty white space, bold black strokes for the hair',sd:'change only the proportions to 2.5-head-tall comedy SD: eyes low in the large head, simple mitten-like hands',collapse:'change only the expression to a comical collapsed face: dot eyes and a big open mouth',toy:'change only the rendering to a smooth vinyl mascot figure: rounded shapes, no outlines',outfit:'change only the outfit to an autumn look: cream cable-knit sweater, teal plaid scarf, beige beret, long plaid skirt'};
function varPrompt(o){var t=['Illustration of '+{haru:'Haru',sia:'Sia',moa:'Moa'}[o.who]+' from the reference images.'],sc=0,miss=[],warn=[];
  if(o.keep){t.push(KEEPTXT[o.who]+'.');sc++;}else miss.push('고정값');
  if(o.axis&&!o.axis2){t.push(AXTXT[o.axis]+'.');sc++;}else if(o.axis&&o.axis2){t.push(AXTXT[o.axis]+'; also change '+o.axis2+'.');warn.push('축을 두 개 바꾸면 무엇이 바뀌었는지 모릅니다(7부 f2)');}else miss.push('바꾸는 축');
  if(o.heads){t.push(o.heads==='sd'?'2.5 heads tall.':'natural adult proportions.');sc++;}else miss.push('등신');
  if(o.exag==='none'||o.exag==='one'){t.push(o.exag==='one'?'exaggerate only one feature.':'calm expression, no exaggeration.');sc++;}else if(o.exag==='many'){t.push('exaggerate everything.');warn.push('과장이 여러 곳이면 감정이 흐려집니다(7부 f6)');}else miss.push('과장');
  if(o.desc==='feat'){sc++;}else if(o.desc==='name'){t.push('in the style of a famous anime.');warn.push('작품 이름을 쓰면 남의 캐릭터를 닮습니다(7부 f8)');}else miss.push('특징 표현');
  if(o.adult&&o.notext){t.push('She is an adult woman in her twenties, not a child. No text, no letters, no calligraphy, no seals, no logos.');sc++;}else{if(o.adult)t.push('She is an adult woman in her twenties, not a child.');if(o.notext)t.push('No text, no letters, no calligraphy, no seals, no logos.');miss.push('성인과 금지');}
  if((o.heads==='sd'||o.axis==='sd')&&!o.adult)warn.push('SD인데 성인 표기가 없어 어려 보일 수 있습니다(7부 f4)');
  if(o.axis==='ink'&&!o.notext)warn.push('수묵풍은 가짜 글씨·도장이 잘 들어갑니다. 글자 금지를 넣으세요');
  if(o.axis==='sd'&&o.heads==='std')warn.push('축은 SD인데 등신은 기본 비율 — 서로 맞지 않습니다');
  return {text:t.join('\n'),score:sc,miss:miss,warn:warn};}
function workshop(){var S=document.getElementById('workshop');if(!S)return;var touched=false;var get=variationForm(S.querySelector('.ow'),function(){touched=true;upd();});var job=S.querySelector('[name=job]');job.addEventListener('change',function(){touched=true;upd();});
  function upd(){var o=get(),r=varPrompt(o);S.querySelector('.g1 pre').textContent=r.text;var jobOk={sticker:o.heads==='sd'&&o.adult,retro:o.axis==='retro'&&o.keep,ink:o.axis==='ink'&&o.notext&&o.desc==='feat'}[job.value];
    board(S.querySelector('.board'),[['점검표',r.score+' / 6',r.score===6],['요청 상황 맞춤',jobOk?'맞음':'부족',jobOk],['경고',r.warn.length+'개',r.warn.length===0],['성인 명시',o.adult?'있음':'없음',o.adult]]);
    var s=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'점검표 막대'});var g2=S.querySelector('.g2');g2.innerHTML='';g2.appendChild(s);var ok6=[o.keep,o.axis&&!o.axis2,!!o.heads,o.exag==='none'||o.exag==='one',o.desc==='feat',o.adult&&o.notext];
    ['고정값','축 하나','등신','과장','특징 표현','성인·금지'].forEach(function(t,i){el('rect',{x:86,y:14+i*30,width:ok6[i]?250:40,height:20,rx:4,fill:ok6[i]?C.teal:'#e3e8ee'},s);ktxt(s,80,29+i*30,t,{size:12.5,anchor:'end',fill:C.ink});});
    var M=[r.score===6&&r.warn.length===0,o.heads==='sd'&&o.adult&&(o.axis==='sd'||!o.axis2),o.axis==='ink'&&o.notext&&o.desc==='feat'];if(touched)missions(S.querySelector('.missions'),M,true);
    say(S.querySelector('.talk'),[['doctor','e10','박사','요청 상황: '+job.options[job.selectedIndex].text+'. '+(jobOk?'필요한 조각이 들어 있다.':'이 상황에 꼭 필요한 조각이 빠졌다.')],['haru','e10','조수','점검표 '+r.score+' / 6'+(r.miss.length?', 빠진 것: '+r.miss.join(', '):'!')],['fruitfly','e09','초파리',r.warn.length?r.warn[0]:'경고 없음. 고정값은 붙잡고 축 하나만 돌렸어.']]);}
  var cp=S.querySelector('.copy');if(cp)cp.addEventListener('click',function(){var t=S.querySelector('.g1 pre').textContent;if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){cp.textContent='복사했습니다';},function(){cp.textContent='직접 선택해 복사하세요';});});upd();}
var DESK_CA=['고정값 빠짐','두 축 동시 변경','군집 사이 어중간','SD 나이 쏠림','SD 부위 그대로','과장 여러 곳','외모 조롱','가짜 글씨·작품 이름'];
var DESK_SYM=['수묵풍으로 바꿨더니 머리띠와 리본이 사라져 누구인지 모른다','80년대풍과 3D 피규어를 한 번에 요청해 무엇이 바뀌었는지 비교할 수 없다','셀도 수채도 3D도 아닌 질감이라 선과 명암이 탁하다','2.5등신 SD가 성인 연구원이 아니라 아이처럼 보인다','큰 머리의 한가운데에 눈이 있어 이마가 넓고, 작은 손에 손가락이 빽빽하다','눈·입·땀·하트를 모두 키워 놀란 건지 좋아하는 건지 모른다','개그 얼굴인데 코와 턱을 흉하게 바꿔 생김새를 놀리는 것 같다','수묵풍 옆에 뜻 없는 글씨와 도장이 있고 남의 작품 옷을 입었다'];
function desk(){var S=document.getElementById('desk');if(!S)return;var CA=DESK_CA,SYM=DESK_SYM;
  var cur=0,streak=0,seen={},wrong=0,right=0,touched=false;var r=rng(Date.now()%9999+1);
  function next(){cur=Math.floor(r()*8);S.querySelector('.sym').textContent='증상: '+SYM[cur];var o=S.querySelector('.deskopts');o.innerHTML='';
    var opts=[cur];while(opts.length<4){var k=Math.floor(r()*8);if(opts.indexOf(k)<0)opts.push(k);}opts.sort(function(){return r()-.5;});
    opts.forEach(function(k){var b=document.createElement('button');b.type='button';b.textContent=CA[k];b.addEventListener('click',function(){touched=true;if(k===cur){streak++;right++;seen[cur]=1;b.classList.add('ok');setTimeout(next,500);}else{streak=0;wrong++;b.classList.add('no');}upd();});o.appendChild(b);});}
  function upd(){var n=Object.keys(seen).length;board(S.querySelector('.board'),[['연속 정답',streak,streak>=3],['맞힌 종류',n+' / 8',n===8],['맞힘',right,right>0],['틀림',wrong,wrong===0]]);
    var M=[streak>=3,n===8,right>=5&&wrong===0];if(touched)missions(S.querySelector('.missions'),M,true);
    var s=el('svg',{viewBox:'0 0 360 200',role:'img','aria-label':'맞힌 실패 종류'});var g=S.querySelector('.g2');g.innerHTML='';g.appendChild(s);CA.forEach(function(t,i){el('rect',{x:16+(i%4)*86,y:20+Math.floor(i/4)*90,width:78,height:70,rx:8,fill:seen[i]?'#e8f6ec':'#f2f4f7',stroke:seen[i]?C.green:'#d5dbe2'},s);ktxt(s,55+(i%4)*86,60+Math.floor(i/4)*90,'f'+(i+1)+(seen[i]?' ✓':''),{size:14,anchor:'middle',fill:C.ink});});
    say(S.querySelector('.talk'),[['doctor','e10','박사','순서: 고정값 → 바꾸는 축 → 등신·나이 → 과장 → 매체·글자·출처.'],['haru','e10','조수','연속 '+streak+'개, 맞힌 종류 '+n+' / 8이에요.'],['x2','e09','평가단 X2',wrong?'틀린 건 7부 실패 카드에서 다시 보세요.':'아직 틀린 게 없어요!']]);}
  next();upd();}
/* 프롬프트 복사 버튼(직접 만들기 실습) */
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.promptbox .copy');if(!b||b.closest('#workshop'))return;var pre=b.parentNode.querySelector('pre');if(!pre)return;var t=pre.textContent;
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(function(){b.textContent='복사했습니다';},function(){b.textContent='직접 선택해 복사하세요';});else b.textContent='직접 선택해 복사하세요';});
/* ===================== 퀴즈·지식 색인·꾸러미 ===================== */
function quiz(q){var ans=+q.getAttribute('data-ans');var fb=q.querySelector('.fb');var OK=q.querySelector('.qok'),NO=q.querySelector('.qno');q.querySelectorAll('.opts button').forEach(function(b,i){b.addEventListener('click',function(){q.querySelectorAll('.opts button').forEach(function(x){x.classList.remove('ok','no');});b.classList.add(i===ans?'ok':'no');fb.innerHTML=i===ans?'⭕ '+OK.innerHTML:'❌ '+NO.innerHTML;});});}
function kg(){var raw=document.getElementById('kg-raw');var mount=document.getElementById('kg-mount');if(!raw||!mount)return;var K=JSON.parse(raw.textContent);
  mount.innerHTML='<input class="kg-search" type="search"><div class="kg-list"></div>';var list=mount.querySelector('.kg-list'),inp=mount.querySelector('input');inp.placeholder='개념 찾기 (예: 등신, 굵기 비, 군집)';inp.setAttribute('aria-label','지식 색인 검색');
  var TY={Concept:'개념',Method:'방법',Analogy:'비유',Application:'쓰임',OpenQuestion:'열린 질문'};var pre=document.body.getAttribute('data-root')||'';
  function render(){var qv=inp.value.trim().toLowerCase();list.innerHTML=K.nodes.filter(function(n){return !qv||(n.label.ko+' '+n.label.en+' '+n.definition.ko).toLowerCase().indexOf(qv)>=0;}).map(function(n){
    var nb=K.edges.filter(function(e){return e.s===n.id||e.o===n.id;}).map(function(e){var o=e.s===n.id?e.o:e.s;var m=K.nodes.filter(function(x){return x.id===o;})[0];return m?m.label.ko:'';}).filter(Boolean);
    return '<div class="kg-item"><span class="t">'+(TY[n.type]||n.type)+'</span><b>'+n.label.ko+'</b><span class="muted">'+n.label.en+'</span><div>'+n.definition.ko+'</div>'+(nb.length?'<div class="muted" style="font-size:12.5px">이웃: '+nb.join(', ')+'</div>':'')+'<a href="'+pre+n.page+n.anchor+'">설명 보러 가기 →</a></div>';}).join('');}
  inp.addEventListener('input',render);render();var ex=document.getElementById('export-mount');if(!ex)return;
  ex.innerHTML='<div class="exp-btns"><button class="btn" data-x="json">kg.json</button><button class="btn" data-x="ld">JSON-LD</button><button class="btn" data-x="ttl">Turtle (Protégé)</button><button class="btn" data-x="csv">CSV (Neo4j·Gephi)</button><button class="btn" data-x="bib">BibTeX</button><button class="btn" data-x="ris">RIS</button></div>';
  function dl(name,text,type){var b=new Blob([text],{type:type||'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);}
  var base=K.page;var refs=JSON.parse((document.getElementById('refs-csl')||{textContent:'[]'}).textContent);
  ex.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){var x=b.getAttribute('data-x');
    if(x==='json')dl(base+'.kg.json',JSON.stringify(K,null,2),'application/json');
    if(x==='ld')dl(base+'.jsonld',document.getElementById('kg-ld').textContent,'application/ld+json');
    if(x==='ttl'){var t='@prefix lab: <urn:lab:> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n';K.nodes.forEach(function(n){t+='<urn:'+n.id+'> a lab:'+n.type+' ;\n  skos:prefLabel "'+n.label.ko+'"@ko , "'+n.label.en+'"@en ;\n  rdfs:comment "'+n.definition.ko.replace(/"/g,'\\"')+'"@ko .\n\n';});K.edges.forEach(function(e){t+='<urn:'+e.s+'> lab:'+e.p+' <urn:'+e.o+'> .\n';});dl(base+'.ttl',t,'text/turtle');}
    if(x==='csv'){var c='id,type,label_ko,label_en,anchor\n'+K.nodes.map(function(n){return [n.id,n.type,n.label.ko,n.label.en,n.page+n.anchor].map(function(v){return '"'+String(v).replace(/"/g,'""')+'"';}).join(',');}).join('\n');c+='\n\nsource,relation,target\n'+K.edges.map(function(e){return [e.s,e.p,e.o].join(',');}).join('\n');dl(base+'.csv',c,'text/csv');}
    if(x==='bib')dl(base+'.bib',refs.map(function(r){return '@misc{'+r.id+',\n  title = {'+r.title+'},\n  author = {'+r.author+'},\n  note = {'+(r.note||'')+'},\n  year = {'+r.year+'}\n}';}).join('\n\n'));
    if(x==='ris')dl(base+'.ris',refs.map(function(r){return 'TY  - GEN\nTI  - '+r.title+'\nAU  - '+r.author+'\nPY  - '+r.year+'\nN1  - '+(r.note||'')+'\nER  - ';}).join('\n'));});});}

function boot(){document.querySelectorAll('[data-panel]').forEach(function(h){var k=h.getAttribute('data-panel');if(P[k]){try{P[k](h);}catch(e){h.textContent='실험을 불러오지 못했습니다.';if(window.console)console.warn(k,e);}}});
  document.querySelectorAll('.quiz').forEach(quiz);kg();practice();
  var pr=document.getElementById('prog');if(pr)window.addEventListener('scroll',function(){var d=document.documentElement;pr.style.width=(100*d.scrollTop/Math.max(1,d.scrollHeight-d.clientHeight))+'%';},{passive:true});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
