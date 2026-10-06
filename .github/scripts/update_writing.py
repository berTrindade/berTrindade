"""Rewrites the README's "Latest writing" section from the blog's RSS feed.

Standard library only, so the workflow needs no install step.
"""
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://btrindade.com/rss.xml"
LIMIT = 5
README = Path(__file__).resolve().parents[2] / "README.md"

request = urllib.request.Request(FEED, headers={"User-Agent": "berTrindade-profile-readme"})
with urllib.request.urlopen(request, timeout=30) as response:
    root = ET.fromstring(response.read())

lines = []
for item in list(root.iter("item"))[:LIMIT]:
    title = item.findtext("title", "").strip()
    link = item.findtext("link", "").strip()
    date = parsedate_to_datetime(item.findtext("pubDate")).date().isoformat()
    lines.append(f"- [{title}]({link}) - {date}")

if not lines:
    # A failed or empty feed must not wipe the section.
    raise SystemExit("feed had no items; README left unchanged")

text = README.read_text()
updated = re.sub(
    r"<!-- writing starts -->.*?<!-- writing ends -->",
    "<!-- writing starts -->\n" + "\n".join(lines) + "\n<!-- writing ends -->",
    text,
    flags=re.S,
)
README.write_text(updated)
print(f"{len(lines)} posts written")
