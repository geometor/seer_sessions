
## train_1

**input:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```


**output:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

### Perception

1.  **Grid Structure:** Both input and output are 2D grids of integers. The value `0` represents the background. Non-zero integers represent distinct objects or markers.
2.  **Core Task:** The transformation involves selectively "painting" or "filling" areas of the grid based on the location and value of specific non-zero cells in the input. The original non-zero cells seem to remain unchanged.
3.  **Trigger Locations & Actions:** There appear to be three distinct trigger conditions based on the location of a non-zero cell in the input grid:
    *   **Right Edge:** A non-zero cell in the last column triggers a horizontal fill leftwards in the same row.
    *   **Second-to-Last Row:** A non-zero cell in the second-to-last row triggers a vertical fill upwards in the same column.
    *   **Left Edge:** A non-zero cell in the first column triggers a diagonal fill upwards and rightwards.
4.  **Fill Color:** The fill operation uses the color (integer value) of the trigger cell.
5.  **Stopping Conditions:** The fill operations do not overwrite existing non-zero cells from the input. Each fill type has specific conditions that stop its propagation:
    *   **Horizontal Fill (Leftwards):** Stops upon encountering any non-zero cell in the same row to its left.
    *   **Vertical Fill (Upwards):** Stops upon encountering a non-zero cell in the same column above it, OR stops just before reaching a row that contains *any* non-zero cell.
    *   **Diagonal Fill (Up-Right):** Stops upon encountering any non-zero cell on its diagonal path, OR stops if the current fill position `(nr, nc)` satisfies `nr <= R` and `nc >= C` for any *other* non-zero cell `(R, C)` present in the original input. It also stops if it goes out of the grid boundaries.
6.  **Independence:** Each trigger cell initiates its fill independently based on the *input* grid state. The resulting fills are combined in the output grid.

### Facts


```yaml
Grid:
  Type: 2D Array of Integers
  BackgroundValue: 0
Objects:
  Type: Non-zero integer cells
  Properties:
    - value (color)
    - position (row, column)
Relationships:
  - Relative Position: Cells can be located at edges (first/last column, last-but-one row) or internally.
  - Proximity: For diagonal fills, the position relative to *other* non-zero cells matters.
Actions:
  - Identify Triggers: Locate non-zero cells based on specific positions (last column, second-last row, first column).
  - Fill: Propagate the trigger cell's value into adjacent background cells according to specific rules.
    - Fill Directions:
      - Horizontal Left (from last column)
      - Vertical Up (from second-last row)
      - Diagonal Up-Right (from first column)
    - Fill Stopping Conditions:
      - Boundary Hit (edge of grid)
      - Collision (encountering a non-zero cell from the input grid)
      - Proximity Constraint (specific condition for diagonal fill related to other objects)
      - Row Constraint (specific condition for vertical fill related to non-empty rows above)
Transformation:
  Rule: Apply fill actions originating from all identified trigger cells onto a copy of the input grid.
  InputPreservation: Original non-zero cells from the input are preserved in the output.
  OutputComposition: The final output is the initial grid state modified by all triggered fill operations.
```


### Natural Language Program

1.  **Initialize:** Create the output grid as an exact copy of the input grid.
2.  **Identify Triggers:** Find all cells `(r, c)` in the input grid that have a non-zero value `V`.
3.  **Process Triggers:** For each identified non-zero trigger cell `(r, c)` with value `V`:
    a.  **Right Edge Trigger:** If the cell is in the last column (`c == width - 1`):
        *   Iterate leftwards from `k = c - 1` down to 0.
        *   If the input cell `input[r][k]` is non-zero, stop this fill.
        *   Otherwise, set the output cell `output[r][k] = V`.
    b.  **Second-to-Last Row Trigger:** If the cell is in the second-to-last row (`r == height - 2`):
        *   Iterate upwards from `i = r - 1` down to 0.
        *   Check if the entire input row `i` contains any non-zero value. If yes, stop this fill.
        *   If the input cell `input[i][c]` is non-zero, stop this fill.
        *   Otherwise, set the output cell `output[i][c] = V`.
    c.  **Left Edge Trigger:** If the cell is in the first column (`c == 0`):
        *   Find the locations `(R, C)` of all *other* non-zero cells in the input grid.
        *   Iterate with `j` starting from 1.
        *   Calculate the potential fill coordinates `nr = r - j`, `nc = c + j`.
        *   If `nr` or `nc` are outside the grid boundaries, stop this fill.
        *   If the input cell `input[nr][nc]` is non-zero, stop this fill.
        *   Check the proximity condition: For each other non-zero cell `(R, C)`, if `nr <= R` AND `nc >= C`, stop this fill.
        *   If none of the stopping conditions are met, set the output cell `output[nr][nc] = V`.
4.  **Finalize:** Return the modified output grid.
```python
import numpy as np
import copy

"""
Transformation Rule Description:

The transformation processes a 2D integer grid. It identifies non-zero cells (objects) in the input grid and uses them as triggers for specific fill operations based on their location. The original objects are preserved in the output. The fills use the value (color) of the trigger object.

1. Initialization: The output grid starts as a copy of the input grid.
2. Trigger Identification: Find all cells (r, c) with a non-zero value V in the input grid.
3. Trigger Processing (applied independently based on the *input* grid):
    a. Right Edge Trigger (cell at last column, c == width - 1):
        - Fill horizontally leftwards (decrementing column index k from c-1 to 0) in the same row r.
        - Stop filling if an input cell input[r][k] is non-zero.
        - Fill uses color V. Updates the *output* grid: output[r][k] = V.
    b. Second-to-Last Row Trigger (cell at second-last row, r == height - 2):
        - Fill vertically upwards (decrementing row index i from r-1 to 0) in the same column c.
        - Stop filling if the input row input[i] contains *any* non-zero value.
        - Stop filling if the input cell input[i][c] is non-zero.
        - Fill uses color V. Updates the *output* grid: output[i][c] = V.
    c. Left Edge Trigger (cell at first column, c == 0):
        - Find locations (R, C) of all *other* non-zero cells in the input.
        - Fill diagonally upwards and rightwards (incrementing step j, calculating nr = r - j, nc = c + j).
        - Stop filling if (nr, nc) goes out of grid boundaries.
        - Stop filling if the input cell input[nr][nc] is non-zero.
        - Stop filling if for *any* other non-zero cell (R, C) in the input, the condition (nr <= R AND nc >= C) is met.
        - Fill uses color V. Updates the *output* grid: output[nr][nc] = V.
4. Output: The final output is the modified grid containing the original objects and the results of all triggered fills.
"""

def find_non_zero_cells(grid):
    """Finds all non-zero cells in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (row, column, value).
    """
    non_zero_cells = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                non_zero_cells.append((r, c, grid[r, c]))
    return non_zero_cells

def does_row_contain_non_zero(grid, row_index):
    """Checks if a specific row contains any non-zero value."""
    return np.any(grid[row_index, :] != 0)

def transform(input_grid):
    """
    Applies the transformation rule based on trigger cell locations.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy
    output_np = input_np.copy()
    height, width = input_np.shape

    # Find all non-zero cells in the original input grid
    non_zero_cells = find_non_zero_cells(input_np)

    # Process each non-zero cell as a potential trigger
    for r, c, V in non_zero_cells:

        # --- Right Edge Trigger ---
        if c == width - 1:
            # Iterate leftwards from the column before the trigger
            for k in range(c - 1, -1, -1):
                # Stop if we hit a non-zero cell in the input
                if input_np[r, k] != 0:
                    break
                # Otherwise, fill the output grid
                output_np[r, k] = V

        # --- Second-to-Last Row Trigger ---
        if r == height - 2:
            # Iterate upwards from the row above the trigger
            for i in range(r - 1, -1, -1):
                 # Stop if the target input row i contains any non-zero value
                if does_row_contain_non_zero(input_np, i):
                    break
                # Stop if the specific input cell we are about to paint is non-zero
                if input_np[i, c] != 0:
                    break
                # Otherwise, fill the output grid
                output_np[i, c] = V

        # --- Left Edge Trigger ---
        if c == 0:
             # Get locations of all *other* non-zero cells for proximity check
            other_non_zero_locs = [(R, C) for R, C, _ in non_zero_cells if (R, C) != (r, c)]
            # Iterate diagonally up-right
            for j in range(1, max(height, width)): # Max possible steps
                nr, nc = r - j, c + j

                # Stop if out of bounds
                if nr < 0 or nc >= width:
                    break

                # Stop if hitting an existing non-zero cell in the input
                if input_np[nr, nc] != 0:
                    break

                # Check proximity condition against all *other* non-zero cells
                proximity_stop = False
                for R, C in other_non_zero_locs:
                    if nr <= R and nc >= C:
                        proximity_stop = True
                        break
                if proximity_stop:
                    break

                # Otherwise, fill the output grid
                output_np[nr, nc] = V

    # Convert the result back to a list of lists
    return output_np.tolist()
```
