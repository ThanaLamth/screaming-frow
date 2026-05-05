# Tokentopnews Next Actions

## Scope

Follow-up local-only pass on `2026-05-05` after the `2026-05-03` refresh.

No WordPress edits or plugin changes were made.

## Live Recheck Summary

The 2 previously flagged wrong-target category redirects are still unresolved:

- `https://tokentopnews.com/category/altcoins/`
  - still `301` to `https://tokentopnews.com/altcoins-gain-during-metals-rally/`
- `https://tokentopnews.com/category/bitcoin/`
  - still `301` to `https://tokentopnews.com/bitcoin-1-292-billion-liquidation/`

## New Finding

The issue is broader than those 2 category URLs.

Multiple top-level section-looking URLs also currently redirect to single articles, for example:

- `/altcoins/`
- `/bitcoin/`
- `/defi/`
- `/cardano/`
- `/dogecoin/`
- `/ethereum/`
- `/ripple/`
- `/xrp/`
- `/solana/`
- `/tron/`

This matters because these paths look like natural archive or hub destinations, but they are not safe redirect targets right now.

## Important Correction To The Old Decision Logic

For old archive-style `404` URLs, the safer living targets are often the archive paths under:

- `/cryptocurrency-news/...`
- `/insights/`
- `/trends/`
- `/crypto-topics/`
- `/learn-crypto/`

Examples confirmed live on `2026-05-05`:

- `https://tokentopnews.com/cryptocurrency-news/bitcoin/` -> `200`
- `https://tokentopnews.com/cryptocurrency-news/cardano/` -> `200`
- `https://tokentopnews.com/cryptocurrency-news/ethereum/` -> `200`
- `https://tokentopnews.com/cryptocurrency-news/ripple/` -> `200`
- `https://tokentopnews.com/cryptocurrency-news/solana/` -> `200`
- `https://tokentopnews.com/cryptocurrency-news/tron/` -> `200`
- `https://tokentopnews.com/trends/defi/` -> `200`
- `https://tokentopnews.com/press-release/` -> `200`
- `https://tokentopnews.com/learn-crypto/` -> `200`

## Files Created In This Pass

- [tokentopnews-404-obvious-remap-batch-2026-05-05.csv](/home/thana2/screaming-frow/Tokentopnews/tokentopnews-404-obvious-remap-batch-2026-05-05.csv)
- [tokentopnews-fix-request-broken-section-hubs-2026-05-05.csv](/home/thana2/screaming-frow/Tokentopnews/tokentopnews-fix-request-broken-section-hubs-2026-05-05.csv)
- [tokentopnews-next-actions-2026-05-05.md](/home/thana2/screaming-frow/Tokentopnews/tokentopnews-next-actions-2026-05-05.md)

## Recommended Order Now

### 1. Site-side review of broken section hubs

Before using `/altcoins/`, `/bitcoin/`, `/defi/`, `/solana/`, and similar paths as redirect destinations, confirm whether they should:

- become real section/archive pages, or
- remain redirected permanently

Use:

- [tokentopnews-fix-request-broken-section-hubs-2026-05-05.csv](/home/thana2/screaming-frow/Tokentopnews/tokentopnews-fix-request-broken-section-hubs-2026-05-05.csv)

### 2. Local-ready obvious `404` remap batch

This small batch can already be used as the first clean `404` remap tranche because the targets were checked live and are less ambiguous.

Use:

- [tokentopnews-404-obvious-remap-batch-2026-05-05.csv](/home/thana2/screaming-frow/Tokentopnews/tokentopnews-404-obvious-remap-batch-2026-05-05.csv)

### 3. Leave the rest of the `404` backlog for manual mapping

The remaining flat-slug `404` rows are still mostly article-to-article remap decisions and should be handled in smaller thematic batches.

## Practical Conclusion

The next Tokentopnews phase should not treat every surviving section-looking URL as a valid redirect target.

There are two separate problems now:

1. broken section hubs that route to single articles
2. old `404` URLs that need remapping into the actually living archive structure
