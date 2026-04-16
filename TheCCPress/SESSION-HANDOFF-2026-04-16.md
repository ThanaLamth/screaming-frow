## TheCCPress Session Handoff

Date: 2026-04-16
Repo: `/home/thana2/screaming-frow`
Site: `https://theccpress.com/`

### Current State

- We have finished the active Coinlineup work for this session and moved to `TheCCPress`.
- No Screaming Frog crawl was run from this environment because the machine does not have Screaming Frog CLI/app available in the terminal session.
- The next session should resume from `TheCCPress` crawl setup and data intake, following the same workflow used for `Coinlineup` and `Tokentopnews`.

### Folder Structure Prepared

- `TheCCPress/Crawl`
- `TheCCPress/GSC`
- `TheCCPress/Backlink`

Drop future exports into those folders.

### Confirmed Live Checks

#### Robots

- `https://theccpress.com/robots.txt` is live.
- It allows normal crawling except `/wp-admin/`.
- Sitemap declared: `https://theccpress.com/sitemap_index.xml`

#### Sitemap

- `sitemap_index.xml` is live and currently includes many `post-sitemap*.xml` files.
- This suggests a large post inventory, so archive/index bloat should be expected and reviewed carefully.

#### Existing Local References

- Old audit workbook exists:
  - `/home/thana2/TheCCPress-SEO-Audit-2026-03-29.xlsx`
  - `/home/thana2/audit-site/TheCCPress-SEO-Audit-2026-03-29.xlsx`
- Category remap references exist:
  - `/home/thana2/theccpress-category-remap-summary-2026-04-02.csv`
  - `/home/thana2/theccpress-category-remap-2026-04-02.csv`
  - `/home/thana2/theccpress-category-manual-review-2026-04-02.csv`
  - duplicates also exist under `/home/thana2/new-category/`

### Important Site-Specific Crawl Priorities

Do not treat `TheCCPress` like a generic crawl-only site. The crawl review should focus on:

1. `author` and `author pagination`
- This site previously had overly noisy author bios with too many low-value social/profile links.
- Check:
  - author archives returning `200`
  - whether author pages are indexed
  - author pagination volume
  - whether author pages have useful bios vs synthetic-looking link blocks

2. `trust pages`
- The trust stack is considered structurally strong, but needs verification in crawl:
  - `about`
  - `authors`
  - `contact`
  - `corrections-policy`
  - `editorial-standards-fact-checking-policy`
  - `sponsored-content-disclosure`
  - `advertising-disclosure`
  - `ownership-disclosure`
  - `financial-disclosures`
  - `privacy-policy`
  - `terms-of-use`
- Check that these are:
  - `200`
  - indexable if intended
  - not orphaned
  - internally linked to one another where appropriate

3. `archive/category structure`
- This site has meaningful narrative taxonomy and category-remap history.
- Special attention should go to archives such as:
  - `/cmc`
  - `/press-release`
  - `/conflicts/*`
  - `/investigations/*`
  - `/people/*`
  - `/power/*`
  - `/stories/*`
- Check:
  - thin archives
  - archive overlap/cannibalization
  - old vs new category structure mismatch
  - whether any archive should end up in `keep`, `improve`, `301`, or `noindex`

4. `press-release` and `cmc`
- These are likely high-risk index quality zones.
- Check:
  - how much of sitemap they occupy
  - whether many URLs are thin or promotional
  - whether they need stricter triage than normal news content

5. `schema / brand mismatch`
- A live homepage check showed suspicious brand/schema leftovers:
  - homepage schema still presents `Organization` / branding as `Blockchain & Cryptocurrencies Tabloid`
  - homepage schema references author `Tiberiu S.`
- This needs manual validation later:
  - homepage schema
  - publisher name consistency
  - article schema
  - author schema
  - OG/meta brand consistency

6. `parameter / duplicate discovery`
- Homepage schema output exposed `?post_type=post&p=...` style URLs inside structured data.
- Check whether these are:
  - harmless schema URLs only
  - or discoverable duplicate URLs that Google can crawl/index

7. `tag archives` and `pagination`
- WordPress/JNews-style sites often bloat here.
- Check:
  - tag archives indexability
  - pagination in sitemap
  - low-value paginated and tag pages

### Recommended Screaming Frog Setup

For the next session, run the crawl using the same workflow as Coinlineup/Tokentopnews:

- Mode: `Spider`
- Start URL: `https://theccpress.com/`
- Scope: `Subdomain`
- Connect `Google Search Console`
- Add backlink data later if available

### Exports Needed After Crawl

Save into `TheCCPress/Crawl`, `TheCCPress/GSC`, and `TheCCPress/Backlink`:

- `Internal`
- `All Inlinks`
- `Redirect Chains`
- `Canonicals`
- `Sitemaps`
- GSC-integrated URL exports if connected
- GSC Pages export
- GSC Performance export if available
- backlink / referring domains export if available

### Planned Workflow After Exports Arrive

1. Merge crawl + GSC + backlink data
2. Build decision sheet for:
- `keep`
- `improve`
- `301`
- `delete`
- `noindex`
3. Prioritize in this order:
- indexing blockers
- redirect/delete cleanup
- noindex cleanup
- improve batch

### Useful Existing Category Summary

From `theccpress-category-remap-summary-2026-04-02.csv`:

- `/cmc` = `1635`
- `/conflicts/company` = `25`
- `/conflicts/ideology` = `3`
- `/conflicts/regulation` = `11318`
- `/investigations/collapse` = `677`
- `/investigations/controversy` = `401`
- `/investigations/fraud` = `1125`
- `/people/founders` = `98`
- `/people/influencers` = `11`
- `/people/institutions` = `44`
- `/power/exchanges` = `36`
- `/power/regulators` = `1`
- `/power/vcs` = `12`
- `/press-release` = `89`
- `/stories/company-sagas` = `1`
- `/stories/market-drama` = `38`

These counts should inform archive triage once the crawl is available.

### Resume Prompt

If restarting tmux/new session, resume with:

`Continue TheCCPress from SESSION-HANDOFF-2026-04-16.md and process the crawl/GSC exports using the same workflow as Coinlineup.`

### Continuation Update

- Verified again on 2026-04-16 that `TheCCPress/Crawl`, `TheCCPress/GSC`, and `TheCCPress/Backlink` still have no export files.
- Prepared working files in `TheCCPress/` so the next session can move directly into triage once data arrives:
  - `theccpress-intake-checklist-2026-04-16.md`
  - `theccpress-url-decision-seed-2026-04-16.csv`
  - `theccpress-priority-fixes-2026-04-16.csv`
- The decision seed already preloads:
  - trust pages
  - high-risk archives such as `/cmc/`, `/press-release/`, `/conflicts/regulation/`
  - notes for schema mismatch and archive-quality review

### Data Intake Completed Later On 2026-04-16

- Crawl, GSC, and backlink files were downloaded into:
  - `TheCCPress/Crawl/`
  - `TheCCPress/GSC/`
  - `TheCCPress/Backlink/`
- `all_inlinks.csv` on Drive is a `1.6G` file.
  - It was later transferred to local successfully.
  - Confirmed local path now contains the real CSV payload:
    - `TheCCPress/Crawl/all_inlinks.csv`
  - File size checked locally: about `1.67G`

### Outputs Built

- `theccpress-url-decision-full-2026-04-16.csv`
- `theccpress-critical-batch-2026-04-16.csv`
- `theccpress-priority-fixes-generated-2026-04-16.csv`
- `theccpress-analysis-summary-2026-04-16.md`
- `theccpress-inlink-source-summary-2026-04-16.md`
- implementation batch files:
  - `theccpress-301-priority-batch-2026-04-16.csv`
  - `theccpress-noindex-priority-batch-2026-04-16.csv`
  - `theccpress-noindex-rules-2026-04-16.md`
  - `theccpress-internal-link-cut-batch-2026-04-16.md`
  - `theccpress-implementation-batch-2026-04-16.md`
- builder script:
  - `build_theccpress_decision_sheet.py`
  - `build_theccpress_implementation_batches.py`

### Key Findings From Initial Merge

- HTML URLs in decision sheet: `25675`
- Indexable HTML URLs: `15179`
- Non-indexable HTML URLs: `9827`
- URLs in sitemap export: `10090`
- Non-indexable HTML URLs still present in sitemap export: `47`
- High-risk volume:
  - tag archives: `3705`
  - pagination URLs: `4119`
  - author archives: `81`
  - author pagination: `1500`
  - AMP URLs: `161`
  - parameter URLs: `10`
  - CMC-pattern URLs: `251`
  - press-release-pattern URLs: `23`
- GSC coverage from imported drilldowns:
  - `Bị loại trừ bởi thẻ 'noindex'` = `256`
  - `Đã thu thập dữ liệu – hiện chưa được lập chỉ mục` = `158`
  - `Trang thay thế có thẻ chính tắc thích hợp` = `5`
  - `Không tìm thấy (404)` = `2`
  - `Trang có lệnh chuyển hướng` = `1`

### Trust Page Reality Check

- The previously planned trust stack does not fully exist live right now.
- Confirmed `200`:
  - `/about-us/`
  - `/contact/`
  - `/editorial-standards-fact-checking-policy/`
  - `/privacy-policy/`
- Confirmed live `404` on 2026-04-16:
  - `/authors/`
  - `/corrections-policy/`
  - `/sponsored-content-disclosure/`
  - `/advertising-disclosure/`
  - `/ownership-disclosure/`
  - `/financial-disclosures/`
  - `/terms-of-use/`

### Recommended Next Session Focus

1. Review `theccpress-critical-batch-2026-04-16.csv`
2. Start with:
   - AMP + parameter `301` cleanup
   - tag/pagination noindex batch
   - author pagination noindex batch
   - sitemap cleanup for non-indexable URLs
3. Manually review:
   - `/cmc/` and its pagination
   - press-release-related archives
   - missing trust pages that now return `404`
4. Use `theccpress-inlink-source-summary-2026-04-16.md` to identify template/path sources that keep feeding:
   - tag archives
   - deep pagination
   - author pagination
   - press-release buckets
   - `/cmc/`
