// あっぷるキャピタルグループ 企業サイト v9 下層ページ共通の動き
document.addEventListener('DOMContentLoaded', function(){
  var H=document.documentElement, ANIM=H.classList.contains('anim');

  // スマホのメニュー
  var mb=document.querySelector('.mbtn'), mn=document.querySelector('.mnav');
  if(mb && mn){ mb.addEventListener('click',function(){ var o=mn.classList.toggle('open'); mb.setAttribute('aria-expanded',o?'true':'false'); document.body.style.overflow=o?'hidden':''; });
    mn.querySelectorAll('a').forEach(function(a){ a.addEventListener('click',function(){ mn.classList.remove('open'); document.body.style.overflow=''; }); }); }

  // 表示されたら浮かび上がる（地図・年表・組み文字も同じ合図で動く）
  var rv=[].slice.call(document.querySelectorAll('.rv'));
  if(!ANIM || !('IntersectionObserver' in window)){ rv.forEach(function(e){e.classList.add('in')}); }
  else { var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} }); },{rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(e){io.observe(e)}); window.addEventListener('beforeprint',function(){rv.forEach(function(e){e.classList.add('in')})}); }

  // 数字を数え上げる
  if(ANIM && 'IntersectionObserver' in window){
    var co=new IntersectionObserver(function(es){ es.forEach(function(e){ if(!e.isIntersecting) return; co.unobserve(e.target);
      var el=e.target, n=+el.dataset.count, s=el.querySelector('small'), unit=s?s.outerHTML:'', t0=performance.now();
      (function f(t){ var p=Math.min(1,(t-t0)/1600), v=Math.round(n*(1-Math.pow(1-p,4))); el.innerHTML=v.toLocaleString('ja-JP')+unit; if(p<1) requestAnimationFrame(f); })(t0); }); },{threshold:.6});
    document.querySelectorAll('[data-count]').forEach(function(e){co.observe(e)});
  }

  // 動画は画面に入ったときだけ再生
  document.querySelectorAll('video[data-inview]').forEach(function(v){
    if(!ANIM || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ v.preload='auto'; var p=v.play(); if(p&&p.catch) p.catch(function(){}); } else v.pause(); }); },{threshold:.25}).observe(v);
  });

  // なめらかなスクロール
  if(ANIM && window.Lenis){ var lenis=new Lenis({lerp:.09}); (function raf(t){ lenis.raf(t); requestAnimationFrame(raf); })(performance.now()); }
});

// IR：資料をこのページの中で開く
document.addEventListener('DOMContentLoaded', function(){
  var b=document.querySelector('[data-viewer]'), v=document.getElementById('viewer');
  if(!b||!v) return;
  b.addEventListener('click',function(){ var f=v.querySelector('iframe'); if(!f.src) f.src=f.dataset.src; v.hidden=!v.hidden; v.classList.add('in'); b.textContent=v.hidden?'このページで見る':'プレビューを閉じる'; if(!v.hidden) v.scrollIntoView({behavior:'smooth',block:'start'}); });
});
