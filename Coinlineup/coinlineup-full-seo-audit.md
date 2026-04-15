# Coinlineup Full SEO Audit

Audit Date: 2026-04-15  
Site Type: Crypto news, market commentary, and commercial crypto content  
Scope: Full audit using live site checks, Screaming Frog exports, and Semrush backlink export

## Executive Summary

- Overall SEO Health Score: 46/100
- CMS / Stack: WordPress with Rank Math, Elementor, Site Kit, Header Footer Elementor, and Typify theme
- Key Site Metrics: 12,136 HTML URLs crawled; 10,472 indexable HTML URLs; 1,664 non-indexable HTML URLs; 7,235 Semrush backlink rows; 257 unique source domains; 1,761 linked target URLs
- Top blockers:
- Utility and low-value archive URLs are indexable and included in sitemap coverage.
- Internal URL architecture is weak, with many internal 404s, 301s, and broken currency redirects.
- Metadata, archive rules, and social metadata templates are inconsistent at scale.
- Backlink profile exists, but much of it is noisy, heavily nofollow, and concentrated on homepage plus scattered article/event URLs rather than a clean editorial architecture.

### Scorecard

| Category | Weight | Score | Weighted | Status |
| --- | --- | --- | --- | --- |
| Technical SEO | 25% | 35 | 8.75 | Poor |
| Content Quality | 25% | 48 | 12.00 | Poor |
| On-Page SEO | 20% | 45 | 9.00 | Poor |
| Schema / Structured Data | 10% | 62 | 6.20 | Fair |
| Performance (CWV) | 10% | 45 | 4.50 | Poor |
| Images / Visual-Media Hygiene | 5% | 35 | 1.75 | Poor |
| AI Search Readiness | 5% | 75 | 3.75 | Good |

## All Issues

| # | Priority | Category | Issue | Impact | Effort | Score Impact | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Critical | Technical SEO | Utility pages such as `/login/`, `/my-account/`, `/bookmarks/`, and `/my-follows/` are `200 + Indexable` and included in sitemap coverage. | High index bloat and crawl waste on low-value URLs. | Medium | High | Open |
| 2 | Critical | Sitemap | Sitemap coverage includes low-value and utility URLs, including `/uncategorized/`, `/sponsored-articles/`, and multiple trust or utility destinations. | Sitemap stops representing the clean indexable set Google should prioritize. | Medium | High | Open |
| 3 | Critical | Redirects | Multiple `/currencies/` URLs redirect to `/cmc-currency-details-advanced-design/`, which returns `404` and also appears in sitemap issue coverage. | Link equity and crawl paths terminate in broken destinations. | High | High | Open |
| 4 | High | Internal Linking | Screaming Frog shows 559 internal 404 URLs, 537 internal 301 URLs, and 132 internal 5xx URLs. | Weak crawl paths, stale internal links, and poor user experience. | High | High | Open |
| 5 | High | Taxonomy | `/uncategorized/` is indexable, in sitemap coverage, and carries 1,292 unique internal inlinks. | Thin taxonomy page absorbs internal equity and dilutes topical structure. | Medium | High | Open |
| 6 | High | Commercial Archive Strategy | `/sponsored-articles/` archive and deep pagination remain indexable. | Commercial archive inventory can compete with editorial sections and expand low-value index coverage. | Low | Medium | Open |
| 7 | High | Archive Rules | Author archives are mostly noindex, but at least one deep author pagination URL is indexable and missing a canonical. | Signals inconsistent template rules and potential index leakage. | Medium | Medium | Open |
| 8 | High | Media Hygiene | Sitemap contains 141 non-indexables, heavily driven by broken or unstable `/wp-content/uploads/` URLs. | Media instability weakens rendering, trust, and sitemap cleanliness. | Medium | Medium | Open |
| 9 | Medium | Metadata | 1,426 missing meta descriptions, 2,239 titles over 60 characters, 65 duplicate titles, and 44 duplicate meta descriptions. | Template duplication weakens CTR and page differentiation. | Medium | Medium | Open |
| 10 | Medium | Duplicate Content | Many duplicate article variants, including `-2` slug patterns, remain live. | Cannibalization and diluted search signals. | Medium | Medium | Open |
| 11 | Medium | Trust Architecture | Important trust pages exist but appear as orphan URLs in crawl exports. | Good trust content is not fully integrated into internal navigation and trust flow. | Low | Medium | Open |
| 12 | Medium | Metadata / Social | Homepage and article templates include duplicated OG and Twitter metadata from Rank Math plus fallback markup. | Creates metadata conflicts and inconsistent social previews. | Medium | Low | Open |
| 13 | Medium | Backlinks | Backlink profile is concentrated on homepage and noisy external ecosystems, with limited clean editorial-page authority spread. | Weakens URL-level resilience when consolidating or deleting pages. | Medium | Medium | Open |
| 14 | Low | External Link Quality | Large portions of the 4xx and 5xx exports come from third-party destinations. | Secondary editorial quality issue, but lower urgency than internal defects. | Low | Low | Open |

## Technical SEO

- Score: 35/100
- Key evidence:
- `robots.txt` is reachable and references `https://coinlineup.com/sitemap_index.xml`.
- `sitemap_index.xml` is live and generated by Rank Math, but the crawl export shows low-value and non-indexable URL inclusion issues.
- Screaming Frog exports show 12,136 internal HTML URLs, with 10,472 indexable and 1,664 non-indexable.
- Utility URLs such as `https://coinlineup.com/login/`, `https://coinlineup.com/my-account/`, `https://coinlineup.com/bookmarks/`, and `https://coinlineup.com/my-follows/` are `200`, indexable, canonical to themselves, and included in sitemap exports.
- Internal error footprint remains large: 559 internal 404s, 537 internal 301s, and 132 internal 5xx URLs.
- Several `/currencies/` URLs redirect to `https://coinlineup.com/cmc-currency-details-advanced-design/`, but that URL returns `404`.
- Risks:
- Crawl budget is spent on utility, archive, and broken URL patterns instead of priority editorial inventory.
- Broken redirect logic can waste internal equity and confuse canonical intent.
- Recommended fixes:
- Noindex and remove utility pages from sitemaps at template level.
- Fix currency routing/template output so every currency URL resolves to a valid canonical target.
- Export inlinks for internal 404 and 301 clusters, then repair source links instead of only fixing destinations.

## Content Quality

- Score: 48/100
- Key evidence:
- The site mixes editorial crypto news with event, exchange, and heavily commercial/promotional content patterns.
- Representative article pages use article schema, breadcrumbs, author info, and summaries, but topical inventory appears broad and uneven.
- Archive and taxonomy quality is weak, especially where low-value archive pages remain indexable.
- Risks:
- Editorial authority gets diluted by promotional or event-style inventory.
- Similar short-form or lightly differentiated articles increase cannibalization risk.
- Recommended fixes:
- Separate editorial, sponsored, and event-driven content architecture more clearly.
- Consolidate weaker same-intent posts into stronger evergreen or authoritative pages.
- Add stricter content thresholds before indexing low-value archives or programmatic article variants.

## Schema

- Score: 62/100
- Present schema:
- Homepage: `NewsMediaOrganization`, `Organization`, `WebSite`, `WebPage`, `Person`, `NewsArticle`
- Article pages: `NewsMediaOrganization`, `WebSite`, `BreadcrumbList`, `WebPage`, `Person`, `NewsArticle`
- Author pages: `ProfilePage`, `Person`
- Risks:
- Homepage is marked as `NewsArticle`, which is not an ideal fit for a home template.
- Social metadata duplication suggests overlapping plugin or fallback behavior that may also reflect schema governance looseness.
- Recommended fixes:
- Simplify homepage schema to `WebSite`, `Organization`, and `WebPage` unless there is a justified editorial feature page model.
- Review template/plugin logic so only one metadata authority controls OG/Twitter and related structured outputs.

## Sitemap

- Findings:
- `sitemap_index.xml` is live and references many post sitemaps plus page, category, and news sitemaps.
- Screaming Frog found 141 non-indexable URLs in sitemap coverage.
- Utility and low-value URLs appear in sitemap exports, including `/login/`, `/my-account/`, `/bookmarks/`, `/my-follows/`, `/uncategorized/`, `/sponsored-articles/`, `/press-release/`, `/contacts/`, `/editorial-policy/`, and `/publish-editorial-standards-fact-checking-policy/`.
- Non-indexable sitemap rows are heavily driven by `/wp-content/uploads/` and one broken currency-detail target.
- Issues:
- Sitemap is not a clean list of canonical search-worthy URLs.
- Media and utility leakage reduce sitemap quality.
- Recommended fixes:
- Restrict sitemaps to canonical URLs intended for search discovery.
- Remove broken media and non-indexable URLs from sitemap generation.
- Decide intentionally which trust pages should remain indexed and keep only those in sitemap coverage.

## Performance

- Score: 45/100
- LCP / CLS / script issues:
- Homepage and article templates load substantial CSS and JS from Elementor, theme assets, ads, Site Kit, and ticker widgets.
- Live HTML includes ad/snippet loading and multiple plugin layers, which likely increase render complexity.
- Internal 5xx media issues suggest origin or CDN instability for images.
- Recommended fixes:
- Reduce non-essential plugin output on key templates.
- Audit ad-related scripts and widget assets on homepage and article pages.
- Stabilize image/CDN delivery before optimizing secondary JS.

## Visual & Mobile

- Findings:
- Site appears to serve images with dimensions and responsive variants in many areas.
- Homepage includes a hidden H1 pattern plus visible logo-led masthead.
- Author and trust pages are present and styled, but some templates appear cluttered by plugin and archive widgets.
- Accessibility / usability issues:
- Hidden or template-driven heading patterns should be reviewed to ensure page hierarchy remains clear.
- Utility and archive sprawl can make navigation feel less intentional.
- Recommended fixes:
- Check mobile rendering for key templates after crawl cleanup, especially homepage, article, and archive pages.
- Simplify archive and widget density where commercial and editorial signals are competing.

## Action Plan

| # | Priority | Action | Category | Effort | Score Impact | Timeline |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Critical | Noindex and remove utility URLs from sitemap generation. | Technical SEO | Medium | High | 0-7 days |
| 2 | Critical | Repair `/currencies/` redirect logic and remove broken target URLs from internal links and sitemaps. | Redirects | High | High | 0-14 days |
| 3 | High | Fix top internal 404 and 301 clusters using inlink exports. | Internal Linking | High | High | 0-21 days |
| 4 | High | Reassign posts out of `/uncategorized/` and deindex or consolidate that archive. | Taxonomy | Medium | High | 0-14 days |
| 5 | High | Decide indexation rules for sponsored/commercial archives and paginated archive pages. | Content Architecture | Low | Medium | 0-14 days |
| 6 | High | Remove broken media URLs from sitemap coverage and stabilize upload/CDN responses. | Images / Media | Medium | Medium | 0-21 days |
| 7 | Medium | Consolidate duplicate post variants and resolve `-2` slug duplication patterns. | Duplicate Content | Medium | Medium | 14-30 days |
| 8 | Medium | Clean metadata templates for tag archives and low-value templates before manual page-level edits. | On-Page SEO | Medium | Medium | 14-30 days |
| 9 | Medium | Review OG/Twitter duplication and assign one metadata owner across templates. | Metadata / Social | Medium | Low | 14-30 days |
| 10 | Medium | Link trust pages more prominently from footer, about, and author pathways. | Trust Architecture | Low | Medium | 14-30 days |
| 11 | Medium | Use backlink data to protect URLs with real referring domains before delete/remap work. | Backlinks | Medium | Medium | Ongoing |

## AI Search Readiness

- Score: 75/100
- Originality signals:
- Site has live editorial-policy content, author profiles, and organization schema.
- Expert / entity signals:
- Homepage and article templates expose organization, author, and article schema.
- Citable-content gaps:
- Archive bloat and promotional overlap weaken the clarity of which pages deserve citation.
- Author pages carry overlinked synthetic-profile patterns rather than clean expertise proof.
- Recommended fixes:
- Trim low-signal author profile links and strengthen concise expertise statements.
- Keep trust pages indexable if intentional, but integrate them cleanly into site architecture.
- Reduce low-value archive inventory so AI systems see clearer authority pages.

## On-Page SEO

- Sample pages checked:
- Homepage: `https://coinlineup.com/`
- Article: `https://coinlineup.com/bitcoin-quantum-scare-priced-in-bernstein-3-5-year-upgrade-window/`
- Sponsored archive: `https://coinlineup.com/sponsored-articles/`
- Author page: `https://coinlineup.com/author/jensen-ackles/`
- Editorial policy: `https://coinlineup.com/editorial-policy/`
- Findings:
- Representative article page has strong basics: title, description, canonical, article schema, author, and breadcrumbs.
- Homepage and article pages both show duplicated OG/Twitter metadata from Rank Math plus fallback markup.
- Sponsored archive is fully indexable and canonical to itself.
- Author page is `noindex`, which is acceptable, but author schema and profile linking remain overly noisy.
- Recommended fixes:
- Keep strong on-page article basics, but clean template duplication and archive rules first.
- Do not spend editorial time rewriting title/meta at scale until crawl/index architecture is stable.

## Plugin Audit

- WordPress evidence observed:
- Rank Math PRO
- Elementor
- Header Footer Elementor
- Site Kit by Google
- Theme: Typify
- Additional ticker/ad or snippet tooling visible in homepage/article HTML

## Cache / SEO Plugin Config

- Live evidence suggests Rank Math controls primary SEO markup.
- Homepage and article pages also emit fallback OG/Twitter blocks, likely from theme or custom code.
- Recommendation:
- Remove fallback social metadata where Rank Math already outputs complete tags.
- Review sitemap and archive settings inside Rank Math plus theme/plugin overrides.

## Theme / Infrastructure Analysis

- Platform / theme / framework observations:
- WordPress with Typify theme and Elementor-heavy rendering.
- Risks:
- Theme/plugin overlap is likely driving metadata duplication, archive leakage, and utility-page exposure.
- Recommended fixes:
- Audit template conditions and archive rules at theme and SEO-plugin level together instead of patching symptoms page by page.

## Backlink Addendum

- Semrush export reviewed: `Backlink Semrush/coinlineup.com-backlinks.csv`
- 7,235 backlink rows across 257 unique source domains and 1,761 target URLs
- 6,418 rows are `nofollow`; only 817 are follow
- Homepage is the strongest target by far with 339 rows and 156 unique source domains
- Backlink profile is concentrated on homepage plus scattered article URLs, event pages, commercial pages, and some image/upload URLs
- 22 internal 404 URLs still have backlink rows, though most are weak; they should be reviewed before deletion
- There are also backlinks pointing to unstable media paths such as `/wp-content/uploads/`

Backlink implications:

- Do not delete internal 404 targets blindly; map weak but real backlink targets to the closest same-intent replacement where one exists.
- Prioritize redirect or restoration for broken URLs that retain multiple referring domains or follow links.
- Use backlink evidence as a protection layer during remap, not as the sole reason to keep low-value pages live.
