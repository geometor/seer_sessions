
## train_1

**input:**
```
8 7 7 8 7 8 7
7 8 8 7 7 7 8
7 7 7 7 7 7 7
7 7 7 7 7 7 8
7 7 7 7 7 8 7
3 3 7 7 8 7 7
7 7 7 8 7 7 7
```


**output:**
```
8 7 7 8 7 8 7
7 8 8 3 3 3 8
7 7 7 3 7 3 7
3 3 3 3 3 3 8
7 7 7 3 7 8 7
3 3 3 3 8 7 7
7 7 7 8 7 7 7
```


## train_2

**input:**
```
7 8 7 8 7
8 7 7 7 8
7 7 7 7 7
7 3 7 7 8
7 3 7 8 7
```


**output:**
```
7 8 7 8 7
8 3 3 3 8
7 3 7 3 7
3 3 3 3 8
7 3 7 8 7
```

**Perception of Task Elements:**

1.  **Input/Output:** Both input and output are grids (matrices) of single-digit integers.
2.  **Grid Size:** The dimensions of the grid remain unchanged from input to output (7x7 for `train_1`, 5x5 for `train_2`).
3.  **Values:** The grids contain primarily the digits 3, 7, and 8.
4.  **Transformation:** The core transformation appears to involve changing some '7' cells to '3' cells. The '8' cells and the initial '3' cells seem to act as constraints or starting points.
5.  **Role of Numbers:**
    *   `8`: Acts as an impenetrable boundary or wall. These cells never change value.
    *   `3`: Acts as a starting "seed" or source for a change. Input '3's generally remain '3' or are part of a larger '3' region in the output.
    *   `7`: Represents a "fillable" or potentially changeable state. Some '7's are changed to '3's based on their relationship to the initial '3's and the '8' boundaries.
6.  **Pattern:** The change seems related to connectivity. A connected region is formed based on the initial '3's and the fillable '7's, bounded by the '8's. Cells within this region are potentially changed to '3'. However, not all '7's within this connected region change; some remain '7', forming "holes" or unchanged areas within the affected region.

**YAML Facts:**

```
yaml
task_elements:
  - object: grid
    properties:
      - type: matrix
      - content: single-digit integers (3, 7, 8)
      - size: variable (e.g., 7x7, 5x5), consistent between input and output
  - object: cell
    properties:
      - value: 3, 7, or 8
      - role:
        - 8: boundary/wall (static)
        - 3: seed/source (initiates change)
        - 7: fillable/changeable state
relationships:
  - type: connectivity
    description: Cells are connected to their 4 adjacent neighbours (up, down, left, right).
  - type: boundary
    description: Connectivity is blocked by cells with value 8.
actions:
  - action: identify_component
    description: Find the connected component of non-8 cells that includes at least one initial '3' cell.
  - action: modify_value
    description: Change the value of certain '7' cells within the identified component to '3'.
    condition: The exact condition for changing a '7' to a '3' within the component is complex and seems to depend on the cell's position relative to boundaries and potentially other cells within the component, leaving some '7's unchanged ("holes").

```

**Natural Language Program:**

1.  Start with the input grid. Create an output grid, initially identical to the input.
2.  Identify all cells in the input grid that contain the value '8'. These are immutable walls. The corresponding cells in the output grid will also be '8'.
3.  Identify all cells in the input grid that contain the value '3'. These are the "source" cells.
4.  Determine the connected region `R` consisting of all non-'8' cells that are reachable from at least one source '3' cell by moving only through adjacent non-'8' cells.
5.  Modify the output grid based on region `R`:
    a.  For any cell `(r, c)` that is *not* in region `R`, its value in the output grid remains the same as its input value (it will be either an '8' or a '7' that wasn't reachable from a '3').
    b.  For any cell `(r, c)` that *is* in region `R`:
        i.  If the input value `input[r][c]` was '3', the output value `output[r][c]` is '3'.
        ii. If the input value `input[r][c]` was '7', apply a specific rule to determine if the output should be '3' or remain '7'. This rule appears to change most '7's in `R` to '3', but preserves certain '7's as '7' (creating "holes"), potentially based on their local neighbourhood configuration or distance from the region's boundary (further investigation needed to specify the exact rule for these exceptions). A likely candidate rule is that a '7' remains '7' only if it is sufficiently "interior" within the region R, meaning it's not adjacent to any '8' wall or grid boundary, although the precise definition might be more complex. All other '7's in R become '3'.
```python
import copy
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  Identify the connected region `R` of all non-'8' cells reachable from any initial '3' cell by moving only through adjacent non-'8' cells (up, down, left, right).
2.  Initialize the output grid as a copy of the input grid.
3.  Iterate through each cell `(r, c)` in the grid.
4.  If the cell `(r, c)` belongs to the identified region `R` and its value in the input grid is '7':
    a. Check if the 2x2 block ending at `(r, c)` (i.e., cells `(r-1, c-1)`, `(r-1, c)`, `(r, c-1)`, and `(r, c)`) satisfies the following conditions:
        i.   The cell is not in the first row or first column (`r > 0` and `c > 0`).
        ii.  All four cells in the 2x2 block had non-'8' values in the input grid.
        iii. All four cells in the 2x2 block belong to the connected region `R`.
    b. If all conditions in step 4a are met, the cell `(r, c)` retains its value '7' in the output grid (it forms a "hole").
    c. Otherwise (if the cell is on the border, or the 2x2 block contains an '8', or any cell in the 2x2 block is outside region `R`), the cell's value is changed to '3' in the output grid.
5.  Cells not in region `R` (original '8's or '7's/ '3's not reachable from an initial '3') retain their original values.
6.  Initial '3' cells within region `R` also retain their value '3'.
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
                region_r.add((r, c))

    # BFS
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is not visited, not an '8'
                if (nr, nc) not in visited and grid[nr][nc] != 8:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    region_r.add((nr, nc))

    return region_r

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies a connected region R from '3' sources avoiding '8's.
    Changes '7's in R to '3's, unless they form a specific 2x2 pattern
    of non-'8' cells entirely within R.
    """
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # Initialize output_grid as a deep copy of input_grid
    output_grid = copy.deepcopy(input_grid)

    # Find initial '3' source cells
    sources = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 3:
                sources.append((r, c))

    # Find the connected region R
    region_r = find_connected_region(input_grid, sources)

    # Iterate through the grid and apply transformation rules
    for r in range(rows):
        for c in range(cols):
            # Check if the cell is a '7' within the connected region R
            if (r, c) in region_r and input_grid[r][c] == 7:
                # Check the 2x2 block condition (Hypothesis 9) for keeping it '7'
                is_hole = False
                if r > 0 and c > 0:
                    # Define the coordinates of the 2x2 block ending at (r, c)
                    tl, tc, bl, br = (r - 1, c - 1), (r - 1, c), (r, c - 1), (r, c)

                    # Check if all cells in the block are non-8 in the input
                    # (input[br] is known to be 7, hence non-8)
                    if (input_grid[tl[0]][tl[1]] != 8 and
                            input_grid[tc[0]][tc[1]] != 8 and
                            input_grid[bl[0]][bl[1]] != 8):

                        # Check if all cells in the block are within region R
                        # (br is known to be in region_r)
                        if (tl in region_r and
                                tc in region_r and
                                bl in region_r):
                            is_hole = True

                # If it's not a hole, change it to '3'
                if not is_hole:
                    output_grid[r][c] = 3

    return output_grid
```
