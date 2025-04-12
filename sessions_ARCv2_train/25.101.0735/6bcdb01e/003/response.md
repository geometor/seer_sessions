```python
import copy
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  **Identify Boundaries and Sources:** Locate all cells with value '8' (boundaries) and value '3' (sources) in the input grid.
2.  **Determine Reachable Region (R):** Find the set `R` containing all grid cells `(r, c)` that satisfy:
    *   The input value `input_grid[r][c]` is not '8'.
    *   There exists a path from at least one source '3' cell to `(r, c)` consisting only of adjacent cells (up, down, left, right) whose input values are not '8'.
3.  **Initialize Output Grid:** Create an output grid, initially identical to the input grid.
4.  **Apply Transformation:** Iterate through each cell `(r, c)` in the grid.
    a.  If the cell `(r, c)` is *not* part of the reachable region `R`, its value in the output grid remains the same as its input value.
    b.  If the cell `(r, c)` *is* part of the reachable region `R`:
        i.  If the input value `input_grid[r][c]` is '3', the output value `output_grid[r][c]` remains '3'.
        ii. If the input value `input_grid[r][c]` is '7', determine the output value based on adjacent cells:
            - Check all 4 adjacent neighbors `(nr, nc)` of `(r, c)`.
            - If *at least one* neighbor `(nr, nc)` exists such that:
                1) It is within the grid boundaries.
                2) Its input value `input_grid[nr][nc]` is '7'.
                3) It is also part of the reachable region `R`.
            - Then, the cell `(r, c)` retains its value '7' in the output grid (it forms part of a "hole" or preserved '7' cluster).
            - Otherwise (if no such adjacent neighbor exists), the cell's value is changed to '3' in the output grid.
5.  **Finalize Output:** The resulting grid after applying these rules is the final output.
"""

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
                region_r.add((r, c)) # Add initial sources to region R

    # BFS to find all reachable non-8 cells
    while queue:
        r, c = queue.popleft()
        region_r.add((r, c)) # Add the current cell to region R

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited and not an '8' wall
                if (nr, nc) not in visited and grid[nr][nc] != 8:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    # Note: We add neighbors to region_r when they are popped from queue
                    # This ensures initial sources are correctly included if they are isolated non-8s

    return region_r


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid based on reachability
    from '3' cells and local neighborhood patterns for '7' cells within the
    reachable region.
    """
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)

    # Find initial '3' source cells
    sources = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 3:
                sources.append((r, c))

    # Determine the connected region R reachable from sources, avoiding '8's
    region_r = find_connected_region(input_grid, sources)

    # perform transformations based on region R and neighbor rules
    for r in range(rows):
        for c in range(cols):
            # Only consider cells within the reachable region R
            if (r, c) in region_r:
                # If the cell is originally '7' in the input grid
                if input_grid[r][c] == 7:
                    # Check neighbors to see if this '7' should be preserved
                    preserve_as_7 = False
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        # Check neighbor bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is also '7' in input and in region R
                            if input_grid[nr][nc] == 7 and (nr, nc) in region_r:
                                preserve_as_7 = True
                                break # Found one such neighbor, no need to check further

                    # If no suitable neighbor found, change to '3'
                    if not preserve_as_7:
                        output_grid[r][c] = 3
                    # Else: it remains '7' (already set during deepcopy)

            # Cells outside region R retain their original input values (already handled by deepcopy)
            # Cells inside region R that were originally '3' or '8' also retain original values

    return output_grid
```