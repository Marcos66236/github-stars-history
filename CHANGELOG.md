# Changelog

## 1.1.0 (2026-09-19)

- **Migrated to GitHub's public star history API** (`/repos/{repo}/stargazers/history`) after the June 2026 access restrictions limited the stargazers listing to repository admins and collaborators — the tool works for any public repository again, with no ownership required
- Star history is now reconstructed as a complete daily series from weekly aggregate counts (no stargazer identities involved)
- CSV export format changed to `date,stars`; JSON export carries a `history` array instead of per-star entries
- Rate limiting is header-based: quota is read from each API response instead of extra probe requests
- Multi-page progress reporting during long histories
- Test suite updated for the new pipeline (week-to-day transformation, pagination, exports)

## 1.0.0 (2026-09-16)

- Initial release
- Full star history with timestamps via GitHub API
- Growth analysis: daily, weekly, monthly, yearly rates
- Peak day detection
- Multi-repo comparison
- CSV and JSON export
- Rate-limit handling with automatic backoff
- GitHub token support for higher rate limits
- Examples: framework comparison, velocity report
- Unit tests
