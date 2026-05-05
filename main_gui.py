"""
main_gui.py
-----------
Entry point for the TitanCampus Algorithmic Assistant (TCAA).

This module owns the Tk root window and the four-tab Notebook layout.
The Notes Search Engine and Algorithm Info tabs are wired to fully
functional frames; the Campus Navigator and Study Planner tabs expose
clearly labelled `ttk.Frame` placeholders ready to receive teammates'
modules without changing this file's structure.

Run with:
    python main_gui.py
"""

import tkinter as tk
from tkinter import ttk

from search_engine import NotesSearchFrame
from algorithm_info import AlgorithmInfoFrame
from graph_algorithms import CampusNavigatorFrame
from study_planner_module import StudyPlannerFrame


# ---------------------------------------------------------------------------
# Application shell
# ---------------------------------------------------------------------------

class TCAAApp:
    """
    Top-level shell that owns the Tk root and the Notebook of tabs.

    Keeping construction in a class (rather than a giant module-level block)
    makes the app easy to test and lets teammates instantiate it from their
    own scripts if they want to.
    """

    WINDOW_TITLE = "TitanCampus Algorithmic Assistant (TCAA)"
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_root()
        self._build_tabs()

    def _configure_root(self) -> None:
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(f"{self.MIN_WIDTH}x{self.MIN_HEIGHT}")
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # Use a modern ttk theme when available; fall back silently otherwise
        try:
            ttk.Style(self.root).theme_use("clam")
        except tk.TclError:
            pass

    def _build_tabs(self) -> None:
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # ----- Tab 1: Campus Navigator -----
        navigator_tab = CampusNavigatorFrame(notebook)
        notebook.add(navigator_tab, text="Campus Navigator")

        # ----- Tab 2: Study Planner -----
        planner_tab = StudyPlannerFrame(notebook)
        notebook.add(planner_tab, text="Study Planner")

        # ----- Tab 3: Notes Search Engine (Module 3 - mine) -----
        search_tab = NotesSearchFrame(notebook)
        notebook.add(search_tab, text="Notes Search Engine")

        # ----- Tab 4: Algorithm Info (Module 4 - mine) -----
        info_tab = AlgorithmInfoFrame(notebook)
        notebook.add(info_tab, text="Algorithm Info")


def main() -> None:
    root = tk.Tk()
    TCAAApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
