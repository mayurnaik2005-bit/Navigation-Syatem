from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from engine import StoreEngine

app = FastAPI(
    title="Indoor Navigation & Layout Engine",
    version="1.0.0",
    description="Dynamic Indoor Spatial Routing & Optimization API"
)

# Initialize a default 10-zone store layout
store = StoreEngine(10)
# Aisle network setup
connections = [
    (0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8),
    (2, 4, 10), (3, 5, 6), (4, 5, 2), (5, 6, 3), (6, 7, 4),
    (7, 8, 2), (8, 9, 3), (5, 9, 7)
]
for u, v, w in connections:
    store.add_aisle(u, v, w)

class RouteRequest(BaseModel):
    source: int = Field(..., ge=0, lt=10, description="Start node ID")
    destination: int = Field(..., ge=0, lt=10, description="Target node ID")
    algorithm: str = Field("dijkstra", description="'dijkstra' or 'bellman-ford'")

class DynamicWeightUpdate(BaseModel):
    u: int = Field(..., ge=0, lt=10)
    v: int = Field(..., ge=0, lt=10)
    new_weight: float = Field(..., description="Congestion or discount adjusted weight")

class ShoppingListRequest(BaseModel):
    entrance: int = Field(0, ge=0, lt=10)
    items: List[int] = Field(..., min_length=1, description="List of shelf node IDs")

@app.post("/api/route", status_code=status.HTTP_200_OK)
def get_route(payload: RouteRequest):
    try:
        if payload.algorithm.lower() == "bellman-ford":
            dists, preds = store.bellman_ford(payload.source)
        else:
            dists, preds = store.dijkstra(payload.source)

        if dists[payload.destination] == float('inf'):
            raise HTTPException(status_code=404, detail="Destination unreachable")

        # Reconstruct path
        path = []
        curr = payload.destination
        while curr != -1:
            path.append(curr)
            curr = preds[curr]
        path.reverse()

        return {
            "source": payload.source,
            "destination": payload.destination,
            "optimal_path": path,
            "total_travel_cost": dists[payload.destination],
            "algorithm_used": payload.algorithm
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/aisle/update", status_code=status.HTTP_200_OK)
def update_aisle(payload: DynamicWeightUpdate):
    store.add_aisle(payload.u, payload.v, payload.new_weight)
    return {"message": f"Aisle ({payload.u}, {payload.v}) updated to weight {payload.new_weight}"}

@app.post("/api/optimize-shopping-list", status_code=status.HTTP_200_OK)
def optimize_list(payload: ShoppingListRequest):
    path, cost = store.optimize_shopping_list_dp(payload.entrance, payload.items)
    return {
        "entrance": payload.entrance,
        "items_to_visit": payload.items,
        "optimized_itinerary": path,
        "total_cost": cost,
        "strategy": "Held-Karp Dynamic Programming (Exact Solution)"
    }
from fastapi.responses import FileResponse

@app.get('/')
async def serve_frontend():
    return FileResponse('index.html')
