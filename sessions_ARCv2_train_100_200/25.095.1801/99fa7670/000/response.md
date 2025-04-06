Okay, let's analyze the provided examples.

## Perception of Task Elements

1.  **Input/Output Format**: Both input and output are 2D grids (matrices) containing non-negative integers. The background value is consistently 0.
2.  **Core Objects**: The primary objects are the grids themselves and the individual cells within them. Cells with non-zero values seem to be the "active" elements triggering the transformation.
3.  **Transformation Type**: The transformation appears to be a "spreading" or "filling" process originating from the non-zero cells in the input grid.
4.  **Spreading Pattern**:
    *   Each non-zero cell `C` at position `(r, c)` in the input influences cells in the output grid.
    *   The influence spreads horizontally to the right within the same row `r`, starting from column `c + 1` to the last column. All these cells take the value `C`.
    *   The influence also spreads vertically downwards in the *last* column of the grid, starting from row `r + 1` to the last row. All these cells also take the value `C`.
5.  **Overwriting**: If multiple non-zero cells influence the same output cell, the one processed later (based on a standard top-to-bottom, left-to-right scan of the input's non-zero cells) determines the final value. The value `C` used for filling always corresponds to the *original* non-zero cell being processed.

## Documented Facts


```yaml
task_type: grid_transformation
description: Fill regions of the grid based on the locations of non-zero values in the input.
components:
  grid:
    type: 2D array
    element_type: integer
    properties:
      - height: number of rows
      - width: number of columns
      - background_value: 0
  cell:
    type: element within the grid
    properties:
      - row_index: integer (0-based)
      - column_index: integer (0-based)
      - value: integer
  non_zero_cell:
    type: cell
    condition: value > 0
    role: initiator of transformation
actions:
  - name: initialize_output
    description: Create an output grid identical to the input grid.
  - name: identify_sources
    description: Find all non_zero_cells in the input grid.
  - name: apply_fill_rule
    description: For each identified source cell, perform horizontal and vertical filling.
    steps:
      - name: fill_right
        input: source_cell (r, c, C), output_grid, grid_width
        output: modified output_grid
        effect: Sets output_grid[r][j] = C for all j from c + 1 to grid_width - 1.
      - name: fill_down_last_column
        input: source_cell (r, c, C), output_grid, grid_height, grid_width
        output: modified output_grid
        effect: Sets output_grid[i][grid_width - 1] = C for all i from r + 1 to grid_height - 1.
processing_order:
  - description: Source cells from the input grid are processed sequentially.
  - standard_order: top-to-bottom (by row), then left-to-right (by column).
  - consequence: Later processing steps can overwrite values set by earlier steps if their fill regions overlap.
```


## Natural Language Program

1.  Create a new grid, `output_grid`, as a copy of the `input_grid`.
2.  Get the dimensions of the grid: `height` (number of rows) and `width` (number of columns).
3.  Iterate through each cell of the `input_grid` row by row, from top to bottom, and within each row, column by column, from left to right. Let the current cell coordinates be `(r, c)`.
4.  Check if the value of the `input_grid` cell at `(r, c)` is non-zero. Let this value be `C`.
5.  If the value `C` is non-zero:
    a.  **Horizontal Fill**: Iterate from column index `j = c + 1` up to `width - 1`. Set the value of the `output_grid` cell at `(r, j)` to `C`.
    b.  **Vertical Fill**: Let `last_col = width - 1`. Iterate from row index `i = r + 1` up to `height - 1`. Set the value of the `output_grid` cell at `(i, last_col)` to `C`.
6.  After iterating through all cells of the `input_grid`, the `output_grid` contains the final transformed result. Return the `output_grid`.