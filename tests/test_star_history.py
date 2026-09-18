"""Tests for star_history module."""

import json
import os
import sys
import unittest
from datetime import date, datetime, timedelta, timezone
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from star_history import (
    analyze_stars,
    export_csv,
    export_json,
    fetch_star_history,
)


def week_ts(year, month, day):
    """Unix timestamp for a UTC midnight (used as a week bucket key)."""
    return int(datetime(year, month, day, tzinfo=timezone.utc).timestamp())


class FakeResponse:
    def __init__(self, payload, status_code=200, links=None):
        self._payload = payload
        self.status_code = status_code
        self.links = links or {}
        self.headers = {
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Reset": "9999999999",
        }

    def json(self):
        return self._payload


class TestFetchStarHistory(unittest.TestCase):
    def test_transforms_weeks_to_daily_series(self):
        # Week of Sunday 2026-09-06 with three active days.
        week = {
            "week": week_ts(2026, 9, 6),
            "total": 6,
            "days": [1, 0, 2, 0, 0, 0, 3],
        }
        with patch("star_history.requests.get", return_value=FakeResponse([week])):
            history = fetch_star_history("owner/repo")

        by_date = {entry["date"]: entry["stars"] for entry in history}
        self.assertEqual(by_date["2026-09-06"], 1)
        self.assertEqual(by_date["2026-09-08"], 2)
        self.assertEqual(by_date["2026-09-12"], 3)
        self.assertEqual(sum(by_date.values()), 6)
        # Full week is included, including zero days.
        self.assertEqual(len(history), 7)
        # Sorted oldest first.
        self.assertEqual(history[0]["date"], "2026-09-06")

    def test_follows_pagination_links(self):
        page_one = [{"week": week_ts(2026, 9, 6), "total": 1, "days": [1, 0, 0, 0, 0, 0, 0]}]
        page_two = [{"week": week_ts(2026, 8, 30), "total": 2, "days": [0, 0, 0, 0, 0, 0, 2]}]
        responses = [
            FakeResponse(page_one, links={"next": {"url": "https://api.github.com/next-page"}}),
            FakeResponse(page_two),
        ]
        with patch("star_history.requests.get", side_effect=responses) as mocked:
            history = fetch_star_history("owner/repo")

        self.assertEqual(mocked.call_count, 2)
        self.assertEqual(sum(entry["stars"] for entry in history), 3)
        # Oldest first across pages.
        self.assertEqual(history[0]["date"], "2026-08-30")

    def test_repository_not_found(self):
        with patch("star_history.requests.get", return_value=FakeResponse({}, status_code=404)):
            self.assertIsNone(fetch_star_history("owner/missing"))


class TestAnalyzeStars(unittest.TestCase):
    def test_empty_input(self):
        self.assertIsNone(analyze_stars([], "test/repo"))

    def test_no_activity(self):
        history = [{"date": "2026-01-01", "stars": 0}]
        result = analyze_stars(history, "test/repo")
        self.assertIn("error", result)
        self.assertEqual(result["total"], 0)

    def test_basic_totals_and_peak(self):
        today = datetime.now(timezone.utc).date()
        history = [
            {"date": (today - timedelta(days=10)).isoformat(), "stars": 1},
            {"date": (today - timedelta(days=5)).isoformat(), "stars": 2},
            {"date": (today - timedelta(days=2)).isoformat(), "stars": 3},
        ]
        result = analyze_stars(history, "test/repo")
        self.assertEqual(result["total"], 6)
        self.assertEqual(result["first_star"], (today - timedelta(days=10)).isoformat())
        self.assertEqual(result["latest_star"], (today - timedelta(days=2)).isoformat())
        self.assertEqual(result["last_7_days"], 5)
        self.assertEqual(result["last_30_days"], 6)
        self.assertEqual(result["peak_day"], (today - timedelta(days=2)).isoformat())
        self.assertEqual(result["peak_count"], 3)


class TestExports(unittest.TestCase):
    def setUp(self):
        self.history = [
            {"date": "2026-09-06", "stars": 1},
            {"date": "2026-09-07", "stars": 0},
        ]
        self.analysis = analyze_stars(self.history, "owner/repo")

    def test_export_csv(self):
        path = os.path.join(os.path.dirname(__file__), "_tmp_export.csv")
        try:
            export_csv(self.history, "owner/repo", filename=path)
            with open(path) as f:
                lines = f.read().strip().splitlines()
            self.assertEqual(lines[0], "date,stars")
            self.assertEqual(lines[1], "2026-09-06,1")
            self.assertEqual(len(lines), 3)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_export_json(self):
        path = os.path.join(os.path.dirname(__file__), "_tmp_export.json")
        try:
            export_json(self.history, self.analysis, "owner/repo", filename=path)
            with open(path) as f:
                data = json.load(f)
            self.assertEqual(data["repository"], "owner/repo")
            self.assertIn("summary", data)
            self.assertIn("history", data)
            self.assertEqual(len(data["history"]), 2)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
