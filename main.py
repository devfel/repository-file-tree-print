import os
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")
BRANCH_SHA = os.getenv("BRANCH_SHA")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# Fetch repository content
url = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{BRANCH_SHA}?recursive=1"
headers = {"Authorization": f"token {ACCESS_TOKEN}"}
response = requests.get(url, headers=headers)
data = response.json()


def get_icon_for_file(filename):
    extension = os.path.splitext(filename)[1]
    icon_mappings = {
        ".txt": "📜",
        ".md": "📜",
        ".js": "📜",
        ".ts": "📜",
        ".tsx": "📜",
        ".xml": "📜",
        ".json": "📜",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".png": "🖼️",
        ".svg": "🖼️",
        ".ico": "🖼️",
        ".lock": "🔒",
    }
    return icon_mappings.get(extension, "📄")


# Process and construct HTML
html_parts = ["<pre>"]

for item in data["tree"]:
    depth = item["path"].count("/")
    indent = "  " * depth
    if item["type"] == "blob":
        icon = get_icon_for_file(item["path"])
        html_parts.append(f"{indent}{icon} {item['path'].split('/')[-1]}")
    else:  # it's a directory
        icon = "📂"
        html_parts.append(f"{indent}{icon} {item['path'].split('/')[-1]}")

html_parts.append("</pre>")
html_content = "\n".join(html_parts)

# Write to HTML file
with open("repo_structure.html", "w", encoding="utf-8") as f:
    f.write(html_content)
