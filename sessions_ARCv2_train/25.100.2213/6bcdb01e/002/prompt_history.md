
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

The task involves transforming a 2D grid of digits based on a spreading or filling rule originating from specific cells.
- The input and output are grids of the same dimensions containing single digits.
- The digits 3, 7, and 8 appear to have distinct roles.
- The digit 3 seems to be the "active" or "source" element.
- The digit 7 seems to be the "background" or "fillable" element.
- The digit 8 seems to be a "barrier" or "boundary" element that stops the spread.
- The transformation involves the digit 3 "spreading" into adjacent cells containing the digit 7. Adjacency is considered horizontal and vertical (not diagonal).
- The spread continues iteratively until no more 7s adjacent to 3s can be converted.
- The initial positions of 3s act as the starting points for the spread.
- Cells containing 8 remain unchanged and block the spread of 3 through them.

## Facts

```yaml
objects:
  - name: grid
    properties:
      - type: 2D array of integers
      - contains cells
  - name: cell
    properties:
      - position: (row, column)
      - value: integer (digit)
  - name: digit_3
    properties:
      - role: source
      - action: spreads_to_neighbors
  - name: digit_7
    properties:
      - role: background
      - state: potentially_replaceable
  - name: digit_8
    properties:
      - role: barrier
      - state: blocks_spread
relationships:
  - type: adjacency
    between: cell
    definition: Cells sharing a horizontal or vertical edge.
  - type: transformation
    input: input_grid
    output: output_grid
    rule: fill_from_sources
actions:
  - name: fill_from_sources
    actor: digit_3
    target: adjacent digit_7 cells
    constraint: blocked_by_digit_8
    effect: changes target cell value from 7 to 3
    condition: continues until no more valid targets exist
```

## Natural Language Program

1.  **Initialize**: Create a copy of the input grid, which will become the output grid.
2.  **Identify Sources**: Find the coordinates of all cells in the input grid that initially contain the digit 3.
3.  **Prepare for Spread**: Create a queue (or similar data structure) and add the coordinates of all identified source cells to it.
4.  **Spread Loop**: While the queue is not empty:
    a.  **Get Current Cell**: Remove one cell's coordinates (row, col) from the front of the queue.
    b.  **Check Neighbors**: Examine the four adjacent cells (up, down, left, right) of the current cell.
    c.  **Process Neighbor**: For each valid neighbor (within grid boundaries):
        i.  **Check if Fillable**: If the neighbor cell in the *output* grid currently contains the digit 7:
            1.  **Fill**: Change the neighbor cell's value in the output grid to 3.
            2.  **Add to Queue**: Add the neighbor cell's coordinates to the queue to continue the spread from this new location.
5.  **Finalize**: Once the queue is empty (meaning no more spreading is possible), the process is complete. The modified grid is the final output.
```python
import collections
import copy

"""
Transforms an input grid by performing a flood fill operation starting from cells containing the digit 3. 
The fill spreads to adjacent (horizontally and vertically) cells containing the digit 7. 
Cells containing the digit 8 act as barriers and block the spread. The spread continues until no 
more adjacent 7s can be reached from the spreading 3s.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a flood fill transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Make a deep copy to avoid modifying the original input and to store the result
    output_grid = [row[:] for row in input_grid]
    
    # Get grid dimensions
    rows = len(output_grid)
    if rows == 0:
        return [] # Handle empty grid case
    cols = len(output_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle grids with empty rows

    # Initialize a queue for the Breadth-First Search (BFS) flood fill
    queue = collections.deque()

    # Identify initial source cells (value 3) and add them to the queue
    for r in range(rows):
        for c in range(cols):
            if output_grid[r][c] == 3:
                # Add initial '3' positions to the queue.
                # Note: We add them even though they are already 3, 
                # because their neighbors need to be checked.
                queue.append((r, c))

    # Define the four cardinal directions for checking neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill (spread loop) using BFS
    while queue:
        # Get the current cell coordinates from the front of the queue
        r, c = queue.popleft()

        # Check neighbors in all four directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor cell is fillable (contains 7)
                if output_grid[nr][nc] == 7:
                    # Fill the neighbor cell with 3
                    output_grid[nr][nc] = 3
                    # Add the newly filled cell to the queue to continue the spread from it
                    queue.append((nr, nc))

    # Return the modified grid after the spread is complete
    return output_grid
```
