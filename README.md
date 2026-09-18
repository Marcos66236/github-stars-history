<p align="center">
  <img src="assets/banner.svg" alt="GitHub Stars History — star growth analytics for any repository" width="720">
</p>

<p align="center">
  <a href="https://buygithub.com/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">
    <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=22&duration=3000&pause=1500&color=F97316&center=true&vCenter=true&width=500&lines=GitHub+Stars+%C2%B7+Followers+%C2%B7+Forks;Aged+Accounts+%C2%B7+Search+Ranking;buygithub.com+%E2%80%93+Real+Engagement" alt="buygithub.com services">
  </a>
</p>

<p align="center">
  <a href="https://buygithub.com/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history"><b>buygithub.com</b></a> · <a href="https://buygithub.com/product/stars/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">How We Deliver Stars</a> · <a href="https://buygithub.com/blog/how-github-stars-work/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">Blog</a>
</p>

<p align="center">
  <a href="https://github.com/Marcos66236/github-stars-history/stargazers"><img src="https://img.shields.io/github/stars/Marcos66236/github-stars-history?style=flat&color=f97316" alt="GitHub stars"></a>
  <a href="https://github.com/Marcos66236/github-stars-history/network/members"><img src="https://img.shields.io/github/forks/Marcos66236/github-stars-history?style=flat&color=22d3ee" alt="Forks"></a>
  <a href="https://github.com/Marcos66236/github-stars-history/releases"><img src="https://img.shields.io/github/v/release/Marcos66236/github-stars-history?style=flat&color=34d399" alt="Release"></a>
  <a href="https://github.com/Marcos66236/github-stars-history/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Marcos66236/github-stars-history?style=flat&color=34d399" alt="MIT license"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8+-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.8+"></a>
  <a href="https://docs.github.com/en/rest/activity/starring"><img src="https://img.shields.io/badge/GitHub%20API-star--history-22c55e?style=flat" alt="Uses the GitHub star history API"></a>
  <a href="#faq"><img src="https://img.shields.io/badge/API%20key-not%20required-34d399?style=flat" alt="No API key required"></a>
</p>

<p align="center">
  Track the star history of <b>any</b> public GitHub repository.<br>
  Daily and weekly growth, peak detection, multi-repo comparison, CSV and JSON export.
</p>

<p align="center">
  <a href="https://buygithub.com/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history"><b>buygithub.com</b></a> · <a href="https://buygithub.com/blog/how-github-stars-work/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">How GitHub Stars Work</a>
</p>

---

## Why star history matters

GitHub uses star velocity as a core signal for its **Trending** page, **Explore** feed, and **search ranking**. A repository gaining 200 stars in 24 hours is more likely to surface than one with 10,000 total stars and flat recent growth.

This tool gives you that data: how many stars a repository gained each day, across its entire life. Compare your project against competitors, measure a launch, verify whether a star spike was earned or delivered, or track your own growth week by week.

## What changed in 2026

Until June 2026, tools like this one read the stargazers listing endpoint to reconstruct per-star timestamps. GitHub then [restricted stargazer and watcher lists](https://github.blog/changelog/2026-06-30-upcoming-access-restrictions-to-public-api-endpoints-and-ui-views) to repository admins and collaborators to protect user privacy — breaking most star-history tools in the ecosystem.

In September 2026, GitHub shipped the fix: a [privacy-safe star history endpoint](https://github.blog/changelog/2026-09-04-new-api-endpoint-provides-privacy-safe-star-history-data) that returns weekly and daily aggregate counts with no stargazer identities. **Version 1.1.0 of this tool migrated to that endpoint.** It works for any public repository again, with no ownership or special access required.

## Features

| Feature | Description |
|---------|-------------|
| **Complete daily history** | Daily star counts from the repository's first star to today |
| **Growth windows** | 7-day, 30-day, 365-day and all-time rates |
| **Peak detection** | The single best day and its exact count |
| **Multi-repo comparison** | Pass any number of repositories and compare their curves |
| **Velocity report** | 30-day view with terminal bar chart (`examples/velocity_report.py`) |
| **CSV + JSON export** | Machine-readable daily series for charting or analysis |
| **Rate-limit aware** | Header-based backoff — no wasted probe requests |
| **No API key needed** | Public data for public repositories; a token only raises rate limits |

## Quick start

```bash
git clone https://github.com/Marcos66236/github-stars-history.git
cd github-stars-history
pip install -r requirements.txt
python star_history.py sindresorhus/np
```

Or install it as a command-line tool:

```bash
pip install git+https://github.com/Marcos66236/github-stars-history.git
star-history owner/repo
```

No token, no signup, no configuration. Works with Python 3.8+.

## Usage

### Single repository

```bash
python star_history.py sindresorhus/np
```

```
Fetching star history for sindresorhus/np...
  Fetched 2,227 stars so far (page 10)...
  Total: 7,712 stars (20 week pages)

Repository: sindresorhus/np
Total stars: 7,712
Created: 2015-08-16
Age: 11 years, 1 month

Growth summary:
  Last 30 days:   +5 stars (0.2/day)
  Last 365 days:  +117 stars (0.3/day)
  All time:       +7,712 stars (1.9/day)

Peak day: 2016-07-07 (+373 stars)
```

### Compare multiple repositories

```bash
python star_history.py facebook/react vuejs/vue sveltejs/svelte
```

### Velocity report

```bash
python examples/velocity_report.py sindresorhus/np
```

Shows the last 30 days of star gains as a terminal bar chart.

### Export formats

```bash
python star_history.py owner/repo --format csv    # daily series (default)
python star_history.py owner/repo --format json   # history + full analysis
python star_history.py owner/repo --summary       # print only, no files
```

CSV output is one row per day: `date,stars`. JSON output adds the full analysis block and metadata.

### GitHub token (optional)

Without a token you get 60 requests/hour; with a token, 5,000. Large repositories need a handful of requests per decade of history, so most users never hit the limit.

```bash
export GITHUB_TOKEN=ghp_your_token_here
python star_history.py torvalds/linux
```

Generate one at [github.com/settings/tokens](https://github.com/settings/tokens) — no special scopes are required for public repositories.

## How it works

```
GET /repos/{owner}/{repo}/stargazers/history
```

The endpoint returns weeks of aggregate daily counts, newest first, paginated backwards to the repository's creation week. The tool reconstructs a single daily series, computes growth windows, and stores nothing.

```
[
  { "week": 1789257600, "total": 126, "days": [0, 0, 0, 0, 104, 22, 0] },
  ...
]
```

Two deliberate design decisions:

- **Daily aggregates, not identities.** GitHub no longer exposes who starred a repository to third parties — and this tool never needed that to measure growth. Counts are enough for velocity, peaks and comparisons.
- **Header-based rate limiting.** Remaining quota is read from every API response instead of probed with extra requests, so a long history costs exactly as many requests as it has pages.

## FAQ

**Does this work for any repository?**
Yes — any public repository, whether you own it or not. Private repositories require a token with access.

**Why does the output show daily counts instead of usernames?**
GitHub restricted stargazer identities to repository admins in June 2026. The public star history endpoint returns aggregate counts only, which is what growth analysis actually uses.

**How far back does the history go?**
To the repository's creation week. The tool paginates through every week automatically.

**Can I see who starred a repository?**
Not through this tool. If it is your repository, GitHub's UI and API still give you full stargazer access. For anyone else's, that data is no longer public.

**How do I detect a suspicious star spike?**
Plot the daily series and look for vertical jumps with no external explanation — a launch, a release, a viral post. Our companion guide covers the checks: [How to tell if GitHub stars are real](https://buygithub.com/how-to-tell-if-github-stars-are-real/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history).

**Do I need Python?**
For this CLI, yes. The raw endpoint is plain HTTP and works from any language — see *How it works* above.

## Project structure

```
github-stars-history/
├── star_history.py            Main tool (fetch, analyze, export)
├── setup.py                   Package configuration
├── requirements.txt           Dependencies (requests only)
├── examples/
│   ├── compare_frameworks.py  Compare frontend frameworks
│   └── velocity_report.py     30-day velocity chart
├── tests/
│   └── test_star_history.py   Unit tests
├── sample-output.json         Example JSON export
├── CHANGELOG.md               Version history
├── CONTRIBUTING.md            Contribution guidelines
└── LICENSE                    MIT
```

## Running tests

```bash
python -m pytest tests/
# or
python -m unittest tests/test_star_history.py
```

## Requirements

- Python 3.8+
- [`requests`](https://pypi.org/project/requests/)

## Related tools

- [github-ranking-audit](https://github.com/nMaas8388/github-ranking-audit) — scores a repository's GitHub search ranking signals
- [github-launch-checklist](https://github.com/repoboost-hq/github-launch-checklist) — the ten checks a repository should pass before launch

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests are welcome.

## License

MIT. See [LICENSE](LICENSE).

---

<p align="center"><b>Related resources from <a href="https://buygithub.com/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">buygithub.com</a></b></p>

<p align="center">
  <a href="https://buygithub.com/buy-github-stars/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">GitHub Stars Service</a> · 
  <a href="https://buygithub.com/buy-github-followers/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">GitHub Followers</a> · 
  <a href="https://buygithub.com/github-search-ranking/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">Search Ranking</a> · 
  <a href="https://buygithub.com/old-github-accounts/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">Aged Accounts</a> · 
  <a href="https://buygithub.com/blog/how-github-stars-work/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">Blog</a>
</p>
