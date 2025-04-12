"""
Transformation Rule Natural Language Description:

1.  Identify Boundaries and Sources: Locate all cells with value '8' (boundaries) and value '3' (sources) in the input grid.
2.  Determine Reachable Region (R): Find the set `R` containing all grid cells `(r, c)` that satisfy:
    *   The input value `input_grid[r][c]` is not '8'.
    *   There exists a path from at least one source '3' cell to `(r, c)` consisting only of adjacent cells (up, down, left, right) whose input values are not '8'. Use a Breadth-First Search (BFS) starting from all source '3' cells.
3.  Initialize Output Grid: Create an output grid, making a deep copy of the input grid.
4.  Apply Transformation with Hole Prevention: Iterate through each cell `(r, c)` of the grid (e.g., row by row, column by column).
    a.  Check if the current cell `(r, c)` is within the determined region `R` *and* its value in the input grid `input_grid[r][c]` is '7'.
    b.  If both conditions in (a) are true:
        i.  Tentatively set the corresponding cell in the output grid to '3': `output_grid[r][c] = 3`.
        ii. Check if this change *completed* a "forbidden" 2x2 block ending at `(r, c)`. A block is forbidden if:
            *   The cell is not in the first row or first column (`r > 0` and `c > 0`).
            *   All four cells forming the 2x2 block ending at `(r, c)` in the **output grid** now have the value '3' (i.e., `output_grid[r-1][c-1]`, `output_grid[r-1][c]`, `output_grid[r][c-1]`, and `output_grid[r][c]` are all '3').
            *   All four corresponding cells in the **input grid** had non-'8' values.
            *   All four corresponding cells belong to the region `R`.
        iii. If all conditions for a forbidden 2x2 block are met, revert the change: set `output_grid[r][c]` back to '7'.
5.  Finalize Output: The output grid, after iterating through all cells and applying the tentative fill and potential reversion, is the final result. Cells not modified in step 4 retain their initial values from the input grid (handled by the initial deep copy).
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
        # No need to add here, added when dequeued if source or when added to queue

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited and not an '8' wall
                if (nr, nc) not in visited and grid[nr][nc] != 8:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    # Add valid neighbors to region R as they are found
                    region_r.add((nr, nc))
                    
    return region_r


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # initialize output_grid as a deep copy of input_grid
    output_grid = copy.deepcopy(input_grid)

    # Find initial '3' source cells
    sources = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 3:
                sources.append((r, c))

    # Determine the connected region R reachable from sources, avoiding '8's
    region_r = find_connected_region(input_grid, sources)

    # Iterate through the grid and apply transformation rules
    for r in range(rows):
        for c in range(cols):
            # Consider only cells that are originally '7' and within the reachable region R
            if input_grid[r][c] == 7 and (r, c) in region_r:
                # Tentatively change the cell to '3' in the output
                output_grid[r][c] = 3

                # Check for the 2x2 hole condition (preventing 2x2 blocks of 3s under certain conditions)
                is_hole = False
                if r > 0 and c > 0:
                    # Coordinates of the 2x2 block ending at (r, c)
                    tl, tc, bl, br = (r - 1, c - 1), (r - 1, c), (r, c - 1), (r, c)

                    # Condition 1: Check if the 2x2 block in the *output* grid consists entirely of '3's
                    if (output_grid[tl[0]][tl[1]] == 3 and
                            output_grid[tc[0]][tc[1]] == 3 and
                            output_grid[bl[0]][bl[1]] == 3 and
                            output_grid[br[0]][br[1]] == 3): # Current cell is already set to 3

                        # Condition 2: Check if the corresponding 2x2 block in the *input* grid was all non-'8's
                        if (input_grid[tl[0]][tl[1]] != 8 and
                                input_grid[tc[0]][tc[1]] != 8 and
                                input_grid[bl[0]][bl[1]] != 8 and
                                input_grid[br[0]][br[1]] != 8): # Current cell was 7, so != 8

                            # Condition 3: Check if all four cells of the block belong to region R
                            if (tl in region_r and
                                    tc in region_r and
                                    bl in region_r and
                                    br in region_r): # Current cell (br) is known to be in R
                                
                                # If all conditions met, this cell should revert to '7'
                                is_hole = True

                # If the conditions for being a hole (reverting to 7) are met
                if is_hole:
                    output_grid[r][c] = 7
                # Otherwise, it remains '3' (as set tentatively above)

            # Cells outside region R, or originally '3' or '8' inside R, retain their original values (handled by deepcopy initially)

    return output_grid