#!/usr/bin/env python3
"""
GitHub Star History Tracker
Track and visualize the star history of any GitHub repository.

Usage:
    python star_history.py owner/repo
    python star_history.py owner/repo --format json
    python star_history.py repo1 repo2 repo3 --summary
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from collections import defaultdict

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def get_headers():
    headers = {
        "Accept": "application/vnd.github.star+json",
        "User-Agent": "github-star-history",
    }
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers


def check_rate_limit():
    resp = requests.get(f"{GITHUB_API}/rate_limit", headers=get_headers())
    if resp.status_code == 200:
        data = resp.json()
        remaining = data["rate"]["remaining"]
        reset_at = data["rate"]["reset"]
        return remaining, reset_at
    return 0, 0


def wait_for_rate_limit():
    remaining, reset_at = check_rate_limit()
    if remaining < 5:
        wait_seconds = max(reset_at - time.time(), 0) + 2
        print(f"  Rate limit low ({remaining} remaining). Waiting {int(wait_seconds)}s...")
        time.sleep(wait_seconds)


def fetch_star_history(repo):
    """Fetch complete star history with timestamps for a repository."""
    stars = []
    page = 1
    per_page = 100

    print(f"Fetching star history for {repo}...")

    while True:
        wait_for_rate_limit()

        url = f"{GITHUB_API}/repos/{repo}/stargazers"
        params = {"page": page, "per_page": per_page}
        resp = requests.get(url, headers=get_headers(), params=params)

        if resp.status_code == 404:
            print(f"  Repository not found: {repo}")
            return None
        elif resp.status_code == 403:
            print(f"  Access denied. Try setting GITHUB_TOKEN.")
            return None
        elif resp.status_code != 200:
            print(f"  API error: {resp.status_code}")
            return None

        data = resp.json()
        if not data:
            break

        for entry in data:
            starred_at = entry.get("starred_at", "")
            user = entry.get("user", {}).get("login", "unknown")
            stars.append({"user": user, "starred_at": starred_at})

        if len(data) < per_page:
            break

        page += 1
        if page % 10 == 0:
            print(f"  Fetched {len(stars)} stars so far (page {page})...")

    print(f"  Total: {len(stars)} stars")
    return stars


def analyze_stars(stars, repo):
    """Analyze star history and return summary statistics."""
    if not stars:
        return None

    dates = []
    for s in stars:
        try:
            dt = datetime.fromisoformat(s["starred_at"].replace("Z", "+00:00"))
            dates.append(dt)
        except (ValueError, KeyError):
            continue

    if not dates:
        return {"repo": repo, "total": len(stars), "error": "No valid timestamps"}

    dates.sort()
    now = datetime.now(timezone.utc)
    total = len(dates)
    first = dates[0]
    latest = dates[-1]
    age_days = (now - first).days or 1

    # Daily counts
    daily = defaultdict(int)
    for d in dates:
        daily[d.strftime("%Y-%m-%d")] += 1

    # Peak day
    peak_day = max(daily, key=daily.get)
    peak_count = daily[peak_day]

    # Recent growth
    def stars_since(days):
        cutoff = now - __import__("datetime").timedelta(days=days)
        return sum(1 for d in dates if d >= cutoff)

    last_7 = stars_since(7)
    last_30 = stars_since(30)
    last_365 = stars_since(365)

    return {
        "repo": repo,
        "total": total,
        "first_star": first.strftime("%Y-%m-%d"),
        "latest_star": latest.strftime("%Y-%m-%d"),
        "age_days": age_days,
        "avg_per_day": round(total / age_days, 1),
        "last_7_days": last_7,
        "last_30_days": last_30,
        "last_365_days": last_365,
        "peak_day": peak_day,
        "peak_count": peak_count,
        "daily": dict(daily),
    }


def print_summary(analysis):
    """Print a formatted summary of the star analysis."""
    if not analysis:
        return

    a = analysis
    print(f"\nRepository: {a['repo']}")
    print(f"Total stars: {a['total']:,}")
    print(f"Created: {a['first_star']}")

    years = a["age_days"] // 365
    months = (a["age_days"] % 365) // 30
    if years > 0:
        print(f"Age: {years} years, {months} months")
    else:
        print(f"Age: {months} months")

    print(f"\nGrowth summary:")
    if a["last_7_days"]:
        print(f"  Last 7 days:    +{a['last_7_days']:,} stars ({a['last_7_days']/7:.1f}/day)")
    if a["last_30_days"]:
        print(f"  Last 30 days:   +{a['last_30_days']:,} stars ({a['last_30_days']/30:.1f}/day)")
    if a["last_365_days"]:
        print(f"  Last 365 days:  +{a['last_365_days']:,} stars ({a['last_365_days']/365:.1f}/day)")
    print(f"  All time:       +{a['total']:,} stars ({a['avg_per_day']}/day)")
    print(f"\nPeak day: {a['peak_day']} (+{a['peak_count']:,} stars)")


def export_csv(stars, repo, filename=None):
    """Export star history to CSV."""
    if not filename:
        filename = repo.replace("/", "_") + "_stars.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user", "starred_at"])
        writer.writeheader()
        writer.writerows(stars)
    print(f"\nExported to {filename}")


def export_json(stars, analysis, repo, filename=None):
    """Export star history and analysis to JSON."""
    if not filename:
        filename = repo.replace("/", "_") + "_stars.json"
    output = {
        "repository": repo,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "summary": {k: v for k, v in analysis.items() if k != "daily"} if analysis else {},
        "stars": stars,
    }
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nExported to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Track the star history of any GitHub repository."
    )
    parser.add_argument(
        "repos",
        nargs="+",
        help="Repository in owner/repo format (e.g., torvalds/linux)",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Export format (default: csv)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary only, no file export",
    )
    args = parser.parse_args()

    if not TOKEN:
        remaining, _ = check_rate_limit()
        if remaining < 100:
            print("Tip: Set GITHUB_TOKEN for 5,000 requests/hour instead of 60.")
            print("  export GITHUB_TOKEN=ghp_your_token\n")

    for repo in args.repos:
        if "/" not in repo:
            print(f"Invalid format: {repo}. Use owner/repo.")
            continue

        stars = fetch_star_history(repo)
        if stars is None:
            continue

        analysis = analyze_stars(stars, repo)
        print_summary(analysis)

        if not args.summary and stars:
            if args.format == "json":
                export_json(stars, analysis, repo)
            else:
                export_csv(stars, repo)

        print()


if __name__ == "__main__":
    main()
