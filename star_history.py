#!/usr/bin/env python3
"""
GitHub Star History Tracker
Track the star history of any GitHub repository.

Uses GitHub's public star-history API, which returns privacy-safe daily and
weekly star counts (no stargazer identities). This is the successor to the
stargazers listing endpoint, which GitHub restricted to repository admins
and collaborators in June 2026.

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
from datetime import date, datetime, timedelta, timezone

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

GITHUB_API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
RATE_LIMIT_FLOOR = 5


def get_headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-star-history",
    }
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers


def check_rate_limit():
    resp = requests.get(f"{GITHUB_API}/rate_limit", headers=get_headers(), timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        remaining = data["rate"]["remaining"]
        reset_at = data["rate"]["reset"]
        return remaining, reset_at
    return 0, 0


def handle_rate_limit(resp):
    """Pause when the response reports the rate limit is nearly exhausted."""
    remaining = resp.headers.get("X-RateLimit-Remaining")
    reset_at = resp.headers.get("X-RateLimit-Reset")
    if remaining is not None and reset_at is not None and int(remaining) <= RATE_LIMIT_FLOOR:
        wait_seconds = max(int(reset_at) - time.time(), 0) + 2
        print(f"  Rate limit low ({remaining} remaining). Waiting {int(wait_seconds)}s...")
        time.sleep(wait_seconds)


def fetch_repo_info(repo):
    """Fetch repository metadata (creation date, star count). None if missing."""
    resp = requests.get(f"{GITHUB_API}/repos/{repo}", headers=get_headers(), timeout=30)
    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        return None
    return resp.json()


def fetch_star_history(repo):
    """Fetch daily star counts for a repository.

    Uses GitHub's public star-history endpoint, which returns weeks of
    aggregate daily counts (Sunday-start) without stargazer identities.
    Returns a list of {"date": "YYYY-MM-DD", "stars": int} sorted oldest
    first, or None if the repository is unavailable.
    """
    print(f"Fetching star history for {repo}...")

    history = []
    url = f"{GITHUB_API}/repos/{repo}/stargazers/history"
    params = {"per_page": 100}
    pages = 0
    today = datetime.now(timezone.utc).date()

    while url:
        resp = requests.get(url, headers=get_headers(), params=params, timeout=30)

        if resp.status_code == 404:
            print(f"  Repository not found: {repo}")
            return None
        if resp.status_code == 403:
            print("  Access denied. Try setting GITHUB_TOKEN.")
            return None
        if resp.status_code != 200:
            print(f"  API error: {resp.status_code}")
            return None

        for week in resp.json():
            start = datetime.fromtimestamp(week["week"], tz=timezone.utc).date()
            for offset, count in enumerate(week.get("days", [])):
                day = start + timedelta(days=offset)
                if day <= today:
                    history.append({"date": day.isoformat(), "stars": count})

        pages += 1
        if pages % 5 == 0:
            fetched = sum(e["stars"] for e in history)
            print(f"  Fetched {fetched:,} stars so far (page {pages})...")

        handle_rate_limit(resp)
        url = resp.links.get("next", {}).get("url")
        params = None

    history.sort(key=lambda entry: entry["date"])
    total = sum(entry["stars"] for entry in history)
    print(f"  Total: {total:,} stars ({pages} week pages)")
    return history


def analyze_stars(history, repo):
    """Analyze daily star counts and return summary statistics."""
    if not history:
        return None

    active = [entry for entry in history if entry["stars"] > 0]
    if not active:
        return {"repo": repo, "total": 0, "error": "No star activity found"}

    total = sum(entry["stars"] for entry in active)
    first = date.fromisoformat(active[0]["date"])
    latest = date.fromisoformat(active[-1]["date"])
    now = datetime.now(timezone.utc).date()
    age_days = max((now - first).days, 1)

    daily = {entry["date"]: entry["stars"] for entry in active}
    peak_day = max(daily, key=daily.get)
    peak_count = daily[peak_day]

    def stars_since(days):
        cutoff = now - timedelta(days=days)
        return sum(count for day, count in daily.items() if date.fromisoformat(day) >= cutoff)

    return {
        "repo": repo,
        "total": total,
        "first_star": first.isoformat(),
        "latest_star": latest.isoformat(),
        "age_days": age_days,
        "avg_per_day": round(total / age_days, 1),
        "last_7_days": stars_since(7),
        "last_30_days": stars_since(30),
        "last_365_days": stars_since(365),
        "peak_day": peak_day,
        "peak_count": peak_count,
        "daily": daily,
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
        print(f"Age: {years} years, {months} month{'s' if months != 1 else ''}")
    else:
        print(f"Age: {months} month{'s' if months != 1 else ''}")

    print(f"\nGrowth summary:")
    if a["last_7_days"]:
        print(f"  Last 7 days:    +{a['last_7_days']:,} stars ({a['last_7_days']/7:.1f}/day)")
    if a["last_30_days"]:
        print(f"  Last 30 days:   +{a['last_30_days']:,} stars ({a['last_30_days']/30:.1f}/day)")
    if a["last_365_days"]:
        print(f"  Last 365 days:  +{a['last_365_days']:,} stars ({a['last_365_days']/365:.1f}/day)")
    print(f"  All time:       +{a['total']:,} stars ({a['avg_per_day']}/day)")
    print(f"\nPeak day: {a['peak_day']} (+{a['peak_count']:,} stars)")


def export_csv(history, repo, filename=None):
    """Export the daily star history to CSV."""
    if not filename:
        filename = repo.replace("/", "_") + "_stars.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "stars"])
        writer.writeheader()
        writer.writerows(history)
    print(f"\nExported to {filename}")


def export_json(history, analysis, repo, filename=None):
    """Export the star history and analysis to JSON."""
    if not filename:
        filename = repo.replace("/", "_") + "_stars.json"
    output = {
        "repository": repo,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "summary": {k: v for k, v in analysis.items() if k != "daily"} if analysis else {},
        "history": history,
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

        history = fetch_star_history(repo)
        if history is None:
            continue

        analysis = analyze_stars(history, repo)
        print_summary(analysis)

        if not args.summary and history:
            if args.format == "json":
                export_json(history, analysis, repo)
            else:
                export_csv(history, repo)

        print()


if __name__ == "__main__":
    main()
