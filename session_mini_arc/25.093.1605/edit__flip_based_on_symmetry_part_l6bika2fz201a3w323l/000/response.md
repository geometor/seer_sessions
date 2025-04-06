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