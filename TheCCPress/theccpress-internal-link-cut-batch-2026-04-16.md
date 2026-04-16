# TheCCPress Internal Link Cut Batch

## Cut First

- Reduce or remove auto-linked tag chips/blocks in article templates.
  Evidence: tag archives receive about `141516` internal inlink rows.
  Most-fed destinations:
  - `/tag/ethereum/`
  - `/tag/ripple/`
  - `/tag/monero/`
  - `/tag/litecoin/`
  - `/tag/bitcoin-cash/`

- Reduce deep numbered archive pagination links.
  Evidence: pagination URLs receive about `27177` internal inlink rows, including links to pages like `/category/latest-news/page/930/`.
  Source paths repeatedly feeding deep pagination include:
  - `/category/latest-news/blockchain-events/page/2/`
  - `/category/latest-news/blockchain-events/page/3/`
  - `/category/blockchain-events/page/2/`
  - `/category/blockchain-events/page/3/`
  - deep `/category/latest-news/page/699+/`

- Remove prominent internal linking to `/submit-press-release/`.
  Evidence: the inlink scan shows about `22464` internal inlink rows to that single URL.

- Reduce archive-to-archive loops in the press-release section.
  Source paths repeatedly feeding the bucket include:
  - `/category/latest-news/press-release/`
  - `/category/latest-news/press-release/page/2/`
  - `/category/latest-news/press-release/page/3/`
  - `/category/latest-news/press-release/page/4/`
  - `/category/latest-news/press-release/page/5/`

- Reduce author-pagination loops.
  Evidence: author-pagination URLs receive about `16470` internal inlink rows.
  Source paths repeatedly feeding that bucket include:
  - `/author/noah-carter/page/3/`
  - `/author/noah-carter/page/7/`
  - `/author/noah-carter/page/17/`
  - `/author/noah-carter/page/19/`
  - `/author/aborisadeglory/page/2/`
  - `/author/aborisadeglory/page/3/`

- Review `/cmc/` and `/category/cmc/` links.
  Evidence: the CMC bucket receives about `6038` internal inlink rows while `/cmc/` itself is currently `404`.

## Redirect Batch

- Priority 301 URLs exported to:
  - `theccpress-301-priority-batch-2026-04-16.csv`

## Notes

- The goal is not only to noindex weak URLs but to stop the site from constantly re-feeding them through template links.
- Start with template/component changes before article-level cleanup.
