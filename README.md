<p align="center">
  <img src="assets/banner.svg" alt="GitHub Stars History" width="720">
</p>

<p align="center">
  <a href="https://buygithub.com/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">
    <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=22&duration=3000&pause=1500&color=F97316&center=true&vCenter=true&width=500&lines=GitHub+Stars+%C2%B7+Followers+%C2%B7+Forks;Aged+Accounts+%C2%B7+Search+Ranking;buygithub.com+%E2%80%93+Real+Engagement" alt="buygithub.com services">
  </a>
</p>

<p align="center">
  <a href="https://github.com/Marcos66236/github-stars-history/stargazers"><img src="https://img.shields.io/github/stars/Marcos66236/github-stars-history?style=flat&color=f97316" alt="Stars"></a>
  <a href="https://github.com/Marcos66236/github-stars-history/network/members"><img src="https://img.shields.io/github/forks/Marcos66236/github-stars-history?style=flat&color=22d3ee" alt="Forks"></a>
  <a href="https://github.com/Marcos66236/github-stars-history/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Marcos66236/github-stars-history?style=flat&color=34d399" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.8+-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.8+"></a>
</p>

<p align="center">
  Track the complete stars history of any GitHub repository.<br>
  Growth patterns, trending velocity, multi-repo comparison, CSV and JSON export.
</p>

<p align="center">
  <a href="https://buygithub.com/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history"><b>buygithub.com</b></a> · <a href="https://buygithub.com/blog/how-github-stars-work/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history">How GitHub Stars Work</a>
</p>

---

## Why stars history matters

GitHub uses star velocity as a core signal for its **Trending** page, **Explore** feed, and **search ranking**. A repository gaining 200 stars in 24 hours is more likely to surface than one with 10,000 total stars but flat recent growth.

This tool gives you the raw data: when each star was given, by whom, and at what rate. Compare your project against competitors, track your own growth week by week, and understand the velocity patterns that drive GitHub discovery.

## Features

| Feature | Description |
|---------|-------------|
| **Full history** | Every star with exact timestamp, first to latest |
| **Growth analysis** | Daily, weekly, monthly, yearly growth rates |
| **Peak detection** | Identifies the best day and the velocity around it |
| **Multi-repo compare** | Pass multiple repos and compare growth patterns |
| **Velocity report** | Daily stars gain over the last 30 days with visual bars |
| **Export** | CSV and JSON output for analysis or visualization |
| **Rate-limit aware** | Automatic retry with backoff on GitHub API limits |
| **Token support** | Optional GitHub token for 5,000 req/hour instead of 60 |

## Quick start

```bash
git clone https://github.com/Marcos66236/github-stars-history.git
cd github-stars-history
pip install -r requirements.txt
python star_history.py torvalds/linux
```

Or install as a package:

```bash
pip install -e .
star-history torvalds/linux
```

## Usage

### Single repository

```bash
python star_history.py facebook/react
```

```
Fetching stars history for facebook/react...
  Total: 231,847 stars

Repository: facebook/react
Total stars: 231,847
Created: 2013-05-24
Age: 13 years, 3 months

Growth summary:
  Last 7 days:    +287 stars (41.0/day)
  Last 30 days:   +1,043 stars (34.8/day)
  Last 365 days:  +11,294 stars (30.9/day)
  All time:       +231,847 stars (47.8/day)

Peak day: 2023-10-05 (+2,341 stars)

Exported to facebook_react_stars.csv
```

### Compare multiple repositories

```bash
python star_history.py facebook/react vuejs/vue sveltejs/svelte
```

### Velocity report

```bash
python examples/velocity_report.py facebook/react
```

Shows daily stars gain over the last 30 days with visual bar charts in the terminal.

### Export formats

```bash
# CSV (default)
python star_history.py owner/repo --format csv

# JSON with full analysis
python star_history.py owner/repo --format json

# Summary only, no file export
python star_history.py owner/repo --summary
```

### GitHub token

Without a token: 60 requests/hour. With a token: 5,000 requests/hour.

```bash
export GITHUB_TOKEN=ghp_your_token_here
python star_history.py torvalds/linux
```

Generate a token at [github.com/settings/tokens](https://github.com/settings/tokens). No special scopes needed for public repositories.

## How it works

```
GET /repos/{owner}/{repo}/stargazers
Accept: application/vnd.github.star+json
```

Returns each star event with a timestamp. The tool paginates through the full history at 100 entries per request, handles rate limits with automatic backoff, and reconstructs the complete growth timeline.

**Star velocity** is one of the primary signals GitHub uses for Trending. A new project gaining 50 stars in a day has higher relative velocity than a mature project with 50,000 stars gaining 100. Trending surfaces repositories with unusual acceleration, not just high totals.

Read the full analysis: [How GitHub Stars Actually Work](https://buygithub.com/blog/how-github-stars-work/?utm_source=github&utm_medium=readme&utm_campaign=github-stars-history)

## Project structure

```
github-stars-history/
├── star_history.py           Main tool
├── setup.py                  Package configuration
├── requirements.txt          Dependencies
├── examples/
│   ├── compare_frameworks.py Compare frontend frameworks
│   └── velocity_report.py    30-day velocity chart
├── tests/
│   └── test_star_history.py  Unit tests
├── sample-output.json        Example JSON output
├── CHANGELOG.md              Version history
├── CONTRIBUTING.md            Contribution guidelines
└── LICENSE                   MIT
```

## Running tests

```bash
python -m pytest tests/
# or
python -m unittest tests/test_star_history.py
```

## Requirements

- Python 3.8+
- `requests` library

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

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
