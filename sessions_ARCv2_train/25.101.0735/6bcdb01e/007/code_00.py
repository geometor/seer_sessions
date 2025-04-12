"""
Transformation Rule Natural Language Description:

1.  Identify Boundaries and Sources: Locate all cells with value '8' (boundaries) and value '3' (sources) in the input grid.
2.  Determine Reachable Region (R): Find the set `R` containing all grid cells `(r, c)` reachable from any source '3' cell via paths of adjacent non-'8' cells, using a Breadth-First Search (BFS).
3.  Create Intermediate Grid (Initial Fill):
    a.  Create a new grid, `intermediate_grid`, as a deep copy of the `input_grid`.
    b.  Iterate through each cell `(r, c)` in the `intermediate_grid`.
    c.  If the cell `(r, c)` is within region `R` *and* its value in the `input_grid` was '7', set `intermediate_grid[r][c] = 3`. (Otherwise, it retains its copied value).
4.  Create Final Output Grid (Hole Preservation):
    a.  Create the `output_grid` as a deep copy of the `intermediate_grid`.
    b.  Iterate through each cell `(r, c)` in the grid.
    c.  Check if this cell `(r, c)` was originally a '7' in the `input_grid` *and* belongs to region `R`.
    d.  If both conditions in (c) are true, check the "hole preservation" rule:
        i.  Verify that the cell is not in the first row or first column (`r > 0` and `c > 0`).
        ii. Define the 2x2 block ending at `(r, c)` using coordinates: `tl=(r-1,c-1)`, `tc=(r-1,c)`, `bl=(r,c-1)`, `br=(r,c)`.
        iii. Check if *all four* cells in this 2x2 block have the value '3' in the `intermediate_grid`.
        iv. Check if *all four* corresponding cells in the `input_grid` had non-'8' values.
        v. Check if *all four* corresponding cells belong to the region `R`.
        vi. If *all* conditions (i) through (v) are met, then this cell forms a "hole": set `output_grid[r][c] = 7` (reverting it from the '3' in the intermediate grid).
5.  Finalize: The `output_grid`, after checking all relevant cells for potential reversion in step 4, is the final result.
"""

import copy
from collections import deque

def find_connected_region(grid: list[list[int]], sources: list[tuple[int, int]]) -> set[tuple[int, int]]:
    """
    Finds the connected region of non-8 cells reachable from source cells using BFS.

    Args:
        grid: The input grid.
        sources: A list of (row, col) tuples representing the starting '3' cells.

    Returns:
        A set of (row, col) tuples representing the connected region R.
    """
    rows = len(grid)
    cols = len(grid[0])
    region_r = set()
    queue = deque()
    visited = set()

    # Initialize queue and visited set with sources that are not '8'
    for r, c in sources:
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] != 8:
            if (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))
                # Add sources to region R immediately if they are valid
                region_r.add((r, c))

    # BFS to find all reachable non-8 cells
    while queue:
        r, c = queue.popleft()
        # Add current cell to region (if not already added as a source)
        region_r.add((r,c))

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited and not an '8' wall
                if (nr, nc) not in visited and grid[nr][nc] != 8:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    # Add valid neighbors to region R as they are found and added to queue
                    region_r.add((nr, nc))

    return region_r


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # 1. Identify Sources
    sources = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 3:
                sources.append((r, c))

    # 2. Determine Reachable Region (R)
    region_r = find_connected_region(input_grid, sources)

    # 3. Create Intermediate Grid (Initial Fill)
    intermediate_grid = copy.deepcopy(input_grid)
    for r in range(rows):
        for c in range(cols):
            if (r, c) in region_r and input_grid[r][c] == 7:
                intermediate_grid[r][c] = 3

    # 4. Create Final Output Grid (Hole Preservation)
    output_grid = copy.deepcopy(intermediate_grid)
    for r in range(rows):
        for c in range(cols):
            # Check if this cell could potentially be reverted to 7
            if input_grid[r][c] == 7 and (r, c) in region_r:
                # Check the "hole preservation" rule based on 2x2 block
                # Condition i: Check bounds
                if r > 0 and c > 0:
                    # Coordinates of the 2x2 block ending at (r, c)
                    tl, tc, bl, br = (r - 1, c - 1), (r - 1, c), (r, c - 1), (r, c)

                    # Condition iii: Check if the 2x2 block in the *intermediate* grid is all '3's
                    if (intermediate_grid[tl[0]][tl[1]] == 3 and
                            intermediate_grid[tc[0]][tc[1]] == 3 and
                            intermediate_grid[bl[0]][bl[1]] == 3 and
                            intermediate_grid[br[0]][br[1]] == 3):

                        # Condition iv: Check if the corresponding 2x2 block in the *input* grid was all non-'8's
                        if (input_grid[tl[0]][tl[1]] != 8 and
                                input_grid[tc[0]][tc[1]] != 8 and
                                input_grid[bl[0]][bl[1]] != 8 and
                                input_grid[br[0]][br[1]] != 8): # br was 7, so != 8

                            # Condition v: Check if all four cells of the block belong to region R
                            if (tl in region_r and
                                    tc in region_r and
                                    bl in region_r and
                                    br in region_r): # br is known to be in R

                                # All conditions met, revert this cell to '7' in the final output
                                output_grid[r][c] = 7

    # 5. Finalize
    return output_grid