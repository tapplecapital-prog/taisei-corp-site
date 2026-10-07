# Taisei LLC / Apple Capital LLC Website

This is the official website for **Taisei LLC** and **Apple Capital LLC**, integrated into a single web presence.

## Overview
The website showcases the three main business pillars:
1.  **Reuse Business**: "Koyashiya" purchase specialty stores.
2.  **Real Estate Leasing**: 8 apartment properties across Japan.
3.  **Retail Business**: "365 Sweets Shop" in Aomori.

## Companies
-   **Taisei LLC (合同会社たいせい)**
-   **Apple Capital LLC (合同会社あっぷるキャピタル)**

## Setup
OPEN `index.html` in your web browser.

## Directory Structure
-   `index.html`: Main website file.
-   `images/`: Contains assets like the representative's profile photo.

## v6（2026-09 刷新・プレビュー）
- 原稿と生成スクリプト: `site/`（`site/pages/*.html` が各ページの原稿、`site/build.py` が生成。Python標準ライブラリのみ）
- プレビュー: `python site/build.py --preview` → `v6/` に出力 → https://tapplecapital-prog.github.io/taisei-corp-site/v6/ （検索よけ付き）
- 独自ドメイン公開時: `python site/build.py --base / --out dist --site https://<ドメイン>/`
- 現行のトップ（`index.html`）は差し替えるまでそのまま。
- 企画・経緯: 統合ハブ PJ00-15（ブランディング・マーケティング戦略の見直し）

## v9（既存の企業サイト確認版）
- 確認URL: https://tapplecapital-prog.github.io/taisei-corp-site/v9/
- トップページとAIページは `v9/index.html` と `v9/ai/index.html` が原本。
- 下層ページの本文と共通フッターは `v9src/build_sub.py` が原本。共通の見た目と動きは `v9/assets/sub.css` と `v9/assets/sub.js`。
- 社名の由来: `v9/name/index.html`。トップの「私たちについて」、会社概要、各ページのフッターから参照する。
- 下層ページ1件だけを変更する場合は、`build_sub.py` の `PAGES` を編集し、`shell(key, PAGES[key])` で対象ページを生成する。手書きページや他のページの変更を上書きしない。
- 配信は GitHub Pages（`main` ブランチの `/`、独自ドメインなし）。今回の配信先・ブランチは2026-10-08にGitHub Pages APIで確認した。
- 反映手順: 対象の原本と生成HTMLを変更 → 文体検査・ローカル表示・リンクの確認 → 対象ファイルだけをコミット → `git push origin main` → Pagesの最新ビルドがそのコミットで成功したことを確認 → 上記URLで実ページを確認。
- 戻す場合は対象変更のコミットを `git revert <commit>` して同じ配信手順を使う。保存データや外部サービスの変更はない。
- `index.html`（旧トップ）とv6/v8は、このv9更新では差し替えない。独自ドメイン移行は別の作業として扱う。
