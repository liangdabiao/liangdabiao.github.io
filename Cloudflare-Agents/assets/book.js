// 主题切换
(function(){
  var root=document.documentElement;
  try{var t=localStorage.getItem('cf-theme');if(t)root.setAttribute('data-theme',t);}catch(e){}
  document.getElementById('themeBtn').addEventListener('click',function(){
    var cur=root.getAttribute('data-theme')==='dark'?'light':'dark';
    root.setAttribute('data-theme',cur);
    try{localStorage.setItem('cf-theme',cur);}catch(e){}
  });
  // 移动端抽屉
  var body=document.body,menu=document.getElementById('menuBtn'),scrim=document.getElementById('scrim');
  if(menu){menu.addEventListener('click',function(){body.classList.toggle('sidebar-open');});}
  if(scrim){scrim.addEventListener('click',function(){body.classList.remove('sidebar-open');});}
  document.querySelectorAll('.toc-link,.toc-home').forEach(function(a){
    a.addEventListener('click',function(){body.classList.remove('sidebar-open');});
  });
  // 代码复制按钮
  document.querySelectorAll('.highlight').forEach(function(pre){
    var btn=document.createElement('button');
    btn.className='copy-btn';btn.textContent='复制';
    btn.addEventListener('click',function(){
      var code=pre.querySelector('code');var txt=code?code.innerText:pre.innerText;
      navigator.clipboard.writeText(txt).then(function(){btn.textContent='已复制';setTimeout(function(){btn.textContent='复制';},1500);});
    });
    pre.appendChild(btn);
  });
})();
