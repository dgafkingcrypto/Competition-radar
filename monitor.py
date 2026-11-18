#!/usr/bin/env python3
"""Public HTTPS webpage research monitor. No login or posting."""
import difflib
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())

def main():
    DATA.mkdir(exist_ok=True)
    targets = json.loads((ROOT / "targets.json").read_text())
    report = ["# Competitive Radar Pulse", "",
              "Generated: " + datetime.now(timezone.utc).isoformat(), "",
              "Public-source observations only. Verify material changes independently.", ""]
    for target in targets:
        name, url = target["name"], target["url"]
        key = hashlib.sha256(url.encode()).hexdigest()[:20]
        report += ["## " + name, "Source: " + url, ""]
        if not url.startswith("https://"):
            report += ["Skipped: HTTPS required.", ""]
            continue
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "CompetitiveRadarResearch/1.0 (public-page monitoring)"})
            with urllib.request.urlopen(req, timeout=18) as response:
                if response.status != 200:
                    raise ValueError("HTTP " + str(response.status))
                html = response.read(1500000).decode("utf-8", errors="replace")
            parser = Extract()
            parser.feed(html)
            extracted = "\n".join(dict.fromkeys(
                re.sub(r"\s+", " ", s) for s in parser.parts if len(s) > 3))[:100000]
            path = DATA / (key + ".txt")
            if path.exists():
                old = path.read_text()
                diff = list(difflib.unified_diff(
                    old.splitlines(), extracted.splitlines(), lineterm="", n=1))
                if diff:
                    report += ["Changed: " + str(len(diff)) + " diff lines.",
                               "```diff", *diff[:80], "```", ""]
                else:
                    report += ["No text changes detected.", ""]
            else:
                report += ["Baseline captured. Changes will appear on the next run.", ""]
            path.write_text(extracted)
        except Exception as exc:
            report += ["Unavailable: " + type(exc).__name__ + ": " + str(exc), ""]
    (ROOT / "PULSE.md").write_text("\n".join(report))
    print("\n".join(report)[:3000])

if __name__ == "__main__":
    main()
