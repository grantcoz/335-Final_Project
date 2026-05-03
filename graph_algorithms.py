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
