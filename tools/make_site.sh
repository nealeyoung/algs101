#!/bin/bash
# Assemble the GitHub Pages site in _site/ from the PDFs built in src/, and a
# zip of each homework template (made from the files in git, so no build
# output; zip stores the macros file's contents, not the symlink).
set -euo pipefail
cd "$(dirname "$0")/.."
SITE=_site
BASE=https://nealeyoung.github.io/algs101
rm -rf "$SITE"; mkdir -p "$SITE/notes" "$SITE/homeworks"

cp src/main.pdf "$SITE/lecture_notes_on_algorithms.pdf"

notes=""
for d in src/[1-9]_*/; do
  for f in "$d"*.tex; do
    grep -q '\\documentclass' "$f" || continue
    pdf="${f%.tex}.pdf"; [ -f "$pdf" ] || continue
    name="$(basename "$d")"
    cp "$pdf" "$SITE/notes/$name.pdf"
    title="$(python3 tools/site_lists.py title "$name")"   # the number comes from the <ol>
    notes="$notes<li><a href=\"notes/$name.pdf\">$title</a></li>"
  done
done
appendices="$(python3 tools/site_lists.py appendices)"
code=$(python3 tools/site_lists.py code)

# from src/appendices/homework_list.tex: the topics (lecture notes) homework N
# covers, and a sublist of its problems' topics, then $2, the links, as a last,
# unnumbered item
topics() { python3 tools/site_lists.py topics "$1"; }
problem_list() {
  echo "<ol>"
  python3 tools/site_lists.py problems "$1" | sed 's|.*|<li>&</li>|'
  echo "<li style=\"list-style: none\">$2</li>"
  echo "</ol>"
}

homeworks=""
for n in $(seq 1 20); do
  # the template is in homework_N.git/ (homework 1: homework_1.git/homework_1/)
  dir=""
  for d in src/homeworks/homework_$n.git/homework_$n src/homeworks/homework_$n.git; do
    if [ -f "$d/homework_$n.tex" ]; then dir=$d; break; fi
  done
  [ -n "$dir" ] || continue
  (cd "$dir" && zip -q -r "$OLDPWD/$SITE/homeworks/homework_$n.zip" $(git ls-files .))
  cp "$dir/homework_$n.pdf" "$SITE/homeworks/homework_$n.pdf"
  zip_url="$BASE/homeworks/homework_$n.zip"
  links="<a href=\"homeworks/homework_$n.pdf\">PDF</a>,
    <a href=\"homeworks/homework_$n.zip\">template</a>,
    <a href=\"https://www.overleaf.com/docs?snip_uri=$zip_url\">Overleaf</a>"
  # the homework's number comes from the <ol> (value= in case one is missing)
  homeworks="$homeworks<li value=\"$n\">$(topics $n)$(problem_list $n "$links")</li>"
done

cat > "$SITE/index.html" <<HTML
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lecture notes on Algorithms</title>
<style>ol.homeworks > li { margin-bottom: 1.2em; }</style></head>
<body style="font-family: system-ui, sans-serif; max-width: 42em; margin: 2em auto; padding: 0 1em; line-height: 1.5;">
<h1>Lecture notes on Algorithms</h1>
<p>These notes are for a typical undergraduate course on algorithms, covering the usual topics, but with more of an emphasis on learning to do proofs than is found in most courses. We take the perspective that being able to verify correctness (via detailed proofs) is an integral part of learning to design algorithms.</p>
<p>By Neal E. Young. Built from <a href="https://github.com/nealeyoung/algs101">github.com/nealeyoung/algs101</a>.</p>
<h2>Lecture notes</h2>
<ol>$notes</ol>
<ul>$appendices<li><a href="lecture_notes_on_algorithms.pdf">All lecture notes, as one book (PDF)</a></li></ul>
<h2>Homework assignments</h2>
<ol class="homeworks">$homeworks</ol>
<h2>Code</h2>
<p>The Python code, on GitHub (<a href="https://github.com/nealeyoung/algs101/tree/main/src/code">all files</a>),
by lecture note.  Each lecture note also lists its code in its last section.</p>
<ul>$code</ul>
<p style="margin-top: 2em; font-size: 90%; color: #555;">&copy; 2018&ndash;2026 Neal E. Young.
The notes and homeworks are licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>
and the code under the MIT License, except where noted; see <a href="https://github.com/nealeyoung/algs101/blob/main/LICENSE">LICENSE</a>.</p>
</body>
</html>
HTML
echo "site assembled in $SITE/"
