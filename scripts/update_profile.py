#!/usr/bin/env python3
"""Refresh generated repository and language sections in the profile README."""
import json
import os
import urllib.request
from pathlib import Path
from html import escape

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "gagan77007")
TOKEN = os.environ.get("GITHUB_TOKEN")
ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PER_PAGE = 100
MAX_REPOS = 6

def github_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-readme-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def replace_section(content, start, end, replacement):
    left = content.find(start)
    right = content.find(end)
    if left < 0 or right < left:
        raise RuntimeError(f"README markers missing: {start} / {end}")
    return content[:left + len(start)] + "\n" + replacement.strip() + "\n" + content[right:]

def main():
    repos = github_get(
        f"https://api.github.com/users/{USERNAME}/repos?type=owner&sort=updated&direction=desc&per_page={PER_PAGE}"
    )
    repos = [
        r for r in repos
        if not r.get("fork") and not r.get("archived") and not r.get("private")
    ]
    repos.sort(key=lambda r: r.get("pushed_at") or r.get("updated_at") or "", reverse=True)
    selected = repos[:MAX_REPOS]

    if selected:
        rows = [
            "| Repository | Description | Language | ⭐ Stars | Updated |",
            "|:--|:--|:--:|--:|:--|",
        ]
        for repo in selected:
            name = escape(repo["name"])
            url = repo["html_url"]
            desc = escape((repo.get("description") or "—").replace("|", "\\|"))
            language = escape(repo.get("language") or "—")
            stars = repo.get("stargazers_count", 0)
            pushed = (repo.get("pushed_at") or "")[:10] or "—"
            rows.append(f"| [{name}]({url}) | {desc} | {language} | {stars} | {pushed} |")
        repo_md = "\n".join(rows)
    else:
        repo_md = "_No public non-fork repositories found yet._"

    languages = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    if languages:
        ordered = sorted(languages.items(), key=lambda item: (-item[1], item[0]))
        lang_md = " · ".join(f"`{escape(name)}` ({count})" for name, count in ordered)
    else:
        lang_md = "_Languages will appear here when your public repositories contain detected languages._"

    content = README.read_text(encoding="utf-8")
    content = replace_section(content, "<!-- REPO-LIST:START -->", "<!-- REPO-LIST:END -->", repo_md)
    content = replace_section(content, "<!-- LANGUAGES:START -->", "<!-- LANGUAGES:END -->", lang_md)
    README.write_text(content, encoding="utf-8")
    print(f"Updated README for {USERNAME}: {len(selected)} repositories, {len(languages)} languages.")

if __name__ == "__main__":
    main()
