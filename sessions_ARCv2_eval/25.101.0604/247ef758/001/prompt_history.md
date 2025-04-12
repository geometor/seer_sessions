
## train_1

**input:**
```
0 4 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
4 4 4 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 4 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 7 0 0 0 0 0 0 0 0 0 0 0 0 7
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
7 7 7 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
7 7 7 2 6 0 0 0 0 0 0 0 0 0 0 0 0 6
7 7 7 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
```


**output:**
```
0 0 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 4 0 0 0 0 0 0 0 3
0 0 0 2 4 0 0 0 4 4 4 0 0 0 0 0 0 4
0 0 0 2 3 0 0 0 0 4 7 7 0 0 0 0 0 3
0 0 0 2 7 0 0 0 0 7 7 7 0 0 0 0 0 7
0 0 0 2 3 0 0 0 0 7 7 7 0 0 0 0 0 3
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 6 0 0 0 0 0 0 0 0 0 0 0 0 6
0 0 0 2 3 0 0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 2 3 3 6 3 3 4 7 3 3 3 3 3 3 3
```


## train_2

**input:**
```
0 5 0 0 3 4 4 7 4 5 4 7 4 4 4
5 0 5 0 3 4 0 0 0 0 0 0 0 0 4
0 5 0 0 3 7 0 0 0 0 0 0 0 0 7
8 0 0 0 3 4 0 0 0 0 0 0 0 0 4
0 8 0 0 3 4 0 0 0 0 0 0 0 0 4
0 0 8 0 3 5 0 0 0 0 0 0 0 0 5
0 7 0 0 3 4 0 0 0 0 0 0 0 0 4
7 7 7 0 3 7 0 0 0 0 0 0 0 0 7
0 7 0 0 3 4 0 0 0 0 0 0 0 0 4
0 0 0 0 3 4 4 7 4 5 4 7 4 4 4
```


**output:**
```
0 0 0 0 3 4 4 7 4 5 4 7 4 4 4
0 0 0 0 3 4 0 7 0 0 0 7 0 0 4
0 0 0 0 3 7 7 7 7 0 7 7 7 0 7
8 0 0 0 3 4 0 7 0 0 0 7 0 0 4
0 8 0 0 3 4 0 0 0 5 0 0 0 0 4
0 0 8 0 3 5 0 0 5 0 5 0 0 0 5
0 0 0 0 3 4 0 7 0 5 0 7 0 0 4
0 0 0 0 3 7 7 7 7 0 7 7 7 0 7
0 0 0 0 3 4 0 7 0 0 0 7 0 0 4
0 0 0 0 3 4 4 7 4 5 4 7 4 4 4
```


## train_3

**input:**
```
0 3 0 1 2 2 2 3 2 2 2 6 2 2
3 3 3 1 2 0 0 0 0 0 0 0 0 2
0 3 0 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 3 0 0 0 0 0 0 0 0 3
0 6 0 1 2 0 0 0 0 0 0 0 0 2
6 0 6 1 2 0 0 0 0 0 0 0 0 2
0 6 0 1 6 0 0 0 0 0 0 0 0 6
0 0 0 1 2 0 0 0 0 0 0 0 0 2
7 7 7 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 2 2 2 3 2 2 2 6 2 2
```


**output:**
```
0 0 0 1 2 2 2 3 2 2 2 6 2 2
0 0 0 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 2 0 0 3 0 0 0 0 0 2
0 0 0 1 3 0 3 3 3 0 0 0 0 3
0 0 0 1 2 0 0 3 0 0 0 0 0 2
0 0 0 1 2 0 0 0 0 0 0 6 0 2
0 0 0 1 6 0 0 0 0 0 6 0 6 6
0 0 0 1 2 0 0 0 0 0 0 6 0 2
7 7 7 1 2 0 0 0 0 0 0 0 0 2
0 0 0 1 2 2 2 3 2 2 2 6 2 2
```

## Perception

1.  **Input/Output Format:** Both input and output are 2D grids of numerical digits, likely representing colors where '0' is the background.
2.  **Grid Dimensions:** The output grid always has the same dimensions as the input grid.
3.  **Axis Column:** A key feature is a vertical column (the "axis") that is mostly preserved from input to output. Its horizontal position varies between tasks (col 3 in train_1, col 4 in train_2, col 3 in train_3). This column seems to act as a separator.
4.  **Value Column:** The column immediately to the right of the axis column (the "value column") in the input plays a crucial role. The value in this column for a given row determines how the right side of that output row is constructed.
5.  **Left Zone Modification:** The area to the left of the axis column in the input is mostly cleared (set to 0) in the output for the middle rows. There are some exceptions where parts of the left side are preserved, but the general rule seems to be clearing.
6.  **Right Zone Modification:** The area to the right of the axis column is significantly modified. For the middle rows, the output pattern seems determined by the value `C` found in the corresponding row of the "value column" (`input[row, axis_col + 1]`). It appears that each non-zero color `C` maps to a specific, predefined shape or "glyph" for that task. This glyph, using color `C` (and sometimes other colors specific to the glyph, like in train_2 and train_3), is drawn onto the right side of the output row, typically centered horizontally within the right zone. If `C` is 0, the right zone remains 0.
7.  **Boundary Rows:** The top and bottom rows of the grid seem to be treated specially: they are copied directly from the input to the output without modification.

## Facts

```yaml
objects:
  - name: input_grid
    properties:
      - grid of digits (colors)
      - height H
      - width W
  - name: output_grid
    properties:
      - grid of digits (colors)
      - height H
      - width W
  - name: axis_column
    properties:
      - vertical column in the grid
      - index: axis_col
      - largely preserved between input and output
      - separates left and right zones
  - name: value_column
    properties:
      - vertical column in the input grid
      - index: axis_col + 1
      - contains selector_color values
  - name: left_zone
    properties:
      - region of the grid
      - columns: 0 to axis_col - 1
  - name: right_zone
    properties:
      - region of the grid
      - columns: axis_col + 1 to W - 1
  - name: middle_rows
    properties:
      - rows: 1 to H - 2
  - name: boundary_rows
    properties:
      - rows: 0 and H - 1
  - name: selector_color
    properties:
      - color C found in input[row, value_column_index]
      - determines the glyph for the output right_zone
  - name: glyph_pattern
    properties:
      - predefined 1D pattern of colors associated with a selector_color C
      - specific to each task (train_1, train_2, train_3 have different glyph sets)
      - drawn into the output right_zone

actions:
  - name: identify_axis_column
    actor: system
    operates_on: input_grid
    description: Find the index (axis_col) of the vertical dividing column.
  - name: copy_column
    actor: system
    operates_on: input_grid, output_grid, axis_column
    description: Copy the axis_column from input to output.
  - name: copy_rows
    actor: system
    operates_on: input_grid, output_grid, boundary_rows
    description: Copy the top and bottom rows from input to output.
  - name: clear_zone
    actor: system
    operates_on: output_grid, left_zone, middle_rows
    description: Set the cells in the left_zone of middle_rows to 0.
  - name: select_color
    actor: system
    operates_on: input_grid, value_column, middle_rows
    description: Get the selector_color C for each middle row r from input[r, axis_col + 1].
  - name: retrieve_glyph
    actor: system
    operates_on: selector_color
    description: Look up the predefined glyph_pattern associated with the selector_color C for the current task.
  - name: draw_glyph
    actor: system
    operates_on: output_grid, right_zone, middle_rows, glyph_pattern
    description: Clear the right_zone and draw the retrieved glyph_pattern into the output row's right_zone, horizontally centered.

relationships:
  - type: spatial
    from: axis_column
    to: left_zone, right_zone
    description: axis_column separates left_zone and right_zone.
  - type: determination
    from: selector_color
    to: glyph_pattern
    description: The selector_color determines which glyph_pattern is used.
  - type: placement
    from: glyph_pattern
    to: output_grid, right_zone
    description: The glyph_pattern is placed within the right_zone of the output_grid.
  - type: preservation
    from: input_grid, boundary_rows
    to: output_grid, boundary_rows
    description: Boundary rows are preserved from input to output.
```

## Natural Language Program

1.  Initialize the `output_grid` with the same dimensions as the `input_grid`.
2.  Identify the vertical `axis_column` in the `input_grid` (this seems to be the first column from the left containing non-zero values that isn't part of a uniform border). Let its index be `axis_col`.
3.  Copy the entire `axis_column` from the `input_grid` to the `output_grid` at index `axis_col`.
4.  Copy the entire top row (row 0) and bottom row (row H-1) from the `input_grid` to the `output_grid`.
5.  For each middle row `r` (from row 1 to H-2):
    a.  Set all cells in the `left_zone` (columns 0 to `axis_col - 1`) of the `output_grid` at row `r` to 0 (background color).
    b.  Get the `selector_color` `C` from the `input_grid` at position (`r`, `axis_col + 1`).
    c.  Clear all cells in the `right_zone` (columns `axis_col + 1` to W-1) of the `output_grid` at row `r` to 0.
    d.  If `C` is not 0:
        i.  Retrieve the task-specific `glyph_pattern` associated with color `C`.
        ii. Calculate the starting column index to place the `glyph_pattern` so it is horizontally centered within the `right_zone` for row `r`.
        iii. Draw the `glyph_pattern` onto the `output_grid` at row `r` starting at the calculated column index.
