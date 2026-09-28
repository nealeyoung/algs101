"""Print HTML list items for the site's front page, from the LaTeX sources:
python3 tools/site_lists.py appendices -- one item per appendix of the book
python3 tools/site_lists.py code       -- the Python code, grouped by lecture note
python3 tools/site_lists.py title DIR  -- the title for a lecture note's folder
python3 tools/site_lists.py topics N   -- the topics (lecture notes) homework N covers
python3 tools/site_lists.py problems N -- the topic of each problem of homework N, one per line
"""

import glob
import html
import re
import sys

REPO = "https://github.com/nealeyoung/algs101/blob/main/src/code"
FOLDER = "https://github.com/nealeyoung/algs101/tree/main/src/code"


def notes():
    """(number, title, driver source) for each lecture note, in order."""
    for d in sorted(glob.glob("src/[1-9]_*/")):
        for f in sorted(glob.glob(d + "*.tex")):
            s = open(f).read()
            t = re.search(r"^\\doTitle\{(\d+)\}\{([^}\\]*)", s, re.M)
            if "\\documentclass" in s and t:
                yield int(t.group(1)), t.group(2).strip(), s


if sys.argv[1] == "appendices":
    s = open("src/appendices/appendices.tex").read()
    for i, title in enumerate(re.findall(r"^\\chapter\{([^}]*)\}", s, re.M)):
        letter = chr(ord("A") + i)
        print(
            f'<li><a href="lecture_notes_on_algorithms.pdf#nameddest=appendix.{letter}">'
            f"Appendix {letter}: {html.escape(title)}</a></li>"
        )
elif sys.argv[1] == "title":
    # a lecture note's folder name in title case: 4_divide_and_conquer -> Divide and Conquer
    TITLES = {
        "2_proofs": "Long-Form Proofs",
        "5_greedy": "Greedy Algorithms",
        "8_flow_reductions_LP": "Flow, Reductions, and Linear Programming",
    }
    SMALL = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to"}
    name = sys.argv[2]
    words = name.split("_", 1)[1].split("_")
    title = " ".join(
        w if (i and w in SMALL) or w.isupper() else w[0].upper() + w[1:]
        for i, w in enumerate(words)
    )
    print(TITLES.get(name, title))
elif sys.argv[1] in ("topics", "problems"):
    # from src/appendices/homework_list.tex (also used by the book's appendix)
    s = open("src/appendices/homework_list.tex").read()
    hws = re.findall(r"^\\homework\{([^\n]*)\}\{\n(.*?)^\}", s, re.M | re.S)
    n = int(sys.argv[2])
    if n <= len(hws):
        topics, body = hws[n - 1]

        def to_html(t: str) -> str:
            return html.escape(t, quote=False).replace("$\\Theta$", "&Theta;")

        if sys.argv[1] == "topics":
            print(to_html(topics))
        else:
            for p in re.findall(r"^\s*\\hwproblem\{(.*)\}\s*$", body, re.M):
                print(to_html(p))
elif sys.argv[1] == "code":
    for n, title, s in notes():
        m = re.search(r"\\codeSection\{([^}]*)\}", s)
        if not m:
            continue
        files = [f.strip() for f in m.group(1).split(",") if f.strip()]
        # link text: just the file name (the folder is in the link)
        items = "".join(
            f'<li><a href="{REPO}/{f}">{html.escape(f.split("/")[-1])}</a></li>' for f in files
        )
        # "TOPIC (lecture note N)"; TOPIC links to the files' folder if they share one
        topic = html.escape(title)
        folders = {f.rpartition("/")[0] for f in files}
        if len(folders) == 1:
            folder = folders.pop()
            topic = (
                f'<a href="{FOLDER}/{folder}">{topic}</a>'
                if folder
                else f'<a href="{FOLDER}">{topic}</a>'
            )
        print(f"<li>{topic} (lecture note {n})<ul>{items}</ul></li>")
