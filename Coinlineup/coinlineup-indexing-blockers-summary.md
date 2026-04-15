# Coinlineup Indexing Blockers Summary

Source files reviewed:
- `Coinlineup/Blockers/1/Bảng.csv`
- `Coinlineup/Blockers/2/Bảng.csv`
- `Coinlineup/Blockers/3/Bảng.csv`
- `Coinlineup/coinlineup-url-decision-full.csv`

## Confirmed blocker split

- `286` URLs: `Bị loại trừ bởi thẻ 'noindex'`
- `31` URLs: `Đã thu thập dữ liệu – hiện chưa được lập chỉ mục`
- `2` URLs: `Trang có lệnh chuyển hướng`

This means Coinlineup is not fully deindexed. The real issue is severe underindexing, with most non-indexed URLs falling into one deliberate media bucket plus a smaller set of quality/canonical candidates.

## What is not the main problem

All `286` `noindex` blocker URLs mapped to `Type=media_asset` and sit under `/p/` as `.webm` files. Example patterns:

- `https://coinlineup.com/p/...webm`

Current interpretation:

- this looks intentional for media assets
- these URLs should not be treated as article pages to "improve"
- the cleanup task is to keep them out of XML sitemaps and avoid wasting crawl demand on them

## What is the main problem

The actionable blocker bucket is the `31` URLs in `Crawled - currently not indexed`.

Breakdown from the merged sheet:

- `18` article URLs
- `12` `/currencies/` URLs
- `1` parameter URL: `https://coinlineup.com/coin/?uuid=fLcU_wBrc`

Important pattern inside the `currencies` set:

- slash and non-slash duplicates both appear in blocker data
- examples: `.../USD` and `.../USD/`

This strongly suggests canonical normalization and duplicate-URL control are still weak in this area.

## Highest-priority URLs to review first

These URLs are indexable `200` pages but still not accepted into index:

- `https://coinlineup.com/lighter-tge-airdrop-2025-details/`
- `https://coinlineup.com/u-s-tariffs-shift-as-supreme-court-curbs-ieepa/`
- `https://coinlineup.com/whales-shift-focus-to-zero-knowledge-proofs-3000x-roi-potential-as-zcash-toncoins-rally-slows-down-8/`
- `https://coinlineup.com/zcash-futures-interest-price-surge/`
- `https://coinlineup.com/zkp-could-deliver-10000x-returns-how-it-stacks-up-against-aave-and-okb-in-2026s-trending-crypto-list/`
- `https://coinlineup.com/solana-whale-pippin-investment-news/`

These already show some external or GSC signal, so they are better recovery candidates than zero-signal pages.

## Redirect blocker

Only `2` URLs were flagged as redirect blockers:

- `https://coinlineup.com/home/`
- `https://coinlineup.com/nft/`

This is minor compared with the underindexing and URL-normalization issues.

Additional taxonomy decision:

- `https://coinlineup.com/news/nft/` should not be treated as a recovery target
- it is a thin category with limited post depth and weak strategic fit for Coinlineup
- preferred action is `301` to `https://coinlineup.com/news/` after article reassignment

## Practical next actions

1. Keep media `.webm` URLs as `noindex`, but remove them from sitemaps and reduce internal surfacing if they are not meant for search.
2. Fix slash/non-slash duplication for `/currencies/` URLs and enforce one canonical format.
3. Remove or canonicalize parameter URLs like `/coin/?uuid=...`.
4. Improve and resubmit the `18` article URLs in the blocker set, starting with the URLs that already have impressions or backlinks.
5. Retire the thin `https://coinlineup.com/news/nft/` taxonomy into `https://coinlineup.com/news/` instead of trying to force indexation.
6. Use the merged blocker columns in `coinlineup-url-decision-full.csv` as the source of truth for execution order.
