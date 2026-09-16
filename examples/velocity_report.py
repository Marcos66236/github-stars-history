#!/usr/bin/env python3
"""
Analyze star velocity for a repository.
Shows daily star gain over the last 30 days to identify trending patterns.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from star_history import fetch_star_history, analyze_stars


def velocity_report(repo):
    stars = fetch_star_history(repo)
    if not stars:
        return

    analysis = analyze_stars(stars, repo)
    if not analysis:
        return

    daily = analysis.get("daily", {})
    sorted_days = sorted(daily.items(), reverse=True)[:30]

    print(f"\nVelocity report for {repo}")
    print(f"{'Date':<14} {'Stars':>6} {'Bar'}")
    print("-" * 50)

    max_count = max(v for _, v in sorted_days) if sorted_days else 1
    for date, count in sorted_days:
        bar_len = int((count / max_count) * 30)
        bar = "█" * bar_len
        print(f"{date:<14} {count:>6} {bar}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python velocity_report.py owner/repo")
        sys.exit(1)
    velocity_report(sys.argv[1])
