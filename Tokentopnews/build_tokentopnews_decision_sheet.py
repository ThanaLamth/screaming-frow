from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path("/home/thana2/screaming-frow/Tokentopnews")
DATE = "2026-04-19"
SITE_HOST = "tokentopnews.com"
SITE_PREFIXES = ("https://tokentopnews.com/", "http://tokentopnews.com/")

SECTION_PREFIXES = (
    "/cryptocurrency-news/",
    "/insights/",
    "/macro/",
    "/narratives/",
    "/trends/",
    "/weekly-recap/",
    "/press-release/",
    "/blog/",
    "/nft/",
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        return list(csv.DictReader(handle))


def read_csv_set(path: Path, key: str = "Address") -> set[str]:
    if not path.exists():
        return set()
    rows = read_csv_rows(path)
    return {row.get(key, "").strip() for row in rows if row.get(key, "").strip()}


def parse_gsc_number(value: str) -> float:
    text = (value or "").strip()
    if not text:
        return 0.0
    return float(text.replace(".", "").replace(",", "."))


def path_only(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    last_segment = path.rsplit("/", 1)[-1]
    if path.endswith("/") or "." in last_segment:
        return path
    return f"{path}/"


def same_site(url: str) -> bool:
    return url.startswith(SITE_PREFIXES)


def truthy(value: str) -> bool:
    return (value or "").strip().lower() in {"true", "yes", "1"}


def classify_type(
    url: str,
    *,
    category_urls: set[str],
    coin_urls: set[str],
    page_urls: set[str],
    press_release_urls: set[str],
    tag_urls: set[str],
) -> str:
    parsed = urlparse(url)
    path = path_only(url)
    query = parsed.query.lower()

    if any(
        token in query
        for token in (
            "amp=1",
            "pa_service_worker=1",
            "page_id=",
            "p=",
            "utm_",
            "prefer_reader_view=1",
            "prefer_safari=1",
        )
    ):
        return "parameter"
    if path == "/":
        return "homepage"
    if path.startswith("/p/"):
        return "media_page"
    if url in tag_urls or "/tag/" in path:
        return "tag_archive"
    if url in page_urls or re.search(r"/page/\d+/?$", path):
        if "/author/" in path:
            return "author_pagination"
        if path.startswith("/cmc/"):
            return "cmc_pagination"
        return "pagination"
    if "/author/" in path:
        return "author_archive"
    if path == "/coin/":
        return "coin_hub"
    if url in coin_urls or path.startswith("/coin/"):
        return "coin_page"
    if path == "/cmc/" or path.startswith("/cmc/"):
        return "cmc_archive"
    if url in press_release_urls or path in {"/press-release/", "/crypto-topics/press-release/", "/crypto-topics/press-releases/"}:
        return "press_release_archive"
    if url in category_urls or path.startswith("/category/"):
        return "category_archive"
    if path.startswith("/news/"):
        return "legacy_news_archive"
    if path.startswith("/feed/") or path.endswith("/feed/"):
        return "feed"
    if path.startswith(SECTION_PREFIXES):
        return "section_archive"
    return "post"


def infer_replacement(url: str, base_row: dict[str, str] | None) -> str:
    if base_row:
        for key in ("Redirect URL", "Canonical Link Element 1"):
            target = (base_row.get(key, "") or "").strip()
            if target and target != url:
                return target

    parsed = urlparse(url)
    if parsed.query:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}"

    path = path_only(url)
    double_slug = re.search(r"/([^/]+)/\1/?$", path)
    if double_slug:
        trimmed = path[: -(len(double_slug.group(1)) + 1)]
        trimmed = trimmed if trimmed.endswith("/") else f"{trimmed}/"
        return f"{parsed.scheme}://{parsed.netloc}{trimmed}"

    if path == "/crypto-topics/press-releases/":
        return f"{parsed.scheme}://{parsed.netloc}/press-release/"

    return ""


def priority_for(
    *,
    url_type: str,
    status_code: str,
    in_sitemap: bool,
    noindex_signal: bool,
    backlink_rows: int,
    follow_rows: int,
    gsc_issue: str,
    clicks: float,
    impressions: float,
    inlinks: int,
) -> str:
    if url_type in {"parameter", "legacy_news_archive", "category_archive"}:
        return "Critical"
    if url_type in {"coin_page", "cmc_archive", "cmc_pagination"}:
        return "Critical"
    if url_type in {"tag_archive", "pagination", "author_pagination", "media_page"} and (inlinks or impressions):
        return "High"
    if in_sitemap and (noindex_signal or status_code.startswith(("3", "4", "5"))):
        return "Critical"
    if status_code.startswith(("4", "5")) and (backlink_rows or follow_rows or clicks or impressions or inlinks):
        return "Critical"
    if "Đã thu thập dữ liệu" in gsc_issue:
        return "High"
    if "Bị loại trừ bởi thẻ 'noindex'" in gsc_issue and impressions:
        return "High"
    if backlink_rows or follow_rows or clicks or impressions:
        return "High"
    if noindex_signal:
        return "Medium"
    return "Low"


def confidence_for(url_type: str, status_code: str, gsc_issue: str) -> str:
    if url_type in {
        "parameter",
        "tag_archive",
        "pagination",
        "author_pagination",
        "media_page",
        "legacy_news_archive",
        "category_archive",
        "coin_page",
        "cmc_archive",
        "cmc_pagination",
    }:
        return "High"
    if status_code.startswith(("3", "4", "5")):
        return "High"
    if "Đã thu thập dữ liệu" in gsc_issue or url_type in {"section_archive", "press_release_archive"}:
        return "Medium"
    return "Low"


def action_for(
    *,
    url_type: str,
    status_code: str,
    indexability: str,
    gsc_issue: str,
    backlink_rows: int,
    follow_rows: int,
    clicks: float,
    impressions: float,
    replacement: str,
    inlinks: int,
) -> str:
    if url_type in {"homepage"}:
        return "keep"
    if status_code.startswith("3"):
        return "301"
    if status_code.startswith(("4", "5")):
        if replacement or backlink_rows or follow_rows or clicks or impressions or inlinks:
            return "301"
        return "delete"
    if url_type == "parameter":
        return "301"
    if url_type in {"tag_archive", "pagination", "author_pagination", "media_page", "cmc_archive", "cmc_pagination", "feed"}:
        return "noindex"
    if url_type == "coin_page":
        return "noindex"
    if "Trang có lệnh chuyển hướng" in gsc_issue:
        return "301"
    if "Bị loại trừ bởi thẻ 'noindex'" in gsc_issue:
        return "noindex"
    if "Đã thu thập dữ liệu" in gsc_issue:
        return "improve"
    if url_type in {"legacy_news_archive", "category_archive"}:
        return "301"
    if url_type in {"section_archive", "press_release_archive", "coin_hub"} and (clicks or impressions or backlink_rows or follow_rows):
        return "improve"
    if indexability == "Non-Indexable" and replacement:
        return "301"
    if backlink_rows or follow_rows or clicks or impressions:
        return "improve"
    return "keep"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    crawl_dir = BASE_DIR / "Crawl"
    gsc_dir = BASE_DIR / "GSC"
    backlink_dir = BASE_DIR / "Backlink"

    base_rows = read_csv_rows(crawl_dir / "internal_all.csv")
    base_map = {row["Address"].strip(): row for row in base_rows if row.get("Address", "").strip()}

    category_urls = read_csv_set(crawl_dir / "category_internal_html.csv")
    coin_urls = read_csv_set(crawl_dir / "coin_internal_html.csv")
    page_urls = read_csv_set(crawl_dir / "page_internal_html.csv")
    press_release_urls = read_csv_set(crawl_dir / "press_release_internal_html.csv")
    tag_urls = read_csv_set(crawl_dir / "tag_internal_html.csv")

    in_sitemap = read_csv_set(crawl_dir / "sitemaps_urls_in_sitemap.csv")
    orphan_urls = read_csv_set(crawl_dir / "sitemaps_orphan_urls.csv")
    noindex_urls = read_csv_set(crawl_dir / "directives_noindex.csv")
    canonicalised = read_csv_set(crawl_dir / "canonicals_canonicalised.csv")
    nonindexable_in_sitemap = read_csv_set(crawl_dir / "sitemaps_nonindexable_urls_in_sitemap.csv")
    meta_duplicate = read_csv_set(crawl_dir / "meta_description_duplicate.csv")
    title_duplicate = read_csv_set(crawl_dir / "page_titles_duplicate.csv")
    title_over_60 = read_csv_set(crawl_dir / "page_titles_over_60_characters.csv")

    gsc_perf: dict[str, dict[str, str]] = {}
    perf_path = gsc_dir / f"tokentopnews.com-Performance-on-Search-{DATE}" / "Trang.csv"
    for row in read_csv_rows(perf_path):
        url = row.get("Trang hàng đầu", "").strip()
        if not same_site(url):
            continue
        gsc_perf[url] = {
            "clicks": row.get("Lượt nhấp", "0"),
            "impressions": row.get("Lượt hiển thị", "0"),
            "ctr": row.get("CTR", ""),
            "position": row.get("Vị trí", ""),
        }

    gsc_issue_map: dict[str, list[str]] = defaultdict(list)
    gsc_last_crawl: dict[str, str] = {}
    for metadata_path in sorted(gsc_dir.glob("tokentopnews.com-Coverage-Drilldown-*")):
        if not metadata_path.is_dir():
            continue
        meta_file = metadata_path / "Siêu dữ liệu.csv"
        table_file = metadata_path / "Bảng.csv"
        if not meta_file.exists() or not table_file.exists():
            continue

        issue = ""
        for row in read_csv_rows(meta_file):
            if row.get("Sản phẩm") == "Sự cố":
                issue = row.get("Giá trị", "").strip()
                break

        for row in read_csv_rows(table_file):
            url = row.get("URL", "").strip()
            if not same_site(url):
                continue
            if issue:
                gsc_issue_map[url].append(issue)
            last_crawl = row.get("Lần thu thập dữ liệu cuối cùng", "").strip()
            if last_crawl:
                gsc_last_crawl[url] = last_crawl

    backlink_rows = Counter()
    follow_rows = Counter()
    referring_domains: dict[str, set[str]] = defaultdict(set)
    for row in read_csv_rows(backlink_dir / "tokentopnews.com-backlinks.csv"):
        target = row.get("Target url", "").strip()
        source = row.get("Source url", "").strip()
        if not same_site(target):
            continue
        backlink_rows[target] += 1
        if source:
            referring_domains[target].add(urlparse(source).netloc.lower())
        if not truthy(row.get("Nofollow", "")) and not truthy(row.get("Sponsored", "")) and not truthy(row.get("Ugc", "")):
            follow_rows[target] += 1

    inlink_row_count = Counter()
    inlink_sources: dict[str, Counter[str]] = defaultdict(Counter)
    inlink_problem_sources: dict[str, Counter[str]] = defaultdict(Counter)
    inlink_type_totals = Counter()
    inlink_type_sources: dict[str, Counter[str]] = defaultdict(Counter)

    with (crawl_dir / "all_inlinks.csv").open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            source = row.get("Source", "").strip()
            destination = row.get("Destination", "").strip()
            status_code = row.get("Status Code", "").strip()
            if not same_site(source) or not same_site(destination):
                continue

            source_path = path_only(source)
            destination_type = classify_type(
                destination,
                category_urls=category_urls,
                coin_urls=coin_urls,
                page_urls=page_urls,
                press_release_urls=press_release_urls,
                tag_urls=tag_urls,
            )
            inlink_row_count[destination] += 1
            inlink_sources[destination][source_path] += 1

            if status_code.startswith(("3", "4", "5")) or destination_type in {
                "tag_archive",
                "pagination",
                "author_pagination",
                "coin_page",
                "cmc_archive",
                "cmc_pagination",
                "legacy_news_archive",
                "category_archive",
            }:
                inlink_problem_sources[destination][source_path] += 1
                inlink_type_totals[destination_type] += 1
                inlink_type_sources[destination_type][source_path] += 1

    urls: set[str] = set()
    for row in base_rows:
        address = row.get("Address", "").strip()
        content_type = row.get("Content Type", "")
        if address and same_site(address) and content_type.startswith("text/html"):
            urls.add(address)
    urls.update(gsc_perf)
    urls.update(gsc_issue_map)

    decision_rows: list[dict[str, str]] = []
    type_counts = Counter()
    gsc_counts = Counter()
    action_counts = Counter()

    for url in sorted(urls):
        base = base_map.get(url)
        url_type = classify_type(
            url,
            category_urls=category_urls,
            coin_urls=coin_urls,
            page_urls=page_urls,
            press_release_urls=press_release_urls,
            tag_urls=tag_urls,
        )
        type_counts[url_type] += 1

        status_code = (base or {}).get("Status Code", "")
        indexability = (base or {}).get("Indexability", "")
        indexability_status = (base or {}).get("Indexability Status", "")
        replacement = infer_replacement(url, base)
        issue_list = sorted(set(gsc_issue_map.get(url, [])))
        for issue in issue_list:
            gsc_counts[issue] += 1

        perf = gsc_perf.get(url, {})
        clicks = parse_gsc_number(perf.get("clicks", "0"))
        impressions = parse_gsc_number(perf.get("impressions", "0"))
        ctr = perf.get("ctr", "")
        position = perf.get("position", "")

        priority = priority_for(
            url_type=url_type,
            status_code=status_code,
            in_sitemap=url in in_sitemap,
            noindex_signal=url in noindex_urls,
            backlink_rows=backlink_rows[url],
            follow_rows=follow_rows[url],
            gsc_issue=" | ".join(issue_list),
            clicks=clicks,
            impressions=impressions,
            inlinks=inlink_row_count[url],
        )
        confidence = confidence_for(url_type, status_code, " | ".join(issue_list))
        suggested_action = action_for(
            url_type=url_type,
            status_code=status_code,
            indexability=indexability,
            gsc_issue=" | ".join(issue_list),
            backlink_rows=backlink_rows[url],
            follow_rows=follow_rows[url],
            clicks=clicks,
            impressions=impressions,
            replacement=replacement,
            inlinks=inlink_row_count[url],
        )
        action_counts[suggested_action] += 1

        note_parts: list[str] = []
        if url_type == "tag_archive":
            note_parts.append("Tag archive is already noindex on-site and still consumes crawl paths")
        if url_type == "coin_page":
            note_parts.append("Coin detail URL is canonicalised to /coin/ and should not stay as an index target")
        if url_type == "cmc_archive":
            note_parts.append("CMC archive is noindex and heavily internally linked")
        if url_type in {"legacy_news_archive", "category_archive"}:
            note_parts.append("Legacy archive path still appears in crawl/GSC and should be consolidated")
        if url in nonindexable_in_sitemap:
            note_parts.append("Non-indexable URL appears in sitemap export")
        if replacement:
            note_parts.append(f"Replacement candidate: {replacement}")
        if issue_list:
            note_parts.append(" | ".join(issue_list))

        decision_rows.append(
            {
                "URL": url,
                "Type": url_type,
                "Status Code": status_code,
                "Indexability": indexability,
                "Indexability Status": indexability_status,
                "In Sitemap": "yes" if url in in_sitemap else "no",
                "Orphan URL": "yes" if url in orphan_urls else "no",
                "Noindex Signal": "yes" if url in noindex_urls else "no",
                "Canonicalised": "yes" if url in canonicalised else "no",
                "Meta Duplicate": "yes" if url in meta_duplicate else "no",
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
                "GSC Last Crawl": gsc_last_crawl.get(url, ""),
                "Top Inlink Sources": " | ".join(
                    f"{src} ({count})" for src, count in inlink_sources[url].most_common(3)
                ),
                "Problem Inlink Sources": " | ".join(
                    f"{src} ({count})" for src, count in inlink_problem_sources[url].most_common(3)
                ),
                "Notes": " | ".join(note_parts),
            }
        )

    decision_path = BASE_DIR / f"tokentopnews-url-decision-full-{DATE}.csv"
    write_csv(decision_path, decision_rows)

    priority_rows = [
        {
            "Priority": "Critical",
            "Category": "Tag Bloat",
            "Issue": "Tag archive footprint is extremely large and mostly low-signal",
            "Evidence": f"Tag archive URLs: {type_counts['tag_archive']} | noindex rows: {sum(1 for row in decision_rows if row['Type'] == 'tag_archive' and row['Noindex Signal'] == 'yes')}",
            "Impact": "Google and internal templates keep revisiting thin tag URLs instead of priority content",
            "Recommended Action": "Keep tag archives noindex, remove them from sitemaps, and reduce template-level tag linking",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "Critical",
            "Category": "Coin Duplicates",
            "Issue": "Coin detail URLs are canonicalised duplicates of /coin/",
            "Evidence": f"Coin duplicate URLs: {type_counts['coin_page']} | sample canonical target: https://tokentopnews.com/coin/",
            "Impact": "Crawl budget is split across duplicate utility URLs with no unique indexable value",
            "Recommended Action": "Noindex the /coin/* family and reduce internal linking into those duplicate URLs",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "Critical",
            "Category": "Legacy Archives",
            "Issue": "Old /news/, /category/, and crypto-topics archive paths are still present",
            "Evidence": f"Legacy news/category URLs: {type_counts['legacy_news_archive'] + type_counts['category_archive']} | internal redirect from /crypto-topics/press-release has 13k+ inlinks in crawl",
            "Impact": "The site keeps feeding obsolete archive paths and redirect targets into crawl",
            "Recommended Action": "Finalize 301 mappings and cut internal links to legacy archive paths",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "High",
            "Category": "GSC Coverage",
            "Issue": "Google is still crawling non-index targets and a smaller set of weak posts",
            "Evidence": " | ".join(f"{key}: {value}" for key, value in sorted(gsc_counts.items())),
            "Impact": "Fresh crawl budget is shared between noindex/media buckets and posts that need stronger quality signals",
            "Recommended Action": "Leave stable noindex rules in place, then work the crawled-not-indexed post batch",
            "Effort": "Medium",
            "Status": "Open",
        },
        {
            "Priority": "High",
            "Category": "Sitemap Hygiene",
            "Issue": "XML sitemap still contains broken upload URLs",
            "Evidence": f"Non-indexable sitemap URLs: {len(nonindexable_in_sitemap)}",
            "Impact": "Sitemap quality is diluted by 522 asset URLs instead of just canonical index targets",
            "Recommended Action": "Remove wp-content upload URLs and any non-indexable entries from sitemap generation",
            "Effort": "Low",
            "Status": "Open",
        },
        {
            "Priority": "High",
            "Category": "CMC Bucket",
            "Issue": "The /cmc/ archive stays live as a large noindex section with heavy internal link volume",
            "Evidence": f"CMC archive URLs: {type_counts['cmc_archive'] + type_counts['cmc_pagination']} | problem inlink rows: {inlink_type_totals['cmc_archive'] + inlink_type_totals['cmc_pagination']}",
            "Impact": "A large noindex archive can still consume crawl and internal-link equity at scale",
            "Recommended Action": "Keep /cmc/ noindex, exclude it from sitemaps, and reduce template-level links if that section is not a search target",
            "Effort": "Medium",
            "Status": "Open",
        },
    ]
    write_csv(BASE_DIR / f"tokentopnews-priority-fixes-generated-{DATE}.csv", priority_rows)

    summary_lines = [
        "# TokenTopNews Analysis Summary",
        "",
        f"- HTML URLs in decision sheet: `{len(decision_rows)}`",
        f"- Indexable HTML URLs: `{sum(1 for row in decision_rows if row['Indexability'] == 'Indexable')}`",
        f"- Non-indexable HTML URLs: `{sum(1 for row in decision_rows if row['Indexability'] == 'Non-Indexable')}`",
        f"- URLs in sitemap: `{len(in_sitemap)}`",
        f"- Non-indexable URLs in sitemap export: `{len(nonindexable_in_sitemap)}`",
        "",
        "## Type Counts",
        "",
        f"- Posts: `{type_counts['post']}`",
        f"- Tag archives: `{type_counts['tag_archive']}`",
        f"- Pagination URLs: `{type_counts['pagination']}`",
        f"- CMC archive + pagination: `{type_counts['cmc_archive'] + type_counts['cmc_pagination']}`",
        f"- Coin duplicate URLs: `{type_counts['coin_page']}`",
        f"- Section archives: `{type_counts['section_archive']}`",
        f"- Press release archives: `{type_counts['press_release_archive']}`",
        f"- Legacy news/category URLs: `{type_counts['legacy_news_archive'] + type_counts['category_archive']}`",
        f"- Media pages (/p/*): `{type_counts['media_page']}`",
        "",
        "## Suggested Actions",
        "",
        f"- Keep: `{action_counts['keep']}`",
        f"- Improve: `{action_counts['improve']}`",
        f"- 301: `{action_counts['301']}`",
        f"- Noindex: `{action_counts['noindex']}`",
        f"- Delete: `{action_counts['delete']}`",
        "",
        "## GSC Coverage Buckets",
        "",
    ]
    for issue, count in sorted(gsc_counts.items()):
        summary_lines.append(f"- {issue}: `{count}`")

    summary_lines.extend(
        [
            "",
            "## Internal Link Waste Signals",
            "",
            f"- Tag archive problem inlink rows: `{inlink_type_totals['tag_archive']}`",
            f"- Coin duplicate problem inlink rows: `{inlink_type_totals['coin_page']}`",
            f"- CMC problem inlink rows: `{inlink_type_totals['cmc_archive'] + inlink_type_totals['cmc_pagination']}`",
            f"- Legacy news/category problem inlink rows: `{inlink_type_totals['legacy_news_archive'] + inlink_type_totals['category_archive']}`",
            "",
            "Top problem-link sources by bucket:",
            f"- Tag archives: `{ ' | '.join(f'{src} ({count})' for src, count in inlink_type_sources['tag_archive'].most_common(5)) }`",
            f"- Coin duplicates: `{ ' | '.join(f'{src} ({count})' for src, count in inlink_type_sources['coin_page'].most_common(5)) }`",
            f"- CMC: `{ ' | '.join(f'{src} ({count})' for src, count in (inlink_type_sources['cmc_archive'] + inlink_type_sources['cmc_pagination']).most_common(5)) }`",
            f"- Legacy news/category: `{ ' | '.join(f'{src} ({count})' for src, count in (inlink_type_sources['legacy_news_archive'] + inlink_type_sources['category_archive']).most_common(5)) }`",
            "",
            "## Immediate Priorities",
            "",
            "- Keep noindex stable on `tag`, `media`, `cmc`, and duplicate utility buckets.",
            "- Stop feeding old archive paths like `/crypto-topics/press-release/`, `/news/`, and old `/category/` URLs.",
            "- Remove upload/image URLs from sitemap output.",
            "- Work the smaller `crawled - currently not indexed` post batch after template cleanup.",
        ]
    )
    (BASE_DIR / f"tokentopnews-analysis-summary-{DATE}.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
