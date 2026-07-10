// 移动端侧边栏开合
(function () {
  var btn = document.querySelector(".menu-toggle");
  var side = document.querySelector(".sidebar");
  if (!btn || !side) return;

  btn.addEventListener("click", function () {
    side.classList.toggle("open");
  });

  // 点击导航链接后自动收起（移动端）
  side.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      side.classList.remove("open");
    }
  });

  // 点击页面其余区域收起
  document.addEventListener("click", function (e) {
    if (
      side.classList.contains("open") &&
      !side.contains(e.target) &&
      !btn.contains(e.target)
    ) {
      side.classList.remove("open");
    }
  });
})();
