# TokenTopNews Noindex Rules

## Immediate Template Rules

- Keep all `/tag/` archives on `noindex,follow`.
  Evidence: `4488` priority tag URLs in the noindex batch and the site already emits tag `noindex`.
- Keep `/p/*.webm` media pages on `noindex,follow`.
  Evidence: GSC `Bị loại trừ bởi thẻ 'noindex'` is dominated by `/p/` media URLs.
- Keep `/cmc/` and its pagination on `noindex,follow` unless you intentionally want that archive indexed.
  Evidence: `/cmc/` is live, noindex, and heavily internally linked.
- Add a noindex rule for `/coin/*` duplicate URLs if those pages must stay live.
  Evidence: `/coin/*` URLs are canonicalised to `/coin/` and do not present unique indexable content.

## Priority URL Batch

- `tokentopnews-noindex-priority-batch-2026-04-19.csv`

## Implementation Notes

- Remove all noindex buckets from XML sitemaps.
- If a bucket is intentionally noindex, reduce template-level links that keep re-feeding it.
- Use `200 + noindex,follow` for stable utility/archive buckets; do not convert them to 404 unless you are intentionally retiring them.
