# TokenTopNews Session Handoff

## Current Local State

There was no existing `Tokentopnews/` workspace inside the repo at the start of this session.

Recovered older TokenTopNews files from `/home/thana2/` and copied them into:

- `Tokentopnews/tokentopnews-category-remap-2026-04-02.csv`
- `Tokentopnews/tokentopnews-category-manual-review-2026-04-02.csv`
- `Tokentopnews/tokentopnews-category-remap-summary-2026-04-02.csv`
- `Tokentopnews/tokentopnews.WordPress.2026-04-02.xml`

## What Those Files Represent

- `tokentopnews-category-remap-summary-2026-04-02.csv`
  Category-path summary with `18` suggested new category paths.
- `tokentopnews-category-remap-2026-04-02.csv`
  Large category remap export with `10326` rows.
- `tokentopnews-category-manual-review-2026-04-02.csv`
  Manual-review subset with `7697` rows.
- `tokentopnews.WordPress.2026-04-02.xml`
  WordPress export from `2026-04-02`.

## Observed Category Direction

The summary file suggests a category model centered on:

- `/cmc`
- `/press-release`
- `insights`
- `insights/institutional`
- `insights/liquidity`
- `insights/on-chain`
- `macro/crypto-macro`
- `macro/fed`
- `macro/global-liquidity`
- `macro/regulation`
- `narratives/altcoin-season`
- `narratives/bitcoin-cycle`
- `narratives/cross-market`
- `narratives/ethereum-ecosystem`
- `trends/ai-crypto`
- `trends/defi`
- `trends/memecoins`
- `weekly-recap/top-stories`

## What Is Missing

There is still no Screaming Frog crawl workspace, GSC intake, backlink export, or prior repo handoff for TokenTopNews.

So the recovered state is enough to continue category remap work, but not enough to continue a full crawl + GSC remediation workflow yet.

## Recommended Next Branch

Choose one of these before going deeper:

1. Continue the April 2 category remap / taxonomy restructuring workflow.
2. Start a fresh full SEO audit workflow with crawl + GSC + backlinks for TokenTopNews.

Until that choice is explicit, assume TokenTopNews currently resumes from the category-remap phase.

## 2026-04-19 Audit Build Update

The full crawl + GSC + backlink intake is now present locally under:

- `Tokentopnews/Crawl/`
- `Tokentopnews/GSC/`
- `Tokentopnews/Backlink/`

Generated outputs:

- `tokentopnews-url-decision-full-2026-04-19.csv`
- `tokentopnews-analysis-summary-2026-04-19.md`
- `tokentopnews-priority-fixes-generated-2026-04-19.csv`
- `tokentopnews-301-priority-batch-2026-04-19.csv`
- `tokentopnews-noindex-priority-batch-2026-04-19.csv`
- `tokentopnews-improve-priority-batch-2026-04-19.csv`
- `tokentopnews-noindex-rules-2026-04-19.md`
- `tokentopnews-internal-link-cut-batch-2026-04-19.md`
- `tokentopnews-implementation-batch-2026-04-19.md`

Scripts added:

- `build_tokentopnews_decision_sheet.py`
- `build_tokentopnews_implementation_batches.py`

Key findings from the generated decision sheet:

- `16648` HTML URLs in the sheet
- `4488` tag archive URLs
- `61` `/coin/*` duplicate URLs canonicalised to `/coin/`
- `34` `/cmc/` archive + pagination URLs staying `noindex`
- `309` `/p/*` media pages
- `27` GSC URLs in `Đã thu thập dữ liệu – hiện chưa được lập chỉ mục`
- `11` non-indexable upload/image URLs in sitemap exports

Recommended next execution order:

1. Fix internal links and legacy archive paths feeding `/crypto-topics/press-release/`, `/news/`, and old `/category/` URLs.
2. Lock stable `noindex` rules for tags, `/cmc/`, `/coin/*`, and media pages.
3. Clean sitemap output to remove upload URLs and other non-indexable entries.
4. Work the `crawled currently not indexed` improve batch.
