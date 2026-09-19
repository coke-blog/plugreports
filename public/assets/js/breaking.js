/* breaking.js — self-contained breaking carousel. Runs immediately (DOM ready or defer-safe). */
(function () {
  var timer = null, idx = 0;
  function show(box, slides, dots, i) {
    idx = (i + slides.length) % slides.length;
    for (var j = 0; j < slides.length; j++) slides[j].classList.toggle('on', j === idx);
    for (var j = 0; j < dots.length; j++) dots[j].classList.toggle('on', j === idx);
  }
  function auto(box, slides, dots) { clearInterval(timer); timer = setInterval(function () { show(box, slides, dots, idx + 1); }, 6000); }
  function init() {
    var box = document.getElementById('breaking'); if (!box) return;
    var slides = box.querySelectorAll('.b-slide'); if (!slides.length) return;
    var dots = box.querySelectorAll('.b-dot');
    for (var d = 0; d < dots.length; d++) (function (dd) { dots[dd].onclick = function () { show(box, slides, dots, +dots[dd].getAttribute('data-i')); auto(box, slides, dots); }; })(d);
    var pv = box.querySelector('.b-prev'), nx = box.querySelector('.b-next');
    if (pv) pv.onclick = function () { show(box, slides, dots, idx - 1); auto(box, slides, dots); };
    if (nx) nx.onclick = function () { show(box, slides, dots, idx + 1); auto(box, slides, dots); };
    box.onmouseenter = function () { clearInterval(timer); };
    box.onmouseleave = function () { auto(box, slides, dots); };
    show(box, slides, dots, 0); auto(box, slides, dots);
  }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
  window._breakingInit = init;
})();
