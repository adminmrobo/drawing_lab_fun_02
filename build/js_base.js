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

