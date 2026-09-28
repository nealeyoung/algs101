# Lecture notes on Algorithms

Lecture notes on the design and analysis of algorithms, by Neal E. Young,
with Python code for many of the algorithms and LaTeX templates for homework
assignments.

The PDFs are built from this repository by GitHub Actions and published at
<https://nealeyoung.github.io/algs101/>:

- the lecture notes as one book, and each lecture note on its own;
- each homework assignment, as a PDF and as a LaTeX template (zip file) that
  you can also open directly in Overleaf.

## Layout

- `src/main.tex` — the book (one chapter per lecture note)
- `src/1_preliminaries/` … `src/9_NP/` — the lecture notes
- `src/code/` — Python code
- `src/homeworks/` — homework templates
- `src/macros/macros.tex` — LaTeX macros shared by all of the above
- `src/refs/` — the lecture notes' label records (made by `tools/refs.sh`), which let the homeworks refer to the notes' sections, exercises and lemmas by `\ref`, with links

To build locally: `latexmk -pdf main.tex` in `src/` (or the same with any
lecture note or homework template, in its own folder).

## For instructors

The homework templates are course-independent by default.  To use them in a
course, edit `src/macros/macros.tex`: set `\classSection` to the course name
(shown in each homework's running head), and change `\Gradescopefalse` to
`\Gradescopetrue` to turn on the instructions for submitting to Gradescope in
its fixed-length grading mode, the hints saying on which page of the PDF each
answer should be, and the student ID in the running head.

## License

&copy; 2018&ndash;2026 Neal E. Young.  The notes and homeworks are licensed under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) and the code
under the MIT License, except for the third-party figures noted in
[LICENSE](LICENSE).
