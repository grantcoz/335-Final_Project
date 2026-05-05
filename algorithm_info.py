"""
algorithm_info.py
-----------------
Module 4 of the TitanCampus Algorithmic Assistant (TCAA).

Renders a scrollable, read-only reference tab containing:
    Section A - Big-O complexity table for every algorithm in the app.
    Section B - A short academic reflection on P vs NP that ties the DP
                0/1-Knapsack used in Module 2 back to the theory.
"""

import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------------------
# Static reference data
# ---------------------------------------------------------------------------

# (Algorithm, Module, Time, Space, Notes)
COMPLEXITY_ROWS = [
    ("BFS",                 "Campus Navigator", "O(V + E)",       "O(V)",    "Fewest-hops path; queue-based traversal."),
    ("DFS",                 "Campus Navigator", "O(V + E)",       "O(V)",    "Used for traversal order and connectivity."),
    ("Dijkstra (heap)",     "Campus Navigator", "O((V + E) log V)", "O(V)",  "Shortest path with non-negative weights."),
    ("Prim's MST (heap)",   "Campus Navigator", "O(E log V)",     "O(V)",    "Minimum spanning tree of the campus graph."),
    ("Greedy Scheduling",   "Study Planner",    "O(n log n)",     "O(n)",    "Sort by ratio/deadline; not always optimal."),
    ("DP 0/1 Knapsack",     "Study Planner",    "O(n * W)",       "O(n * W)","Pseudo-polynomial; W = available time budget."),
    ("Naive Search",        "Notes Search",     "O(n * m)",       "O(1)",    "Brute force; simple but slow on near-matches."),
    ("Rabin-Karp",          "Notes Search",     "O(n + m) avg / O(n*m) worst", "O(1)", "Rolling hash; great for multi-pattern variants."),
    ("KMP",                 "Notes Search",     "O(n + m)",       "O(m)",    "LPS table avoids re-scanning the text."),
]


P_VS_NP_REFLECTION = """\
P vs NP Reflection
==================

P is the class of decision problems that a deterministic machine can
SOLVE in polynomial time -- problems for which we already know an
efficient algorithm (sorting, shortest paths, minimum spanning trees,
and the string matchers in this app). NP is the broader class of
problems for which a candidate solution can be VERIFIED in polynomial
time, even if finding that solution may require exhaustively searching
an exponential space of possibilities. Every problem in P is in NP, but
the central open question of computer science is whether P = NP -- that
is, whether every problem whose solution is easy to check is also easy
to find. Most researchers believe P != NP, which would mean there exist
problems (the NP-complete ones) that are fundamentally harder to solve
than to verify.

The 0/1 Knapsack problem used in our Study Planner is a clean
illustration of this gap. It is NP-complete in the general case: with n
tasks, the search space contains 2^n possible subsets, and no algorithm
is known that finds the truly optimal subset in time polynomial in n
plus the bit-length of the input. Our dynamic programming solution
runs in O(n * W) where W is the available time budget. That looks
polynomial, but the W axis is exponential in the number of bits used to
represent the budget -- this is what we call a *pseudo-polynomial*
algorithm. Doubling the precision of the time inputs roughly doubles
the runtime, so the cost still escalates quickly as the problem scales.

The Greedy Scheduler is dramatically faster -- O(n log n) -- because it
makes a single locally-optimal decision per task (sort by value/time
ratio, then pack while time remains). The catch is that greed can be
wrong: it may leave a high-value task on the table because it didn't
'fit' the heuristic, even though swapping it in would have produced a
better total. That trade-off is the practical face of P vs NP. When we
choose Greedy we are choosing speed and accepting the risk of a
suboptimal answer; when we choose DP we pay the pseudo-polynomial price
to guarantee optimality. Until (or unless) someone proves P = NP, this
trade-off between exact solutions and tractable approximations is the
defining tension of algorithm engineering.
"""


# ---------------------------------------------------------------------------
# Tkinter UI: Algorithm Info tab
# ---------------------------------------------------------------------------

class AlgorithmInfoFrame(ttk.Frame):
    """
    A scrollable, read-only frame displaying the complexity table and the
    P vs NP reflection. Implemented with a Canvas + inner Frame so that
    arbitrary ttk widgets (Treeview, Labels, etc.) can scroll together.
    """

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, padding=10)
        self._build_scroll_container()
        self._build_section_a()
        self._build_section_b()

    # -- scrolling scaffolding ---------------------------------------------

    def _build_scroll_container(self) -> None:
        """Create a Canvas + inner Frame that scrolls together."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scroll.set)

        # widgets are added to this inner frame, not directly to the canvas
        inner = ttk.Frame(canvas)
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.columnconfigure(0, weight=1)

        # keep the scroll region in sync as widgets are added/resized
        def on_inner_config(_event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", on_inner_config)

        # make the inner frame match the canvas width so labels wrap nicely
        def on_canvas_config(event):
            canvas.itemconfigure(inner_id, width=event.width)
        canvas.bind("<Configure>", on_canvas_config)

        # mouse wheel support (Windows-style delta)
        def on_mousewheel(event):
            canvas.yview_scroll(int(-event.delta / 120), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        self._inner = inner

    # -- Section A: complexity table ---------------------------------------

    def _build_section_a(self) -> None:
        header = ttk.Label(
            self._inner,
            text="Section A  -  Big-O Complexity Reference",
            font=("Segoe UI", 13, "bold"),
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 8))

        columns = ("algorithm", "module", "time", "space", "notes")
        tree = ttk.Treeview(
            self._inner, columns=columns, show="headings", height=len(COMPLEXITY_ROWS)
        )
        for key, label, width, anchor in (
            ("algorithm", "Algorithm",       170, "w"),
            ("module",    "Module",          150, "w"),
            ("time",      "Time Complexity", 200, "w"),
            ("space",     "Space",           90,  "w"),
            ("notes",     "Notes",           360, "w"),
        ):
            tree.heading(key, text=label)
            tree.column(key, width=width, anchor=anchor, stretch=True)

        for row in COMPLEXITY_ROWS:
            tree.insert("", "end", values=row)

        tree.grid(row=1, column=0, sticky="ew", pady=(0, 16))

    # -- Section B: P vs NP reflection -------------------------------------

    def _build_section_b(self) -> None:
        header = ttk.Label(
            self._inner,
            text="Section B  -  P vs NP Reflection",
            font=("Segoe UI", 13, "bold"),
        )
        header.grid(row=2, column=0, sticky="w", pady=(0, 8))

        body = tk.Text(
            self._inner,
            wrap="word",
            font=("Segoe UI", 10),
            height=28,
            borderwidth=1,
            relief="solid",
        )
        body.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        body.insert("1.0", P_VS_NP_REFLECTION)
        body.configure(state="disabled")  # read-only
