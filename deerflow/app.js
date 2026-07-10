function onScroll(){
  var h=document.documentElement, b=document.body;
  var sc=h.scrollTop||b.scrollTop, height=h.scrollHeight-h.clientHeight;
  var pct=height>0?(sc/height*100):0;
  var bar=document.getElementById('progress');
  if(bar) bar.style.width=pct+'%';
}
window.addEventListener('scroll',onScroll,{passive:true});
onScroll();
var prev=document.querySelector('.pager-btn');
var next=document.querySelectorAll('.pager-btn');
var nxt=next.length>1?next[1]:null;
document.addEventListener('keydown',function(e){
  var t=e.target;
  if(t&&/INPUT|TEXTAREA/.test(t.tagName))return;
  if(e.key==='ArrowLeft'&&prev){window.location.href=prev.href;}
  if(e.key==='ArrowRight'&&nxt){window.location.href=nxt.href;}
});