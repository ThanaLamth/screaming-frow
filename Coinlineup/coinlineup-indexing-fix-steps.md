# Coinlineup Indexing Fix Steps

Use this file as the execution checklist after the blocker merge in `coinlineup-url-decision-full.csv`.

## Step 1: Lock the source of truth

Open these files first:

- `Coinlineup/coinlineup-url-decision-full.csv`
- `Coinlineup/coinlineup-indexing-blockers-summary.md`

Keep these conclusions fixed while working:

- `286` `noindex` URLs are media `.webm` assets under `/p/`
- `31` URLs are the real indexing blocker set
- `2` redirect URLs are cleanup-only, not the main issue

## Step 2: Clean up media `.webm` URLs

Goal:

- keep them `noindex`
- stop treating them like content that needs improvement
- reduce crawl waste

Actions:

1. Check whether `/p/*.webm` URLs are present in XML sitemaps.
2. Remove those media URLs from sitemaps if they are included.
3. Check whether feeds, archive blocks, or internal widgets expose too many of these media URLs.
4. Leave them as `noindex` unless there is a deliberate media-indexing strategy.

Expected outcome:

- Google stops wasting indexing attention on non-content asset URLs.

## Step 3: Fix `/currencies/` URL normalization

This is one of the clearest technical blocker patterns.

Observed problem:

- both slash and non-slash variants appear in blocker data
- examples: `.../USD` and `.../USD/`

Actions:

1. Pick one canonical format for `/currencies/` URLs.
2. Redirect the non-canonical version with `301`.
3. Set self-canonical tags on the preferred version only.
4. Keep only the preferred version in XML sitemaps.
5. Update internal links so they point only to the preferred version.

Expected outcome:

- duplicate URL signals are reduced
- canonical intent becomes consistent

## Step 4: Remove or canonicalize parameter URLs

Priority URL:

- `https://coinlineup.com/coin/?uuid=fLcU_wBrc`

Actions:

1. Identify the clean canonical destination.
2. If the parameter URL is just a variant, apply `301` or canonical to the clean version.
3. Remove parameter URLs from XML sitemaps.
4. Remove internal links that point directly to parameterized versions.

Expected outcome:

- Google sees a single preferred page instead of fragmented variants.

## Step 5: Improve the 18 article URLs in `Crawled - currently not indexed`

This is the main content task.

Start with the strongest recovery candidates:

- `https://coinlineup.com/lighter-tge-airdrop-2025-details/`
- `https://coinlineup.com/u-s-tariffs-shift-as-supreme-court-curbs-ieepa/`
- `https://coinlineup.com/whales-shift-focus-to-zero-knowledge-proofs-3000x-roi-potential-as-zcash-toncoins-rally-slows-down-8/`
- `https://coinlineup.com/zcash-futures-interest-price-surge/`
- `https://coinlineup.com/zkp-could-deliver-10000x-returns-how-it-stacks-up-against-aave-and-okb-in-2026s-trending-crypto-list/`
- `https://coinlineup.com/solana-whale-pippin-investment-news/`

For each article, review in this order:

1. Confirm the page returns `200`.
2. Confirm the page is indexable and not `noindex`.
3. Confirm the canonical points to itself.
4. Check for title, H1, and topic duplication against similar URLs.
5. Expand thin sections with original information, context, or clearer synthesis.
6. Add relevant internal links from stronger pages or category hubs.
7. Confirm the URL is in the XML sitemap.

Expected outcome:

- Google has clearer reasons to keep the URL indexed.

## Step 6: Clean the 2 redirect blocker URLs

URLs:

- `https://coinlineup.com/home/`
- `https://coinlineup.com/nft/`

Actions:

1. Check where each URL redirects.
2. Keep the redirect if the destination is correct.
3. Remove these URLs from XML sitemaps if they are listed.
4. Update internal links so they point directly to final destinations.

Expected outcome:

- redirect noise is removed from indexing workflows.

## Step 7: Resubmit after fixes

After technical cleanup and article improvements:

1. Resubmit the sitemap in Google Search Console.
2. Use URL Inspection for the improved article URLs.
3. Request indexing only for pages that were actually improved or normalized.
4. Do not request indexing for `.webm` asset URLs.

## Step 8: Recheck after Google recrawls

Wait roughly `5` to `14` days, then verify again.

Actions:

1. Export the updated GSC indexing report.
2. Compare the new export against `coinlineup-url-decision-full.csv`.
3. Check whether the `Crawled - currently not indexed` bucket drops.
4. If not, review sitewide quality, template duplication, and weak archive/internal-link patterns.

## Working order

Use this sequence:

1. Media sitemap cleanup
2. `/currencies/` canonical normalization
3. Parameter URL cleanup
4. Priority article improvements
5. Redirect cleanup
6. GSC resubmission
7. Recheck after recrawl
