# Coinlineup Thin Category Cleanup - 2026-04-15

## Scope

Handled 5 live thin or empty category archives to reduce crawl waste before opening any new category hubs.

## Redirects Applied

| Old URL | Status | Target |
|---|---:|---|
| `https://coinlineup.com/guides/crypto-trading/` | `301` | `https://coinlineup.com/guides/` |
| `https://coinlineup.com/guides/defi/` | `301` | `https://coinlineup.com/guides/` |
| `https://coinlineup.com/guides/security/` | `301` | `https://coinlineup.com/guides/` |
| `https://coinlineup.com/guides/wallets/` | `301` | `https://coinlineup.com/guides/` |
| `https://coinlineup.com/projects/` | `301` | `https://coinlineup.com/cmc/` |

These redirects are handled by the active WordPress plugin `coinlineup-redirect-guards`.

## Taxonomy Cleanup

`Crypto Trading` was the only one of the 5 categories that still had posts attached.

Posts updated:

| Post ID | Slug | Category result |
|---|---|---|
| `2969` | `how-to-start-forex-trading-with-100` | kept only in `Guides` |
| `2388` | `best-crypto-trading-strategies-for-maximum-profits-in-2024` | kept only in `Guides` |

Verification after update:

| Term | Slug | Count |
|---|---|---:|
| `Crypto Trading` | `crypto-trading` | `0` |
| `Defi` | `defi` | `0` |
| `Security` | `security` | `0` |
| `Wallets` | `wallets` | `0` |
| `Projects` | `projects` | `0` |

## Why This Was Done

- prevents thin archives from staying indexable and consuming crawl budget
- consolidates weak archive signals into stronger parent hubs
- reduces noise before any future category expansion work

## Next Recommended Step

Wait for Google to recrawl the redirected archives and continue content-quality cleanup on thin or duplicated articles, not new category creation yet.
