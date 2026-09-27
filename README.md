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
