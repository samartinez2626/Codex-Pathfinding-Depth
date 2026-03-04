# BFS + DFS Pathfinding (Python Console)

## Run
```bash
python pathfinding.py
```

## What to look for
- BFS returns a shortest path in this unweighted 4-neighbor grid.
- DFS may return a longer path depending on exploration order.
- Output prints found, path length, and visited node count for each algorithm.

## Files
- `pathfinding.py`: BFS/DFS implementations, render helpers, and a simple turn-based "Monster Chase" demo.
- `AGENTS.md`: repository rules for safe Codex iteration.

## Reflection (comparison summary)
### 1) Example where DFS path is longer
`Example Map 3` in `pathfinding.py` is intentionally shaped so DFS follows a deeper branch before reaching the goal. In this map, BFS finds a shorter route while DFS still finds a valid route, but with more steps.

### 2) Visited count comparison
BFS often visits many nodes in a wavefront because it expands by distance layers. DFS can visit fewer or more nodes depending on branch order and where the goal is relative to the first deep branch explored.

### 3) Why BFS is shortest-path here but DFS is not
Each move has equal cost (1 step), so the grid is an unweighted graph. BFS explores all nodes at distance `d` before distance `d+1`, guaranteeing the first time it reaches `G` is via a shortest path. DFS does not preserve distance layers; it commits to one branch deeply, so the first found goal can be suboptimal.

## Monster Chase (required idea)
`pathfinding.py` includes `game_loop(mode="BFS"|"DFS")`:
- Player (`P`) moves with WASD.
- Monster (`M`) recomputes a path to player each turn using BFS or DFS mode.
- Monster advances one step along that path.
- Lose if the monster reaches player; win if player reaches `G`.

Try in a Python shell:
```python
from pathfinding import game_loop
game_loop("BFS")
```
