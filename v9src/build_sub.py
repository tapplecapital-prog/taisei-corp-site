"""あっぷるキャピタルグループ 企業サイト v9 の下層ページを作るスクリプト（Python標準ライブラリのみ）。

使い方:  python build_sub.py
出力先:  ../v9/<ページ>/index.html（トップページ v9/index.html と AIページ v9/ai/ は手書きのため対象外）
共通の見た目と動き: ../v9/assets/sub.css, ../v9/assets/sub.js
本文はこのファイルの PAGES に書く。@@A@@ は画像などの置き場（../../v8/assets/）、@@R@@ はサイトの起点（../）。
"""
import math, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "v9"

NAV = [("#about", "私たちについて"), ("tax/", "税務・会計"), ("real-estate/", "不動産"), ("stores/", "店舗"),
       ("ai/", "AI・業務改善"), ("profile/", "代表"), ("company/", "会社概要"), ("ir/", "IR")]
FNAV = NAV + [("name/", "社名に込めた思い"), ("privacy/", "プライバシーポリシー")]

MONO = ('<svg viewBox="0 0 120 120" role="img" aria-label="あっぷるキャピタルグループの組み文字">'
        '<circle class="s" pathLength="1" cx="60" cy="60" r="56" stroke-width="1.6"/>'
        '<path class="s" pathLength="1" d="M88 38 A 34 34 0 1 0 88 82" stroke-width="7"/>'
        '<path class="s" pathLength="1" d="M44 84 L 62 34 L 80 84" stroke-width="7" stroke-linejoin="miter"/>'
        '<path class="s" pathLength="1" d="M50 66 L 74 66" stroke-width="5"/>'
        '<rect class="dot" x="58.5" y="71" width="7" height="7"/></svg>')

# 保有物件の所在地（市町のおおよその位置）
POINTS = [("札幌", 43.06, 141.35), ("江別", 43.10, 141.54), ("青森", 40.82, 140.74), ("弘前", 40.60, 140.46), ("十和田", 40.61, 141.21),
          ("花巻", 39.39, 141.12), ("仙台", 38.27, 140.87), ("村田", 38.12, 140.72), ("米沢", 37.92, 140.12), ("南相馬", 37.64, 140.96),
          ("郡山", 37.40, 140.38), ("東松山", 36.04, 139.40), ("静岡", 34.98, 138.38), ("岐阜", 35.42, 136.76)]
LABELS = [("札幌・江別", 43.08, 141.45, "end", -5.0, 1.0), ("青森・弘前・十和田", 40.70, 140.80, "end", -6.5, 1.0),
          ("花巻", 39.39, 141.12, "start", 3.2, 1.0), ("仙台・村田・米沢", 38.12, 140.60, "end", -6.8, 1.0),
          ("郡山・南相馬", 37.52, 140.67, "start", 4.2, 3.6), ("東松山", 36.04, 139.40, "start", 3.2, 1.0),
          ("静岡", 34.98, 138.38, "start", 3.2, 1.0), ("岐阜", 35.42, 136.76, "start", 3.2, -1.8)]


def map_svg():
    S, LON0, LAT0, K = 10, 136.4, 43.3, math.cos(math.radians(39))
    def xy(lat, lon):
        return round((lon - LON0) * K * S, 1), round((LAT0 - lat) * S, 1)
    g = []
    for lat in (36, 38, 40, 42):
        y = round((LAT0 - lat) * S, 1)
        g.append(f'<line x1="-24" x2="54" y1="{y}" y2="{y}" stroke="#6D7FEA" stroke-opacity=".22" stroke-width=".18"/>')
        g.append(f'<text x="53" y="{y-0.8}" font-size="1.8" fill="#7F8A99" text-anchor="end" font-family="Inter Tight,sans-serif">{lat}°N</text>')
    for i, (_, lat, lon) in enumerate(POINTS):
        x, y = xy(lat, lon)
        g.append(f'<g class="pt" style="transition-delay:{i*0.08:.2f}s"><circle cx="{x}" cy="{y}" r="2.8" fill="#E4506F" fill-opacity=".14"/>'
                 f'<circle cx="{x}" cy="{y}" r="1.2" fill="url(#pin)"/></g>')
    for name, lat, lon, anchor, dx, dy in LABELS:
        x, y = xy(lat, lon)
        g.append(f'<text x="{round(x+dx,1)}" y="{round(y+dy,1)}" font-size="2.6" fill="#131313" text-anchor="{anchor}" font-family="Noto Sans JP,sans-serif">{name}</text>')
    return ('<svg viewBox="-24 -6 80 96" role="img" aria-label="保有物件の所在地（北海道から中部までの14か所）">'
            '<defs><linearGradient id="pin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A8FE0"/><stop offset=".55" stop-color="#6D7FEA"/><stop offset="1" stop-color="#E4506F"/></linearGradient></defs>'
            + "".join(g) + "</svg>")


PROPS = [("2020.09", "岐阜県岐阜市", "ベイセジュール", 10, "RC造", "t"), ("2020.09", "静岡県静岡市", "T-style広野", 10, "木造", "t"),
         ("2020.12", "青森県青森市", "メゾンドアーク", 10, "木造", "t"), ("2021.10", "北海道江別市", "パレルモ", 10, "木造", "a"),
         ("2021.12", "山形県米沢市", "KS春日", 8, "木造", "p"), ("2022.07", "宮城県柴田郡村田町", "アーバンプレステージ", 10, "木造", "a"),
         ("2022.07", "青森県弘前市", "ウェストヒルハイツ", 12, "木造", "a"), ("2023.10", "北海道札幌市", "エクセレンス東苗穂", 16, "鉄骨造", "a"),
         ("2024.10", "岩手県花巻市", "プリムローズ", 20, "木造", "a"), ("2025.03", "福島県郡山市", "グレースランド", 10, "木造", "a"),
         ("2025.11", "青森県十和田市", "メゾントワダ稲生", 30, "木造", "a"), ("2026.01", "福島県南相馬市", "コーポMOMO", 24, "木造", "a"),
         ("2026.04", "宮城県仙台市", "ズーリング（Ⅰ番館・Ⅱ番館）", 16, "木造", "p"), ("2026.06", "埼玉県東松山市", "ヴェルディ（A棟・B棟）", 22, "木造", "a")]
OWN = {"a": "あっぷるキャピタル", "t": "たいせい", "p": "代表個人"}
prop_rows = "".join(f'<tr><td class="num" data-l="取得">{d}</td><td data-l="所在地">{c}</td><td data-l="物件名">{n}</td><td class="r num" data-l="室数">{u}</td><td data-l="構造">{s}</td><td data-l="保有"><span class="own {o}">{OWN[o]}</span></td></tr>' for d, c, n, u, s, o in PROPS)

KS = ["k08", "k05", "k02", "k13", "k04", "k16", "k09", "k15"]
ks_imgs = "".join(f'<img src="@@A@@img/ks/{k}.webp" width="600" height="750" alt="" loading="lazy">' for k in KS)

PAGES = {
"name": dict(
  title="社名に込めた思い",
  desc="あっぷるキャピタルには、自分たちの事業を着実に育て、その実りを次の世代へつなぐ願いを込めています。社名の原点となったリンゴ農園の記憶と、経営への考え方をご紹介します。",
  nav="name/", en="Origin", h1="社名に込めた思い",
  lead="あっぷるキャピタルには、自分たちの事業を着実に育て、その実りを次の世代へつないでいきたいという願いを込めています。",
  body='''
<article class="name-story" aria-label="あっぷるキャピタルの社名の由来">
<section class="sec"><div class="wrap two">
  <div><p class="lab">Apple</p><h2>リンゴ農園の記憶</h2></div>
  <div class="prose">
    <p>この願いの原点は、青森にある母方の実家のリンゴ農園です。幼い頃から愛着のあったその農園で、小さな実が少しずつ大きくなり、やがて収穫を迎える姿を見て育ちました。子どもの私には、それが奇跡のように思えました。</p>
    <p>時間をかけて育ったものが、実を結ぶ。その驚きと喜びを、いまも覚えています。自分たちの事業にも同じように愛着を持ち、実を結ぶまで育てたい。「あっぷる」という名前は、この思いから生まれました。</p>
  </div>
</div></section>
<section class="sec alt"><div class="wrap two">
  <div><p class="lab">Growth</p><h2>私たちが引き受ける責任</h2></div>
  <div class="prose">
    <p>自分たちの手が届く事業を、一つずつ着実に育てる。それが、私たちの経営の出発点です。住まいや店舗に手を入れ、収益を上げ、得た利益で事業を続けるための備えをつくる。まずは、その営みに責任を持ちたいと考えています。</p>
    <p>思い描いたとおりに進まないときも、工夫を重ね、実を結ぶまで向き合い続ける。遠回りや試行錯誤も引き受けながら、次の世代が育てていける事業として残すことを目指しています。</p>
    <p>自分たちの事業を健全に育て、長く続けていくこと。それが私たちの考える社会的責任です。その積み重ねが、そこで暮らす人や働く人の生活を支え、未来の社会にもつながっていくと考えています。</p>
  </div>
</div></section>
<section class="sec"><div class="wrap two">
  <div><p class="lab">Capital</p><h2>「キャピタル」の役割</h2></div>
  <div class="prose">
    <p>「キャピタル」は、この成長を支える資本を意味します。</p>
    <p>事業から得た利益を、住まいや店舗の手入れ、運営の改善、次の事業へ戻していく。育てた事業が生む資金で、また事業を育てる。その循環をつくり、次の世代へ引き継ぐための会社でありたいと考えています。</p>
    <p>「実らせて、未来へつなぐ。」この言葉には、自分たちの事業に向き合い続け、その実りを次の担い手へ手渡す決意を込めています。</p>
    <p class="name-signature">あっぷるキャピタルグループ<br>代表　三上 浩平</p>
  </div>
</div></section>
</article>
<section class="sec alt"><div class="wrap name-related">
  <a class="btn line" href="@@R@@#about">私たちについて<span class="arr" aria-hidden="true"></span></a>
  <a class="btn line" href="@@R@@company/">会社概要<span class="arr" aria-hidden="true"></span></a>
</div></section>'''),
"tax": dict(
  title="税務・会計｜三上浩平税理士事務所",
  desc="三上浩平税理士事務所（東京税理士会所属）のご案内。不動産オーナーの税務顧問を中心に、個人・法人の税務申告、会計、相続税申告、創業支援を行っています。",
  nav="tax/", en="Tax &amp; Accounting", h1="税務・会計",
  lead="三上浩平税理士事務所は、不動産オーナーの税務顧問を中心に、個人・法人の税務申告、会計、相続税申告、創業支援を行っています。代表税理士は公認会計士でもあり、代表社員を務める2社と個人で、賃貸住宅14棟208室を保有・運営しています。",
  op="このページは三上浩平税理士事務所（東京税理士会所属）のご案内です。税理士業務は当事務所が行います",
  body='''
<section class="sec"><div class="wrap two">
  <div class="rv"><p class="lab">Services</p><h2>業務内容</h2></div>
  <div class="cards">
    <article class="card rv"><span class="k">主な業務</span><h3>不動産オーナーの税務顧問</h3><p>記帳、決算、確定申告（法人の場合は法人税申告）に加え、法人化の検討、物件の購入・売却時の税額の試算、金融機関に提出する決算資料の整理を、年間を通じて行います。</p></article>
    <article class="card rv d1"><span class="k">個人のお客さま</span><h3>確定申告</h3><p>申告書の作成と、節税のご相談をお受けします。資料のやり取りは、できるだけ手間のかからない形にしています。</p></article>
    <article class="card rv"><span class="k">これから事業を始める方</span><h3>創業支援</h3><p>会社の設立、資金計画、事業計画の作成を支援します。</p></article>
    <article class="card rv d1"><span class="k">資産の承継</span><h3>相続税申告</h3><p>相続税の申告、生前の対策、財産の評価を行います。不動産を多く所有されるご家庭のご相談に対応しています。</p></article>
  </div>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div class="rv"><p class="lab">Features</p><h2>当事務所の特長</h2></div>
  <div class="prose rv d1">
    <h3>賃貸経営の実務経験</h3>
    <p>代表税理士は2020年から賃貸住宅を取得し、借入、決算、税務申告を自ら行っています。物件の取得や法人化のご相談にも、自分の事業で確かめてきた数字をもとにお答えします。</p>
    <h3>金融機関での実務経験</h3>
    <p>三井住友銀行でリスク管理と投資銀行業務に携わった経験から、金融機関が決算書で確認する項目を踏まえて資料を作成します。</p>
    <h3>公認会計士による会計の確認</h3>
    <p>税務申告に加え、法人の会計と資金繰りまで一体で確認します。</p>
    <h3>経理の仕組みづくり</h3>
    <p>書類の回収から試算表の作成までを自社で組み直してきた経験をもとに、記帳の手間を減らす方法もご提案します。<a href="@@R@@ai/">経理の流れの例</a></p>
    <p class="note">掲載している物件数・室数は、代表が代表社員を務める合同会社2社と代表個人が保有する物件の合計です（2026年9月時点）。投資の成果や節税の効果を保証するものではありません。</p>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div class="rv"><p class="lab">Office</p><h2>事務所概要</h2></div>
  <dl class="dl rv d1">
    <dt>名称</dt><dd>三上浩平税理士事務所</dd>
    <dt>所長</dt><dd>税理士 三上浩平（公認会計士）</dd>
    <dt>所属</dt><dd>東京税理士会（登録番号 <span class="nw">第144424号</span>）</dd>
    <dt>所在地</dt><dd>東京都港区港南4-2-7-4020</dd>
    <dt>開業</dt><dd>2021年</dd>
    <dt>業務</dt><dd>税務代理、税務書類の作成、税務相談、会計業務</dd>
  </dl>
</div></section>'''),

"real-estate": dict(
  title="不動産",
  desc="合同会社あっぷるキャピタルと合同会社たいせいは、2020年から北海道・東北・関東・中部で一棟の賃貸住宅を取得し、保有・運営しています。保有物件の所在地と一覧、運営方針をご案内します。",
  nav="real-estate/", en="Real Estate", h1="不動産",
  lead="合同会社あっぷるキャピタルと合同会社たいせいは、2020年から北海道・東北・関東・中部で一棟の賃貸住宅を取得し、保有・運営しています。古くからある住まいに手を入れ、長く住み続けられる建物として引き継いでいくことを大切にしています。",
  body='''
<section class="sec"><div class="wrap mapwrap rv">
  <div>
    <p class="lab">Portfolio</p>
    <h2 style="font-family:var(--mincho);font-size:clamp(24px,2.6vw,36px);letter-spacing:.12em;margin:16px 0 20px">保有物件の所在地</h2>
    <p style="color:var(--ink2)">9道県・14市町に、計14棟208室を保有しています。このうち12棟184室を合同会社あっぷるキャピタルと合同会社たいせいが、2棟24室を代表個人が保有しています（2026年9月時点）。</p>
    <div class="stats">
      <div><b data-count="14">14<small>棟</small></b><span>保有する賃貸住宅</span></div>
      <div><b data-count="208">208<small>室</small></b><span>賃貸住宅の室数</span></div>
      <div><b data-count="9">9<small>道県</small></b><span>保有エリア</span></div>
    </div>
    <p class="note">棟数は物件の数で数えています（ズーリングとヴェルディは、2棟でそれぞれ1物件です）。地図上の点は、各物件が所在する市町のおおよその位置です。</p>
  </div>
  @@MAP@@
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sech rv"><p class="lab">List</p><h2>保有物件一覧</h2><p class="intro">取得した時期の順に掲載しています。</p></div>
  <div class="tbl rv d1"><table>
    <thead><tr><th>取得</th><th>所在地</th><th>物件名</th><th class="r">室数</th><th>構造</th><th>保有</th></tr></thead>
    <tbody>@@PROPS@@</tbody>
  </table></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="photos">
    <figure class="rv"><img src="@@A@@img/p-koriyama.webp" alt="福島県郡山市の保有物件の外観" loading="lazy"><figcaption>福島県郡山市</figcaption></figure>
    <figure class="rv d1"><img src="@@A@@img/p-towada.webp" alt="青森県十和田市の保有物件の外観" loading="lazy"><figcaption>青森県十和田市</figcaption></figure>
    <figure class="rv d2"><img src="@@A@@img/p-sapporo.webp" alt="北海道札幌市の保有物件の外観" loading="lazy"><figcaption>北海道札幌市</figcaption></figure>
    <figure class="rv"><img src="@@A@@img/p-yonezawa-snow.webp" alt="雪の日の山形県米沢市の保有物件" loading="lazy"><figcaption>山形県米沢市</figcaption></figure>
    <figure class="rv d1"><img src="@@A@@img/p-sendai.webp" alt="宮城県仙台市の保有物件の外観" loading="lazy"><figcaption>宮城県仙台市</figcaption></figure>
    <figure class="rv d2"><img src="@@A@@img/p-interior.webp" alt="保有物件の室内" loading="lazy"><figcaption>室内</figcaption></figure>
  </div>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div class="rv"><p class="lab">Policy</p><h2>運営の方針</h2></div>
  <div class="prose rv d1">
    <h3>取得の前に、立地を数字で確かめる</h3>
    <p>人口推計、地価の推移、自治体の都市計画を確かめ、賃貸の需要が続く立地かどうかを判断してから取得します。2026年からは、東北6県を1km四方の区画ごとに格付けした地図でも確かめています。<a href="@@R@@#estate">格付けの地図</a></p>
    <h3>保有中は、毎月の数字を追う</h3>
    <p>各地の管理会社と連携し、入居と退去、修繕、家賃の入金を毎月確認しています。集計は、AIを用いた社内の仕組みで行っています。</p>
    <h3>手元に残るお金と、売るときの価格まで見る</h3>
    <p>取得時の表面利回りだけでなく、借入を返した後に手元に残る資金と、売却するときに見込まれる価格を含めて評価しています。</p>
  </div>
</div></section>'''),

"stores": dict(
  title="店舗",
  desc="あっぷるキャピタルグループが運営する店舗のご案内。買取専門店「こやし屋」（大森山王店・野方店・大口通店）と、青森市の24時間営業の無人販売店「365スイーツショップ青森本店」。",
  nav="stores/", en="Retail", h1="店舗",
  lead="合同会社たいせいが、東京と横浜で買取専門店「こやし屋」を3店舗、青森市で24時間営業のスイーツの無人販売店を運営しています。どの店舗も、日々の売上と経費を会計の仕組みで集計し、数字を見ながら運営しています。",
  body='''
<section class="sec dark"><div class="wrap two">
  <div class="rv"><p class="lab">Stores</p><h2 style="font-family:var(--mincho);font-size:clamp(26px,3vw,42px);letter-spacing:.12em;margin-top:16px">買取専門店<br>こやし屋</h2><p class="s" style="color:#A69F92">運営：合同会社たいせい</p></div>
  <div class="rv d1">
    <p>ご家庭で使われなくなった貴金属、ブランド品、時計、カメラ、骨董、お酒などを、店頭で査定してお買い取りしています。引き出しの奥で眠っていた品物に、もう一度値段をつけて、次に使う人へ渡す仕事です。</p>
    <ul class="chips"><li>貴金属</li><li>ブランド品</li><li>時計</li><li>カメラ</li><li>骨董・古銭</li><li>お酒</li></ul>
    <div class="shops">
      <a class="shop" href="https://coyashiya.jp/store/omorisannou/" target="_blank" rel="noopener"><span class="n">01</span><div><h3>大森山王店</h3><p>東京都大田区山王　JR大森駅</p></div><span class="go" aria-hidden="true"></span></a>
      <a class="shop" href="https://coyashiya.jp/store/nogata/" target="_blank" rel="noopener"><span class="n">02</span><div><h3>野方店</h3><p>東京都中野区野方　西武新宿線 野方駅　2025年3月開店</p></div><span class="go" aria-hidden="true"></span></a>
      <a class="shop" href="https://coyashiya.jp/store/kanagawa-ookuchi/" target="_blank" rel="noopener"><span class="n">03</span><div><h3>大口通店</h3><p>神奈川県横浜市神奈川区　大口通商店街</p></div><span class="go" aria-hidden="true"></span></a>
    </div>
    <p class="note" style="border-color:rgba(255,255,255,.2);color:#8C867B">店名から「こやし屋」の各店舗のページへ移動します。写真は各店舗でお買い取りした品物の一部です。</p>
  </div>
</div>
<div class="wrap"><div class="igrid rv">@@KS@@</div></div></section>

<section class="sec pink"><div class="wrap sw2">
  <div class="rv"><div class="phone"><video muted loop playsinline preload="none" data-inview poster="@@A@@media/365-loop.jpg" aria-label="店頭と商品の短い動画（音声なし）"><source src="@@A@@media/365-loop.mp4" type="video/mp4"></video></div></div>
  <div class="rv d1">
    <p class="lab">Sweets</p>
    <h2 style="font-family:var(--mincho);font-size:clamp(26px,3vw,42px);letter-spacing:.1em;margin:16px 0 22px">365スイーツショップ<br>青森本店</h2>
    <p style="color:var(--ink2)">青森市古川で、24時間営業のスイーツの無人販売店を運営しています。ショーケースに並ぶケーキ、アイス、季節のスイーツを、お客さまが自分で選び、店内のセルフレジでお支払いいただく形です。仕事帰りの遅い時間でも、思い立ったときに甘いものを選べる店です。</p>
    <dl class="dl" style="margin-top:26px"><dt>所在地</dt><dd>青森県青森市古川</dd><dt>営業</dt><dd>24時間（無人販売）</dd><dt>開業</dt><dd>2024年1月</dd><dt>運営</dt><dd>合同会社たいせい</dd></dl>
    <div class="pics"><img src="@@A@@img/s365-front.webp" alt="店舗の外観" loading="lazy"><img src="@@A@@img/s365-crepe.webp" alt="いちごを使ったスイーツ" loading="lazy"><img src="@@A@@img/s365-cheese.webp" alt="ショーケースに並ぶケーキ" loading="lazy"></div>
    <a class="ig" href="https://www.instagram.com/365sweets.aomori/" target="_blank" rel="noopener">Instagram　@365sweets.aomori</a>
  </div>
</div></section>'''),

"company": dict(
  title="会社概要",
  desc="あっぷるキャピタルグループの会社概要。合同会社あっぷるキャピタル、合同会社たいせい、三上浩平税理士事務所（東京税理士会所属）の設立、所在地、事業内容と沿革。",
  nav="company/", en="Company", h1="会社概要",
  lead="あっぷるキャピタルグループは、税理士事務所と2つの合同会社からなる企業グループです。",
  body='''
<section class="sec"><div class="wrap">
  <div class="emb rv">@@MONO@@</div>
  <div class="orgtop rv"><div><small>代表</small>三上 浩平</div></div>
  <div class="org">
    <article class="card rv"><span class="k">2020年12月設立</span><h3>合同会社あっぷるキャピタル</h3><p>賃貸不動産の保有・運営</p></article>
    <article class="card rv d1"><span class="k">2020年6月設立</span><h3>合同会社たいせい</h3><p>賃貸不動産の保有・運営、買取専門店「こやし屋」3店舗と「365スイーツショップ青森本店」の運営</p></article>
    <article class="card rv d2"><span class="k">2021年開業</span><h3>三上浩平税理士事務所</h3><p>税務代理、税務書類の作成、税務相談、会計業務</p></article>
  </div>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div class="rv"><h2>合同会社<br>あっぷるキャピタル</h2></div>
  <dl class="dl rv d1"><dt>代表社員</dt><dd>三上浩平</dd><dt>設立</dt><dd>2020年（令和2年）12月21日</dd><dt>所在地</dt><dd>東京都港区港南4-2-7-4020</dd><dt>事業内容</dt><dd>賃貸不動産の保有・運営</dd></dl>
</div></section>
<section class="sec"><div class="wrap two">
  <div class="rv"><h2>合同会社たいせい</h2></div>
  <dl class="dl rv d1"><dt>代表社員</dt><dd>三上浩平</dd><dt>設立</dt><dd>2020年（令和2年）6月19日</dd><dt>所在地</dt><dd>東京都港区港南4-2-7-4020</dd><dt>事業内容</dt><dd>賃貸不動産の保有・運営、買取専門店の運営、無人販売店の運営</dd></dl>
</div></section>
<section class="sec alt"><div class="wrap two">
  <div class="rv"><h2>三上浩平<br>税理士事務所</h2></div>
  <dl class="dl rv d1"><dt>所長</dt><dd>税理士 三上浩平（公認会計士）</dd><dt>所属</dt><dd>東京税理士会（登録番号 <span class="nw">第144424号</span>）</dd><dt>開業</dt><dd>2021年</dd><dt>所在地</dt><dd>東京都港区港南4-2-7-4020</dd><dt>業務内容</dt><dd>税務代理、税務書類の作成、税務相談、会計業務</dd></dl>
</div></section>

<section class="sec"><div class="wrap two">
  <div class="rv"><p class="lab">History</p><h2>沿革</h2></div>
  <div class="tl rv d1"><span class="fill" aria-hidden="true"></span>
    <div><b>2020.06</b>合同会社たいせいを設立</div>
    <div><b>2020.09</b>岐阜県岐阜市、静岡県静岡市で最初の賃貸住宅を取得</div>
    <div><b>2020.12</b>合同会社あっぷるキャピタルを設立</div>
    <div><b>2021</b>三上浩平税理士事務所を開業</div>
    <div><b>2023.10</b>北海道札幌市の賃貸マンションを取得</div>
    <div><b>2024.01</b>青森市で「365スイーツショップ青森本店」を開業</div>
    <div><b>2025.03</b>買取専門店「こやし屋 野方店」を開店</div>
    <div><b>2025.11</b>青森県十和田市の賃貸住宅（30室）を取得</div>
    <div><b>2026.06</b>埼玉県東松山市の賃貸住宅を取得。調査部門「あっぷる総研」を設立</div>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div><p class="lab">Origin</p><h2>社名に込めた思い</h2></div>
  <div class="prose">
    <p>あっぷるキャピタルには、自分たちの事業を着実に育て、その実りを次の世代へつなぐ願いを込めています。その原点は、代表が幼い頃に親しんだ、母方の実家のリンゴ農園にあります。</p>
    <div class="acts"><a class="btn line" href="@@R@@name/">社名の由来を読む<span class="arr" aria-hidden="true"></span></a></div>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <p class="note" style="margin:0">税理士業務は三上浩平税理士事務所が行います。合同会社あっぷるキャピタルおよび合同会社たいせいは、税理士業務を行いません。</p>
</div></section>'''),

"profile": dict(
  title="代表プロフィール 三上浩平",
  desc="あっぷるキャピタルグループ代表、公認会計士・税理士の三上浩平のプロフィール。三井住友銀行、EYストラテジー・アンド・コンサルティングを経て、2020年に合同会社を設立。",
  nav="profile/", en="Profile", h1="三上 浩平",
  lead="あっぷるキャピタルグループ 代表。公認会計士・税理士（東京税理士会所属、登録番号 第144424号）。三上浩平税理士事務所 所長、合同会社あっぷるキャピタル・合同会社たいせい 代表社員。",
  body='''
<section class="sec"><div class="wrap pf">
  <figure class="rv"><img src="@@A@@img/portrait-hq.webp" width="900" height="1284" alt="三上浩平"></figure>
  <div class="prose rv d1">
    <p>三井住友銀行に在職中に公認会計士試験に合格し、EYストラテジー・アンド・コンサルティングを経て、2020年に合同会社たいせいと合同会社あっぷるキャピタルを設立しました。同じ年から地方の一棟の賃貸住宅の取得を始め、現在は北海道から中部までの14棟208室を保有・運営しています。2021年に三上浩平税理士事務所を開業し、買取専門店3店舗と無人販売店1店舗も経営しています。</p>
    <h3>経歴</h3>
    <div class="tl rv"><span class="fill" aria-hidden="true"></span>
      <div><b>2008</b>東北大学経済学部を卒業し、三井住友銀行に入行。連結会計の統括、リスク管理、投資銀行部門に従事</div>
      <div><b>2018</b>公認会計士試験に合格</div>
      <div><b>2019</b>EYストラテジー・アンド・コンサルティングに入社。財務・経営のコンサルティングを担当</div>
      <div><b>2020</b>合同会社たいせい、合同会社あっぷるキャピタルを設立</div>
      <div><b>2021</b>三上浩平税理士事務所を開業</div>
    </div>
    <h3>資格</h3>
    <p>公認会計士／税理士（東京税理士会所属、登録番号 <span class="nw">第144424号</span>）</p>
    <h3>取り組んでいること</h3>
    <ul>
      <li>不動産オーナーの税務、法人化、相続（三上浩平税理士事務所として）</li>
      <li>地方の一棟の賃貸住宅の取得、保有、売却の判断</li>
      <li>経理と店舗運営の仕組みづくり（<a href="@@R@@ai/">AI・業務改善</a>）</li>
    </ul>
    <h3>メディア掲載</h3>
    <ul><li><a href="https://www.rakumachi.jp/news/column/406727" target="_blank" rel="noopener">楽待新聞「大家業のひとびと」#91（2026年9月25日）</a></li></ul>
  </div>
</div></section>'''),

"ir": dict(
  title="IR・決算説明",
  desc="合同会社あっぷるキャピタルの決算説明資料と、不動産事業の中長期成長戦略を掲載しています。",
  nav="ir/", en="Investor Relations", h1="IR・決算説明",
  lead="合同会社あっぷるキャピタルの決算説明資料と、不動産事業の中長期の方針をまとめた資料を掲載しています。金融機関や取引先の皆さまに、当社の現状を数字でご確認いただくための資料です。",
  body='''
<section class="sec"><div class="wrap two">
  <div class="rv"><p class="lab">Results</p><h2>決算説明資料</h2><p class="s">合同会社あっぷるキャピタル（単体）</p></div>
  <div>
    <article class="doc rv d1">
      <div class="dh"><span class="new">最新</span><span class="dt">作成日 2026年7月24日　全25ページ</span></div>
      <h3>第6期（2026年6月期）決算説明資料</h3>
      <p>財務三表と物件ごとの内訳に加え、稼働率、NOI（運営純収益）、財務の健全性、金利上昇の影響、事業等のリスク、来期の見込み、長期のロードマップを掲載しています。</p>
      <div class="kpis">
        <div><b>9<small>棟</small>154<small>室</small></b><span>保有物件（期末）</span></div>
        <div><b>5,561<small>万円</small></b><span>売上高（賃料等）</span></div>
        <div><b>4億8,187<small>万円</small></b><span>総資産（期末）</span></div>
      </div>
      <div class="acts"><a class="btn" href="fy2026/" target="_blank" rel="noopener">資料を開く<span class="arr" aria-hidden="true"></span></a><button class="btn line" type="button" data-viewer>このページで見る</button></div>
    </article>
    <div class="viewer rv" id="viewer" hidden><iframe title="第6期 決算説明資料" loading="lazy" data-src="fy2026/"></iframe></div>
  </div>
</div></section>

<section class="sec alt"><div class="wrap two">
  <div class="rv"><p class="lab">Strategy</p><h2>経営の方針</h2></div>
  <div>
    <article class="doc rv d1">
      <div class="dh"><span class="dt">2026年6月策定</span></div>
      <h3>不動産事業 中長期成長戦略</h3>
      <p>地方の収益不動産の市場が縮小していく中で、当社がどのように成長を図るかの方針をまとめた資料です。</p>
      <div class="acts"><a class="btn line" href="strategy/" target="_blank" rel="noopener">資料を開く<span class="arr" aria-hidden="true"></span></a></div>
    </article>
  </div>
</div></section>

<section class="sec"><div class="wrap two">
  <div class="rv"><p class="lab">Profile</p><h2>対象の会社</h2></div>
  <div class="rv d1">
    <dl class="dl"><dt>商号</dt><dd>合同会社あっぷるキャピタル</dd><dt>代表者</dt><dd>代表社員 三上浩平</dd><dt>設立</dt><dd>2020年（令和2年）12月21日</dd><dt>決算期</dt><dd>6月30日（事業年度は毎年7月1日から翌年6月30日まで）</dd><dt>事業内容</dt><dd>賃貸用不動産の保有・賃貸</dd></dl>
    <p class="note">本ページに掲載する情報は開示した時点のものであり、将来の業績などを保証するものではありません。合同会社たいせいと代表個人が保有する物件は、この資料の対象に含みません。</p>
  </div>
</div></section>'''),

"privacy": dict(
  title="プライバシーポリシー",
  desc="あっぷるキャピタルグループ（合同会社あっぷるキャピタル、合同会社たいせい、三上浩平税理士事務所）の個人情報の取り扱いについて。",
  nav="privacy/", en="Privacy", h1="プライバシーポリシー",
  lead="合同会社あっぷるキャピタル、合同会社たいせい、三上浩平税理士事務所（以下「当グループ」）は、お預かりする個人情報を次のとおり取り扱います。",
  body='''
<section class="sec"><div class="wrap two">
  <div></div>
  <div class="prose rv">
    <h3>1. 取得する情報</h3>
    <p>メールや書面でお知らせいただいたお名前、会社名、メールアドレス、電話番号、ご相談の内容を取得します。</p>
    <h3>2. 利用の目的</h3>
    <p>ご相談への回答、面談の日程調整、ご依頼いただいた業務の遂行のためにだけ利用します。</p>
    <h3>3. 第三者への提供</h3>
    <p>法令に基づく場合を除き、ご本人の同意なく第三者に提供しません。</p>
    <h3>4. 共同利用</h3>
    <p>1.の情報は、2.の目的の範囲で、当グループの3者が共同して利用することがあります。管理の責任者は、合同会社あっぷるキャピタル 代表社員 三上浩平です。ただし、税理士業務でお預かりした情報は共同利用の対象に含めず、三上浩平税理士事務所だけが取り扱います。</p>
    <h3>5. 安全管理</h3>
    <p>取得した情報は、漏えい・紛失を防ぐための措置を講じて管理します。税理士業務でお預かりする情報は、税理士法の守秘義務に従って取り扱います。</p>
    <h3>6. 開示・訂正・削除のご請求</h3>
    <p>ご本人からのご請求があった場合は、本人確認のうえ、遅滞なく対応します。当グループ（東京都港区港南4-2-7-4020、代表 三上浩平）まで書面でお知らせください。</p>
    <h3>7. アクセス解析</h3>
    <p>当サイトでは現在、アクセス解析のツールを使用していません。使用を始める場合は、このページでお知らせします。</p>
    <p class="note">制定：2026年9月</p>
  </div>
</div></section>'''),
}


def shell(key, p):
    R, A = "../", "../../v8/assets/"
    nav = "".join(f'<a href="{R}{h}"{" aria-current=\"page\"" if h == p["nav"] else ""}>{t}</a>' for h, t in NAV)
    mnav = "".join(f'<a href="{R}{h}"{" aria-current=\"page\"" if h == p["nav"] else ""}>{t}</a>' for h, t in NAV)
    fnav = "".join(f'<a href="{R}{h}">{t}</a>' for h, t in FNAV)
    crumb = f'<a href="{R}">トップ</a>　／　{p["h1"] if key != "profile" else "代表プロフィール"}'
    op = f'<span class="op">{p["op"]}</span>' if p.get("op") else ""
    body = (p["body"].replace("@@MAP@@", map_svg()).replace("@@PROPS@@", prop_rows).replace("@@KS@@", ks_imgs.replace("@@A@@", A))
            .replace("@@MONO@@", MONO).replace("@@A@@", A).replace("@@R@@", R))
    title = p["title"] + "｜あっぷるキャピタルグループ"
    return f'''<!DOCTYPE html>
<html lang="ja" data-theme="apple">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title}</title>
<meta name="description" content="{p["desc"]}">
<meta name="theme-color" content="#E4F3FB">
<link rel="icon" href="../../v6/assets/img/logo-color.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@200;300;400;500&family=Noto+Sans+JP:wght@400;500&family=Shippori+Mincho+B1:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/sub.css">
<script>(function(){{var q=location.search.indexOf('noanim')>-1;var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;if(!q&&!rm)document.documentElement.classList.add('anim');}})();</script>
</head>
<body>
<header class="hd">
  <a class="brand" href="{R}"><span class="mark" aria-hidden="true"></span><span><b>あっぷるキャピタルグループ</b><small>APPLE CAPITAL GROUP</small></span></a>
  <nav aria-label="主要メニュー">{nav}</nav>
  <button class="mbtn" type="button" aria-label="メニュー" aria-expanded="false"><i></i></button>
</header>
<nav class="mnav" aria-label="メニュー">{mnav}</nav>
<main>
<section class="ph"><div class="wrap">
  <nav class="crumb" aria-label="現在の位置">{crumb}</nav>
  <p class="en">{p["en"]}</p>
  <h1>{p["h1"]}</h1>
  <p class="lead">{p["lead"]}</p>
  {op}
</div></section>
{body}
</main>
<footer class="ft"><div class="wrap">
  <div class="word" aria-hidden="true">Apple Capital Group</div>
  <div class="cols">
    <nav aria-label="フッター">{fnav}</nav>
    <span class="cp"><span>{MONO}</span>© 2026 Apple Capital Group</span>
  </div>
</div></footer>
<div class="badge">PREVIEW v9</div>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="../assets/sub.js" defer></script>
</body>
</html>
'''


if __name__ == "__main__":
    for key, p in PAGES.items():
        d = OUT / key
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(shell(key, p), encoding="utf-8")
        print("wrote", d / "index.html")
