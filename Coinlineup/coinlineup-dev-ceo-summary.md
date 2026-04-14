# Coinlineup SEO Summary

Audit date: 2026-04-14  
Evidence source: Screaming Frog exports in this folder

Coinlineup is carrying a structural crawl/indexation problem, not just normal metadata debt. The crawl shows `12,136` HTML URLs, of which `10,472` are indexable and `1,664` are non-indexable. The highest-risk issue is that utility URLs such as `/login/`, `/my-account/`, `/bookmarks/`, and `/my-follows/` are live as `200 + Indexable` and are also included in XML sitemap coverage.

The second major blocker is broken internal URL architecture. The exports show `559` internal `404` URLs, `537` internal `301` URLs, and `132` internal `5xx` URLs. A particularly bad pattern is multiple `/currencies/` URLs redirecting to `/cmc-currency-details-advanced-design/`, while that destination itself returns `404` and also appears in sitemap issue coverage.

Taxonomy quality is also weak. `/uncategorized/` is indexable, present in sitemap coverage, and has `1,292` unique internal inlinks. In parallel, there are `32` indexable `/sponsored-articles/` archive URLs, which expands low-value archive inventory and risks mixing commercial and editorial intent.

Metadata problems are real but should be treated as second wave cleanup. The crawl found `1,426` missing meta descriptions, `2,239` titles over 60 characters, `65` duplicate titles, and `44` duplicate meta descriptions. Most of this debt appears template-driven, especially on tag archives and duplicate post variants with `-2` suffixes.

Recommended fix order:

1. Remove utility URLs and low-value archives from indexation and XML sitemaps.
2. Repair broken internal redirects and the `/currencies/` routing/template issue.
3. Clean internal broken links and unstable media/CDN responses.
4. Fix taxonomy and duplicate-content patterns.
5. Do metadata cleanup after the crawl/index architecture is stable.
