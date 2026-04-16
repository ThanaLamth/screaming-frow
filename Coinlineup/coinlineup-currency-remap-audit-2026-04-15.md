# Coinlineup Currency Remap Audit

Date: 2026-04-15

Scope: the `7` suspicious currency rows that were excluded from the `301` batch.

## Final Decision

Do **not** `301` these source URLs to the sheet targets.

Do **not** `410` these source URLs either.

Current decision for all `7` rows: `KEEP`.

## Why

Each source URL is currently a valid live currency page:

- returns `200`
- self-canonical
- indexable (`robots` allows index/follow)
- title and H1 match the intended stablecoin page

Each proposed sheet target is wrong:

- it resolves to a different coin page entirely, or
- it redirects to an unrelated placeholder URL

This means the raw sheet mapping is not a cleanup opportunity. It is a bad redirect suggestion.

## URL-by-URL Verdict

1. Keep `https://coinlineup.com/currencies/USD1/usd1-wlfi/`
   - source page: `World Liberty Financial USD (USD1)`
   - proposed target: `https://coinlineup.com/currencies/1/usd1-wlfi/`
   - target page is a different coin: `Ucan fix life in1day (1)`

2. Keep `https://coinlineup.com/currencies/USDC/usd-coin/`
   - source page: `USDC (USDC)`
   - proposed target: `https://coinlineup.com/currencies/C/usd-coin/`
   - target page is a different coin: `Chainbase Token (C)`

3. Keep `https://coinlineup.com/currencies/USDE/ethena-usde/`
   - source page: `Ethena USDe (USDE)`
   - proposed target: `https://coinlineup.com/currencies/E/ethena-usde/`
   - target URL does not resolve to the same coin page
   - live behavior observed: `301` to `https://coinlineup.com/cmc-currency-details-advanced-design/`

4. Keep `https://coinlineup.com/currencies/USDF/falcon-finance/`
   - source page: `Falcon USD (USDF)`
   - proposed target: `https://coinlineup.com/currencies/F/falcon-finance/`
   - target page is a different coin: `SynFutures (F)`

5. Keep `https://coinlineup.com/currencies/USDG/global-dollar/`
   - source page: `Global Dollar (USDG)`
   - proposed target: `https://coinlineup.com/currencies/G/global-dollar/`
   - target page is a different coin: `Gravity (G)`

6. Keep `https://coinlineup.com/currencies/USDS/usds/`
   - source page: `USDS (USDS)`
   - proposed target: `https://coinlineup.com/currencies/S/usds/`
   - target page is a different coin: `Sonic (S)`

7. Keep `https://coinlineup.com/currencies/USDT/tether/`
   - source page: `Tether USD (USDT)`
   - proposed target: `https://coinlineup.com/currencies/T/tether/`
   - target page is a different coin: `Threshold (T)`

## Recommended Sheet Update

For these `7` rows:

- change status from `exclude_review` to `keep`
- remove the proposed `Replacement URL`
- add note: `Source URL is the correct live coin page; proposed target is wrong coin / wrong route`
