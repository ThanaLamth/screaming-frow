# TheCCPress Noindex Rules

## Immediate Template Rules

- `noindex,follow` all `/tag/` archives.
  Evidence: the decision sheet marks `3705` tag archives for noindex and the inlink scan shows about `141516` internal inlink rows feeding tag URLs.
- `noindex,follow` all archive pagination such as `/category/.../page/2+`.
  Evidence: `4119` pagination URLs were found and the deepest ones still receive internal links.
- `noindex,follow` all author pagination such as `/author/.../page/2+`.
  Evidence: `1500` author-pagination URLs and about `16470` internal inlink rows point into that bucket.
- Keep `/p/*.webm` media pages as `200` but enforce `noindex,follow` and exclude them from sitemaps.
  Evidence: GSC `Bị loại trừ bởi thẻ 'noindex'` is dominated by media-page URLs.
- `noindex,follow` `/submit-press-release/`.
  Evidence: the inlink scan shows about `22464` internal inlink rows pointing to this URL.
- `noindex,follow` surviving press-release archive variants:
  - `https://theccpress.com/category/latest-news/press-release/`
  - `https://theccpress.com/category/press-releases/`

## Priority URL Batch

- Priority noindex URLs exported to:
  - `theccpress-noindex-priority-batch-2026-04-16.csv`

## Counts In Priority Batch

- Tag archives: `123`
- Pagination URLs: `51`
- Press-release archive URLs: `4`
- Other URLs: `3`

## Implementation Notes

- Remove all noindex buckets from XML sitemaps.
- Do not return `404` for these buckets unless you are intentionally deleting the URL family.
- The safest default is `200` + `noindex,follow` + sitemap exclusion + reduced internal link prominence.
