import tkinter as tk
from tkinter import ttk
from collections import deque
import heapq

class CampusGraph:
    def __init__(self):
        self.graph = {}

    def add_building(self, building):
        if building not in self.graph:
            self.graph[building] = []

    def add_path(self, building1, building2, distance):
        self.add_building(building1)
        self.add_building(building2)

        self.graph[building1].append((building2, distance))
        self.graph[building2].append((building1, distance))

    # BFS: fewest hops
    def bfs(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None

        queue = deque([(start, [start])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == end:
                return path

            if current not in visited:
                visited.add(current)

                for neighbor, _ in self.graph[current]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        return None

    # DFS traversal + connectivity
    def dfs(self, start):
        if start not in self.graph:
            return []

        visited = set()
        order = []

        def dfs_helper(node):
            visited.add(node)
            order.append(node)

            for neighbor, _ in self.graph[node]:
                if neighbor not in visited:
                    dfs_helper(neighbor)

        dfs_helper(start)
        return order

    # Dijkstra: shortest weighted path
    def dijkstra(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None, float("inf")

        distances = {node: float("inf") for node in self.graph}
        previous = {node: None for node in self.graph}

        distances[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node]:
                new_distance = current_distance + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        path = []
        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        if distances[end] == float("inf"):
            return None, float("inf")

        return path, distances[end]

    # Prim's Minimum Spanning Tree
    def prim_mst(self, start):
        if start not in self.graph:
            return [], 0

        visited = set()
        mst_edges = []
        total_weight = 0

        min_heap = [(0, start, None)]

        while min_heap:
            weight, current, parent = heapq.heappop(min_heap)

            if current in visited:
                continue

            visited.add(current)

            if parent is not None:
                mst_edges.append((parent, current, weight))
                total_weight += weight

            for neighbor, edge_weight in self.graph[current]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (edge_weight, neighbor, current))

        return mst_edges, total_weight


# Example campus graph
def build_sample_campus_graph():
    campus = CampusGraph()

    campus.add_path("Library", "Student Union", 4)
    campus.add_path("Library", "Engineering", 6)
    campus.add_path("Student Union", "Gym", 3)
    campus.add_path("Student Union", "Cafeteria", 2)
    campus.add_path("Engineering", "Science Hall", 5)
    campus.add_path("Engineering", "Parking Lot", 7)
    campus.add_path("Science Hall", "Cafeteria", 4)
    campus.add_path("Gym", "Parking Lot", 8)
    campus.add_path("Cafeteria", "Bookstore", 3)
    campus.add_path("Bookstore", "Parking Lot", 6)

    return campus


class CampusNavigatorFrame(ttk.Frame):
    """Tkinter frame for exploring the campus graph."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, padding=10)
        self._campus = build_sample_campus_graph()
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        header = ttk.Label(
            self,
            text="Campus Navigator",
            font=("Segoe UI", 16, "bold"),
        )
        header.grid(row=0, column=0, sticky="w", pady=(0, 10))

        node_names = sorted(self._campus.graph)

        controls = ttk.Frame(self)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)

        ttk.Label(controls, text="Start:").grid(row=0, column=0, sticky="w")
        self._start_choice = ttk.Combobox(
            controls,
            values=node_names,
            state="readonly",
        )
        self._start_choice.grid(row=0, column=1, sticky="ew", padx=(4, 12))
        self._start_choice.set(node_names[0])

        ttk.Label(controls, text="End:").grid(row=0, column=2, sticky="w")
        self._end_choice = ttk.Combobox(
            controls,
            values=node_names,
            state="readonly",
        )
        self._end_choice.grid(row=0, column=3, sticky="ew", padx=(4, 0))
        self._end_choice.set(node_names[-1])

        button_bar = ttk.Frame(self)
        button_bar.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        for col, (label, command) in enumerate((
            ("BFS", self._run_bfs),
            ("DFS", self._run_dfs),
            ("Dijkstra", self._run_dijkstra),
            ("Prim MST", self._run_prim),
        )):
            ttk.Button(button_bar, text=label, command=command).grid(
                row=0, column=col, padx=4, sticky="ew"
            )
            button_bar.columnconfigure(col, weight=1)

        result_frame = ttk.Frame(self)
        result_frame.grid(row=4, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)

        self._results = tk.Text(
            result_frame,
            wrap="word",
            height=18,
            font=("Consolas", 10),
            state="disabled",
        )
        self._results.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(
            result_frame, orient="vertical", command=self._results.yview
        )
        scroll.grid(row=0, column=1, sticky="ns")
        self._results.configure(yscrollcommand=scroll.set)

        self._write_results(
            "Campus graph loaded. Pick a traversal or path algorithm and click a button."
        )

    def _run_bfs(self) -> None:
        start = self._start_choice.get()
        end = self._end_choice.get()
        path = self._campus.bfs(start, end)
        if path is None:
            self._write_results(f"No BFS path found between {start} and {end}.")
        else:
            self._write_results(
                f"BFS fewest-hops path from {start} to {end}:\n"
                f"{path}\n"
                f"Hops: {len(path) - 1}"
            )

    def _run_dfs(self) -> None:
        start = self._start_choice.get()
        order = self._campus.dfs(start)
        if not order:
            self._write_results(f"No DFS traversal from {start}.")
        else:
            self._write_results(
                f"DFS traversal from {start}:\n"
                f"{order}\n"
                f"Visited: {len(order)} nodes."
            )

    def _run_dijkstra(self) -> None:
        start = self._start_choice.get()
        end = self._end_choice.get()
        path, distance = self._campus.dijkstra(start, end)
        if path is None:
            self._write_results(f"No Dijkstra path found between {start} and {end}.")
        else:
            self._write_results(
                f"Dijkstra shortest path from {start} to {end}:\n"
                f"{path}\n"
                f"Distance: {distance}"
            )

    def _run_prim(self) -> None:
        start = self._start_choice.get()
        mst_edges, total_weight = self._campus.prim_mst(start)
        if not mst_edges:
            self._write_results(f"No MST could be built from {start}.")
        else:
            edge_lines = "\n".join(
                f"{u} - {v} : {w}" for u, v, w in mst_edges
            )
            self._write_results(
                f"Prim's MST starting from {start}:\n"
                f"{edge_lines}\n\n"
                f"Total weight: {total_weight}"
            )

    def _write_results(self, text: str) -> None:
        self._results.configure(state="normal")
        self._results.delete("1.0", tk.END)
        self._results.insert(tk.END, text)
        self._results.configure(state="disabled")


if __name__ == "__main__":
    campus = build_sample_campus_graph()

    print("BFS fewest hops:")
    print(campus.bfs("Library", "Parking Lot"))

    print("\nDFS traversal:")
    print(campus.dfs("Library"))

    print("\nDijkstra shortest path:")
    path, distance = campus.dijkstra("Library", "Parking Lot")
    print("Path:", path)
    print("Distance:", distance)

    print("\nPrim MST:")
    mst, total = campus.prim_mst("Library")
    print("MST edges:", mst)
    print("Total weight:", total)
