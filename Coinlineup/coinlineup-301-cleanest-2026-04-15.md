# Coinlineup 301 Cleanest Review

Date: 2026-04-15

Source sheet reviewed: `coinlineup-url-decision-full.csv`

## What was checked

This was reviewed in 3 passes:

1. Sheet sanity check
   - `648` rows marked `Suggested Action = 301`
   - raw sheet mix: `540` sheet-status `301`, `9` sheet-status `200`, `21` sheet-status `404`, `78` blank status, `22` blank replacement target
2. Targeted live spot checks
   - checked `/home/`, `/uncategorized/`, `/news/nft/`, and the suspicious currency remap rows
3. Full live pass on all `648` source URLs
   - first full pass result: `615` return `301`, `21` return `404`, `8` return `200`, `4` return `410`
4. Manual mapping implementation
   - mapped and implemented `21/21` previously unresolved `404` rows
   - verified all `21` now return exact `301` to the intended live target
   - current practical state: `637` return `301`, `7` return `200`, `4` return `410`

## Final verdict

Do not action the raw `648` rows as a direct backlog.

Cleanest current split:

- `636` rows: already done
- `11` rows: exclude from current 301 batch
- `1` row: optional low-value cleanup

## Already done

`636` rows do not need work now.

Breakdown:

- `613` rows already live-redirect to the expected target after URL normalization
- `1` extra row already handled outside the sheet target field:
  - `https://coinlineup.com/home/` -> `https://coinlineup.com/`
- `1` newly added live rule:
  - `https://coinlineup.com/uncategorized/` -> `https://coinlineup.com/news/`
- `21` manual-mapped rows now implemented and verified exact:
  - audit trail: `coinlineup-301-manual-mapping-candidates-2026-04-15.csv`

Notes:

- `/news/nft/` is already fixed and now redirects to `/news/`
- many currency `/USD` rows are already working; server returns relative `Location` headers, which is why some sheet/manual spot checks can look inconsistent if not normalized

## Ready Now

No clean 301 rows remain in the immediate batch.

## Manual Mapping Status

The previous `21` unresolved `404` rows are no longer open.

- all `21` were mapped to closest same-intent live articles
- all `21` were implemented in `coinlineup-redirect-guards`
- all `21` were verified live as exact `301` matches

Reference file:

- `coinlineup-301-manual-mapping-candidates-2026-04-15.csv`

## Exclude From Current 301 Batch

Do not implement these in the current batch.

### Suspicious currency remaps

These `7` rows are still live `200`.

Audit result:

- keep the source URLs live
- do not `301` them to the suggested targets
- do not `410` them

Reason:

- each source URL is the correct coin page
- each proposed target is a different coin page or a broken route

Reference file:

- `coinlineup-currency-remap-audit-2026-04-15.md`

- `https://coinlineup.com/currencies/USD1/usd1-wlfi/` -> `https://coinlineup.com/currencies/1/usd1-wlfi/`
- `https://coinlineup.com/currencies/USDC/usd-coin/` -> `https://coinlineup.com/currencies/C/usd-coin/`
- `https://coinlineup.com/currencies/USDE/ethena-usde/` -> `https://coinlineup.com/currencies/E/ethena-usde/`
- `https://coinlineup.com/currencies/USDF/falcon-finance/` -> `https://coinlineup.com/currencies/F/falcon-finance/`
- `https://coinlineup.com/currencies/USDG/global-dollar/` -> `https://coinlineup.com/currencies/G/global-dollar/`
- `https://coinlineup.com/currencies/USDS/usds/` -> `https://coinlineup.com/currencies/S/usds/`
- `https://coinlineup.com/currencies/USDT/tether/` -> `https://coinlineup.com/currencies/T/tether/`

### No-value rows already removed

These `4` rows are already `410` and have no current value for a 301 batch.

- `https://www.coinlineup.com/fluid-suspends-usr-marketplace-promises-full-compensation-to-affected-users/`
- `https://www.coinlineup.com/resolv-labs-usr-stablecoin-loses-peg-after-attacker-mints-80-million-tokens/`
- `https://www.coinlineup.com/sec-cftc-joint-crypto-regulation-guidance-takes-effect-monday/`
- `https://coinlineup.com/currencies///`

## Optional Low-Value Cleanup

One row is already redirecting, but not to the exact destination suggested in the sheet:

- source: `https://coinlineup.com/nft/`
- live now: `301` -> `https://coinlineup.com/`
- sheet target: `https://coinlineup.com/news/`

This can be corrected later if you want a cleaner topical redirect, but it is not worth prioritizing ahead of the currency remap audit.

## Cleanest Implementation Order

1. Ignore the `636` already-done rows
2. Audit the `7` currency remaps separately before touching them
3. Leave `/nft/` for later unless you want to tidy that edge case now
