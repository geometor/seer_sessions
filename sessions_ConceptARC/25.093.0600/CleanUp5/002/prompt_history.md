
## train_1

**input:**
```
0 0 0 0 0 2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 3 0 2 0 0 0 2 0 3 0 0 0 2 0 0 0 2 0 0 3
0 0 2 0 0 0 0 0 2 0 0 0 3 0 0 0 0 0 3 0 0
0 2 0 3 0 0 0 0 0 2 0 2 0 0 0 3 0 0 0 2 0
2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


## train_2

**input:**
```
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 4 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0
```

Okay, I will analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) containing single-digit non-negative integers.
2.  **Grid Size:** The grid dimensions can vary between examples (6x21 in train\_1, 6x24 in train\_2), but the output grid always has the same dimensions as the corresponding input grid.
3.  **Values:** The grids contain the value 0 and other non-zero digits (2, 3 in train\_1; 4 in train\_2).
4.  **Transformation:** The core transformation involves selectively changing some non-zero digits in the input grid to 0 in the output grid. Other digits (including existing 0s and some non-zero digits) remain unchanged.
5.  **Pattern:**
    *   In `train_1`, all instances of the digit '3' are changed to '0', while all instances of '2' remain unchanged.
    *   In `train_2`, *some* instances of the digit '4' are changed to '0', while others remain '4'.
    *   Observing the positions, the non-zero digits that are changed to 0 appear to be those that do not have any adjacent cells (including diagonals - Moore neighborhood) containing the *same* non-zero digit. Conversely, non-zero digits that *do* have at least one neighbor with the same value are preserved in the output.

**YAML Facts:**


```yaml
task_description: "Filter a 2D grid of digits, setting non-zero digits to zero if they lack neighbors of the same value."
elements:
  - object: grid
    properties:
      - type: 2D array (matrix)
      - content: non-negative single digits
      - dimensionality: [rows, columns] (variable)
  - object: cell
    properties:
      - value: integer (0-9)
      - position: [row_index, column_index]
      - neighbors: set of 8 adjacent cells (Moore neighborhood)
relationships:
  - type: adjacency
    between: cell
    details: A cell is adjacent to up to 8 other cells (horizontally, vertically, diagonally). Boundary cells have fewer neighbors.
actions:
  - action: process_grid
    actor: system
    input: input_grid
    output: output_grid
    rule: "Iterate through each cell of the input grid."
  - action: evaluate_cell
    actor: system
    input: current_cell (value, position), input_grid
    output: output_cell_value
    rule: |
      1. Get the value (v) and position of the current cell.
      2. If v is 0, the output_cell_value is 0.
      3. If v is non-zero:
         a. Examine the values of the 8 neighboring cells (Moore neighborhood) in the input_grid. Handle boundary conditions (ignore non-existent neighbors).
         b. Check if any neighbor has the same value v.
         c. If at least one neighbor has value v, the output_cell_value is v.
         d. If no neighbor has value v, the output_cell_value is 0.
  - action: construct_output
    actor: system
    input: results of evaluate_cell for all cells
    output: output_grid
    rule: "Assemble the output_cell_values into a new grid with the same dimensions as the input grid."

```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid.
2.  Iterate through each cell `(r, c)` of the input grid. Let the value of the input cell be `v`.
3.  If `v` is 0, set the corresponding cell `(r, c)` in the output grid to 0.
4.  If `v` is not 0:
    a.  Check all 8 neighboring cells (including diagonals) of `(r, c)` within the bounds of the input grid.
    b.  Determine if any of these neighboring cells in the *input* grid has the same value `v`.
    c.  If at least one neighbor has the value `v`, set the corresponding cell `(r, c)` in the output grid to `v`.
    d.  If *none* of the neighbors have the value `v`, set the corresponding cell `(r, c)` in the output grid to 0.
5.  Return the completed output grid.
```python
import copy

"""
Filters a 2D grid of digits. For each non-zero cell in the input grid,
it checks its 8 neighbors (Moore neighborhood). If at least one neighbor
in the input grid has the same value as the cell, the cell's value is 
kept in the output grid. Otherwise (if the cell value is 0 or if it's 
non-zero but has no neighbors with the same value), the corresponding 
cell in the output grid is set to 0.
"""

def _is_valid(r, c, num_rows, num_cols):
    """
    Helper function to check if coordinates (r, c) are within the grid boundaries.

    Args:
        r (int): Row index.
        c (int): Column index.
        num_rows (int): Total number of rows in the grid.
        num_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if the coordinates are valid, False otherwise.
    """
    return 0 <= r < num_rows and 0 <= c < num_cols

def _has_same_neighbor(grid, r, c, value, num_rows, num_cols):
    """
    Helper function to check if any of the 8 neighbors of cell (r, c) 
    in the grid has the specified value.

    Args:
        grid (list[list[int]]): The input grid.
        r (int): Row index of the cell to check neighbors for.
        c (int): Column index of the cell to check neighbors for.
        value (int): The value to look for in the neighbors.
        num_rows (int): Total number of rows in the grid.
        num_cols (int): Total number of columns in the grid.

    Returns:
        bool: True if at least one neighbor has the specified value, False otherwise.
    """
    # Define relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    # Iterate through all potential neighbor positions
    for dr, dc in neighbor_deltas:
        nr, nc = r + dr, c + dc
        
        # Check if the neighbor coordinates are valid (within grid bounds)
        if _is_valid(nr, nc, num_rows, num_cols):
            # Check if the neighbor cell in the grid has the target value
            if grid[nr][nc] == value:
                return True # Found a neighbor with the same value

    # If the loop completes without finding a matching neighbor
    return False

def transform(input_grid):
    """
    Transforms the input grid based on neighbor values.

    A non-zero cell retains its value if at least one of its 8 neighbors 
    has the same value. Otherwise, the cell becomes 0. Zero cells remain 0.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A new 2D list representing the transformed grid.
    """
    # Handle empty or invalid input grid
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        # Or raise an error, depending on desired behavior
        return [] 

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize the output grid with the same dimensions, filled with zeros
    # Using list comprehension for initialization
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            cell_value = input_grid[r][c]

            # Process only non-zero cells
            if cell_value != 0:
                # Check if the current cell has at least one neighbor with the same value
                # Pass the original input_grid to the helper function for checking neighbors
                if _has_same_neighbor(input_grid, r, c, cell_value, num_rows, num_cols):
                    # If it has a matching neighbor, retain the value in the output grid
                    output_grid[r][c] = cell_value
                # Else: The cell value becomes 0 (already initialized)

            # If cell_value is 0, the output_grid[r][c] remains 0 (as initialized)

    # Return the newly constructed output grid
    return output_grid
```
