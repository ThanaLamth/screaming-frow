from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


BASE_DIR = Path("/home/thana2/screaming-frow/Tokentopnews")
DATE = "2026-04-19"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def impl_note(row: dict[str, str]) -> str:
    url_type = row["Type"]
    replacement = row["Replacement URL"]
    if url_type == "parameter":
        return "301 query/variant URL to the clean canonical URL."
    if url_type == "legacy_news_archive":
        if replacement:
            return f"301 legacy /news/ path to {replacement}."
        return "Legacy /news/ path still needs a manual destination before redirecting."
    if url_type == "category_archive":
        if replacement:
            return f"301 old /category/ path to {replacement}."
        return "Old category URL still needs a surviving archive destination."
    if url_type == "press_release_archive":
        if replacement:
            return f"Keep the surviving archive and consolidate old variant to {replacement}."
        return "Press-release archive variant needs a manual surviving target."
    if row["Status Code"].startswith(("404", "5")):
        if replacement:
            return f"301 broken URL to {replacement}."
        return "Broken URL has signals but no safe replacement was inferred; map manually."
    if replacement:
        return f"Redirect to {replacement}."
    return "Manual review required."


def main() -> None:
    decision_rows = read_rows(BASE_DIR / f"tokentopnews-url-decision-full-{DATE}.csv")

    redirect_rows = [
        row for row in decision_rows
        if row["Suggested Action"] == "301" and row["Priority"] in {"Critical", "High"}
    ]
    redirect_rows.sort(key=lambda row: (row["Type"], row["URL"]))
    redirect_batch = [
        {
            "URL": row["URL"],
            "Type": row["Type"],
            "Status Code": row["Status Code"],
            "Replacement URL": row["Replacement URL"],
            "Priority": row["Priority"],
            "Decision Confidence": row["Decision Confidence"],
            "GSC Indexing Blocker": row["GSC Indexing Blocker"],
            "Top Inlink Sources": row["Top Inlink Sources"],
            "Notes": row["Notes"],
            "Implementation Notes": impl_note(row),
        }
        for row in redirect_rows
    ]
    write_csv(BASE_DIR / f"tokentopnews-301-priority-batch-{DATE}.csv", redirect_batch)

    noindex_rows = [
        row for row in decision_rows
        if row["Suggested Action"] == "noindex" and row["Priority"] in {"Critical", "High"}
    ]
    noindex_rows.sort(key=lambda row: (row["Type"], row["URL"]))
    noindex_batch = [
        {
            "URL": row["URL"],
            "Type": row["Type"],
            "Status Code": row["Status Code"],
            "In Sitemap": row["In Sitemap"],
            "GSC Indexing Blocker": row["GSC Indexing Blocker"],
            "Priority": row["Priority"],
            "Top Inlink Sources": row["Top Inlink Sources"],
            "Notes": row["Notes"],
        }
        for row in noindex_rows
    ]
    write_csv(BASE_DIR / f"tokentopnews-noindex-priority-batch-{DATE}.csv", noindex_batch)

    improve_rows = [
        row for row in decision_rows
        if row["Suggested Action"] == "improve" and row["Priority"] in {"Critical", "High"}
    ]
    improve_rows.sort(
        key=lambda row: (
            0 if "Đã thu thập dữ liệu" in row["GSC Indexing Blocker"] else 1,
            -float(row["GSC Clicks"].replace(".", "").replace(",", ".") or 0),
            -float(row["GSC Impressions"].replace(".", "").replace(",", ".") or 0),
            -int(row["Backlink Rows"] or 0),
            row["URL"],
        )
    )
    improve_batch = [
        {
            "URL": row["URL"],
            "Type": row["Type"],
            "Status Code": row["Status Code"],
            "GSC Clicks": row["GSC Clicks"],
            "GSC Impressions": row["GSC Impressions"],
            "Backlink Rows": row["Backlink Rows"],
            "Follow Rows": row["Follow Rows"],
            "Priority": row["Priority"],
            "GSC Indexing Blocker": row["GSC Indexing Blocker"],
            "GSC Last Crawl": row["GSC Last Crawl"],
            "Notes": row["Notes"],
        }
        for row in improve_rows[:100]
    ]
    write_csv(BASE_DIR / f"tokentopnews-improve-priority-batch-{DATE}.csv", improve_batch)

    redirect_type_counts = Counter(row["Type"] for row in redirect_rows)
    noindex_type_counts = Counter(row["Type"] for row in noindex_rows)
    improve_type_counts = Counter(row["Type"] for row in improve_rows)

    noindex_rules_md = f"""# TokenTopNews Noindex Rules

## Immediate Template Rules

- Keep all `/tag/` archives on `noindex,follow`.
  Evidence: `{noindex_type_counts.get('tag_archive', 0)}` priority tag URLs in the noindex batch and the site already emits tag `noindex`.
- Keep `/p/*.webm` media pages on `noindex,follow`.
  Evidence: GSC `Bị loại trừ bởi thẻ 'noindex'` is dominated by `/p/` media URLs.
- Keep `/cmc/` and its pagination on `noindex,follow` unless you intentionally want that archive indexed.
  Evidence: `/cmc/` is live, noindex, and heavily internally linked.
- Add a noindex rule for `/coin/*` duplicate URLs if those pages must stay live.
  Evidence: `/coin/*` URLs are canonicalised to `/coin/` and do not present unique indexable content.

## Priority URL Batch

- `tokentopnews-noindex-priority-batch-{DATE}.csv`

## Implementation Notes

- Remove all noindex buckets from XML sitemaps.
- If a bucket is intentionally noindex, reduce template-level links that keep re-feeding it.
- Use `200 + noindex,follow` for stable utility/archive buckets; do not convert them to 404 unless you are intentionally retiring them.
"""
    (BASE_DIR / f"tokentopnews-noindex-rules-{DATE}.md").write_text(noindex_rules_md, encoding="utf-8")

    internal_links_md = f"""# TokenTopNews Internal Link Cut Batch

## Cut First

- Stop linking templates to legacy `/crypto-topics/press-release/` paths and keep only the surviving `/press-release/` archive.
- Reduce bulk tag-chip linking into `/tag/` pages.
- Reduce internal discovery of `/coin/*` duplicate URLs and prefer the canonical `/coin/` hub when that section needs to stay accessible.
- If `/cmc/` remains noindex, reduce its prominence in nav/widgets so it stops consuming crawl at archive depth.
- Remove links to legacy `/news/` and old `/category/` paths that now 404 or redirect.

## Batch Files

- `tokentopnews-301-priority-batch-{DATE}.csv`
- `tokentopnews-noindex-priority-batch-{DATE}.csv`
- `tokentopnews-improve-priority-batch-{DATE}.csv`
"""
    (BASE_DIR / f"tokentopnews-internal-link-cut-batch-{DATE}.md").write_text(internal_links_md, encoding="utf-8")

    overview_md = f"""# TokenTopNews Implementation Batch

## Files

- `tokentopnews-301-priority-batch-{DATE}.csv`
- `tokentopnews-noindex-priority-batch-{DATE}.csv`
- `tokentopnews-improve-priority-batch-{DATE}.csv`
- `tokentopnews-noindex-rules-{DATE}.md`
- `tokentopnews-internal-link-cut-batch-{DATE}.md`

## Redirect Batch Counts

- Total priority 301 URLs: `{len(redirect_rows)}`
- Legacy archives: `{redirect_type_counts.get('legacy_news_archive', 0) + redirect_type_counts.get('category_archive', 0)}`
- Broken posts/pages: `{sum(1 for row in redirect_rows if row['Status Code'].startswith(('404', '5')))}`
- Parameter variants: `{redirect_type_counts.get('parameter', 0)}`

## Noindex Batch Counts

- Total priority noindex URLs: `{len(noindex_rows)}`
- Tags: `{noindex_type_counts.get('tag_archive', 0)}`
- Coin duplicates: `{noindex_type_counts.get('coin_page', 0)}`
- CMC archive + pagination: `{noindex_type_counts.get('cmc_archive', 0) + noindex_type_counts.get('cmc_pagination', 0)}`
- Media pages: `{noindex_type_counts.get('media_page', 0)}`

## Improve Batch Counts

- Total priority improve URLs: `{len(improve_rows)}`
- Crawled currently not indexed URLs in top batch: `{sum(1 for row in improve_batch if 'Đã thu thập dữ liệu' in row['GSC Indexing Blocker'])}`
- Section/archive URLs needing quality work: `{improve_type_counts.get('section_archive', 0) + improve_type_counts.get('press_release_archive', 0)}`

## Execution Order

1. Fix legacy archive redirects and internal links to retired paths.
2. Lock stable noindex rules for tags, media pages, `/cmc/`, and `/coin/*`.
3. Remove non-indexable URLs from XML sitemaps.
4. Improve the smaller GSC crawled-not-indexed post batch.
"""
    (BASE_DIR / f"tokentopnews-implementation-batch-{DATE}.md").write_text(overview_md, encoding="utf-8")


if __name__ == "__main__":
    main()
