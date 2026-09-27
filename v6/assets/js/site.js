// あっぷるキャピタルグループ 企業サイト v6 — 必要最小限のスクリプト。
// スクリプトが動かなくても全ページの内容は読める作りにしている。
(function () {
  // スマートフォンのメニュー：リンクを押したら閉じる
  document.querySelectorAll('.menu nav a').forEach(function (a) {
    a.addEventListener('click', function () { var d = a.closest('details'); if (d) d.removeAttribute('open'); });
  });

  // ご相談窓口：目的に応じて宛先を分け、メールソフトを開く。
  // 税務・会計のご相談は三上浩平税理士事務所の窓口へ、それ以外はグループの窓口へ届く。
  // （独自ドメイン取得後は、サーバー側の受付フォームに差し替える）
  var form = document.getElementById('contact-form');
  if (!form) return;
  var user = { tax: 'kohei.mikami.zeirishi', other: 't.applecapital' };
  var host = 'gmail.com';
  var labels = { tax: '税務・会計のご相談', ai: 'AI・業務改善のご相談', property: '物件情報のご提供', media: '取材・講演のご依頼', other: 'その他のお問い合わせ' };

  var q = new URLSearchParams(location.search).get('type');
  if (q && labels[q]) { var r = form.querySelector('input[name=purpose][value=' + q + ']'); if (r) r.checked = true; }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = new FormData(form);
    var purpose = f.get('purpose') || 'other';
    var to = (purpose === 'tax' ? user.tax : user.other) + '@' + host;
    var subject = '【' + labels[purpose] + '】' + (f.get('name') || '') + '様より';
    var lines = [
      'ご相談の種類：' + labels[purpose],
      'お名前：' + (f.get('name') || ''),
      '会社名：' + (f.get('company') || ''),
      'メール：' + (f.get('email') || ''),
      '電話：' + (f.get('tel') || ''),
      '', '内容：', (f.get('body') || '')
    ];
    location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    var done = document.getElementById('contact-done');
    if (done) { done.hidden = false; done.querySelector('.addr').textContent = to; }
  });
})();
