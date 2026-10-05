import heapq
import networkx as nx
import matplotlib.pyplot as plt

class StoreNavigator:
    def __init__(self, node_count):
        self.V = node_count
        self.adj = {i: [] for i in range(node_count)}
        self.edges = []

    def add_aisle(self, u, v, weight):
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
        self.edges.append((u, v, weight))

    def dijkstra(self, start_node):
        distances = [float('inf')] * self.V
        predecessors = [-1] * self.V
        distances[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            curr_d, u = heapq.heappop(pq)
            if curr_d > distances[u]:
                continue
            for v, weight in self.adj[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (distances[v], v))
        return distances, predecessors

    def get_path(self, predecessors, destination):
        path = []
        curr = destination
        while curr != -1:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        return path

# 1. Initialize a 6-node store floorplan
store = StoreNavigator(6)
store.add_aisle(0, 1, 4)  # 0: Entrance, 1: Bakery
store.add_aisle(0, 2, 2)  # 2: Produce
store.add_aisle(1, 2, 1)
store.add_aisle(1, 3, 5)  # 3: Dairy
store.add_aisle(2, 3, 8)
store.add_aisle(2, 4, 10) # 4: Beverages
store.add_aisle(3, 5, 6)  # 5: Checkout
store.add_aisle(4, 5, 2)

# 2. Calculate shortest route from Entrance (0) to Checkout (5)
dists, preds = store.dijkstra(0)
optimal_route = store.get_path(preds, 5)

print(f"Optimal Path: {optimal_route}")
print(f"Total Distance/Time Cost: {dists[5]}")

# 3. Render and save the store graph
G = nx.Graph()
for u, v, w in store.edges:
    G.add_edge(u, v, weight=w)

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(7, 5))
nx.draw_networkx(G, pos, node_color='lightblue', node_size=700, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Highlight calculated route
route_edges = [(optimal_route[i], optimal_route[i+1]) for i in range(len(optimal_route)-1)]
nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', width=3)

plt.title("Store Indoor Route: Entrance to Checkout")
plt.savefig("store_route.png")
print("Visual map saved as 'store_route.png'.")
plt.show()