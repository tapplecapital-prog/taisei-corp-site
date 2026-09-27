"""あっぷるキャピタルグループ 企業サイト v6 の生成スクリプト（Python標準ライブラリのみ）。

使い方:
  python build.py --preview            # GitHub Pages のプレビュー（/taisei-corp-site/v6/ に出力・検索よけ付き）
  python build.py --base / --out ../dist --site https://applecapital.co.jp   # 独自ドメイン公開用

ページの原稿は pages/*.html。先頭の <!--meta {...} --> にタイトル等を書き、本文はHTMLで書く。
本文中の @@BASE@@ はサイトの基準パス、@@MAP@@ は保有物件の地図に置き換わる。
"""
import argparse, json, math, re, shutil, pathlib, datetime, html

HERE = pathlib.Path(__file__).resolve().parent
PAGES = HERE / "pages"
ASSETS = HERE / "assets"

NAV = [
    ("about/", "私たちについて", "About"),
    ("tax/", "税務・会計", "Tax & Accounting"),
    ("real-estate/", "不動産", "Real Estate"),
    ("ai/", "AI・業務改善", "AI"),
    ("stores/", "店舗", "Stores"),
    ("numbers/", "数字で見る", "Numbers"),
    ("insights/", "研究・発信", "Insights"),
]
X_URL = "https://x.com/applecapital_ri"
RAKUMACHI_URL = "https://www.rakumachi.jp/news/column/406727"

# 保有物件の所在地（地図の点）。緯度経度は市役所・町役場付近の概略値
POINTS = [
    ("札幌", 43.06, 141.35), ("江別", 43.10, 141.54),
    ("青森", 40.82, 140.74), ("弘前", 40.60, 140.46), ("十和田", 40.61, 141.21),
    ("花巻", 39.39, 141.12), ("仙台", 38.27, 140.87), ("村田", 38.12, 140.72),
    ("米沢", 37.92, 140.12), ("南相馬", 37.64, 140.96), ("郡山", 37.40, 140.38),
    ("東松山", 36.04, 139.40), ("静岡", 34.98, 138.38), ("岐阜", 35.42, 136.76),
]
LABELS = [  # 近い点はまとめて1つのラベルにする
    ("札幌・江別", 43.08, 141.45, "end", -5.0, 1.0),
    ("青森・弘前・十和田", 40.70, 140.80, "end", -6.5, 1.0),
    ("花巻", 39.39, 141.12, "start", 3.2, 1.0),
    ("仙台・村田・米沢", 38.12, 140.60, "end", -6.8, 1.0),
    ("郡山・南相馬", 37.52, 140.67, "start", 4.2, 3.6),
    ("東松山", 36.04, 139.40, "start", 3.2, 1.0),
    ("静岡", 34.98, 138.38, "start", 3.2, 1.0),
    ("岐阜", 35.42, 136.76, "start", 3.2, -1.8),
]


def map_svg() -> str:
    S, LON0, LAT0, K = 10, 136.4, 43.3, math.cos(math.radians(39))
    def xy(lat, lon):
        return round((lon - LON0) * K * S, 1), round((LAT0 - lat) * S, 1)
    g = []
    for lat in (36, 38, 40, 42):
        y = round((LAT0 - lat) * S, 1)
        g.append(f'<line x1="-24" x2="54" y1="{y}" y2="{y}" stroke="#A8874A" stroke-opacity=".25" stroke-width=".18"/>')
        g.append(f'<text x="53" y="{y-0.8}" font-size="1.8" fill="#7A5E2A" fill-opacity=".7" text-anchor="end" font-family="Inter,sans-serif">{lat}°N</text>')
    for _, lat, lon in POINTS:
        x, y = xy(lat, lon)
        g.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#A8874A" fill-opacity=".14"/>')
        g.append(f'<circle cx="{x}" cy="{y}" r="1.15" fill="url(#foil)"/>')
    for name, lat, lon, anchor, dx, dy in LABELS:
        x, y = xy(lat, lon)
        g.append(f'<text x="{round(x+dx,1)}" y="{round(y+dy,1)}" font-size="2.6" fill="#1C1B19" text-anchor="{anchor}" font-family="Noto Sans JP,sans-serif">{name}</text>')
    return ('<svg viewBox="-24 -6 80 96" role="img" aria-label="保有物件の所在地（北海道から中部まで14か所）">'
            '<defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7E5E28"/>'
            '<stop offset=".45" stop-color="#D9BE7E"/><stop offset="1" stop-color="#A8874A"/></linearGradient></defs>'
            + "".join(g) + "</svg>")


def parse(p: pathlib.Path):
    src = p.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", src, re.S)
    if not m:
        raise SystemExit(f"meta がありません: {p.name}")
    return json.loads(m.group(1)), src[m.end():]


def jsonld(kind: str, site: str) -> str:
    org = {
        "@type": "Organization", "@id": site + "#org", "name": "あっぷるキャピタルグループ",
        "alternateName": "APPLE CAPITAL GROUP", "url": site,
        "logo": site + "assets/img/logo-color.png",
        "founder": {"@id": site + "about/profile/#person"},
        "subOrganization": [
            {"@type": "Organization", "name": "合同会社あっぷるキャピタル", "foundingDate": "2020-12-21"},
            {"@type": "Organization", "name": "合同会社たいせい", "foundingDate": "2020-06-19"},
        ],
        "sameAs": [X_URL],
    }
    person = {
        "@type": "Person", "@id": site + "about/profile/#person", "name": "三上浩平",
        "alternateName": "Kohei Mikami", "jobTitle": "公認会計士・税理士",
        "worksFor": {"@id": site + "#org"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "東北大学"},
        "sameAs": [X_URL], "url": site + "about/profile/",
    }
    tax = {
        "@type": "AccountingService", "name": "三上浩平税理士事務所", "url": site + "tax/",
        "founder": {"@id": site + "about/profile/#person"},
        "address": {"@type": "PostalAddress", "addressRegion": "東京都", "addressLocality": "港区", "streetAddress": "港南4-2-7", "addressCountry": "JP"},
        "areaServed": "JP",
    }
    graph = {"index": [org, person], "profile": [person, org], "tax": [tax, person]}.get(kind)
    if not graph:
        return ""
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>"


def layout(meta: dict, body: str, base: str, site: str, preview: bool) -> str:
    path = meta.get("path", "")
    title = meta["title"] + ("" if meta.get("home") else "｜あっぷるキャピタルグループ")
    desc = meta["description"]
    canonical = site + path
    nav = "".join(
        f'<a href="{base}{href}"{" aria-current=\"page\"" if path.startswith(href) else ""}>{ja}</a>'
        for href, ja, _ in NAV)
    mnav = "".join(f'<a href="{base}{href}">{ja}<small>{en}</small></a>' for href, ja, en in NAV)
    robots = '<meta name="robots" content="noindex,nofollow">' if preview else ""
    note = ('<div class="preview-note">公開前の確認用ページです（検索エンジンには表示されません）。'
            '内容・数字は最終確認前のものを含みます。</div>') if preview else ""
    chrome = not meta.get("bare")
    header = f"""
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{base}"><span class="mark" aria-hidden="true"></span><span><b>あっぷるキャピタルグループ</b><span>APPLE CAPITAL GROUP</span></span></a>
    <nav class="gnav" aria-label="主要メニュー">{nav}<a class="btn btn-primary" href="{base}contact/">ご相談窓口</a></nav>
    <details class="menu"><summary aria-label="メニューを開く"><i aria-hidden="true"></i>MENU</summary>
      <nav aria-label="主要メニュー（スマートフォン）"><a href="{base}">トップ<small>Home</small></a>{mnav}<a class="btn btn-primary" href="{base}contact/">ご相談窓口</a></nav>
    </details>
  </div>
</header>""" if chrome else ""
    footer = f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="top">
      <div>
        <a class="brand" href="{base}"><span class="mark" aria-hidden="true"></span><span><b>あっぷるキャピタルグループ</b><span>APPLE CAPITAL GROUP</span></span></a>
        <p class="entities">合同会社あっぷるキャピタル／合同会社たいせい<br>三上浩平税理士事務所（税理士業務は同事務所が行います）<br>東京都港区港南4-2-7</p>
      </div>
      <div><h4>Business</h4><ul>
        <li><a href="{base}tax/">税務・会計</a></li><li><a href="{base}real-estate/">不動産</a></li>
        <li><a href="{base}ai/">AI・業務改善</a></li><li><a href="{base}stores/">店舗</a></li></ul></div>
      <div><h4>Company</h4><ul>
        <li><a href="{base}about/">私たちについて</a></li><li><a href="{base}about/profile/">代表プロフィール</a></li>
        <li><a href="{base}numbers/">数字で見るグループ</a></li><li><a href="{base}insights/">研究・発信</a></li>
        <li><a href="{base}company/">会社概要</a></li><li><a href="{base}privacy/">プライバシーポリシー</a></li>
        <li><a href="{base}contact/">ご相談窓口</a></li><li><a href="{X_URL}" rel="noopener">X（三上浩平）</a></li></ul></div>
    </div>
    <div class="bottom"><span>© {datetime.date.today().year} APPLE CAPITAL GROUP</span><span>掲載の数字は2026年9月時点</span></div>
  </div>
</footer>""" if chrome else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{"website" if meta.get("home") else "article"}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}assets/img/logo-color.png">
<meta property="og:locale" content="ja_JP">
<meta name="theme-color" content="#0B1B3B">
<link rel="icon" href="{base}assets/img/logo-color.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=Inter:wght@500;600&family=Noto+Sans+JP:wght@400;500;700&family=Shippori+Mincho+B1:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/css/site.css">
{jsonld(meta.get("jsonld", ""), site)}
</head>
<body>
<a class="skip" href="#main">本文へ移動</a>
{note}{header}
<main id="main">
{body}
</main>
{footer}
<script src="{base}assets/js/site.js" defer></script>
</body>
</html>
"""


VCARD = """BEGIN:VCARD
VERSION:3.0
N;CHARSET=UTF-8:三上;浩平;;;
FN;CHARSET=UTF-8:三上 浩平
X-PHONETIC-FIRST-NAME;CHARSET=UTF-8:こうへい
X-PHONETIC-LAST-NAME;CHARSET=UTF-8:みかみ
ORG;CHARSET=UTF-8:あっぷるキャピタルグループ
TITLE;CHARSET=UTF-8:代表／公認会計士・税理士
EMAIL;TYPE=INTERNET,WORK:t.applecapital@gmail.com
URL:{url}
NOTE;CHARSET=UTF-8:三上浩平税理士事務所 所長／合同会社あっぷるキャピタル・合同会社たいせい 代表社員
END:VCARD
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--base", default="/taisei-corp-site/v6/")
    ap.add_argument("--out", default=str(HERE.parent / "v6"))
    ap.add_argument("--site", default="https://tapplecapital-prog.github.io/taisei-corp-site/v6/")
    a = ap.parse_args()
    site = a.site if a.site.endswith("/") else a.site + "/"
    base = a.base if a.base.endswith("/") else a.base + "/"
    out = pathlib.Path(a.out).resolve()
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ASSETS, out / "assets")
    svg = map_svg()
    urls = []
    for p in sorted(PAGES.glob("*.html")):
        meta, body = parse(p)
        body = body.replace("@@BASE@@", base).replace("@@MAP@@", svg).replace("@@X@@", X_URL).replace("@@RAKUMACHI@@", RAKUMACHI_URL)
        dest = out / meta.get("path", "") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(layout(meta, body, base, site, a.preview), encoding="utf-8")
        urls.append(site + meta.get("path", ""))
    (out / "hello" / "mikami.vcf").write_text(VCARD.format(url=site), encoding="utf-8", newline="\r\n")
    today = datetime.date.today().isoformat()
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls if "/hello/" not in u)
        + "</urlset>\n", encoding="utf-8")
    if not a.preview:
        (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /hello/\nSitemap: {site}sitemap.xml\n", encoding="utf-8")
    print(f"built {len(urls)} pages -> {out}")


if __name__ == "__main__":
    main()
