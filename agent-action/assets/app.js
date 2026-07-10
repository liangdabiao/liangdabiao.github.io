
document.addEventListener('DOMContentLoaded', function () {
  // 高亮当前页
  var path = location.pathname.split('/').pop();
  if (!path) path = 'index.html';
  document.querySelectorAll('.toc a').forEach(function (a) {
    if (a.getAttribute('data-file') === path) a.classList.add('active');
  });

  // 移动端目录开关
  var btn = document.getElementById('menuBtn');
  var sb = document.getElementById('sidebar');
  var scrim = document.getElementById('scrim');
  function close() { if (sb) sb.classList.remove('open'); if (scrim) scrim.classList.remove('show'); }
  if (btn) btn.addEventListener('click', function () {
    if (sb) sb.classList.toggle('open');
    if (scrim) scrim.classList.toggle('show');
  });
  if (scrim) scrim.addEventListener('click', close);

  // Mermaid 渲染：把 <pre><code class="language-mermaid"> 转成 <div class="mermaid">
  if (window.mermaid) {
    mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose', flowchart: { htmlLabels: true } });
    var blocks = document.querySelectorAll('pre code.language-mermaid');
    blocks.forEach(function (el) {
      var div = document.createElement('div');
      div.className = 'mermaid';
      div.textContent = el.textContent;
      el.parentNode.replaceWith(div);
    });
    if (blocks.length) mermaid.run();
  }
});
