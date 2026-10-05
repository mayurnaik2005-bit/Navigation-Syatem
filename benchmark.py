import time
import random
import matplotlib.pyplot as plt
from engine import StoreEngine

def build_random_graph(V, dense=False):
    g = StoreEngine(V)
    p = 0.5 if dense else (4.0 / V if V > 4 else 0.8)
    for i in range(V):
        for j in range(i + 1, V):
            if random.random() < p:
                g.add_aisle(i, j, random.randint(1, 25))
    return g

def run_benchmarks():
    sizes = [20, 50, 100, 150, 200]
    dijkstra_sparse, bellman_sparse = [], []
    dijkstra_dense, bellman_dense = [], []

    print("Running benchmarks across graph topologies...")
    for v in sizes:
        # Sparse Graph
        g_s = build_random_graph(v, dense=False)
        t0 = time.perf_counter()
        g_s.dijkstra(0)
        dijkstra_sparse.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        g_s.bellman_ford(0)
        bellman_sparse.append(time.perf_counter() - t0)

        # Dense Graph
        g_d = build_random_graph(v, dense=True)
        t0 = time.perf_counter()
        g_d.dijkstra(0)
        dijkstra_dense.append(time.perf_counter() - t0)

        t0 = time.perf_counter()
        g_d.bellman_ford(0)
        bellman_dense.append(time.perf_counter() - t0)

    # Plot comparison
    plt.figure(figsize=(9, 5))
    plt.plot(sizes, dijkstra_sparse, 'g-o', label='Dijkstra (Sparse O((V+E)logV))')
    plt.plot(sizes, dijkstra_dense, 'g--s', label='Dijkstra (Dense)')
    plt.plot(sizes, bellman_sparse, 'r-^', label='Bellman-Ford (Sparse O(VE))')
    plt.plot(sizes, bellman_dense, 'r--x', label='Bellman-Ford (Dense)')
    plt.xlabel('Number of Vertices (|V|)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('AOA Empirical Benchmark: Dijkstra vs. Bellman-Ford')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("complexity_benchmark.png")
    print("Benchmark completed. Saved graph as 'complexity_benchmark.png'")
    plt.show()

if __name__ == "__main__":
    run_benchmarks()