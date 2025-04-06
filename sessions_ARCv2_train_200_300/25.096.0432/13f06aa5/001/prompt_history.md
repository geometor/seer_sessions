
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 4 4 1 4 4 2 2
2 2 2 2 2 2 2 2 4 4 4 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 2 2 2 2 2
2 4 4 2 2 2 2 2 2 2 2 2 2 2
2 4 8 2 2 2 2 2 2 2 2 2 2 2
2 4 4 2 2 2 2 2 2 2 2 2 2 2
2 2 4 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 0
2 2 2 2 2 2 2 2 2 1 2 2 2 8
2 2 2 2 2 2 2 2 2 2 2 2 2 8
2 2 2 2 2 2 2 4 4 1 4 4 2 8
2 2 2 2 2 2 2 2 4 4 4 2 2 8
2 2 2 2 2 2 2 2 2 2 2 2 2 8
2 2 4 2 2 2 2 2 2 2 2 2 2 8
2 4 4 2 2 2 2 2 2 2 2 2 2 8
2 4 8 2 8 2 8 2 8 2 8 2 8 8
2 4 4 2 2 2 2 2 2 2 2 2 2 8
2 2 4 2 2 2 2 2 2 2 2 2 2 8
2 2 2 2 2 2 2 2 2 2 2 2 2 8
```


## train_2

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 8 1 1 1 8 8 3 8 8 1
1 1 1 8 8 1 1 1 8 8 8 1 1
1 1 1 2 8 1 1 1 1 1 1 1 1
1 1 1 8 8 1 1 1 1 1 1 1 1
1 1 1 8 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
0 3 3 3 3 3 3 3 3 3 3 3 3
2 1 1 1 1 1 1 1 1 3 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
2 1 1 8 1 1 1 8 8 3 8 8 1
2 1 1 8 8 1 1 1 8 8 8 1 1
2 2 1 2 8 1 1 1 1 1 1 1 1
2 1 1 8 8 1 1 1 1 1 1 1 1
2 1 1 8 1 1 1 1 1 1 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
2 1 1 1 1 1 1 1 1 1 1 1 1
```


## train_3

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 1 1 1 3 3 3 3 3
3 3 3 1 1 6 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 1 1 1 3 3 3 3 3
3 3 3 1 1 6 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 6 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3
6 6 6 6 6 6 6 6 6 6 6 6
```

Okay, I will analyze the provided training examples to understand the transformation logic.

## Perception of Elements

Based on the three training examples, the task involves transforming an input grid of numbers into an output grid of the same dimensions. The transformation appears to modify specific rows, columns, or individual cells based on certain rules that might involve the cell's original value, its row/column index, and potentially index parity (even/odd). The background color (the most frequent number in the input) often seems to be the target for changes. New colors are introduced in the modified locations. In some cases, the intersection of modified rows and columns receives a special value (like 0).

## YAML Fact Documentation


```yaml
task_type: grid_transformation
grid_properties:
  dimensionality: 2D
  cell_content: integer_numbers
  size_constraint: output_grid_same_size_as_input_grid
objects:
  - input_grid: A 2D array of integers.
  - output_grid: A 2D array of integers, derived from the input_grid.
  - rows: Horizontal lines of cells in the grid.
  - columns: Vertical lines of cells in the grid.
  - cells: Individual elements within the grid, identified by row and column index.
properties:
  - cell_value: The integer contained within a cell.
  - row_index: The vertical position of a cell/row (0-based).
  - column_index: The horizontal position of a cell/column (0-based).
  - grid_height: Number of rows.
  - grid_width: Number of columns.
  - background_color: The most frequent cell value in the input grid (potentially).
  - modification_target_value: The specific cell value targeted for change (often the background_color).
  - fill_color: The new value assigned to modified cells. Multiple fill colors can exist per task.
  - special_rows: Specific rows targeted for modification (e.g., row 0, row 8, last row).
  - special_columns: Specific columns targeted for modification (e.g., col 0, col 5, last col).
  - special_cells: Specific individual cells targeted for modification.
  - index_condition: A condition based on row or column index (e.g., even index, index >= 4) that may gate modification.
  - corner_value: A specific value assigned to the intersection of a modified row and column.
actions:
  - copy_grid: Initialize the output grid with the contents of the input grid.
  - identify_parameters: Determine the specific rows, columns, cells, colors, and conditions for modification based on the task instance.
  - modify_line: Iterate through cells in a specified row or column. If a cell's value matches the target value and any index condition is met, change its value in the output grid to the corresponding fill color.
  - modify_cell: Change the value of a specific cell in the output grid.
  - modify_corner: Set the value of the cell at the intersection of a modified row and column to the corner value.
relationships:
  - Modification depends on the original cell value (often the background color).
  - Modification location is specific (certain rows, columns, or cells).
  - Modification value (fill color) can depend on the location (e.g., different fill for a row vs. a column).
  - Modification within a line can be conditional on the other index (e.g., even columns in a specific row).
```


## Natural Language Program

1.  **Initialization:** Create the `output_grid` as an identical copy of the `input_grid`.
2.  **Parameter Identification:** For the specific task instance, identify the following parameters:
    *   The `modification_target_value` (typically the most common value in the input).
    *   A set of `special_rows` or `special_columns` designated for modification.
    *   Associated `fill_colors` for each special row/column.
    *   Optional `index_conditions` (e.g., even/odd index, index range) that must be met for modification within a special line.
    *   An optional `corner_value` for intersections of modified lines.
    *   A set of `special_cells` (row, column pairs) for individual modification, along with their specific `fill_colors`.
3.  **Line Modifications:**
    *   For each `special_row`: Iterate through its columns. If the cell at `(special_row, column)` in the `input_grid` contains the `modification_target_value` AND any associated `index_condition` (applied to the column index) is met, update the corresponding cell in the `output_grid` with the row's `fill_color`.
    *   For each `special_column`: Iterate through its rows. If the cell at `(row, special_column)` in the `input_grid` contains the `modification_target_value` AND any associated `index_condition` (applied to the row index) is met, update the corresponding cell in the `output_grid` with the column's `fill_color`.
4.  **Corner Modification:** If a `special_row` and `special_column` are both defined and a `corner_value` is specified, set the cell `output_grid[special_row, special_column]` to the `corner_value`, potentially overwriting previous modifications.
5.  **Special Cell Modifications:** For each `special_cell` `(r, c)` with its designated `
