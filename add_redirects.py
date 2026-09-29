"""Make every page in docs/ redirect to the matching page of the new book.

Targets come from redirects.json (old page name -> path within the new book;
"" means the new book's home page). Re-run after rebuilding the book:

    python3 add_redirects.py
"""
import glob, json, os, re

BASE = "https://dlsun.github.io/skis/"
START, END = "<!-- redirect to new book -->", "<!-- end redirect -->"

def snippet(path):
    url = BASE + path
    canonical = url.split("#")[0]
    return f'''{START}
<link rel="canonical" href="{canonical}" />
<meta http-equiv="refresh" content="0; url={url}" />
<script>window.location.replace("{url}");</script>
{END}
'''

targets = json.load(open("redirects.json"))

for f in sorted(glob.glob("docs/*.html")):
    name = os.path.basename(f)[:-5]
    if name == "404":
        continue
    s = open(f, encoding="utf-8").read()
    block = snippet(targets[name])
    # remove any previous redirect block
    s = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", "", s, count=1, flags=re.S)
    s, n = re.subn(r"<head>\n?", lambda m: "<head>\n" + block, s, count=1)
    assert n == 1, f
    open(f, "w", encoding="utf-8").write(s)

# Old URLs that no longer exist as files fall back to the home page.
open("docs/404.html", "w", encoding="utf-8").write(f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Moved: Introduction to Probability</title>
{snippet("")}</head>
<body>
<p>This book has moved to <a href="{BASE}">{BASE}</a>.</p>
</body>
</html>
''')
