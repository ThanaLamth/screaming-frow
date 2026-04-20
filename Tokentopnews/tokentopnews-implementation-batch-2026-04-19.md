# TokenTopNews Implementation Batch

## Files

- `tokentopnews-301-priority-batch-2026-04-19.csv`
- `tokentopnews-noindex-priority-batch-2026-04-19.csv`
- `tokentopnews-improve-priority-batch-2026-04-19.csv`
- `tokentopnews-noindex-rules-2026-04-19.md`
- `tokentopnews-internal-link-cut-batch-2026-04-19.md`

## Redirect Batch Counts

- Total priority 301 URLs: `305`
- Legacy archives: `9`
- Broken posts/pages: `280`
- Parameter variants: `9`

## Noindex Batch Counts

- Total priority noindex URLs: `4809`
- Tags: `4488`
- Coin duplicates: `61`
- CMC archive + pagination: `34`
- Media pages: `1`

## Improve Batch Counts

- Total priority improve URLs: `809`
- Crawled currently not indexed URLs in top batch: `20`
- Section/archive URLs needing quality work: `7`

## Execution Order

1. Fix legacy archive redirects and internal links to retired paths.
2. Lock stable noindex rules for tags, media pages, `/cmc/`, and `/coin/*`.
3. Remove non-indexable URLs from XML sitemaps.
4. Improve the smaller GSC crawled-not-indexed post batch.
