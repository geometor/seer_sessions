
## train_1

**input:**
```
5 0 0 0 5
0 0 0 0 0
5 0 0 0 5
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
5 1 1 1 5
1 0 0 0 1
5 1 1 1 5
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0
0 5 0 0 5
0 0 0 0 0
0 0 0 0 0
0 5 0 0 5
```


**output:**
```
0 0 0 0 0
0 5 1 1 5
0 1 0 0 1
0 1 0 0 1
0 5 1 1 5
```


## train_3

**input:**
```
0 5 0 0 5
0 5 0 0 5
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 5 1 1 5
0 5 1 1 5
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
5 0 5 0 0
0 0 0 0 0
0 0 5 0 5
0 0 0 0 0
5 0 5 0 5
```


**output:**
```
5 1 5 0 0
1 0 1 0 0
1 0 5 1 5
1 0 0 0 1
5 1 5 1 5
```

**Perception:**

The task involves transforming a 2D grid of numbers (representing colors). The input grids contain the numbers 0 and 5. The output grids contain the numbers 0, 1, and 5. The transformation appears to involve changing some of the 0s to 1s based on their proximity to the 5s. The positions and values of the 5s remain unchanged from input to output. The change from 0 to 1 seems to occur for cells that are directly adjacent (horizontally or vertically) to a cell containing a 5.

**Facts:**


```yaml
Objects:
  - name: Grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (e.g., 5x5 in examples)
      - cell_values: [0, 1, 5] (0 and 5 in input, 0, 1, 5 in output)
  - name: Cell
    properties:
      - value: integer (0, 1, or 5)
      - position: (row, column) coordinates
      - neighbors: adjacent cells (up, down, left, right)

Relationships:
  - Adjacency: Cells can be adjacent horizontally or vertically.
  - Transformation Trigger: A cell with value 5 triggers a change in adjacent cells with value 0.

Actions:
  - Identify cells with value 5 in the input grid.
  - For each cell with value 5, identify its adjacent cells (up, down, left, right).
  - If an adjacent cell has a value of 0 in the input grid, change its value to 1 in the output grid.
  - Cells that originally had value 5 remain 5 in the output grid.
  - Cells that originally had value 0 and are not adjacent to any 5 remain 0 in the output grid.
```


**Natural Language Program:**

1.  Create a new grid with the same dimensions as the input grid, initially copying all values from the input grid.
2.  Iterate through each cell `(r, c)` of the input grid.
3.  If the value of the input cell `input[r][c]` is 0:
    a.  Check its neighbors (up: `input[r-1][c]`, down: `input[r+1][c]`, left: `input[r][c-1]`, right: `input[r][c+1]`), making sure to stay within the grid boundaries.
    b.  If any of these valid neighbors has a value of 5 in the *input* grid, set the value of the corresponding cell in the *output* grid `output[r][c]` to 1.
4.  If the value of the input cell `input[r][c]` is 5, keep the value 5 in the output grid `output[r][c]`.
5.  Return the modified output grid.
```python
import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by changing cells with value 0 to 1 if they are
    horizontally or vertically adjacent to a cell with value 5. Cells with value
    5 remain unchanged. Cells with value 0 that are not adjacent to a 5 also
    remain unchanged.

    Args:
      input_grid (list of lists or numpy array): The input 2D grid containing 0s and 5s.

    Returns:
      numpy array: The transformed 2D grid containing 0s, 1s, and 5s.
    """

    # Convert input to numpy array for easier handling
    input_arr = np.array(input_grid)
    rows, cols = input_arr.shape

    # Initialize output_grid as a copy of the input grid
    # Use a copy to avoid modifying the input while iterating
    output_arr = np.copy(input_arr)

    # Define the relative coordinates for neighbors (up, down, left, right)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell in the input grid is 0
            if input_arr[r, c] == 0:
                # Check its neighbors
                is_neighbor_5 = False
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the *input* grid is 5
                        if input_arr[nr, nc] == 5:
                            is_neighbor_5 = True
                            break # Found a neighbor 5, no need to check others

                # If any neighbor was 5, change the corresponding cell in the output grid to 1
                if is_neighbor_5:
                    output_arr[r, c] = 1
            # Cells with value 5 remain 5 (already handled by the initial copy)
            # Cells with value 0 not adjacent to 5 remain 0 (also handled by the initial copy)

    # Return the modified output grid
    return output_arr.tolist() # Convert back to list of lists if required by the environment

```
```python
import numpy as np

def _find_nearest_5_left(grid_row, c):
    """Find the column index of the nearest 5 to the left in a row."""
    for c_left in range(c - 1, -1, -1):
        if grid_row[c_left] == 5:
            return c_left
    return None

def _find_nearest_5_right(grid_row, c, cols):
    """Find the column index of the nearest 5 to the right in a row."""
    for c_right in range(c + 1, cols):
        if grid_row[c_right] == 5:
            return c_right
    return None

def _find_nearest_5_up(grid_col, r):
    """Find the row index of the nearest 5 above in a column."""
    for r_up in range(r - 1, -1, -1):
        if grid_col[r_up] == 5:
            return r_up
    return None

def _find_nearest_5_down(grid_col, r, rows):
    """Find the row index of the nearest 5 below in a column."""
    for r_down in range(r + 1, rows):
        if grid_col[r_down] == 5:
            return r_down
    return None

def _is_path_clear_horizontal(grid_row, c_left, c_right):
    """Check if the horizontal path between c_left and c_right contains only 0s."""
    return np.all(grid_row[c_left + 1 : c_right] == 0)

def _is_path_clear_vertical(grid_col, r_up, r_down):
    """Check if the vertical path between r_up and r_down contains only 0s."""
    return np.all(grid_col[r_up + 1 : r_down] == 0)

def transform(input_grid):
    """
    Transforms the input grid. A cell with value 0 is changed to 1 if it lies on
    a straight horizontal or vertical line segment between two cells with value 5,
    and all cells on that segment (excluding the endpoints) are 0s in the input.
    Cells with value 5 remain unchanged. Cells with value 0 not meeting the
    path criteria remain 0.
    """
    # Convert input to numpy array for efficient operations
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape

    # Initialize output_grid as a copy of the input grid
    # We will modify this grid based on the rules
    output_arr = np.copy(input_arr)

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Only consider cells that are 0 in the input
            if input_arr[r, c] == 0:
                
                # --- Check Horizontally ---
                c_left = _find_nearest_5_left(input_arr[r, :], c)
                c_right = _find_nearest_5_right(input_arr[r, :], c, cols)

                # Check if 5s were found on both sides and the path between them is clear
                if c_left is not None and c_right is not None:
                    if _is_path_clear_horizontal(input_arr[r, :], c_left, c_right):
                        output_arr[r, c] = 1
                        continue # Cell changed, move to the next cell

                # --- Check Vertically (only if horizontal check didn't change the cell) ---
                r_up = _find_nearest_5_up(input_arr[:, c], r)
                r_down = _find_nearest_5_down(input_arr[:, c], r, rows)

                # Check if 5s were found above and below and the path between them is clear
                if r_up is not None and r_down is not None:
                     if _is_path_clear_vertical(input_arr[:, c], r_up, r_down):
                        output_arr[r, c] = 1
                        # No need for continue here as it's the last check for this cell

    # Return the modified grid, converted back to list of lists
    return output_arr.tolist()
```
