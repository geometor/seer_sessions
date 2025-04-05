
## train_1

**input:**
```
7 7 7 0 0
0 7 0 0 0
7 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
7 7 7 0 0
0 7 0 0 0
0 0 7 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 0 0
0 4 4 4 0
0 0 4 0 0
0 0 4 0 0
0 0 0 4 0
```


**output:**
```
0 0 4 0 0
0 4 4 4 0
0 0 4 0 0
0 0 4 0 0
0 4 0 0 0
```


## train_3

**input:**
```
0 0 0 0 6
6 6 6 6 6
0 6 6 6 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
6 0 0 0 0
6 6 6 6 6
0 6 6 6 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
0 0 8 0 0
8 8 0 8 8
0 0 0 8 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 8 0 0
8 8 0 8 8
0 8 0 0 0
0 0 0 0 0
0 0 0 0 0
```

## Perception

The input and output are represented as 2D grids (matrices) containing single digits. The digit '0' appears to function as a background color. Other non-zero digits represent foreground colors, forming shapes or patterns within the grid.

Comparing each input grid to its corresponding output grid reveals that the transformation involves moving a single foreground-colored cell within its row. The rest of the grid remains unchanged. The cell that moves is always one that is "horizontally isolated," meaning its left and right neighbors within the same row are both background cells (0) or grid boundaries. The destination column for the moved cell appears determined by reflecting its original column position across the center of the horizontal span (minimum to maximum column index) occupied by *all* non-zero cells in the entire input grid.

## Facts


```yaml
objects:
  - name: Grid
    properties:
      - type: 2D array of integers
      - dimensions: height, width
      - cells: list of Cell objects
  - name: Cell
    properties:
      - position: (row_index, column_index)
      - value: integer (digit 0-9)
      - type: BACKGROUND (if value is 0), FOREGROUND (if value is non-zero)
  - name: Horizontally_Isolated_Foreground_Cell
    isa: Cell
    properties:
      - value: non-zero integer
      - condition: Left and right neighbors in the same row are BACKGROUND cells or grid boundaries.
    constraints:
      - Exactly one such cell exists in each input grid.

properties:
  - name: Global_Non_Zero_Column_Range
    description: The range of column indices containing at least one FOREGROUND cell across the entire grid.
    attributes:
      - min_column_index
      - max_column_index

actions:
  - name: Identify_Non_Zero_Cells
    input: Grid
    output: List of FOREGROUND Cell positions and values
  - name: Calculate_Global_Column_Range
    input: List of FOREGROUND Cell positions
    output: min_column_index, max_column_index
  - name: Find_Horizontally_Isolated_Cell
    input: Grid
    output: The single Horizontally_Isolated_Foreground_Cell (position and value)
  - name: Calculate_Destination_Column
    input:
      - original_column: column index of the Horizontally_Isolated_Foreground_Cell
      - min_column_index: from Global_Non_Zero_Column_Range
      - max_column_index: from Global_Non_Zero_Column_Range
    output: destination_column
    logic: destination_column = min_column_index + max_column_index - original_column
  - name: Move_Cell
    input:
      - input_grid: Grid
      - moving_cell: Horizontally_Isolated_Foreground_Cell (position and value)
      - destination_column: calculated destination column index
    output: output_grid: Grid
    logic:
      - Create a copy of the input_grid.
      - Set the original position of the moving_cell in the copied grid to 0 (BACKGROUND).
      - Set the cell at (moving_cell.row_index, destination_column) in the copied grid to moving_cell.value.

relationships:
  - The transformation modifies only one cell's position.
  - The cell to be moved is uniquely identified by its non-zero value and horizontal isolation.
  - The destination column is determined by reflecting the original column across the center of the global horizontal extent of all non-zero cells.
```


## Natural Language Program

1.  **Analyze the Input Grid:** Examine the input grid to identify all cells with non-zero values (foreground cells).
2.  **Determine Global Column Boundaries:** Find the minimum column index (`min_nz_col`) and the maximum column index (`max_nz_col`) among all foreground cells identified in step 1.
3.  **Locate the Moving Cell:** Scan the input grid row by row to find the unique foreground cell `(r_move, c_move)` with value `v_move` that has background cells (0) or grid boundaries immediately to its left and right within the same row `r_move`.
4.  **Calculate the Destination Column:** Compute the target column index `c_new` for the moving cell using the formula: `c_new = min_nz_col + max_nz_col - c_move`.
5.  **Construct the Output Grid:**
    a. Create a new grid identical to the input grid.
    b. Change the value of the cell at the original position `(r_move, c_move)` in the new grid to 0.
    c. Change the value of the cell at the destination position `(r_move, c_new)` in the new grid to `v_move`.
6.  **Output:** The modified grid is the final output.
```python
import copy

"""
1.  **Analyze the Input Grid:** Examine the input grid to identify all cells with non-zero values (foreground cells).
2.  **Determine Global Column Boundaries:** Find the minimum column index (`min_nz_col`) and the maximum column index (`max_nz_col`) among all foreground cells identified in step 1.
3.  **Locate the Moving Cell:** Scan the input grid row by row to find the unique foreground cell `(r_move, c_move)` with value `v_move` that has background cells (0) or grid boundaries immediately to its left and right within the same row `r_move`.
4.  **Calculate the Destination Column:** Compute the target column index `c_new` for the moving cell using the formula: `c_new = min_nz_col + max_nz_col - c_move`.
5.  **Construct the Output Grid:**
    a. Create a new grid identical to the input grid.
    b. Change the value of the cell at the original position `(r_move, c_move)` in the new grid to 0.
    c. Change the value of the cell at the destination position `(r_move, c_new)` in the new grid to `v_move`.
6.  **Output:** The modified grid is the final output.
"""

def find_non_zero_cells(grid):
    """Finds all cells with non-zero values."""
    non_zero_cells = []
    height = len(grid)
    if height == 0:
        return non_zero_cells
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                non_zero_cells.append({'r': r, 'c': c, 'v': grid[r][c]})
    return non_zero_cells

def get_global_column_range(non_zero_cells):
    """Calculates the min and max column index containing non-zero cells."""
    if not non_zero_cells:
        return None, None # Or handle as appropriate for the task context
    min_c = min(cell['c'] for cell in non_zero_cells)
    max_c = max(cell['c'] for cell in non_zero_cells)
    return min_c, max_c

def find_horizontally_isolated_cell(grid):
    """Finds the unique non-zero cell horizontally isolated by zeros or boundaries."""
    height = len(grid)
    if height == 0:
        return None
    width = len(grid[0])
    if width == 0:
        return None

    for r in range(height):
        for c in range(width):
            value = grid[r][c]
            if value != 0:
                # Check left neighbor
                is_left_bg = (c == 0) or (grid[r][c - 1] == 0)
                # Check right neighbor
                is_right_bg = (c == width - 1) or (grid[r][c + 1] == 0)

                if is_left_bg and is_right_bg:
                    return {'r': r, 'c': c, 'v': value}
    return None # Should not happen based on problem description

def transform(input_grid):
    """
    Transforms the input grid by finding a horizontally isolated non-zero cell
    and moving it horizontally based on the global column range of all non-zero cells.
    The destination column is calculated by reflecting the original column across
    the center of the global non-zero column range.
    """
    # Ensure input is not modified
    output_grid = copy.deepcopy(input_grid)
    height = len(output_grid)
    if height == 0:
        return output_grid
    width = len(output_grid[0])
    if width == 0:
        return output_grid

    # 1. Analyze the Input Grid & 2. Determine Global Column Boundaries
    non_zero_cells = find_non_zero_cells(output_grid)
    if not non_zero_cells:
        return output_grid # No non-zero cells to move

    min_nz_col, max_nz_col = get_global_column_range(non_zero_cells)

    # 3. Locate the Moving Cell
    moving_cell = find_horizontally_isolated_cell(output_grid)
    if not moving_cell:
         # If no isolated cell found (shouldn't happen based on examples), return original
        return output_grid

    r_move = moving_cell['r']
    c_move = moving_cell['c']
    v_move = moving_cell['v']

    # 4. Calculate the Destination Column
    # Reflect c_move across the center point (min_nz_col + max_nz_col) / 2
    # The formula is: new_pos = min + max - old_pos
    c_new = min_nz_col + max_nz_col - c_move

    # Ensure destination column is within grid bounds (although logic implies it should be if min/max are correct)
    # This check might be redundant if the logic is always sound for the ARC context,
    # but good practice for general robustness.
    if 0 <= c_new < width:
        # 5. Construct the Output Grid (modify the copy)
        # a. Clear the original position
        output_grid[r_move][c_move] = 0
        # b. Place the value at the new position
        output_grid[r_move][c_new] = v_move
    # else: handle error or unexpected case? For now, assume c_new is valid.

    # 6. Output
    return output_grid
```
