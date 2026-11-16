import json
import os
import html
import urllib.request
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================

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


# ==========================================
# GITHUB API
# ==========================================

def github_api(url):

    request = urllib.request.Request(
        url,
        headers=HEADERS
    )

    with urllib.request.urlopen(
        request,
        timeout=30
    ) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def safe(value):

    return html.escape(
        str(value or ""),
        quote=True
    )


def truncate(text, limit):

    text = str(text or "")

    if len(text) > limit:
        return text[:limit - 3] + "..."

    return text


def svg_start(height):

    return f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="1000"
    height="{height}"
    viewBox="0 0 1000 {height}">

    <defs>

      <linearGradient id="border"
        x1="0" y1="0" x2="1" y2="1">

        <stop offset="0%" stop-color="#00F5FF"/>
        <stop offset="50%" stop-color="#4263EB"/>
        <stop offset="100%" stop-color="#A855F7"/>

      </linearGradient>

      <linearGradient id="panel"
        x1="0" y1="0" x2="1" y2="1">

        <stop offset="0%" stop-color="#101C35"/>
        <stop offset="100%" stop-color="#080D20"/>

      </linearGradient>

      <filter id="glow"
        x="-30%" y="-30%" width="160%" height="160%">

        <feGaussianBlur stdDeviation="2.5"
          result="blur"/>

        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>

      </filter>

    </defs>

    <rect
      x="5"
      y="5"
      width="990"
      height="{height - 10}"
      rx="18"
      fill="url(#panel)"
      stroke="url(#border)"
      stroke-width="2"
      filter="url(#glow)"
    />

    '''


def svg_end():

    return "</svg>"


def save_svg(filename, content):

    path = ASSETS / filename

    path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"Generated: {path}")


# ==========================================
# TERMINAL DESIGN
# ==========================================

def create_terminal():

    content = svg_start(155)

    content += '''

    <circle cx="32" cy="28" r="6" fill="#FF5F57"/>
    <circle cx="52" cy="28" r="6" fill="#FEBC2E"/>
    <circle cx="72" cy="28" r="6" fill="#28C840"/>

    <text x="100" y="33"
      fill="#8FA3C8"
      font-size="13"
      font-family="monospace">

      gagan@developer:~

    </text>

    <text x="35" y="76"
      fill="#00F5FF"
      font-size="18"
      font-family="monospace">

      $ whoami

    </text>

    <text x="35" y="110"
      fill="#EAFBFF"
      font-size="17"
      font-family="monospace">

      Full Stack Developer | Tech Enthusiast

    </text>

    <rect x="690" y="94"
      width="9"
      height="19"
      fill="#00F5FF">

      <animate
        attributeName="opacity"
        values="1;0;1"
        dur="1.2s"
        repeatCount="indefinite"/>

    </rect>

    '''

    content += svg_end()

    save_svg(
        "terminal.svg",
        content
    )


# ==========================================
# PROFILE DASHBOARD
# ==========================================

def create_dashboard(user, repos):

    total_stars = sum(
        repo["stargazers_count"]
        for repo in repos
    )

    followers = user.get("followers", 0)

    public_repos = user.get(
        "public_repos", 0
    )

    bio = safe(
        user.get("bio")
        or "Building, learning and exploring technology."
    )

    bio = truncate(bio, 100)

    cards = [

        ("PUBLIC REPOSITORIES", public_repos),

        ("FOLLOWERS", followers),

        ("TOTAL STARS", total_stars)

    ]

    content = svg_start(210)

    content += f'''

    <text x="35" y="45"
      fill="#00F5FF"
      font-size="20"
      font-weight="bold"
      font-family="Arial">

      DEVELOPER PROFILE

    </text>

    <text x="35" y="76"
      fill="#DCEBFF"
      font-size="14"
      font-family="Arial">

      {bio}

    </text>

    '''

    for index, (label, value) in enumerate(cards):

        x = 35 + index * 315

        content += f'''

        <rect
          x="{x}"
          y="105"
          width="285"
          height="75"
          rx="12"
          fill="#111D36"
          stroke="#294B75"
          stroke-width="1.3"
        />

        <text
          x="{x + 18}"
          y="135"
          fill="#8FA3C8"
          font-size="12"
          font-family="Arial">

          {label}

        </text>

        <text
          x="{x + 18}"
          y="163"
          fill="#00F5FF"
          font-size="25"
          font-weight="bold"
          font-family="Arial">

          {value}

        </text>

        '''

    content += svg_end()

    save_svg(
        "profile-dashboard.svg",
        content
    )


# ==========================================
# PROJECT CARDS
# ==========================================

def create_projects(repos):

    projects = sorted(
        repos,
        key=lambda repo: (
            repo["stargazers_count"],
            repo["updated_at"]
        ),
        reverse=True
    )[:4]

    height = 100 + max(1, len(projects)) * 105

    content = svg_start(height)

    content += '''

    <text x="35" y="45"
      fill="#00F5FF"
      font-size="20"
      font-weight="bold"
      font-family="Arial">

      LATEST GITHUB PROJECTS

    </text>

    '''

    if not projects:

        content += '''

        <text x="35" y="100"
          fill="#EAFBFF"
          font-size="16"
          font-family="Arial">

          No public projects available yet.

        </text>

        '''

    for index, repo in enumerate(projects):

        y = 65 + index * 105

        name = safe(
            truncate(repo["name"], 48)
        )

        description = safe(
            truncate(
                repo.get("description")
                or "Explore this project on GitHub.",
                95
            )
        )

        language = safe(
            repo.get("language") or "Various"
        )

        stars = repo.get(
            "stargazers_count", 0
        )

        content += f'''

        <rect
          x="25"
          y="{y}"
          width="950"
          height="88"
          rx="12"
          fill="#101B32"
          stroke="#29466C"
          stroke-width="1.2"
        />

        <text
          x="48"
          y="{y + 30}"
          fill="#00F5FF"
          font-size="17"
          font-weight="bold"
          font-family="Arial">

          {name}

        </text>

        <text
          x="48"
          y="{y + 53}"
          fill="#B8C8E6"
          font-size="12"
          font-family="Arial">

          {description}

        </text>

        <text
          x="48"
          y="{y + 75}"
          fill="#A78BFA"
          font-size="11"
          font-family="Arial">

          {language}  •  ★ {stars}

        </text>

        '''

    content += svg_end()

    save_svg(
        "projects.svg",
        content
    )


# ==========================================
# README UPDATE
# ==========================================

def update_readme(start, end, replacement):

    text = README.read_text(
        encoding="utf-8"
    )

    first = text.find(start)

    last = text.find(end)

    if first == -1 or last == -1:

        raise ValueError(
            f"README markers missing: {start}"
        )

    if last < first:

        raise ValueError(
            "README markers are in the wrong order."
        )

    last += len(end)

    text = (
        text[:first]
        + replacement
        + text[last:]
    )

    README.write_text(
        text,
        encoding="utf-8"
    )


# ==========================================
# AUTOMATIC REPOSITORY LIST
# ==========================================

def update_repo_list(repos):

    rows = [

        "| Repository | Language | Stars |",

        "|---|---|---:|"

    ]

    latest = sorted(
        repos,
        key=lambda repo: repo["updated_at"],
        reverse=True
    )[:8]

    for repo in latest:

        name = repo["name"]

        url = repo["html_url"]

        language = repo.get(
            "language"
        ) or "Various"

        stars = repo["stargazers_count"]

        rows.append(
            f"| [{name}]({url}) | {language} | ⭐ {stars} |"
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


# ==========================================
# AUTOMATIC LANGUAGE STATISTICS
# ==========================================

def update_languages(repos):

    totals = {}

    for repo in repos:

        try:

            languages = github_api(
                repo["languages_url"]
            )

            for language, amount in languages.items():

                totals[language] = (
                    totals.get(language, 0)
                    + amount
                )

        except Exception as error:

            print(
                f"Language fetch failed: {error}"
            )

    total_bytes = sum(
        totals.values()
    )

    if total_bytes == 0:

        rows = [
            "No language data available yet."
        ]

    else:

        rows = [

            "| Language | Usage |",

            "|---|---:|"

        ]

        for language, amount in sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True
        )[:8]:

            percentage = (
                amount / total_bytes
            ) * 100

            rows.append(
                f"| {language} | {percentage:.1f}% |"
            )

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


# ==========================================
# MAIN
# ==========================================

def main():

    print("\nStarting GitHub profile update...\n")

    print("Fetching profile...")

    user = github_api(
        f"https://api.github.com/users/{USERNAME}"
    )

    print("Fetching repositories...")

    repos = github_api(
        f"https://api.github.com/users/{USERNAME}/repos"
        "?per_page=100&sort=updated"
    )

    repos = [
        repo for repo in repos
        if not repo.get("fork", False)
    ]

    print("Generating visual panels...")

    create_terminal()

    create_dashboard(
        user,
        repos
    )

    create_projects(
        repos
    )

    print("Updating repositories...")

    update_repo_list(
        repos
    )

    print("Updating languages...")

    update_languages(
        repos
    )

    print("\nGitHub profile updated successfully!")


if __name__ == "__main__":

    main()
