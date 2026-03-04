# AGENTS.md

## Project Goal
Teach grid pathfinding by implementing:
- BFS using a queue (`collections.deque`)
- DFS using a stack (Python list, iterative only)

## Rules for Codex
- Modify only existing files (`pathfinding.py`, `README.md`, `AGENTS.md`).
- Do not change function signatures in `pathfinding.py`.
- DFS must be iterative (no recursion).
- BFS must use `collections.deque`.
- Use `visited: set[(r, c)]` and `parent: dict[child] = parent`.
- Mark visited when enqueued/pushed.
- Keep changes minimal and keep `main()` runnable.

## Output Contract
Running `python pathfinding.py` must:
- run BFS and DFS on at least 2 maps
- print found/path length/visited count
- print rendered maps with overlays

## Student Workflow Tips
- Put repo rules here first so Codex follows them consistently.
- If Codex goes off track, paste failing output and ask: "follow AGENTS.md, minimal diff, fix only X".
