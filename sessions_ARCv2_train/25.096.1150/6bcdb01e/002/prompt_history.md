
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

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Structure:** Both inputs and outputs are 2D grids (matrices) containing numerical digits.
2.  **Grid Dimensions:** The dimensions of the output grid are identical to the dimensions of the input grid in each example.
3.  **Cell Values:** The grids contain the digits 3, 7, and 8.
4.  **Key Transformation:** The primary change observed is that some cells with the value 7 in the input grid are changed to the value 3 in the output grid.
5.  **Value Persistence:** Cells with the value 8 in the input grid remain unchanged in the output grid. Cells with the value 3 in the input grid also remain unchanged (value 3) in the output grid.
6.  **Spatial Relationship:** The change from 7 to 3 appears to depend on the spatial arrangement and connectivity. Specifically, it seems related to the proximity or reachability from cells initially containing the value 3. The 7s that change to 3s seem to form connected regions (horizontally and vertically adjacent) that include or touch the original 3s. The 8s seem to act as barriers, blocking this transformation or connection.

**YAML Facts:**


```yaml
task_description: Apply a flood fill transformation starting from '3' cells.
elements:
  - object: grid
    properties:
      - type: 2D array
      - content: cells containing numerical digits (3, 7, 8)
  - object: cell
    properties:
      - type: grid element
      - value: integer (3, 7, or 8)
      - position: (row, column) coordinates
      - adjacency: connected horizontally or vertically to neighboring cells
relationships:
  - type: connectivity
    description: Cells with value 7 can be connected horizontally or vertically to other cells with value 7 or 3.
  - type: barrier
    description: Cells with value 8 block connectivity and are not changed.
actions:
  - action: identify_seeds
    input: input_grid
    output: list of coordinates for cells with value 3
    description: Find all cells initially containing the value 3.
  - action: flood_fill
    input: input_grid, seed_coordinates
    output: modified_grid
    description: >
      Starting from the seed cells (value 3), change the value of all reachable
      adjacent cells (horizontally or vertically) that contain the value 7 to 3.
      This process continues recursively/iteratively through newly changed cells.
      Cells with value 8 are barriers and stop the fill.
  - action: copy_unchanged
    input: input_grid
    output: partial_output_grid
    description: >
      Copy cells with values 3 and 8 from the input grid to the output grid
      at their original positions. Copy cells with value 7 that were *not*
      reached by the flood_fill.
transformation:
  - step: Initialize the output grid as a copy of the input grid.
  - step: Identify all 'seed' cells in the input grid (those with value 3).
  - step: Perform a flood fill starting from the seed cells.
  - step: >
      The fill propagates horizontally and vertically to adjacent cells.
      If a cell contains 7, change its value to 3 in the output grid and continue the fill from this cell.
  - step: The fill cannot enter or pass through cells containing 8.
  - step: Cells that were initially 3 or 8 remain unchanged.
  - step: Cells that were initially 7 but were not reached by the flood fill remain 7.
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Identify the locations (row, column coordinates) of all cells in the input grid that contain the value 3. These are the starting points ("seeds") for the transformation.
3.  Maintain a list or queue of locations to process, initially populated with the seed locations identified in step 2.
4.  While there are locations left to process:
    a.  Select a location from the list.
    b.  Examine its four adjacent neighbors (up, down, left, right), if they exist within the grid boundaries.
    c.  For each neighbor:
        i.  If the neighbor cell in the *input* grid contains the value 7 AND its corresponding cell in the *output* grid currently contains 7 (meaning it hasn't been processed/changed yet):
            1.  Change the value of this neighbor cell in the *output* grid to 3.
            2.  Add the location of this neighbor cell to the list of locations to process.
5.  The final state of the output grid is the result of the transformation. (Cells initially containing 3 or 8, and 7s not reachable from the initial 3s via a path of 7s, retain their original values).
```python
import copy
from collections import deque

"""
Apply a flood fill transformation starting from cells with value 3. 
The fill propagates horizontally and vertically to adjacent cells containing the value 7, changing them to 3. 
Cells with value 8 act as barriers and stop the fill. 
Cells initially containing 3 or 8, and 7s not reached by the fill, remain unchanged.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on a flood fill rule originating from '3' cells.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """

    # Get grid dimensions
    if not input_grid or not input_grid[0]:
        return []
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This ensures that 8s, initial 3s, and unreachable 7s are preserved
    # unless explicitly changed by the flood fill.
    output_grid = [row[:] for row in input_grid] # Sufficient for lists of ints

    # Initialize a queue for the flood fill (BFS)
    queue = deque()

    # Find initial seed cells (value 3) and add them to the queue
    # Note: Cells initially 3 don't need to be explicitly processed by the fill
    # logic itself, but their neighbors do. We add neighbors of 3s that are 7s
    # or we can just add the 3s and let the main loop handle neighbors.
    # Adding the 3s themselves is simpler and covers all cases.
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 3:
                 # Although the 3 itself doesn't change, it acts as a source.
                 # We add its coords to potentially start filling adjacent 7s.
                 # No need to explicitly mark visited, as we only change 7s to 3s
                 # in the output_grid, and the check output_grid[nr][nc] == 7 handles this.
                 queue.append((r, c))


    # Perform the flood fill using Breadth-First Search (BFS)
    while queue:
        r, c = queue.popleft()

        # Define potential neighbors (up, down, left, right)
        neighbors = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]

        for nr, nc in neighbors:
            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor cell in the *input* grid contains 7
                # AND if its corresponding cell in the *output* grid is still 7
                # (meaning it hasn't been reached/processed by the fill yet).
                # The condition input_grid[nr][nc] == 7 is technically redundant if
                # we start correctly, as only 7s can become 3s, but it's safer
                # to include, matching the natural language description precisely.
                if input_grid[nr][nc] == 7 and output_grid[nr][nc] == 7:
                    # Change the value in the output grid to 3
                    output_grid[nr][nc] = 3
                    # Add this newly changed cell to the queue to process its neighbors
                    queue.append((nr, nc))

    # The output_grid now contains the final state after the flood fill
    return output_grid
```
