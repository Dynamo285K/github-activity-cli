# GitHub Activity CLI

A simple command-line tool that fetches and displays the recent public activity of a GitHub user.


## Example

$ ./github-activity-cli.py Dynamo285K --limit 3
- [30.09.2026 18:39] Pushed to main in Dynamo285K/task-tracker
- [30.09.2026 18:39] Merged pull request #1 in Dynamo285K/task-tracker
- [30.09.2026 18:39] Opened pull request #1 in Dynamo285K/task-tracker

## Requirements

- Python 3.9+
- [requests](https://pypi.org/project/requests/)

## Installation

git clone https://github.com/Dynamo285K/github-activity-cli.git
cd github-activity-cli
python3 -m pip install requests
chmod +x github-activity-cli.py

## Usage

./github-activity-cli.py <username> [--limit N]

| Argument   | Description                         | Default |
|------------|-------------------------------------|---------|
| `username` | GitHub username                     | required |
| `--limit`  | Number of events to show (1–100)    | 10      |

## Supported events

- PushEvent: pushes to a branch
- CreateEvent: new branches, tags and repositories
- PullRequestEvent: opened, merged, closed and updated pull requests
- Other event types are shown in a generic format.

## Error handling

- Non-existent user (404)
- API rate limit exceeded (403 / 429)
- Network errors and timeouts
- Invalid `--limit` values
- Users with no recent activity

## Development

Lint, format and syntax-check the code:

./check.sh

Requires [ruff](https://docs.astral.sh/ruff/).

## Known limitations

- The GitHub Events API no longer includes commit counts in PushEvent payloads, so pushes are shown without the number of commits.
- Unauthenticated requests are limited to 60 per hour.