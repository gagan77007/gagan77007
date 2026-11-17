import json
import html
import os
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

USERNAME = "gagan77007"

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
README = ROOT / "README.md"

ASSETS.mkdir(exist_ok=True)

TOKEN = os.getenv("GITHUB_TOKEN", "")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": USERNAME
}

if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def api(url):
    request = urllib.request.Request(
        url,
        headers=HEADERS
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def safe(value):
    return html.escape(str(value or ""), quote=True)


def svg_start(height):
    return f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="1000" height="{height}"
    viewBox="0 0 1000 {height}">

    <defs>

      <linearGradient id="neon" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#00F5FF"/>
        <stop offset="50%" stop-color="#4263EB"/>
        <stop offset="100%" stop-color="#D946EF"/>
      </linearGradient>

      <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#00F5FF"/>
        <stop offset="100%" stop-color="#D946EF"/>
      </linearGradient>

      <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#10172C"/>
        <stop offset="100%" stop-color="#030713"/>
      </linearGradient>

      <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="2.5" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>

    </defs>

    <rect width="1000" height="{height}" fill="#030713"/>
    '''


def panel(x, y, width, height, radius=15):
    return f'''
    <rect x="{x}" y="{y}"
      width="{width}" height="{height}"
      rx="{radius}"
      fill="url(#panel)"
      stroke="url(#neon)"
      stroke-width="1.5"/>
    '''


def label(x, y, value, size=15, color="#EAFBFF", weight="normal"):
    return f'''
    <text x="{x}" y="{y}"
      fill="{color}"
      font-size="{size}"
      font-weight="{weight}"
      font-family="Arial, sans-serif">
      {safe(value)}
    </text>
    '''


def save(name, content):
    path = ASSETS / name
    path.write_text(content + "\n</svg>", encoding="utf-8")
    print("Generated:", name)


def update_readme(start, end, replacement):
    content = README.read_text(encoding="utf-8")

    first = content.find(start)
    last = content.find(end)

    if first == -1 or last == -1 or last < first:
        raise ValueError(f"Missing README markers: {start}")

    last += len(end)

    content = content[:first] + replacement + content[last:]

    README.write_text(content, encoding="utf-8")


# ------------------------------------------
# HEADER
# ------------------------------------------

def create_header():

    content = svg_start(230)

    content += label(
        500, 35,
        "// DEVELOP • BUILD • INNOVATE",
        14, "#91DFFF"
    ).replace(
        '<text x="500"',
        '<text text-anchor="middle" x="500"',
        1
    )

    content += '''
    <path d="M170 65 H215 M170 65 V115 M830 65 H785 M830 65 V115"
      fill="none" stroke="url(#neon)" stroke-width="3"
      filter="url(#glow)"/>

    <text x="500" y="125"
      text-anchor="middle"
      font-size="65"
      font-weight="bold"
      font-family="Arial"
      fill="url(#title)"
      filter="url(#glow)">
      GAGAN REDDY
    </text>

    <text x="500" y="165"
      text-anchor="middle"
      font-size="20"
      letter-spacing="6"
      fill="#00F5FF"
      font-family="Arial">
      DEVELOPER
    </text>
    '''

    content += label(
        500, 205,
        "BUILDING IDEAS INTO REALITY  •  LEARNING EVERY DAY",
        13, "#B8C8E6"
    ).replace(
        '<text x="500"',
        '<text text-anchor="middle" x="500"',
        1
    )

    save("header.svg", content)


# ------------------------------------------
# PROFILE
# ------------------------------------------

def create_profile(user, repos):

    stars = sum(r["stargazers_count"] for r in repos)

    content = svg_start(235)

    content += panel(20, 10, 960, 215)

    content += label(65, 60, "ABOUT ME", 21, "#00F5FF", "bold")

    bio = user.get("bio") or "Developer • Technology enthusiast"

    content += label(65, 95, bio[:65], 15)

    content += label(
        65, 135,
        "Learning • Building • Creating",
        14, "#B8C8E6"
    )

    content += label(
        65, 175,
        "GITHUB.COM/GAGAN77007",
        13, "#A78BFA"
    )

    stats = [
        ("REPOSITORIES", user.get("public_repos", 0)),
        ("STARS", stars),
        ("FOLLOWERS", user.get("followers", 0)),
        ("FOLLOWING", user.get("following", 0))
    ]

    for i, (name, value) in enumerate(stats):

        x = 370 + i * 145

        content += panel(x, 55, 130, 120, 12)

        content += label(
            x + 65, 110, value, 25, "#00F5FF", "bold"
        ).replace(
            '<text x=',
            '<text text-anchor="middle" x=',
            1
        )

        content += label(
            x + 65, 145, name, 10, "#B8C8E6"
        ).replace(
            '<text x=',
            '<text text-anchor="middle" x=',
            1
        )

    save("profile.svg", content)


# ------------------------------------------
# TECHNOLOGY PANEL
# ------------------------------------------

def create_technology():

    content = svg_start(150)

    content += panel(20, 10, 960, 130)

    content += label(
        500, 42,
        "✦  TECHNOLOGIES I USE",
        20, "#00F5FF", "bold"
    ).replace(
        '<text x="500"',
        '<text text-anchor="middle" x="500"',
        1
    )

    skills = [
        "PYTHON", "JAVA", "JAVASCRIPT",
        "TYPESCRIPT", "HTML", "CSS",
        "REACT", "NODE.JS", "GIT",
        "GITHUB", "VSCODE", "MYSQL"
    ]

    for i, skill in enumerate(skills):

        row = i // 6
        col = i % 6

        x = 43 + col * 153
        y = 57 + row * 39

        content += panel(x, y, 135, 32, 7)

        content += label(
            x + 67, y + 21,
            skill, 11, "#EAFBFF", "bold"
        ).replace(
            '<text x=',
            '<text text-anchor="middle" x=',
            1
        )

    save("technology.svg", content)


# ------------------------------------------
# PROJECT CARDS
# ------------------------------------------

def create_projects(repos):

    projects = sorted(
        repos,
        key=lambda r: (
            r["stargazers_count"],
            r["updated_at"]
        ),
        reverse=True
    )[:3]

    content = svg_start(300)

    content += panel(20, 10, 960, 280)

    content += label(
        50, 48,
        "✦ FEATURED PROJECTS",
        20, "#00F5FF", "bold"
    )

    for i, repo in enumerate(projects):

        x = 43 + i * 305

        content += panel(x, 75, 285, 185, 12)

        content += label(
            x + 18, 112,
            repo["name"][:28],
            16, "#00F5FF", "bold"
        )

        description = (
            repo.get("description")
            or "Explore this project on GitHub."
        )

        content += label(
            x + 18, 145,
            description[:34],
            12
        )

        content += label(
            x + 18, 170,
            description[34:68],
            12
        )

        content += label(
            x + 18, 225,
            f"★ {repo['stargazers_count']}  •  {repo.get('language') or 'Code'}",
            12, "#C8C8FF"
        )

    if not projects:
        content += label(50, 110, "No public projects available yet.")

    save("projects.svg", content)


# ------------------------------------------
# FOOTER
# ------------------------------------------

def create_footer():

    content = svg_start(160)

    content += panel(20, 10, 960, 140)

    content += label(
        500, 65,
        "LET'S CONNECT",
        23, "#00F5FF", "bold"
    ).replace(
        '<text x="500"',
        '<text text-anchor="middle" x="500"',
        1
    )

    content += label(
        500, 100,
        "THANK YOU FOR VISITING MY PROFILE",
        14, "#EAFBFF"
    ).replace(
        '<text x="500"',
        '<text text-anchor="middle" x="500"',
        1
    )

    content += label(
        500, 125,
        "Designed with passion • Built with code",
        11, "#AABBD5"
    ).replace(
        '<text x="500"',
        '<text text-anchor="middle" x="500"',
        1
    )

    save("footer.svg", content)


# ------------------------------------------
# REPOSITORY TABLE
# ------------------------------------------

def update_repositories(repos):

    rows = [
        "| Repository | Language | Stars |",
        "|---|---|---:|"
    ]

    latest = sorted(
        repos,
        key=lambda r: r["updated_at"],
        reverse=True
    )[:6]

    for repo in latest:

        rows.append(
            f"| [{repo['name']}]({repo['html_url']}) "
            f"| {repo.get('language') or 'Various'} "
            f"| ⭐ {repo['stargazers_count']} |"
        )

    replacement = (
        "<!-- REPO-LIST:START -->\n"
        + "\n".join(rows)
        + "\n<!-- REPO-LIST:END -->"
    )

    update_readme(
        "<!-- REPO-LIST:START -->",
        "<!-- REPO-LIST:END -->",
        replacement
    )


# ------------------------------------------
# LANGUAGE STATISTICS
# ------------------------------------------

def update_languages(repos):

    totals = {}

    for repo in repos:

        try:
            languages = api(repo["languages_url"])

            for language, amount in languages.items():
                totals[language] = (
                    totals.get(language, 0) + amount
                )

        except Exception as error:
            print("Language error:", error)

    total = sum(totals.values())

    rows = [
        "| Language | Usage |",
        "|---|---:|"
    ]

    if total:
        for language, amount in sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True
        )[:6]:

            percentage = amount / total * 100

            rows.append(
                f"| {language} | {percentage:.1f}% |"
            )
    else:
        rows = ["No language information available yet."]

    replacement = (
        "<!-- LANGUAGES:START -->\n"
        + "\n".join(rows)
        + "\n<!-- LANGUAGES:END -->"
    )

    update_readme(
        "<!-- LANGUAGES:START -->",
        "<!-- LANGUAGES:END -->",
        replacement
    )


# ------------------------------------------
# MAIN
# ------------------------------------------

def main():

    print("Fetching GitHub profile...")

    user = api(
        f"https://api.github.com/users/{USERNAME}"
    )

    print("Fetching repositories...")

    repos = api(
        f"https://api.github.com/users/{USERNAME}/repos"
        "?per_page=100&sort=updated"
    )

    repos = [
        r for r in repos
        if not r.get("fork", False)
    ]

    print("Generating dashboard...")

    create_header()
    create_profile(user, repos)
    create_technology()
    create_projects(repos)
    create_footer()

    print("Updating repository list...")

    update_repositories(repos)

    print("Updating language statistics...")

    update_languages(repos)

    print("Profile successfully updated!")


if __name__ == "__main__":
    main()
