# TokenTopNews Next Actions

## Verified Live State on 2026-04-20

- `https://tokentopnews.com/crypto-topics/press-release/` already `301` redirects to `/press-release/`
- `https://tokentopnews.com/cmc/` is live as `200` with `noindex,follow`
- `https://tokentopnews.com/tag/gbtc/` is live as `200` with `noindex,follow`
- `?prefer_reader_view=1&prefer_safari=1` variants already `301` to the clean canonical URL
- `/coin/*` URLs are still live as `200` with `index,follow` and canonical to `/coin/`

## What Still Needs Work

### 1. Add `noindex,follow` to `/coin/*`

This is the clearest remaining technical issue.

- The site has `61` live `/coin/*` URLs
- They are duplicate utility URLs rather than unique search targets
- They currently rely on canonicalization alone, which is weaker than a direct `noindex`
- Batch file:
  - `tokentopnews-coin-duplicate-batch-2026-04-20.csv`

Highest-feed examples:

- `/coin/bitcoin/` with about `4084` internal inlink rows
- `/coin/ethereum/` with about `3262` internal inlink rows
- `/coin/just/` with about `120` internal inlink rows

Safest implementation:

- keep `/coin/*` on `200`
- add `noindex,follow`
- keep the canonical to `/coin/` if the hub remains the surviving utility page
- exclude `/coin/*` from XML sitemaps

### 2. Reduce internal links into `/coin/*`

Noindex alone is not enough if templates keep feeding the bucket.

- Check article templates, widgets, auto-entity links, or glossary modules that create `/coin/*` links
- If the coin hub is needed, prefer linking to `/coin/`
- If the coin detail pages are not useful, remove those links rather than just hiding them from Google

### 3. Keep current noindex rules for tags and `/cmc/`

These appear to be working already, so do not loosen them.

- keep `/tag/*` on `noindex,follow`
- keep `/cmc/` and its pagination on `noindex,follow`
- keep both families out of XML sitemaps

### 4. Optional cleanup: promote malformed 404 URLs to `410`

These are junk URLs with placeholder/path-fragment pollution rather than real content URLs.

- Batch file:
  - `tokentopnews-garbage-410-batch-2026-04-20.csv`
- Count: `51` URLs
- Patterns:
  - `/N/A`
  - `/URL`
  - `url_placeholder`
  - encoded title/source fragments like `%20`

This batch is safe because:

- all URLs already return `404`
- no safe canonical replacement was inferred
- backlink counts are `0` across the batch

### 5. Manual decisions still needed

These should not be auto-mapped yet:

- `https://tokentopnews.com/news/`
- `https://tokentopnews.com/news/metaverse/`
- `https://tokentopnews.com/crypto-topics/page/5/`
- `https://tokentopnews.com/crypto-topics/page/6/`
- `https://tokentopnews.com/crypto-topics/page/27/`

Use either:

- `301` to the closest surviving archive if there is a real replacement
- or `410` if the old archive path is intentionally retired

## Recommended Order

1. Add `noindex,follow` to `/coin/*`
2. Exclude `/coin/*` from sitemaps and reduce template links into that bucket
3. Leave `/tag/*` and `/cmc/` noindex rules in place
4. Apply the `410` batch for malformed junk URLs
5. Resolve the few remaining legacy archive URLs manually

## Quick Verification

```bash
curl -I 'https://tokentopnews.com/coin/just/'
curl -I 'https://tokentopnews.com/cmc/'
curl -I 'https://tokentopnews.com/tag/gbtc/'
curl -I 'https://tokentopnews.com/bitcoin-whale-131-btc-binance-transfer/?prefer_reader_view=1&prefer_safari=1'
```

Expected state:

- `/coin/*` should become `200` with `noindex`
- `/cmc/` stays `200` with `noindex`
- `/tag/*` stays `200` with `noindex`
- reader-view query URLs stay `301`
