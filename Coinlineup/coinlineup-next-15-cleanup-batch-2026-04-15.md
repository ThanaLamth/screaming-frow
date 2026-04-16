# Coinlineup Next 15 Cleanup Batch - 2026-04-15

This is the next execution batch after the first recovery round.

Selection logic:

- prioritize live article URLs that are still weak but can be salvaged
- prioritize URLs already in the GSC blocker set
- protect URLs with real backlink signals before broader delete work
- defer giant bulk cleanup of zero-value broken URLs until the higher-signal items below are handled

## A. Improve First - Live URLs

These should be improved, internally linked, then resubmitted in GSC.

| Priority | URL | Why it is in the batch |
|---|---|---|
| 1 | `https://coinlineup.com/alliance-dao-seeks-crypto-founders/` | In GSC blocker export as crawled but not indexed. |
| 2 | `https://coinlineup.com/binance-alpha-airdrop-requires-credits/` | In GSC blocker export as crawled but not indexed. |
| 3 | `https://coinlineup.com/crypto-profit-perpetual-positions-unconfirmed/` | In GSC blocker export as crawled but not indexed. |
| 4 | `https://coinlineup.com/ethgas-gwei-token-distribution-details/` | In GSC blocker export as crawled but not indexed. |
| 5 | `https://coinlineup.com/sec-bitcoin-etp-approval-crypto-stance/` | In GSC blocker export as crawled but not indexed. |
| 6 | `https://coinlineup.com/peakai-raises-2-million-seed-funding-web3-marketing-analytics/` | Medium priority but strongest live backlink signal in the next tier: `6` referring domains, `11` backlink rows. |
| 7 | `https://coinlineup.com/what-happens-to-usdc-if-polymarket-launches-its-own-stablecoin/` | Strong live backlink protection case: `5` referring domains, `9` backlink rows. |
| 8 | `https://coinlineup.com/sec-cftc-joint-crypto-regulation-guidance-effect/` | Strong backlink support: `4` referring domains, `36` backlink rows. |
| 9 | `https://coinlineup.com/uk-regulator-seizes-illegal-drugs-linked-to-crypto-founder/` | Strong backlink support: `4` referring domains, `28` backlink rows. |
| 10 | `https://coinlineup.com/walmart-onepay-crypto-expansion/` | Strong backlink support: `4` referring domains, `23` backlink rows. |

## B. Redirect Next - Broken URLs With Backlinks

These should not be deleted blindly. Map them to the closest same-intent live URL.

| Priority | Broken URL | Signal to protect |
|---|---|---|
| 11 | `https://coinlineup.com/bitcoin-etf-outflows-hit-225m-as-eth-and-sol-spot-funds-also-bleed/` | `2` referring domains, `2` backlink rows. |
| 12 | `https://coinlineup.com/bitcoin-nears-70k-as-seller-resistance-builds/` | `2` referring domains, `2` backlink rows. |
| 13 | `https://coinlineup.com/bitcoin-traders-dump-btc-within-48-hours-of-fed-meetings-heres-the-pattern/` | `2` referring domains, `2` backlink rows. |
| 14 | `https://coinlineup.com/cftc-chair-michael-selig-says-financial-systems-are-outdated-highlights-blockchain/` | `2` referring domains, `2` backlink rows. |
| 15 | `https://coinlineup.com/circle-announces-cirbtc-a-1-1-bitcoin-backed-token/` | `2` referring domains, `2` backlink rows. |

## Execution Order

1. Improve items `1-10`.
2. Add internal links from related live articles into those improved URLs.
3. Request indexing for improved URLs.
4. For items `11-15`, choose exact replacement targets and apply `301`.
5. Only after this batch, move into larger-scale delete or `410` cleanup for zero-signal broken URLs.

## Notes

- This batch intentionally avoids utility pages, media assets, `/USD` variants, and thin taxonomy work because those have separate cleanup tracks.
- This batch also avoids the already handled recovery URLs from the first round.
