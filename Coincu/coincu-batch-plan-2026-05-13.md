## Coincu Batch Plan - 2026-05-13

This plan assumes:
- no direct WordPress edits from this workflow
- execution will be handled by the site owner or dev/editor team

### Batch 1 - Sitemap and Image/Media Emergency

Why this is first:
- `sitemaps_all.csv` contains large volumes of bad or low-value URLs
- image/media redirects appear to be failing at destination
- live sitemap endpoints returned `520` during spot checks

#### What to remove from sitemap feeds

Do not allow these URL groups in XML sitemaps:
- `/wp-content/`
- `/wp-admin/`
- `/coincu-login/`
- `/convert-crypto-to-fiat/`
- `/t/` tag archives if they remain `noindex`
- `/author/` profiles that remain `noindex`
- search-result or utility URLs

#### Why

Current sitemap snapshot includes:
- `/wp-content/`: 53,412
- `/t/`: 24,058
- `/convert-crypto-to-fiat/`: 10,952
- `/wp-admin/`: 357
- `/coincu-login/`: 226

This is enough on its own to waste crawl budget and pollute GSC indexing coverage.

#### Image/media checks

Investigate immediately:
- old `news.coincu.com/wp-content/...` media URLs redirecting to `coincu.com/wp-content/...`
- destination media returning `520` or `403`
- malformed media paths such as broken filenames or invalid extensions

Representative files:
- [batch1_sitemap_wp_content_sample.csv](/home/thana2/coincu/batch1_sitemap_wp_content_sample.csv:1)
- [batch1_sitemap_convert_sample.csv](/home/thana2/coincu/batch1_sitemap_convert_sample.csv:1)
- [batch1_sitemap_tag_sample.csv](/home/thana2/coincu/batch1_sitemap_tag_sample.csv:1)
- [batch1_sitemap_wpadmin_sample.csv](/home/thana2/coincu/batch1_sitemap_wpadmin_sample.csv:1)
- [batch1_sitemap_login_sample.csv](/home/thana2/coincu/batch1_sitemap_login_sample.csv:1)

#### Validation after fix

- `sitemap_index.xml` must load `200`
- child sitemaps must load `200`
- sample image URLs must load `200`
- `news.coincu.com` media redirects must land on working `200` files

### Batch 2 - Dead URL Sets and Search URL Deindexing

Why this is second:
- GSC `404` and robots-blocked search URLs are large, noisy, and easy to define by pattern

#### Priority pattern A: `/convert-crypto-to-fiat/`

Current state:
- 10,952 URLs in sitemap snapshot
- 10,950 are `404`

Action:
- remove the entire dead set from sitemaps
- if this feature is discontinued, return clean `410` or keep `404` but make sure there are no sitemap/internal references left
- if the feature should exist, restore only canonical live URLs and do not regenerate dead combinations

#### Priority pattern B: search URLs

Current GSC pattern:
- blocked by robots
- some are still indexed despite robots
- sample URLs use `/?s=` and `/search/...`

Action:
- stop exposing random search-result URLs in crawlable internal surfaces
- if you want them gone from Google, do not rely only on robots blocking
- ensure search pages are not linked in ways that keep generating crawl demand

Representative files:
- [batch2_gsc_404_sample.csv](/home/thana2/coincu/batch2_gsc_404_sample.csv:1)
- [batch2_gsc_crawled_not_indexed_sample.csv](/home/thana2/coincu/batch2_gsc_crawled_not_indexed_sample.csv:1)
- [batch2_gsc_discovered_not_indexed_sample.csv](/home/thana2/coincu/batch2_gsc_discovered_not_indexed_sample.csv:1)
- [batch2_gsc_blocked_robots_sample.csv](/home/thana2/coincu/batch2_gsc_blocked_robots_sample.csv:1)
- [batch2_gsc_indexed_blocked_robots_sample.csv](/home/thana2/coincu/batch2_gsc_indexed_blocked_robots_sample.csv:1)

#### Interpretation note

`Crawled - currently not indexed` and `Discovered - currently not indexed` samples show many duplicate-path or low-priority article variants such as:
- `/news/...`
- `/blockchain/...`
- bare-root article slugs

Those should be reviewed for duplication and sitemap eligibility.

### Batch 3 - Redirect and Duplicate Cleanup

Why this is third:
- a large amount of redirect noise remains, but it is less urgent than sitemap and image failures

#### High-priority redirect groups

- `/news/...` variants: mostly `301`
- `/analysis/...` variants: mostly `301`
- `/top-crypto-coins/...`: heavy mix of `200`, `302`, and some `404`

#### Observed problem types

- legacy paths still crawled instead of only canonical destinations
- redirect-error samples concentrated in `/top-crypto-coins/...-price-update`
- content blocks using links that resolve through extra redirects

Representative files:
- [batch3_gsc_redirect_sample.csv](/home/thana2/coincu/batch3_gsc_redirect_sample.csv:1)
- [batch3_gsc_redirect_error_sample.csv](/home/thana2/coincu/batch3_gsc_redirect_error_sample.csv:1)
- [batch3_gsc_5xx_sample.csv](/home/thana2/coincu/batch3_gsc_5xx_sample.csv:1)

#### What to do

- update internal links to point directly at final `200` destinations
- review route logic for `/top-crypto-coins/` URLs returning `302`
- review article path duplication across root, `/news/`, `/analysis/`, `/blockchain/`, and category variants
- verify that canonical tags match the intended kept version

### Execution order

1. Fix sitemap generation and live sitemap availability
2. Fix media redirect failures and image `520/403`
3. Remove dead `/convert-crypto-to-fiat/` URLs from sitemap and URL generation
4. Clean up search-result URLs and reduce robots-only deindex attempts
5. Reduce redirect chains and duplicate path variants

### Success checks

- GSC `5xx`, `404`, and `redirect` begin trending down
- image index stabilizes and image URLs return `200`
- sitemap contains only canonical, indexable URLs
- `Crawled - currently not indexed` begins shrinking on newly recrawled batches
