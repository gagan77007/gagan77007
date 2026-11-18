
import json
import urllib.request
from pathlib import Path
from html import escape

# ==========================================
# SETTINGS
# ==========================================

USERNAME = "gagan77007"
DISPLAY_NAME = "GAGAN REDDY"

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

CYAN = "#00F5FF"
PURPLE = "#A78BFA"
WHITE = "#EAFBFF"
MUTED = "#A8B8D8"


# ==========================================
# GITHUB API
# ==========================================

def api(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Gagan-GitHub-Profile"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


# ==========================================
# SVG DESIGN HELPERS
# ==========================================

def svg_start(height):
    return f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="1000" height="{height}" viewBox="0 0 1000 {height}">

    <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#07111F"/>
            <stop offset="55%" stop-color="#101B38"/>
            <stop offset="100%" stop-color="#24164A"/>
        </linearGradient>

        <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#00F5FF"/>
            <stop offset="50%" stop-color="#7C3AED"/>
            <stop offset="100%" stop-color="#00F5FF"/>
        </linearGradient>

        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <rect width="1000" height="{height}" rx="22" fill="url(#bg)"/>

    <rect x="4" y="4" width="992" height="{height - 8}"
        rx="19" fill="none"
        stroke="url(#border)" stroke-width="2"
        filter="url(#glow)"/>
    '''


def panel(x, y, width, height):
    return f'''
    <rect x="{x}" y="{y}" width="{width}" height="{height}"
        rx="16" fill="#0B1730"
        stroke="#263B68" stroke-width="1.2"/>
    '''


def label(x, y, value, size=16, color=WHITE, weight="normal"):
    return f'''
    <text x="{x}" y="{y}" fill="{color}"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="{size}" font-weight="{weight}">
        {escape(str(value))}
    </text>
    '''


def centered_label(x, y, value, size=16, color=WHITE, weight="normal"):
    return f'''
    <text x="{x}" y="{y}" text-anchor="middle"
        fill="{color}"
        font-family="JetBrains Mono, Consolas, monospace"
        font-size="{size}" font-weight="{weight}">
        {escape(str(value))}
    </text>
    '''


def save(filename, content):
    (ASSETS / filename).write_text(
        content + "\n</svg>",
        encoding="utf-8"
    )


# ==========================================
# HEADER
# ==========================================

def create_header():
    content = svg_start(220)

    content += '''
    <circle cx="500" cy="95" r="105"
        fill="#312E81" opacity="0.12"/>

    <circle cx="500" cy="95" r="75"
        fill="#0891B2" opacity="0.10"/>
    '''

    content += centered_label(
        500, 100, DISPLAY_NAME,
        48, WHITE, "bold"
    )

    content += centered_label(
        500, 139,
        "BUILDING  •  LEARNING  •  CREATING",
        15, CYAN, "bold"
    )

    content += centered_label(
        500, 178,
        "DEVELOPER  /  TECHNOLOGY ENTHUSIAST",
        12, MUTED
    )

    save("header.svg", content)


# ==========================================
# ABOUT ME
# ==========================================

def create_profile(user):
    content = svg_start(170)

    content += panel(20, 12, 960, 146)

    content += label(
        50, 52, "01  /  ABOUT ME",
        21, CYAN, "bold"
    )

    bio = user.get("bio") or "Developer | Always learning and building"

    content += label(
        50, 91, bio[:100],
        15, WHITE
    )

    content += label(
        50, 123,
        "Learning • Building • Creating",
        14, MUTED
    )

    content += label(
        50, 146,
        "GITHUB.COM/GAGAN77007",
        12, PURPLE
    )

    save("profile.svg", content)


# ==========================================
# DEVELOPER TERMINAL
# ==========================================

def create_terminal():
    content = svg_start(190)

    content += panel(20, 12, 960, 166)

    content += label(
        50, 48,
        "02  /  DEVELOPER TERMINAL",
        19, CYAN, "bold"
    )

    content += '''
    <circle cx="920" cy="39" r="5" fill="#FB7185"/>
    <circle cx="940" cy="39" r="5" fill="#FACC15"/>
    <circle cx="960" cy="39" r="5" fill="#4ADE80"/>
    '''

    lines = [
        ("$ whoami", "#7CFC8A"),
        ("Gagan Reddy — Developer", WHITE),
        ("$ current_focus", "#7CFC8A"),
        ("Learning • Building • Creating", WHITE),
        ("$ status", "#7CFC8A"),
        ("Always exploring new ideas...", PURPLE)
    ]

    for index, (value, color) in enumerate(lines):
        content += label(
            55, 76 + index * 17,
            value, 12, color
        )

    save("terminal.svg", content)


# ==========================================
# AUTOMATIC PROJECT CARDS
# ==========================================

def create_projects(repos):

    selected = sorted(
        [
            repo for repo in repos
            if not repo.get("fork", False)
            and not repo.get("private", False)
        ],
        key=lambda repo: repo.get("updated_at", ""),
        reverse=True
    )[:3]

    project_links = []

    for index, repo in enumerate(selected, start=1):

        name = repo.get("name", "Project")

        description = (
            repo.get("description")
            or "A project built with curiosity and creativity."
        )

        language = repo.get("language") or "Project"

        filename = f"project_{index}.svg"

        content = svg_start(150)

        content += panel(15, 12, 970, 126)

        content += label(
            40, 49,
            f"0{index}  /  {name[:35]}",
            18, CYAN, "bold"
        )

        content += label(
            40, 80,
            description[:95],
            13, WHITE
        )

        content += label(
            40, 111,
            f"PROJECT  /  {language}",
            12, PURPLE
        )

        save(filename, content)

        project_url = escape(
            repo.get("html_url", ""),
            quote=True
        )

        project_links.append(
            f'<a href="{project_url}">'
            f'<img src="./assets/{filename}" '
            f'width="100%" alt="{escape(name, quote=True)}"/>'
            f'</a>'
        )

    if not selected:
        project_links.append(
            "<p>No public projects found yet.</p>"
        )

    (ASSETS / "project_cards.html").write_text(
        "\n".join(project_links),
        encoding="utf-8"
    )


# ==========================================
# FOOTER
# ==========================================

def create_footer():
    content = svg_start(115)

    content += centered_label(
        500, 48,
        "LET'S BUILD SOMETHING GREAT",
        19, CYAN, "bold"
    )

    content += centered_label(
        500, 78,
        "GITHUB  •  CONNECT  •  CREATE",
        12, MUTED
    )

    save("footer.svg", content)


# ==========================================
# README GENERATOR
# ==========================================

def create_readme():

    project_cards_path = ASSETS / "project_cards.html"

    project_cards = project_cards_path.read_text(
        encoding="utf-8"
    ) if project_cards_path.exists() else ""

    readme = f'''<div align="center">

<img src="./assets/header.svg" width="100%" alt="Gagan Reddy"/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=16&duration=2500&pause=800&color=00F5FF&center=true&vCenter=true&width=650&lines=ASPIRING+DEVELOPER;TECHNOLOGY+ENTHUSIAST;ALWAYS+LEARNING+AND+BUILDING;TURNING+IDEAS+INTO+REALITY" alt="Typing animation"/>

<img src="./assets/profile.svg" width="100%" alt="About me"/>

### MY CODING SPACE

<img src="./coding-room.gif" width="100%" alt="Coding workspace"/>

<img src="./assets/terminal.svg" width="100%" alt="Developer terminal"/>

### FEATURED PROJECTS

{project_cards}

### GITHUB CONTRIBUTIONS

<img src="https://raw.githubusercontent.com/{USERNAME}/{USERNAME}/output/github-contribution-grid-snake.svg" width="100%" alt="GitHub contribution snake"/>

### CONNECT WITH ME

<a href="https://github.com/{USERNAME}">
<img src="https://img.shields.io/badge/GitHub-Profile-0B1730?style=for-the-badge&logo=github&logoColor=00F5FF"/>
</a>

<img src="./assets/footer.svg" width="100%" alt="Footer"/>

</div>
'''

    (ROOT / "README.md").write_text(
        readme,
        encoding="utf-8"
    )


# ==========================================
# MAIN
# ==========================================

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

    print("Creating premium profile...")

    create_header()
    create_profile(user)
    create_terminal()
    create_projects(repos)
    create_footer()
    create_readme()

    print("Profile updated successfully!")


if __name__ == "__main__":
    main()
