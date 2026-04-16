from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


BASE_DIR = Path("/home/thana2/screaming-frow/TheCCPress")
DATE = "2026-04-16"


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
    url = row["URL"]
    replacement = row["Replacement URL"]
    if url_type == "amp":
        return "301 AMP variant to canonical non-AMP URL and remove AMP URLs from sitemaps."
    if url_type == "parameter":
        return "301 parameter URL to canonical clean URL; remove parameter discovery from schema/internal links."
    if url_type == "press_release_archive":
        if replacement:
            return f"Archive variant should 301 to {replacement}."
        return "Archive should not stay live as an index target; use closest surviving parent if needed."
    if url_type == "cmc_archive":
        return "Current /cmc/ URL is 404; map to the surviving CMC archive/category or retire with a controlled redirect."
    if row["Status Code"].startswith("404"):
        if replacement:
            return f"404 URL should 301 to {replacement}."
        return "404 URL has no safe replacement in the decision sheet; manual destination mapping required before redirect."
    if replacement:
        return f"Redirect to {replacement}."
    return "Manual review required."


def main() -> None:
    decision_rows = read_rows(BASE_DIR / f"theccpress-url-decision-full-{DATE}.csv")

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
            "Notes": row["Notes"],
            "Implementation Notes": impl_note(row),
        }
        for row in redirect_rows
    ]
    write_csv(BASE_DIR / f"theccpress-301-priority-batch-{DATE}.csv", redirect_batch)

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
            "Priority": row["Priority"],
            "GSC Indexing Blocker": row["GSC Indexing Blocker"],
            "Notes": row["Notes"],
        }
        for row in noindex_rows
    ]
    write_csv(BASE_DIR / f"theccpress-noindex-priority-batch-{DATE}.csv", noindex_batch)

    type_counts = Counter(row["Type"] for row in noindex_rows)
    redirect_type_counts = Counter(row["Type"] for row in redirect_rows)

    rules_md = f"""# TheCCPress Noindex Rules

## Immediate Template Rules

- `noindex,follow` all `/tag/` archives.
  Evidence: the decision sheet marks `3705` tag archives for noindex and the inlink scan shows about `141516` internal inlink rows feeding tag URLs.
- `noindex,follow` all archive pagination such as `/category/.../page/2+`.
  Evidence: `4119` pagination URLs were found and the deepest ones still receive internal links.
- `noindex,follow` all author pagination such as `/author/.../page/2+`.
  Evidence: `1500` author-pagination URLs and about `16470` internal inlink rows point into that bucket.
- Keep `/p/*.webm` media pages as `200` but enforce `noindex,follow` and exclude them from sitemaps.
  Evidence: GSC `Bị loại trừ bởi thẻ 'noindex'` is dominated by media-page URLs.
- `noindex,follow` `/submit-press-release/`.
  Evidence: the inlink scan shows about `22464` internal inlink rows pointing to this URL.
- `noindex,follow` surviving press-release archive variants:
  - `https://theccpress.com/category/latest-news/press-release/`
  - `https://theccpress.com/category/press-releases/`

## Priority URL Batch

- Priority noindex URLs exported to:
  - `theccpress-noindex-priority-batch-{DATE}.csv`

## Counts In Priority Batch

- Tag archives: `{type_counts.get('tag_archive', 0)}`
- Pagination URLs: `{type_counts.get('pagination', 0)}`
- Press-release archive URLs: `{type_counts.get('press_release_archive', 0)}`
- Other URLs: `{sum(type_counts.values()) - type_counts.get('tag_archive', 0) - type_counts.get('pagination', 0) - type_counts.get('press_release_archive', 0)}`

## Implementation Notes

- Remove all noindex buckets from XML sitemaps.
- Do not return `404` for these buckets unless you are intentionally deleting the URL family.
- The safest default is `200` + `noindex,follow` + sitemap exclusion + reduced internal link prominence.
"""
    (BASE_DIR / f"theccpress-noindex-rules-{DATE}.md").write_text(rules_md, encoding="utf-8")

    internal_links_md = """# TheCCPress Internal Link Cut Batch

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
"""
    (BASE_DIR / f"theccpress-internal-link-cut-batch-{DATE}.md").write_text(internal_links_md, encoding="utf-8")

    overview_md = f"""# TheCCPress Implementation Batch

## Files

- `theccpress-301-priority-batch-{DATE}.csv`
- `theccpress-noindex-priority-batch-{DATE}.csv`
- `theccpress-noindex-rules-{DATE}.md`
- `theccpress-internal-link-cut-batch-{DATE}.md`

## Redirect Batch Counts

- Total priority 301 URLs: `{len(redirect_rows)}`
- AMP URLs: `{redirect_type_counts.get('amp', 0)}`
- Parameter URLs: `{redirect_type_counts.get('parameter', 0)}`
- Other URLs needing manual mapping or category cleanup: `{len(redirect_rows) - redirect_type_counts.get('amp', 0) - redirect_type_counts.get('parameter', 0)}`

## Noindex Batch Counts

- Total priority noindex URLs: `{len(noindex_rows)}`
- Tag archives: `{type_counts.get('tag_archive', 0)}`
- Pagination URLs: `{type_counts.get('pagination', 0)}`
- Press-release archive URLs: `{type_counts.get('press_release_archive', 0)}`

## Execution Order

1. Implement AMP + parameter redirects from the 301 batch.
2. Add template-level noindex rules for tags, archive pagination, author pagination, and media pages.
3. Remove noindex/non-indexable URLs from XML sitemaps.
4. Cut the internal-link sources listed in the internal-link batch.
5. Manually map the remaining `404` URLs in the 301 batch that still have a blank replacement target.
"""
    (BASE_DIR / f"theccpress-implementation-batch-{DATE}.md").write_text(overview_md, encoding="utf-8")


if __name__ == "__main__":
    main()
