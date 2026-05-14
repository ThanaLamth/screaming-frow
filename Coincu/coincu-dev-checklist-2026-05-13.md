## Coincu Dev/WP Checklist - 2026-05-13

Do not treat this as a full audit. This is the shortest execution list for the current incident.

### Batch 1 - Do First

1. Fix `sitemap_index.xml` and child sitemap availability.
   - Current live spot checks returned `520`.
   - Verify:
     - `https://coincu.com/sitemap_index.xml`
     - `post-sitemap.xml`
     - `page-sitemap.xml`
     - `category-sitemap.xml`
     - `post-tag-sitemap.xml`
     - `author-sitemap.xml`

2. Remove bad URL groups from sitemap generation.
   - Must not appear:
     - `/wp-content/`
     - `/wp-admin/`
     - `/coincu-login/`
     - `/convert-crypto-to-fiat/`
     - `/?s=`
     - `/search/`
     - `/t/` if those pages remain `noindex`
     - `/author/` pages that remain `noindex`

3. Fix image/media redirects from `news.coincu.com` to `coincu.com`.
   - Sample pattern:
     - `news.coincu.com/wp-content/uploads/...` -> `coincu.com/wp-content/uploads/...`
   - Destination media must return `200`, not `520` or `403`.

4. Fix malformed media files.
   - Sample:
     - `/wp-content/uploads/2023/10/so5.pngon`
     - `/wp-content/uploads/2023/10/so6on`
   - Decide restore, redirect, or remove from references.

5. Recheck image response behavior.
   - Test at least 20 old media URLs and 20 current media URLs.
   - Confirm Googlebot is not being blocked by CDN/WAF/image rules.

### Batch 2 - Do Next

1. Kill the dead `/convert-crypto-to-fiat/` set.
   - Current sitemap snapshot contains about `10.9k` of these.
   - Nearly all sampled URLs are `404`.
   - Stop generating them.
   - Remove from sitemap and internal surfaces.

2. Clean up search-result URL exposure.
   - Current robots blocks:
     - `/?s=`
     - `/search/`
   - But GSC still shows indexed and blocked search URLs.
   - Reduce internal pathways that keep generating crawlable search URLs.

3. Review duplicate-path article publishing.
   - Sample GSC `crawled-not-indexed` includes:
     - root article path
     - `/news/...`
     - `/blockchain/...`
   - Decide one canonical route pattern per article type.

4. Review low-value discovered URLs.
   - Sample `discovered-not-indexed` looks like templated or low-priority article slugs.
   - Confirm they should exist before letting them enter sitemap.

### Batch 3 - Cleanup After Stabilization

1. Update internal links that still hit redirects.
   - `/news/...` legacy URLs
   - `/analysis/...` legacy URLs
   - old category or path variants

2. Fix `/top-crypto-coins/` route issues.
   - Current mix includes many `200`, many `302`, and some `404`.
   - Review route logic and canonical behavior.

3. Review author archive quality.
   - Most author pages are non-indexable.
   - Keep them out of sitemap unless they are intentionally indexable and complete.

4. Review tag archive policy.
   - `/t/` currently dominates the `noindex` bucket.
   - If tags stay `noindex`, they must stay out of sitemap.

### Verification Checklist

1. Sitemap files return `200`.
2. Sitemap contains only canonical indexable URLs.
3. Sample old media redirects land on `200` images.
4. Sample broken media no longer return `520/403`.
5. `convert-crypto-to-fiat` URLs no longer appear in sitemap.
6. Search URLs stop appearing as indexed despite robots block.
7. Internal links point to final `200` destinations, not `301/302`.
