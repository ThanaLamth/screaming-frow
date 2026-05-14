## Coincu Audit Handoff - 2026-05-13

Data sources reviewed:
- `/home/thana2/coincu/*.csv` from Screaming Frog
- `/home/thana2/gsc coincu/...` GSC coverage, drilldowns, performance

Key findings:
- GSC indexed pages dropped from roughly 191k in mid-February 2026 to roughly 69k by mid-March 2026, while non-indexed pages rose to ~338k.
- Main GSC issue counts:
  - `Crawled - currently not indexed`: 313,386
  - `Discovered - currently not indexed`: 33,438
  - `404`: 8,531
  - `Redirect`: 8,069
  - `Blocked by robots.txt`: 4,033
  - `5xx`: 219
- Screaming Frog `internal_all.csv` shows:
  - top path groups: `/wp-content/` 110,228, `/t/` 24,058, `/convert-crypto-to-fiat/` 10,954, `/top-crypto-coins/` 2,214
  - status counts: `200` 105,134, `301` 52,764, `403` 21,167, `404` 13,954
- `sitemaps_all.csv` is highly problematic:
  - includes `/wp-content/` 53,412
  - includes `/t/` 24,058
  - includes `/convert-crypto-to-fiat/` 10,954
  - includes `/wp-admin/` 357
  - includes `/coincu-login/` 226
  - sitemap status mix: `301` 52,764, `200` 48,208, `403` 21,167, `404` 13,954
- `noindex` is mostly intentional `/t/` tag URLs:
  - `Meta noindex total`: 24,332
  - `/t/`: 24,040
- GSC drilldown samples:
  - `404`: many `/convert-crypto-to-fiat/...` URLs, plus translated `/de/` and `/ar/` variants
  - `Crawled - currently not indexed`: article, news, and blockchain duplicate-path variants
  - `Discovered - currently not indexed`: many thin or templated article slugs
  - `Indexed though blocked by robots`: search result URLs
  - `Redirect error`: several `/top-crypto-coins/...-price-update`
  - `5xx`: mixed articles, `/t/.../amp/`, and `/convert-crypto-to-fiat/...`
- Media/image issue is credible:
  - many `news.coincu.com/wp-content/...` URLs 301 to `coincu.com/wp-content/...`
  - sample destination images returned `520` live during checking
  - sample malformed media paths also returned `520`

Live checks performed:
- `https://coincu.com/robots.txt` allows standard site crawl but blocks `/?s=` and `/search/`
- `https://coincu.com/sitemap_index.xml` and direct sitemap endpoints returned `520` during this session, so live sitemap availability should be rechecked from another network/browser

Priority order recommended:
1. Stop feeding bad URLs in sitemap
2. Triage image/media migration and old `news.coincu.com` media redirects
3. Remove or de-index dead `/convert-crypto-to-fiat/` URL set
4. Clean search-result URLs that are indexed despite robots blocks
5. Reduce duplicate path variants across `/news/`, `/analysis/`, `/blockchain/`

Constraint:
- Do not edit WordPress directly from this workflow without explicit user action. Provide batches/instructions only.
