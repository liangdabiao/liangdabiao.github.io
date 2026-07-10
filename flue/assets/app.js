
(function(){
  var root = document.documentElement;
  function applyTheme(t){
    root.setAttribute('data-theme', t);
    var btn = document.getElementById('themeBtn');
    if(btn) btn.textContent = (t === 'dark') ? '☀️' : '🌙';
  }
  var saved = localStorage.getItem('flue-theme');
  if(saved){ applyTheme(saved); }
  else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){ applyTheme('dark'); }
  else { applyTheme('light'); }

  var themeBtn = document.getElementById('themeBtn');
  if(themeBtn){ themeBtn.addEventListener('click', function(){
    var next = (root.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
    applyTheme(next); localStorage.setItem('flue-theme', next);
  }); }

  var menuBtn = document.getElementById('menuBtn');
  var sidebar = document.getElementById('sidebar');
  if(menuBtn && sidebar){ menuBtn.addEventListener('click', function(){ sidebar.classList.toggle('open'); }); }
  if(sidebar){ sidebar.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click', function(){ sidebar.classList.remove('open'); });
  }); }
})();
