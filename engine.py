import heapq
import numpy as np

class StoreEngine:
    def __init__(self, vertices):
        self.V = vertices
        self.adj = {i: [] for i in range(vertices)}
        self.edges = []
        self.matrix = [[float('inf')] * vertices for _ in range(vertices)]
        for i in range(vertices):
            self.matrix[i][i] = 0

    def add_aisle(self, u, v, weight, bidirectional=True):
        self.adj[u].append((v, weight))
        self.edges.append((u, v, weight))
        self.matrix[u][v] = weight
        if bidirectional:
            self.adj[v].append((u, weight))
            self.edges.append((v, u, weight))
            self.matrix[v][u] = weight

    def dijkstra(self, start):
        """Single-Source Shortest Path using Min-Heap: O((V + E) log V)"""
        distances = [float('inf')] * self.V
        predecessors = [-1] * self.V
        distances[start] = 0
        pq = [(0, start)]

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if curr_dist > distances[u]:
                continue
            for v, weight in self.adj[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (distances[v], v))
        return distances, predecessors

    def bellman_ford(self, start):
        """Single-Source Shortest Path with Negative Weight Cycle Detection: O(V * E)"""
        distances = [float('inf')] * self.V
        predecessors = [-1] * self.V
        distances[start] = 0

        # Relax edges V - 1 times
        for _ in range(self.V - 1):
            updated = False
            for u, v, weight in self.edges:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    updated = True
            if not updated:
                break

        # Check for negative weight cycles
        for u, v, weight in self.edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                raise ValueError("Graph contains a negative weight cycle!")
        return distances, predecessors

    def floyd_warshall(self):
        """All-Pairs Shortest Path: O(V^3)"""
        dist = [row[:] for row in self.matrix]
        for k in range(self.V):
            for i in range(self.V):
                for j in range(self.V):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    def optimize_shopping_list_dp(self, entrance, item_nodes):
        """Exact Multi-Item Route Planning via Held-Karp Dynamic Programming"""
        apsp = self.floyd_warshall()
        nodes = [entrance] + [n for n in item_nodes if n != entrance]
        n = len(nodes)
        node_map = {idx: nodes[idx] for idx in range(n)}
        
        memo = {}

        def visit(mask, u):
            if mask == (1 << n) - 1:
                return 0, [node_map[u]]
            state = (mask, u)
            if state in memo:
                return memo[state]

            best_cost = float('inf')
            best_path = []
            for v in range(n):
                if not (mask & (1 << v)):
                    sub_cost, sub_path = visit(mask | (1 << v), v)
                    total_cost = apsp[node_map[u]][node_map[v]] + sub_cost
                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_path = [node_map[u]] + sub_path

            memo[state] = (best_cost, best_path)
            return memo[state]

        cost, path = visit(1, 0)
        return path, cost