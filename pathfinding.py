from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

Pos = Tuple[int, int]  # (row, col)
Grid = List[List[str]]

EXAMPLE_MAP_1 = """
##########
#S..#....#
#..##.##.#
#...#...G#
##########
""".strip("\n")

EXAMPLE_MAP_2 = """
############
#S.....#...#
###.##.#.#.#
#...#..#.#G#
#.###..#...#
#......###.#
############
""".strip("\n")

EXAMPLE_MAP_3 = """
###########
#S........#
#.........#
#....#.#..#
#.....#...#
#........G#
###########
""".strip("\n")

GAME_MAP = """
############
#P....#....#
#.##..#.#..#
#....##.#G.#
#.##....#..#
#..M....#..#
############
""".strip("\n")

MODE = "BFS"  # Switch to "DFS" to make the monster chase less direct.


def parse_grid(text: str) -> Tuple[Grid, Pos, Pos]:
    """
    Convert a multiline string map into a grid plus start and goal positions.

    Map legend:
    '#' wall
    '.' floor
    'S' start (exactly one)
    'G' goal (exactly one)
    """
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Grid text is empty")

    width = len(lines[0])
    if any(len(line) != width for line in lines):
        raise ValueError("Grid must be rectangular")

    grid: Grid = [list(line) for line in lines]
    start: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                if start is not None:
                    raise ValueError("Grid must contain exactly one S")
                start = (r, c)
            elif ch == "G":
                if goal is not None:
                    raise ValueError("Grid must contain exactly one G")
                goal = (r, c)

    if start is None or goal is None:
        raise ValueError("Grid must contain exactly one S and one G")

    return grid, start, goal


def neighbors(grid: Grid, node: Pos) -> List[Pos]:
    """Return valid 4-direction neighbors that are not walls."""
    rows = len(grid)
    cols = len(grid[0])
    r, c = node
    result: List[Pos] = []

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            result.append((nr, nc))

    return result


def reconstruct_path(parent: Dict[Pos, Pos], start: Pos, goal: Pos) -> Optional[List[Pos]]:
    """Reconstruct path from start->goal using parent pointers. Return None if goal unreachable."""
    if start == goal:
        return [start]
    if goal not in parent:
        return None

    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def bfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Queue-based BFS.
    Return (path, visited).
    - path is a list of positions from start to goal (inclusive), or None.
    - visited contains all explored/seen nodes.
    """
    queue = deque([start])
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while queue:
        cur = queue.popleft()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in neighbors(grid, cur):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = cur
            queue.append(nxt)

    return None, visited


def dfs_path(grid: Grid, start: Pos, goal: Pos) -> Tuple[Optional[List[Pos]], Set[Pos]]:
    """
    Stack-based DFS (iterative, no recursion).
    Return (path, visited).
    """
    stack: List[Pos] = [start]
    visited: Set[Pos] = {start}
    parent: Dict[Pos, Pos] = {}

    while stack:
        cur = stack.pop()
        if cur == goal:
            return reconstruct_path(parent, start, goal), visited

        for nxt in neighbors(grid, cur):
            if nxt in visited:
                continue
            visited.add(nxt)
            parent[nxt] = cur
            stack.append(nxt)

    return None, visited


def render(grid: Grid, path: Optional[List[Pos]] = None, visited: Optional[Set[Pos]] = None) -> str:
    """
    Render the grid as text.
    Overlay rules:
    - path tiles shown as '*'
    - visited tiles shown as '+'
    - preserve 'S' and 'G'
    """
    canvas = [row[:] for row in grid]

    if visited:
        for r, c in visited:
            if canvas[r][c] in {".", "P", "M"}:
                canvas[r][c] = "+"

    if path:
        for r, c in path:
            if canvas[r][c] in {".", "+", "P", "M"}:
                canvas[r][c] = "*"

    return "\n".join("".join(row) for row in canvas)


def run_one(label: str, grid_text: str) -> None:
    grid, start, goal = parse_grid(grid_text)

    print("=" * 60)
    print(label)
    print("- Raw map")
    print(render(grid))

    path_bfs, visited_bfs = bfs_path(grid, start, goal)
    print("\n- BFS")
    print(f"found={path_bfs is not None} path_len={(len(path_bfs) if path_bfs else None)} visited={len(visited_bfs)}")
    print(render(grid, path=path_bfs, visited=visited_bfs))

    path_dfs, visited_dfs = dfs_path(grid, start, goal)
    print("\n- DFS")
    print(f"found={path_dfs is not None} path_len={(len(path_dfs) if path_dfs else None)} visited={len(visited_dfs)}")
    print(render(grid, path=path_dfs, visited=visited_dfs))


@dataclass
class GameState:
    grid: Grid
    player: Pos
    monster: Pos
    goal: Pos


def parse_game_map(text: str) -> GameState:
    lines = [line for line in text.splitlines() if line.strip()]
    grid = [list(line) for line in lines]

    player: Optional[Pos] = None
    monster: Optional[Pos] = None
    goal: Optional[Pos] = None

    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "P":
                player = (r, c)
                grid[r][c] = "."
            elif ch == "M":
                monster = (r, c)
                grid[r][c] = "."
            elif ch == "G":
                goal = (r, c)

    if player is None or monster is None or goal is None:
        raise ValueError("Game map must include one P, one M, and one G")

    return GameState(grid=grid, player=player, monster=monster, goal=goal)


def move_if_valid(grid: Grid, src: Pos, direction: str) -> Pos:
    delta = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1),
    }
    if direction not in delta:
        return src

    dr, dc = delta[direction]
    nr, nc = src[0] + dr, src[1] + dc
    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
        return nr, nc
    return src


def render_game(state: GameState) -> str:
    canvas = [row[:] for row in state.grid]
    pr, pc = state.player
    mr, mc = state.monster
    canvas[pr][pc] = "P"
    canvas[mr][mc] = "M"
    return "\n".join("".join(row) for row in canvas)


def game_loop(mode: str = MODE) -> None:
    state = parse_game_map(GAME_MAP)
    mode = mode.upper()
    if mode not in {"BFS", "DFS"}:
        raise ValueError("Mode must be BFS or DFS")

    print("=" * 60)
    print(f"Monster Chase (Turn-Based) mode={mode}")
    print("Move with WASD, then press Enter. q to quit.")

    while True:
        print(render_game(state))
        if state.player == state.monster:
            print("You were caught by the monster. You lose.")
            return
        if state.player == state.goal:
            print("You reached the exit. You win!")
            return

        cmd = input("move> ").strip().lower()
        if cmd == "q":
            print("Quit game.")
            return

        state.player = move_if_valid(state.grid, state.player, cmd[:1] if cmd else "")

        if state.player == state.monster:
            print(render_game(state))
            print("You ran into the monster. You lose.")
            return

        chase_grid = [row[:] for row in state.grid]
        pr, pc = state.player
        mr, mc = state.monster
        chase_grid[pr][pc] = "G"
        chase_grid[mr][mc] = "S"

        if mode == "BFS":
            path, _ = bfs_path(chase_grid, state.monster, state.player)
        else:
            path, _ = dfs_path(chase_grid, state.monster, state.player)

        if path and len(path) >= 2:
            state.monster = path[1]

        if state.player == state.monster:
            print(render_game(state))
            print("The monster reached you. You lose.")
            return


def main() -> None:
    run_one("Example Map 1", EXAMPLE_MAP_1)
    run_one("Example Map 2", EXAMPLE_MAP_2)
    run_one("Example Map 3 (DFS is longer)", EXAMPLE_MAP_3)

    print("\nTip: run game_loop('BFS') or game_loop('DFS') from a Python shell to play Monster Chase.")


if __name__ == "__main__":
    main()
