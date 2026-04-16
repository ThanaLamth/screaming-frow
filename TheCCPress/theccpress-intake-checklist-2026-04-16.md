# TheCCPress Intake Checklist

Date: 2026-04-16
Site: `https://theccpress.com/`
Workflow: same Screaming Frog + GSC + backlink triage flow used for Coinlineup

## Current Intake Status

- `Crawl/`: missing exports
- `GSC/`: missing exports
- `Backlink/`: missing exports
- Existing local references available outside this folder:
  - `/home/thana2/TheCCPress-SEO-Audit-2026-03-29.xlsx`
  - `/home/thana2/audit-site/TheCCPress-SEO-Audit-2026-03-29.xlsx`
  - `/home/thana2/theccpress-category-remap-summary-2026-04-02.csv`
  - `/home/thana2/theccpress-category-remap-2026-04-02.csv`
  - `/home/thana2/theccpress-category-manual-review-2026-04-02.csv`

## Required Exports

Drop these into the prepared folders before triage:

- `Crawl/Internal`
- `Crawl/All Inlinks`
- `Crawl/Redirect Chains`
- `Crawl/Canonicals`
- `Crawl/Sitemaps`
- `GSC/Pages`
- `GSC/Performance`
- `Backlink/Referring domains` or equivalent URL-level backlink export

## Crawl Setup

- Mode: `Spider`
- Start URL: `https://theccpress.com/`
- Scope: `Subdomain`
- Connect `Google Search Console`

## First Triage Segments

Process these first once exports arrive:

1. Trust pages
   - `/about-us/`
   - `/authors/`
   - `/contact/`
   - `/corrections-policy/`
   - `/editorial-standards-fact-checking-policy/`
   - `/sponsored-content-disclosure/`
   - `/advertising-disclosure/`
   - `/ownership-disclosure/`
   - `/financial-disclosures/`
   - `/privacy-policy/`
   - `/terms-of-use/`
2. Author archives and author pagination
3. High-risk archive buckets
   - `/cmc/`
   - `/press-release/`
   - `/conflicts/*`
   - `/investigations/*`
   - `/people/*`
   - `/power/*`
   - `/stories/*`
4. Tag archives and pagination
5. Parameter and duplicate patterns, especially `?post_type=post&p=...`
6. Homepage/article schema and brand consistency

## Known Site-Specific Notes

- `robots.txt` is live and declares `https://theccpress.com/sitemap_index.xml`
- Sitemap index includes many post sitemaps, so archive and pagination bloat should be expected
- Homepage schema previously surfaced brand text similar to `Blockchain & Cryptocurrencies Tabloid`
- Homepage schema previously referenced author `Tiberiu S.`
- Category remap summary suggests especially large buckets:
  - `/conflicts/regulation` = `11318`
  - `/cmc` = `1635`
  - `/investigations/fraud` = `1125`
  - `/investigations/collapse` = `677`
  - `/investigations/controversy` = `401`
  - `/press-release` = `89`

## Next Files To Use

- `theccpress-url-decision-seed-2026-04-16.csv`
- `theccpress-priority-fixes-2026-04-16.csv`

Fill crawl, GSC, and backlink metrics into the decision sheet first, then finalize `keep` / `improve` / `301` / `delete` / `noindex`.
