"""Tests for star_history module."""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from star_history import analyze_stars


class TestAnalyzeStars(unittest.TestCase):
    def test_empty_input(self):
        result = analyze_stars([], "test/repo")
        self.assertIsNone(result)

    def test_basic_analysis(self):
        stars = [
            {"user": "alice", "starred_at": "2026-01-01T10:00:00Z"},
            {"user": "bob", "starred_at": "2026-01-02T14:30:00Z"},
            {"user": "carol", "starred_at": "2026-01-03T09:15:00Z"},
        ]
        result = analyze_stars(stars, "test/repo")
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["first_star"], "2026-01-01")
        self.assertEqual(result["repo"], "test/repo")

    def test_peak_detection(self):
        stars = [
            {"user": f"user{i}", "starred_at": "2026-06-15T10:00:00Z"}
            for i in range(50)
        ] + [
            {"user": f"other{i}", "starred_at": "2026-06-16T10:00:00Z"}
            for i in range(10)
        ]
        result = analyze_stars(stars, "test/repo")
        self.assertEqual(result["peak_day"], "2026-06-15")
        self.assertEqual(result["peak_count"], 50)

    def test_invalid_timestamps(self):
        stars = [
            {"user": "alice", "starred_at": "invalid"},
            {"user": "bob", "starred_at": "also-invalid"},
        ]
        result = analyze_stars(stars, "test/repo")
        self.assertIsNotNone(result)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
