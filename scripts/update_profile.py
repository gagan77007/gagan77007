
import json
import os
import re
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "gagan77007")
TOKEN = os.environ.get("GITHUB_TOKEN")

README = Path(__file__).resolve().parents[1] / "README.md"
MAX_REPOS = 8


def github_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def replace_section(text, start, end, replacement):
    left = text.find(start)
    right = text.find(end)

    if left == -1 or right == -1 or right < left:
        raise ValueError("README update markers are missing.")

    return (
        text[:left + len(start)]
        + "\n"
        + replacement.strip()
        + "\n"
        + text[right:]
    )


def get_repositories():
    repos = github_get(
        f"https://api.github.com/users/{USERNAME}/repos"
        "?type=owner&sort=updated&direction=desc&per_page=100"
    )

    repos = [
        repo for repo in repos
        if not repo.get("private")
        and not repo.get("fork")
        and not repo.get("archived")
    ]

    repos.sort(
        key=lambda r: r.get("pushed_at") or r.get("updated_at") or "",
        reverse=True
    )

    return repos


def make_repository_table(repos):
    lines = [
        "| Repository | Description | Language | ⭐ Stars | Updated |",
        "|:--|:--|:--:|--:|:--|"
    ]

    for repo in repos[:MAX_REPOS]:
        name = str(repo.get("name", "Project")).replace("|", "\\|")
        url = repo.get("html_url", "")
        description = (
            repo.get("description") or "A project from my GitHub profile."
        )
        description = re.sub(r"\s+", " ", description).replace("|", "\\|")

        language = repo.get("language") or "—"
        stars = repo.get("stargazers_count", 0)
        updated = (
            repo.get("pushed_at") or repo.get("updated_at") or ""
        )[:10]

        lines.append(
            f"| [{name}]({url}) | {description} | "
            f"{language} | {stars} | {updated} |"
        )

    if not repos:
        lines.append("| No public repositories found. | | | | |")

    return "\n".join(lines)


def make_language_badges(repos):
    totals = {}

    for repo in repos:
        try:
            languages = github_get(repo["languages_url"])
        except Exception as error:
            print("Could not read languages:", error)
            continue

        for language, size in languages.items():
            totals[language] = totals.get(language, 0) + size

    total = sum(totals.values())

    if total == 0:
        return "_No language information available yet._"

    badges = []

    for language, size in sorted(
        totals.items(), key=lambda item: item[1], reverse=True
    ):
        percentage = size / total * 100

        safe_name = (
            language.replace("#", "sharp")
            .replace("+", "plus")
            .replace(" ", "")
        )

        badges.append(
            f'<img src="https://img.shields.io/badge/'
            f'{safe_name}-{percentage:.1f}%25-172554?style=for-the-badge" '
            f'alt="{language} {percentage:.1f}%"/>'
        )

    return "\n".join(badges)


def main():
    repos = get_repositories()

    content = README.read_text(encoding="utf-8")

    content = replace_section(
        content,
        "<!-- REPO-LIST:START -->",
        "<!-- REPO-LIST:END -->",
        make_repository_table(repos)
    )

    content = replace_section(
        content,
        "<!-- LANGUAGES:START -->",
        "<!-- LANGUAGES:END -->",
        make_language_badges(repos)
    )

    README.write_text(content, encoding="utf-8")

    print("Profile README updated successfully!")


if __name__ == "__main__":
    main()
