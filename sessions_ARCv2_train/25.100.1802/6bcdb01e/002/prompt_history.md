
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

## Perception

1.  **Data Format:** The input and output are grids (2D arrays or matrices) containing single-digit integer values.
2.  **Grid Dimensions:** The dimensions of the output grid are identical to the dimensions of the input grid for each example.
3.  **Values:** The grids primarily contain the numbers 7 and 8. The number 3 also appears, both in the input and more extensively in the output.
4.  **Transformation Pattern:** Many grid cells retain their original value from input to output. The primary change involves the value 7 being replaced by the value 3 in certain locations. The value 8 appears unchanged between input and output.
5.  **Origin of Change:** The new 3s in the output seem to originate or spread from the locations where 3s were present in the input.
6.  **Spread Mechanism:** The value 3 appears to "flood fill" or propagate into adjacent (up, down, left, right) cells.
7.  **Propagation Rules:**
    *   The fill only replaces cells containing the value 7.
    *   The fill does not replace cells containing the value 8. 8s act as barriers.
    *   The fill does not extend beyond the grid boundaries.
    *   The propagation seems iterative: a 7 changed to a 3 can then cause its adjacent 7s to change to 3 in the next step, until no more 7s are adjacent to any 3s.

## Facts


```yaml
objects:
  - grid:
      description: A 2D array of integer values.
      properties:
        - rows: Number of rows.
        - columns: Number of columns.
        - cells: Individual elements within the grid.
  - cell:
      description: An element within the grid at a specific position.
      properties:
        - row_index: The vertical position (0-based).
        - column_index: The horizontal position (0-based).
        - value: The integer contained in the cell (e.g., 3, 7, 8).
relationships:
  - adjacency: Cells sharing an edge (up, down, left, right) are adjacent.
  - boundary: The edges of the grid define its limits.
  - barrier: Cells with value 8 prevent the propagation of value 3.
properties:
  - fill_value: The value 3, which spreads.
  - target_value: The value 7, which can be replaced by the fill_value.
  - barrier_value: The value 8, which blocks the spread.
actions:
  - identify_initial_fill_cells: Find all cells in the input grid with the fill_value (3).
  - propagate_fill: Iteratively change adjacent target_value (7) cells to the fill_value (3), starting from the initial fill cells and continuing from newly filled cells.
  - respect_barriers: Do not change cells with the barrier_value (8).
  - respect_boundaries: Do not attempt to fill outside the grid limits.
```


## Natural Language Program

1.  Initialize the output grid as a direct copy of the input grid.
2.  Identify all cells in the input grid that contain the value 3. Maintain a list or set of coordinates for these "active" 3-cells.
3.  Start an iterative process:
    a.  Create an empty list for newly changed cells in the current iteration.
    b.  For each active 3-cell coordinate identified in the previous step (or the initial identification):
        i.  Examine its adjacent neighbors (up, down, left, right).
        ii. For each neighbor within the grid boundaries:
            *   If the neighbor cell in the *output* grid currently contains the value 7:
                *   Change the value of this neighbor cell in the *output* grid to 3.
                *   Add the coordinates of this newly changed cell to the list for the current iteration.
    c.  Replace the list of active 3-cells with the list of newly changed cells from this iteration.
    d.  If no cells were changed in this iteration (the list of newly changed cells is empty), stop the process.
    e.  Otherwise, repeat from step 3a.
4.  The final state of the output grid is the result of the transformation.
```python
import copy
from collections import deque

"""
Flood fill transformation:
1. Copy the input grid to create the output grid.
2. Identify all cells initially containing the value 3 (fill_value).
3. Use a queue-based iterative process (like Breadth-First Search) to propagate the fill_value (3).
4. In each step, check the neighbors (up, down, left, right) of the cells currently containing the fill_value.
5. If a neighbor cell contains the target_value (7) and is within the grid boundaries, change its value to the fill_value (3) and add it to the queue for further propagation in the next iteration.
6. Cells with the barrier_value (8) block the propagation; they are neither changed nor allow propagation through them.
7. Continue the process until the queue is empty, meaning no more target_value cells are adjacent to fill_value cells.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a flood fill transformation where the value 3 propagates
    into adjacent cells containing 7, stopping at cells containing 8
    or the grid boundaries.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)

    # Define the values
    fill_value = 3
    target_value = 7
    barrier_value = 8

    # Initialize a queue for BFS (Breadth-First Search) propagation
    # Store coordinates (row, col) of cells to process
    queue = deque()

    # Find initial fill cells (value 3) and add them to the queue
    for r in range(rows):
        for c in range(cols):
            if output_grid[r][c] == fill_value:
                # Add initial 3s to the queue to start propagation
                queue.append((r, c))
                # No need to mark initial 3s as processed, they won't be changed

    # Define neighbor directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Perform the flood fill using BFS
    processed_target_cells = set() # Keep track of 7s added to queue to avoid cycles

    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is a target cell (value 7)
                # and hasn't been added to the queue yet
                if output_grid[nr][nc] == target_value and (nr, nc) not in processed_target_cells:
                    # Change the target cell to the fill value
                    output_grid[nr][nc] = fill_value
                    # Add the newly filled cell to the queue for further propagation
                    queue.append((nr, nc))
                    # Mark this cell as processed
                    processed_target_cells.add((nr, nc))
                # Note: barrier_value (8) cells implicitly stop propagation
                # as they don't match target_value.

    return output_grid
```
