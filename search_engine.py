"""
search_engine.py
----------------
Module 3 of the TitanCampus Algorithmic Assistant (TCAA): the Notes Search
Engine. Provides:

    1. From-scratch implementations of three classic string-matching
       algorithms (Naive, Rabin-Karp, KMP).
    2. A Tkinter Frame (`NotesSearchFrame`) that wires those algorithms
       to a file-upload + search UI.

The frame is designed to be dropped into the main application notebook
without depending on anything outside the standard library + file_parser.
"""

import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from file_parser import extract_text


# ---------------------------------------------------------------------------
# String-matching algorithms (all return a list of 0-based match indices)
# ---------------------------------------------------------------------------

def naive_search(text: str, pattern: str) -> list:
    """
    Brute-force pattern matching.

    Time:  O(n * m)   (n = len(text), m = len(pattern))
    Space: O(1)
    """
    n, m = len(text), len(pattern)
    matches = []
    if m == 0 or m > n:
        return matches

    for i in range(n - m + 1):
        # compare character-by-character; bail out on first mismatch
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            matches.append(i)
    return matches


def rabin_karp_search(text: str, pattern: str,
                      base: int = 256, prime: int = 1_000_003) -> list:
    """
    Rabin-Karp uses a rolling hash to skip mismatched windows in O(1) each.

    Average time:  O(n + m)
    Worst time:    O(n * m)   (lots of hash collisions)
    Space:         O(1)
    """
    n, m = len(text), len(pattern)
    matches = []
    if m == 0 or m > n:
        return matches

    # high-order multiplier used when sliding the window: base^(m-1) mod prime
    h = pow(base, m - 1, prime)

    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        window_hash = (base * window_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        # hash match? verify char-by-char to rule out collisions
        if pattern_hash == window_hash and text[i:i + m] == pattern:
            matches.append(i)

        # roll the hash forward by one character
        if i < n - m:
            window_hash = (
                base * (window_hash - ord(text[i]) * h) + ord(text[i + m])
            ) % prime
            # python's % keeps the result non-negative, but be explicit
            if window_hash < 0:
                window_hash += prime

    return matches


def _build_kmp_lps(pattern: str) -> list:
    """
    Build the KMP "longest proper prefix that is also a suffix" table.
    lps[i] = length of the longest border of pattern[0..i].
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix-suffix
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # fall back to the previous border and try again
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text: str, pattern: str) -> list:
    """
    Knuth-Morris-Pratt uses the LPS table to never re-examine text chars.

    Time:  O(n + m)
    Space: O(m)
    """
    n, m = len(text), len(pattern)
    matches = []
    if m == 0 or m > n:
        return matches

    lps = _build_kmp_lps(pattern)

    i = 0  # index into text
    j = 0  # index into pattern
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                # continue scanning for further matches
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches


# ---------------------------------------------------------------------------
# Tkinter UI: Notes Search Engine tab
# ---------------------------------------------------------------------------

# Algorithm registry shared by the radio buttons and the comparison runner
ALGORITHMS = {
    "Naive":      naive_search,
    "Rabin-Karp": rabin_karp_search,
    "KMP":        kmp_search,
}


class NotesSearchFrame(ttk.Frame):
    """
    Self-contained tab for Module 3.

    Workflow:
        1. User clicks "Upload File" -> picks .txt/.pdf/.docx
        2. file_parser.extract_text() loads the document (lowercased)
        3. User types a pattern, picks an algorithm, clicks "Search"
        4. Match indices + timing are written to the results pane
    """

    PREVIEW_CHARS = 60  # how much surrounding text to show per match

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, padding=10)

        # backing state
        self._document_text: str = ""
        self._document_path: str = ""
        self._algo_choice = tk.StringVar(value="Naive")

        self._build_widgets()

    # -- UI construction ----------------------------------------------------

    def _build_widgets(self) -> None:
        # let the results widget expand when the window grows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        # Row 0: file controls
        file_bar = ttk.Frame(self)
        file_bar.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        file_bar.columnconfigure(1, weight=1)

        ttk.Button(
            file_bar, text="Upload File", command=self._on_upload
        ).grid(row=0, column=0, padx=(0, 8))

        self._file_label = ttk.Label(
            file_bar, text="No file loaded.", foreground="#555"
        )
        self._file_label.grid(row=0, column=1, sticky="w")

        # Row 1: pattern entry
        pattern_bar = ttk.Frame(self)
        pattern_bar.grid(row=1, column=0, sticky="ew", pady=6)
        pattern_bar.columnconfigure(1, weight=1)

        ttk.Label(pattern_bar, text="Search pattern:").grid(
            row=0, column=0, padx=(0, 8)
        )
        self._pattern_entry = ttk.Entry(pattern_bar)
        self._pattern_entry.grid(row=0, column=1, sticky="ew")
        # Enter key triggers a search for convenience
        self._pattern_entry.bind("<Return>", lambda _e: self._on_search())

        # Row 2: algorithm picker
        algo_bar = ttk.LabelFrame(self, text="Algorithm")
        algo_bar.grid(row=2, column=0, sticky="ew", pady=6)
        for col, label in enumerate(("Naive", "Rabin-Karp", "KMP", "ALL")):
            ttk.Radiobutton(
                algo_bar, text=label, value=label,
                variable=self._algo_choice
            ).grid(row=0, column=col, padx=10, pady=4, sticky="w")

        # Row 3: search button
        ttk.Button(
            self, text="Search", command=self._on_search
        ).grid(row=3, column=0, sticky="w", pady=(4, 8))

        # Row 4: results pane (Text + Scrollbar)
        results_frame = ttk.Frame(self)
        results_frame.grid(row=4, column=0, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self._results = tk.Text(
            results_frame, wrap="word", height=15,
            font=("Consolas", 10), state="disabled"
        )
        self._results.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            results_frame, orient="vertical", command=self._results.yview
        )
        scroll.grid(row=0, column=1, sticky="ns")
        self._results.configure(yscrollcommand=scroll.set)

    # -- Event handlers -----------------------------------------------------

    def _on_upload(self) -> None:
        """Open a file dialog and load the chosen document into memory."""
        path = filedialog.askopenfilename(
            title="Select a notes file",
            filetypes=[
                ("Supported files", "*.txt *.pdf *.docx"),
                ("Text files",      "*.txt"),
                ("PDF files",       "*.pdf"),
                ("Word documents",  "*.docx"),
                ("All files",       "*.*"),
            ],
        )
        if not path:
            return

        try:
            self._document_text = extract_text(path)
        except (ImportError, ValueError, FileNotFoundError) as e:
            messagebox.showerror("Cannot load file", str(e))
            return
        except Exception as e:
            # last-resort guard so a corrupt PDF doesn't kill the app
            messagebox.showerror(
                "Cannot load file",
                f"Failed to parse the document:\n{e}",
            )
            return

        self._document_path = path
        char_count = len(self._document_text)
        self._file_label.configure(
            text=f"Loaded: {path}   ({char_count:,} characters)",
            foreground="black",
        )
        self._write_results(
            f"Loaded '{path}'\n"
            f"Document length (lowercased): {char_count:,} characters.\n"
            f"Type a pattern above and click Search."
        )

    def _on_search(self) -> None:
        """Run the selected algorithm(s) against the loaded document."""
        if not self._document_text:
            messagebox.showinfo(
                "No document",
                "Please upload a .txt, .pdf, or .docx file first.",
            )
            return

        pattern = self._pattern_entry.get().strip().lower()
        if not pattern:
            messagebox.showinfo(
                "Empty pattern",
                "Type a search pattern before pressing Search.",
            )
            return

        choice = self._algo_choice.get()
        if choice == "ALL":
            output = self._run_comparison(pattern)
        else:
            output = self._run_single(choice, pattern)

        self._write_results(output)

    # -- Search runners -----------------------------------------------------

    def _run_single(self, algo_name: str, pattern: str) -> str:
        """Execute one algorithm and format the result."""
        algo = ALGORITHMS[algo_name]

        start = time.perf_counter()
        matches = algo(self._document_text, pattern)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        lines = [
            f"Algorithm : {algo_name}",
            f"Pattern   : '{pattern}'",
            f"Matches   : {len(matches)}",
            f"Time      : {elapsed_ms:.4f} ms",
            "",
        ]
        if matches:
            lines.append("First match indices:")
            # cap the listed previews to keep the UI responsive on huge docs
            for idx in matches[:25]:
                lines.append(f"  [{idx}] ...{self._snippet(idx, len(pattern))}...")
            if len(matches) > 25:
                lines.append(f"  ... and {len(matches) - 25} more matches.")
        else:
            lines.append("No matches found.")
        return "\n".join(lines)

    def _run_comparison(self, pattern: str) -> str:
        """Run all three algorithms and produce a side-by-side report."""
        results = []  # (name, matches, elapsed_ms)
        for name, algo in ALGORITHMS.items():
            start = time.perf_counter()
            matches = algo(self._document_text, pattern)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            results.append((name, matches, elapsed_ms))

        lines = [
            f"Comparison Mode  --  pattern = '{pattern}'",
            "-" * 60,
            f"{'Algorithm':<12} {'Matches':>10} {'Time (ms)':>14}",
            "-" * 60,
        ]
        for name, matches, elapsed_ms in results:
            lines.append(f"{name:<12} {len(matches):>10} {elapsed_ms:>14.4f}")
        lines.append("-" * 60)

        # sanity check: every algorithm should find the same indices
        index_sets = [tuple(m) for _, m, _ in results]
        if len(set(index_sets)) == 1:
            lines.append("All three algorithms agree on the match indices.")
        else:
            lines.append(
                "WARNING: algorithms disagree on the match indices "
                "(this should not happen)."
            )

        # show the indices once (they're identical across algorithms when ok)
        shared_matches = results[0][1]
        if shared_matches:
            lines.append("")
            lines.append(f"Match indices ({len(shared_matches)} total):")
            preview = ", ".join(str(i) for i in shared_matches[:30])
            lines.append("  " + preview)
            if len(shared_matches) > 30:
                lines.append(f"  ... and {len(shared_matches) - 30} more.")
        else:
            lines.append("")
            lines.append("No matches found by any algorithm.")

        # call out the fastest run, ignoring ties under the timer's resolution
        fastest = min(results, key=lambda r: r[2])
        lines.append("")
        lines.append(f"Fastest this run: {fastest[0]} ({fastest[2]:.4f} ms)")
        return "\n".join(lines)

    # -- Helpers ------------------------------------------------------------

    def _snippet(self, index: int, pattern_len: int) -> str:
        """Return a short surrounding-context preview for a match index."""
        start = max(0, index - self.PREVIEW_CHARS // 2)
        end = min(len(self._document_text),
                  index + pattern_len + self.PREVIEW_CHARS // 2)
        # collapse newlines so the preview stays on one line
        return self._document_text[start:end].replace("\n", " ")

    def _write_results(self, text: str) -> None:
        """Replace the contents of the results pane."""
        self._results.configure(state="normal")
        self._results.delete("1.0", tk.END)
        self._results.insert(tk.END, text)
        self._results.configure(state="disabled")
