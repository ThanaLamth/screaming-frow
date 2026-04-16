# TheCCPress Implementation Batch

## Files

- `theccpress-301-priority-batch-2026-04-16.csv`
- `theccpress-noindex-priority-batch-2026-04-16.csv`
- `theccpress-noindex-rules-2026-04-16.md`
- `theccpress-internal-link-cut-batch-2026-04-16.md`

## Redirect Batch Counts

- Total priority 301 URLs: `207`
- AMP URLs: `168`
- Parameter URLs: `14`
- Other URLs needing manual mapping or category cleanup: `25`

## Noindex Batch Counts

- Total priority noindex URLs: `181`
- Tag archives: `123`
- Pagination URLs: `51`
- Press-release archive URLs: `4`

## Execution Order

1. Implement AMP + parameter redirects from the 301 batch.
2. Add template-level noindex rules for tags, archive pagination, author pagination, and media pages.
3. Remove noindex/non-indexable URLs from XML sitemaps.
4. Cut the internal-link sources listed in the internal-link batch.
5. Manually map the remaining `404` URLs in the 301 batch that still have a blank replacement target.
