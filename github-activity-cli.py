#!/usr/bin/env python3


import argparse
import sys
from datetime import datetime

import requests

ACTIONS = {
    "synchronize": "Updated",
    "review_requested": "Requested review on",
}

ERRORS = {
    404: "User not found",
    403: "Rate limit exceeded. Try again later.",
    429: "Too many requests. Try again later.",
}

HEADERS = {"User-Agent": "github-activity-cli", "Accept": "application/vnd.github+json"}


class GitHubError(Exception):
    """Raised when fetching data from GitHub fails."""


def fetch_events(username, limit):
    url = f"https://api.github.com/users/{username}/events"

    try:
        response = requests.get(
            url, headers=HEADERS, params={"per_page": limit}, timeout=10
        )
    except requests.exceptions.RequestException as e:
        raise GitHubError(f"Network error: {e}")

    if response.status_code != 200:
        raise GitHubError(
            ERRORS.get(
                response.status_code, f"Github API Error: {response.status_code}"
            )
        )

    return response.json()


def format_time(iso_string):
    dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
    return dt.astimezone().strftime("%d.%m.%Y %H:%M")


def format_event(event):
    event_type = event["type"]
    repo = event["repo"]["name"]
    payload = event["payload"]

    if event_type == "PushEvent":
        branch = payload["ref"].removeprefix("refs/heads/")
        return f"Pushed to {branch} in {repo}"

    elif event_type == "CreateEvent":
        ref = payload.get("ref")
        if ref is not None:
            return f"Created {payload['ref_type']} {ref} in {repo}"
        else:
            return f"Created {payload['ref_type']} {repo}"

    elif event_type == "PullRequestEvent":
        action = payload["action"]
        pr = payload.get("pull_request", {})
        if action == "closed" and pr.get("merged"):
            action = "merged"
        verb = ACTIONS.get(action, action.capitalize())

        return f"{verb} pull request #{payload['number']} in {repo}"

    else:
        return f"{event_type} in {repo}"


def positive_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a number")
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError("limit must be between 1 and 100")
    return number


def main():
    parser = argparse.ArgumentParser(
        description="Show recent Github activity of a user"
    )

    parser.add_argument("username", type=str, help="Enter github username")
    parser.add_argument(
        "--limit", type=positive_int, default=10, help="Number of events 1-100"
    )

    args = parser.parse_args()

    username = args.username.strip()

    try:
        events = fetch_events(username, args.limit)
    except GitHubError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if not events:
        print(f"No recent activity for '{username}'.")
        sys.exit(0)

    for event in events:
        when = format_time(event["created_at"])
        print(f"- [{when}] {format_event(event)}")


if __name__ == "__main__":
    main()
