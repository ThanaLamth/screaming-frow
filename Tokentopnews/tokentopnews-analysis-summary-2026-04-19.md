# TokenTopNews Analysis Summary

- HTML URLs in decision sheet: `16648`
- Indexable HTML URLs: `10609`
- Non-indexable HTML URLs: `5708`
- URLs in sitemap: `10411`
- Non-indexable URLs in sitemap export: `11`

## Type Counts

- Posts: `11490`
- Tag archives: `4488`
- Pagination URLs: `228`
- CMC archive + pagination: `34`
- Coin duplicate URLs: `61`
- Section archives: `19`
- Press release archives: `3`
- Legacy news/category URLs: `9`
- Media pages (/p/*): `309`

## Suggested Actions

- Keep: `9587`
- Improve: `814`
- 301: `1130`
- Noindex: `5117`
- Delete: `0`

## GSC Coverage Buckets

- Bị loại trừ bởi thẻ 'noindex': `312`
- Trang có lệnh chuyển hướng: `2`
- Đã thu thập dữ liệu – hiện chưa được lập chỉ mục: `27`

## Internal Link Waste Signals

- Tag archive problem inlink rows: `15256`
- Coin duplicate problem inlink rows: `7972`
- CMC problem inlink rows: `18856`
- Legacy news/category problem inlink rows: `133`

Top problem-link sources by bucket:
- Tag archives: `/best-crypto-to-invest-in-apemars-22300-gains-vs-dogecoin-and-shiba-inu-news/ (37) | /analysts-spot-apemars-as-the-next-100x-meme-coin-after-buttcoin-and-gigachad/ (32) | /new-crypto-coins-watchlist-2026-apemars-chainlink-stellar/ (30) | /best-altcoins-to-invest-apemars-whitelist-live-ada-btc-rise/ (30) | /missed-shiba-inu-this-1000x-meme-coin-is-your-second-shot/ (26)`
- Coin duplicates: `/missed-hypes-breakout-why-this-layer-1-project-dominates-as-the-most-popular-cryptocurrency-of-2025/ (9) | /sky-hits-resistance-ethereum-slows-qubetics-could-be-the-next-best-crypto-to-buy-right-now/ (8) | /best-1000x-meme-coins-bullzilla-wif-and-trump/ (8) | /solana-blockdag-and-cosmos-top-cryptos-to-buy-now-for-major-growth/ (7) | /bullzilla-polkadot-and-wlfi-dominate-the-top-cryptos-to-invest-in-washington-dc/ (6)`
- CMC: `/cmc/page/9/ (60) | /cmc/page/8/ (60) | /cmc/page/7/ (60) | /cmc/page/6/ (60) | /cmc/page/5/ (60)`
- Legacy news/category: `/morgan-stanley-crypto-increasingly-centralized/ (3) | /politics-and-cryptocurrency-merge-in-argentina/ (3) | /what-are-bip-and-why-should-every-crypto-trader-follow-them/ (3) | /ripple-and-ethereum-soon-to-be-interoperable/ (3) | /trust-in-binance-is-falling/ (3)`

## Immediate Priorities

- Keep noindex stable on `tag`, `media`, `cmc`, and duplicate utility buckets.
- Stop feeding old archive paths like `/crypto-topics/press-release/`, `/news/`, and old `/category/` URLs.
- Remove upload/image URLs from sitemap output.
- Work the smaller `crawled - currently not indexed` post batch after template cleanup.