from __future__ import annotations

import csv
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path("/home/thana2/screaming-frow/TheCCPress")
DATE = "2026-04-16"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        return list(csv.DictReader(handle))


def read_csv_set(path: Path, key: str = "Address") -> set[str]:
    rows = read_csv_rows(path)
    return {row[key].strip() for row in rows if row.get(key, "").strip()}


def read_zip_csv_map(path: Path) -> dict[str, list[dict[str, str]]]:
    output: dict[str, list[dict[str, str]]] = {}
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            with archive.open(info) as handle:
                text = handle.read().decode("utf-8-sig", "replace").splitlines()
            if not text:
                output[info.filename] = []
                continue
            output[info.filename] = list(csv.DictReader(text))
    return output


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1"}


def path_only(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    return path if path.endswith("/") or "." in path.rsplit("/", 1)[-1] else f"{path}/"


def classify_type(url: str) -> str:
    parsed = urlparse(url)
    path = path_only(url)
    query = parsed.query.lower()

    trust_pages = {
        "/about-us/",
        "/authors/",
        "/contact/",
        "/corrections-policy/",
        "/editorial-standards-fact-checking-policy/",
        "/sponsored-content-disclosure/",
        "/advertising-disclosure/",
        "/ownership-disclosure/",
        "/financial-disclosures/",
        "/privacy-policy/",
        "/terms-of-use/",
    }
    if any(token in query for token in ("post_type=", "page_id=", "p=", "utm_")):
        return "parameter"
    if path == "/":
        return "homepage"
    if path in trust_pages:
        return "trust_page"
    if path.startswith("/p/"):
        return "media_page"
    if "/amp/" in path or query == "amp" or query.endswith("&amp"):
        return "amp"
    if "/tag/" in path:
        return "tag_archive"
    if "press-release" in path or "press-releases" in path:
        if re.search(r"/page/\d+/?$", path):
            return "pagination"
        return "press_release_archive"
    if re.search(r"/page/\d+/?$", path) or "paged=" in query:
        if "/author/" in path:
            return "author_pagination"
        return "pagination"
    if "/author/" in path:
        return "author_archive"
    if path == "/cmc/" or path.startswith("/cmc/"):
        return "cmc_archive"
    if path.startswith("/conflicts/"):
        return "conflicts_archive"
    if path.startswith("/investigations/"):
        return "investigations_archive"
    if path.startswith("/people/"):
        return "people_archive"
    if path.startswith("/power/"):
        return "power_archive"
    if path.startswith("/stories/"):
        return "stories_archive"
    return "post"


def infer_replacement(url: str, base_row: dict[str, str] | None) -> str:
    if base_row:
        for key in ("Redirect URL", "Canonical Link Element 1"):
            target = base_row.get(key, "").strip()
            if target and target != url:
                return target
    parsed = urlparse(url)
    if "/amp/" in parsed.path:
        return url.replace("/amp/", "/")
    if parsed.query:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"
    return ""


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def priority_for(
    url_type: str,
    status_code: str,
    in_sitemap: bool,
    noindex: bool,
    backlink_rows: int,
    gsc_issue: str,
    clicks: float,
    impressions: float,
) -> str:
    if url_type == "trust_page":
        return "Critical"
    if url_type in {"amp", "parameter"}:
        return "Critical"
    if url_type in {"tag_archive", "pagination", "author_pagination"} and in_sitemap:
        return "Critical"
    if url_type in {"press_release_archive", "cmc_archive"}:
        return "Critical"
    if status_code.startswith(("4", "5")) and (backlink_rows or impressions or clicks):
        return "Critical"
    if "Đã thu thập dữ liệu" in gsc_issue:
        return "High"
    if "noindex" in gsc_issue.lower() and in_sitemap:
        return "High"
    if backlink_rows or clicks or impressions:
        return "High"
    if noindex:
        return "Medium"
    return "Low"


def confidence_for(url_type: str, status_code: str, gsc_issue: str) -> str:
    if url_type in {
        "trust_page",
        "amp",
        "parameter",
        "tag_archive",
        "pagination",
        "author_pagination",
        "press_release_archive",
        "media_page",
    }:
        return "High"
    if status_code.startswith(("3", "4", "5")) or "Trang thay thế" in gsc_issue:
        return "High"
    if url_type.endswith("_archive") or "Đã thu thập dữ liệu" in gsc_issue:
        return "Medium"
    return "Low"


def action_for(
    url: str,
    url_type: str,
    status_code: str,
    indexability: str,
    gsc_issue: str,
    backlink_rows: int,
    clicks: float,
    impressions: float,
    replacement: str,
) -> str:
    if url_type in {"trust_page", "homepage"}:
        return "keep"
    if status_code.startswith("3"):
        return "301"
    if status_code.startswith(("4", "5")):
        return "301" if replacement or backlink_rows or clicks or impressions else "delete"
    if url_type in {"amp", "parameter"}:
        return "301"
    if url_type in {"tag_archive", "pagination", "author_pagination", "media_page"}:
        return "noindex"
    if url_type == "press_release_archive":
        return "noindex"
    if "Trang thay thế có thẻ chính tắc thích hợp" in gsc_issue:
        return "301"
    if "Bị loại trừ bởi thẻ 'noindex'" in gsc_issue:
        return "noindex"
    if url_type in {"author_archive", "cmc_archive", "conflicts_archive", "investigations_archive", "people_archive", "power_archive", "stories_archive", "press_release_post"}:
        return "improve"
    if "Đã thu thập dữ liệu" in gsc_issue:
        return "improve"
    if indexability == "Non-Indexable" and not replacement:
        return "noindex"
    if backlink_rows or clicks or impressions:
        return "improve"
    return "keep"


def main() -> None:
    crawl_dir = BASE_DIR / "Crawl"
    gsc_dir = BASE_DIR / "GSC"
    backlink_dir = BASE_DIR / "Backlink"

    base_rows = read_csv_rows(crawl_dir / "all_internal_all.csv")
    base_map = {row["Address"].strip(): row for row in base_rows if row["Address"].strip()}

    in_sitemap = read_csv_set(crawl_dir / "sitemaps_urls_in_sitemap.csv")
    orphan_urls = read_csv_set(crawl_dir / "sitemaps_orphan_urls.csv")
    noindex_urls = read_csv_set(crawl_dir / "directives_noindex.csv")
    canonical_missing = read_csv_set(crawl_dir / "canonicals_missing.csv")
    canonicalised = read_csv_set(crawl_dir / "canonicals_canonicalised.csv")
    meta_missing = read_csv_set(crawl_dir / "meta_description_missing.csv")
    meta_duplicate = read_csv_set(crawl_dir / "meta_description_duplicate.csv")
    title_duplicate = read_csv_set(crawl_dir / "page_titles_duplicate.csv")
    title_missing = read_csv_set(crawl_dir / "page_titles_missing.csv")
    title_over_60 = read_csv_set(crawl_dir / "page_titles_over_60_characters.csv")
    nonindexable_in_sitemap = read_csv_set(crawl_dir / "sitemaps_nonindexable_urls_in_sitemap.csv")

    gsc_perf = {}
    perf_files = read_zip_csv_map(gsc_dir / f"theccpress.com-Performance-on-Search-{DATE}.zip")
    for row in perf_files.get("Trang.csv", []):
        url = row.get("Trang hàng đầu", "").strip()
        if not url:
            continue
        gsc_perf[url] = {
            "clicks": row.get("Lượt nhấp", "0").replace(".", "").replace(",", "."),
            "impressions": row.get("Lượt hiển thị", "0").replace(".", "").replace(",", "."),
            "ctr": row.get("CTR", ""),
            "position": row.get("Vị trí", "").replace(",", "."),
        }

    gsc_issue_map: dict[str, list[str]] = defaultdict(list)
    coverage_zips = sorted(gsc_dir.glob("theccpress.com-Coverage-Drilldown-*.zip"))
    for zip_path in coverage_zips:
        zip_map = read_zip_csv_map(zip_path)
        metadata_rows = zip_map.get("Siêu dữ liệu.csv", [])
        issue = ""
        for row in metadata_rows:
            if row.get("Sản phẩm") == "Sự cố":
                issue = row.get("Giá trị", "").strip()
                break
        for row in zip_map.get("Bảng.csv", []):
            url = row.get("URL", "").strip()
            if url and issue:
                gsc_issue_map[url].append(issue)

    backlink_rows = Counter()
    follow_rows = Counter()
    referring_domains: dict[str, set[str]] = defaultdict(set)
    for row in read_csv_rows(backlink_dir / "theccpress.com-backlinks.csv"):
        target = row.get("Target url", "").strip()
        source = row.get("Source url", "").strip()
        if not target:
            continue
        backlink_rows[target] += 1
        if source:
            referring_domains[target].add(urlparse(source).netloc.lower())
        if not truthy(row.get("Nofollow", "")) and not truthy(row.get("Sponsored", "")) and not truthy(row.get("Ugc", "")):
            follow_rows[target] += 1

    inlink_row_count = Counter()
    inlink_sources: dict[str, Counter[str]] = defaultdict(Counter)
    inlink_problem_sources: dict[str, Counter[str]] = defaultdict(Counter)
    with (crawl_dir / "all_inlinks.csv").open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source = row.get("Source", "").strip()
            destination = row.get("Destination", "").strip()
            status_code = row.get("Status Code", "").strip()
            if not source or not destination:
                continue
            if not destination.startswith(("https://theccpress.com/", "http://theccpress.com/")):
                continue
            if not source.startswith(("https://theccpress.com/", "http://theccpress.com/")):
                continue
            source_path = path_only(source)
            inlink_row_count[destination] += 1
            inlink_sources[destination][source_path] += 1
            destination_type = classify_type(destination)
            if status_code.startswith(("3", "4", "5")) or destination_type in {
                "amp",
                "parameter",
                "tag_archive",
                "pagination",
                "author_pagination",
                "press_release_archive",
                "cmc_archive",
            }:
                inlink_problem_sources[destination][source_path] += 1

    urls: set[str] = set()
    for row in base_rows:
        address = row["Address"].strip()
        if address and row["Content Type"].startswith("text/html"):
            urls.add(address)
    urls.update(gsc_perf)
    urls.update(gsc_issue_map)

    decision_rows: list[dict[str, str]] = []
    type_counts = Counter()
    gsc_counts = Counter()
    pattern_counts = Counter()

    for url in sorted(urls):
        base = base_map.get(url)
        url_type = classify_type(url)
        type_counts[url_type] += 1
        if "/amp/" in url:
            pattern_counts["amp"] += 1
        if any(token in url for token in ("?page_id=", "?p=", "?post_type=", "?utm_")):
            pattern_counts["parameter"] += 1
        if "/cmc/" in url:
            pattern_counts["cmc"] += 1
        if ("press-release" in url or "press-releases" in url) and "/tag/" not in url:
            pattern_counts["press_release"] += 1

        status_code = (base or {}).get("Status Code", "")
        indexability = (base or {}).get("Indexability", "")
        replacement = infer_replacement(url, base)
        issue_list = sorted(set(gsc_issue_map.get(url, [])))
        for issue in issue_list:
            gsc_counts[issue] += 1

        perf = gsc_perf.get(url, {})
        clicks = float(perf.get("clicks") or 0)
        impressions = float(perf.get("impressions") or 0)
        ctr = perf.get("ctr", "")
        position = perf.get("position", "")

        note_parts = []
        if url_type in {"amp", "parameter"}:
            note_parts.append("Duplicate or variant URL pattern")
        if url_type == "press_release_archive":
            note_parts.append("High-risk archive bucket")
        if url_type == "cmc_archive":
            note_parts.append("Large CMC archive footprint")
        if url_type in {"author_archive", "author_pagination"}:
            note_parts.append("Review author quality and pagination")
        if url in nonindexable_in_sitemap:
            note_parts.append("Non-indexable URL appears in sitemap")
        if issue_list:
            note_parts.append(" | ".join(issue_list))

        priority = priority_for(
            url_type=url_type,
            status_code=status_code,
            in_sitemap=url in in_sitemap,
            noindex=url in noindex_urls,
            backlink_rows=backlink_rows[url],
            gsc_issue=" | ".join(issue_list),
            clicks=clicks,
            impressions=impressions,
        )
        confidence = confidence_for(url_type, status_code, " | ".join(issue_list))
        suggested_action = action_for(
            url=url,
            url_type=url_type,
            status_code=status_code,
            indexability=indexability,
            gsc_issue=" | ".join(issue_list),
            backlink_rows=backlink_rows[url],
            clicks=clicks,
            impressions=impressions,
            replacement=replacement,
        )

        decision_rows.append(
            {
                "URL": url,
                "Type": url_type,
                "Status Code": status_code,
                "Indexability": indexability,
                "In Sitemap": "yes" if url in in_sitemap else "no",
                "Orphan URL": "yes" if url in orphan_urls else "no",
                "Noindex Signal": "yes" if url in noindex_urls else "no",
                "Canonical Missing": "yes" if url in canonical_missing else "no",
                "Canonicalised": "yes" if url in canonicalised else "no",
                "Meta Missing": "yes" if url in meta_missing else "no",
                "Meta Duplicate": "yes" if url in meta_duplicate else "no",
                "Title Missing": "yes" if url in title_missing else "no",
                "Title Duplicate": "yes" if url in title_duplicate else "no",
                "Title Over 60": "yes" if url in title_over_60 else "no",
                "Backlink Rows": str(backlink_rows[url]),
                "Referring Domains": str(len(referring_domains[url])),
                "Follow Rows": str(follow_rows[url]),
                "All Inlinks Rows": str(inlink_row_count[url]),
                "GSC Clicks": perf.get("clicks", ""),
                "GSC Impressions": perf.get("impressions", ""),
                "GSC CTR": ctr,
                "GSC Position": position,
                "Suggested Action": suggested_action,
                "Replacement URL": replacement,
                "Priority": priority,
                "Decision Confidence": confidence,
                "GSC Indexing Blocker": " | ".join(issue_list),
                "GSC Last Crawl": "",
                "Top Inlink Sources": " | ".join(
                    f"{src} ({count})" for src, count in inlink_sources[url].most_common(3)
                ),
                "Problem Inlink Sources": " | ".join(
                    f"{src} ({count})" for src, count in inlink_problem_sources[url].most_common(3)
                ),
                "Notes": " | ".join(note_parts),
            }
        )

    decision_output = BASE_DIR / f"theccpress-url-decision-full-{DATE}.csv"
    with decision_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(decision_rows[0].keys()))
        writer.writeheader()
        writer.writerows(decision_rows)

    priority_rows = [
        {
            "Priority": "Critical",
            "Category": "Sitemap Hygiene",
            "Issue": "Large non-indexable footprint remains in XML sitemaps",
            "Evidence": f"{len(nonindexable_in_sitemap)} URLs in sitemaps_nonindexable_urls_in_sitemap.csv",
            "Impact": "Sitemaps are sending mixed canonical and quality signals to Google",
            "Recommended Action": "Remove AMP, parameter, noindex, redirect, and other non-indexable URLs from sitemap generation",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "Critical",
            "Category": "Archive Bloat",
            "Issue": "Tag and pagination volume is very large",
            "Evidence": f"Tag URLs: {type_counts['tag_archive']} | Pagination URLs: {type_counts['pagination']}",
            "Impact": "High crawl waste and index bloat risk on low-value archive pages",
            "Recommended Action": "Noindex tag and pagination templates unless a small curated set is intentionally indexed",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "Critical",
            "Category": "Author Archives",
            "Issue": "Author archive footprint is large",
            "Evidence": f"Author archive URLs: {type_counts['author_archive']} | Author pagination URLs: {type_counts['author_pagination']}",
            "Impact": "Thin author pages and pagination can dilute crawl budget and trust signals",
            "Recommended Action": "Audit main author archives for quality and noindex author pagination by default",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "Critical",
            "Category": "Duplicate Variants",
            "Issue": "AMP and parameter URLs remain discoverable",
            "Evidence": f"AMP URLs: {type_counts['amp']} | Parameter URLs: {type_counts['parameter']}",
            "Impact": "Duplicates split crawl and canonical signals",
            "Recommended Action": "301 AMP and parameter variants to their canonical destinations and remove them from sitemaps",
            "Effort": "High",
            "Status": "Open",
        },
        {
            "Priority": "High",
            "Category": "GSC Coverage",
            "Issue": "Google continues to crawl low-value and duplicate URLs",
            "Evidence": " | ".join(f"{key}: {value}" for key, value in sorted(gsc_counts.items())),
            "Impact": "Crawl budget is spent on duplicates and weak URLs instead of priority content",
            "Recommended Action": "Start with noindex and crawled-not-indexed batches, then clean redirect and canonical issues",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "High",
            "Category": "High-Risk Archives",
            "Issue": "Archive sections called out in handoff are present at scale",
            "Evidence": f"CMC pattern URLs: {pattern_counts['cmc']} | Press release pattern URLs: {pattern_counts['press_release']}",
            "Impact": "Low-value archive clusters can weaken overall site quality",
            "Recommended Action": "Review /cmc and /press-release first for noindex or stricter pruning rules",
            "Effort": "High",
            "Status": "Open",
        },
        {
            "Priority": "Medium",
            "Category": "Data Intake",
            "Issue": "All Inlinks export is available but very large",
            "Evidence": "all_inlinks.csv is ~1.67G and is being used as a streamed source rather than a fully materialized merge table",
            "Impact": "Deep source-link tracing is available, but repeated rescans of the raw file will be slower than the other datasets",
            "Recommended Action": "Use the generated inlink source columns in the decision sheet first and rescan the raw file only for template-level debugging",
            "Effort": "Low",
            "Status": "Open",
        },
    ]
    priority_output = BASE_DIR / f"theccpress-priority-fixes-generated-{DATE}.csv"
    with priority_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(priority_rows[0].keys()))
        writer.writeheader()
        writer.writerows(priority_rows)

    summary_output = BASE_DIR / f"theccpress-analysis-summary-{DATE}.md"
    summary_lines = [
        "# TheCCPress Analysis Summary",
        "",
        f"- HTML URLs in crawl: `{type_counts.total()}`",
        f"- Indexable HTML URLs: `{sum(1 for row in decision_rows if row['Indexability'] == 'Indexable')}`",
        f"- Non-indexable HTML URLs: `{sum(1 for row in decision_rows if row['Indexability'] == 'Non-Indexable')}`",
        f"- URLs in sitemap: `{len(in_sitemap)}`",
        f"- Non-indexable URLs in sitemap: `{len(nonindexable_in_sitemap)}`",
        "",
        "## Key Sections",
        "",
        f"- Tag archives: `{type_counts['tag_archive']}`",
        f"- Pagination URLs: `{type_counts['pagination']}`",
        f"- Author archives: `{type_counts['author_archive']}`",
        f"- Author pagination: `{type_counts['author_pagination']}`",
        f"- AMP URLs: `{pattern_counts['amp']}`",
        f"- Parameter URLs: `{pattern_counts['parameter']}`",
        f"- CMC pattern URLs: `{pattern_counts['cmc']}`",
        f"- Press release pattern URLs: `{pattern_counts['press_release']}`",
        "",
        "## GSC Coverage",
        "",
    ]
    for issue, count in sorted(gsc_counts.items()):
        summary_lines.append(f"- {issue}: `{count}`")
    summary_lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- `theccpress-url-decision-full-{DATE}.csv`",
            f"- `theccpress-priority-fixes-generated-{DATE}.csv`",
        ]
    )
    summary_output.write_text("\n".join(summary_lines), encoding="utf-8")

    critical_batch = [row for row in decision_rows if row["Priority"] in {"Critical", "High"} and row["Suggested Action"] != "keep"]
    action_rank = {"301": 0, "noindex": 1, "delete": 2, "improve": 3, "keep": 4}
    priority_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    critical_batch.sort(key=lambda row: (priority_rank[row["Priority"]], action_rank[row["Suggested Action"]], row["Type"], row["URL"]))
    critical_output = BASE_DIR / f"theccpress-critical-batch-{DATE}.csv"
    with critical_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(decision_rows[0].keys()))
        writer.writeheader()
        writer.writerows(critical_batch)


if __name__ == "__main__":
    main()
