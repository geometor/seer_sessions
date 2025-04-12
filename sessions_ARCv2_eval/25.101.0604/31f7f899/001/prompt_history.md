
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8
8 8 8 8 8 8 7
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 8 8 8 8 7
8 8 8 8 8 8 8
```

## Perception

The task involves transforming an input grid of digits into an output grid. Key elements observed:
1.  **Grid Structure:** Both input and output are rectangular grids of single digits.
2.  **Background Color:** The digit '8' serves as a predominant background color.
3.  **Axis Row:** A unique row exists in each input grid, characterized by the presence of the digit '6' and potentially other non-'8' digits. This row remains unchanged in the output and acts as a horizontal axis of transformation. Let's call its index 'R'.
4.  **Axis Pattern:** The non-'6' digits within the axis row R form a pattern that seems crucial for the transformation.
5.  **Transformation Logic:** The output grid appears to be constructed by reflecting or projecting the axis pattern vertically, symmetrically around the axis row R.
6.  **Filtering/Masking:** The projection isn't a simple copy. The values from the input grid at both a cell's location `(r, c)` and its symmetric location `(r_sym, c)` relative to the axis R influence whether the axis pattern value `input[R, c]` appears at `output[r, c]`. Specifically, it appears that `output[r, c]` takes the value `input[R, c]` if the symmetrically opposite input cell `input[r_sym, c]` matches `input[R, c]`.

## Facts

```yaml
objects:
  - name: input_grid
    properties:
      - type: 2D array of integers (digits 0-9)
      - background_color: 8
      - contains_axis_row: true
  - name: output_grid
    properties:
      - type: 2D array of integers (digits 0-9)
      - dimensions: same as input_grid
      - background_color: 8
  - name: axis_row
    properties:
      - type: row vector within the input_grid
      - identifier: contains the digit 6
      - index: R
      - contains_axis_pattern: true
  - name: axis_pattern
    properties:
      - type: set of (value, column_index) pairs
      - derived_from: axis_row (values != 6)
  - name: cell
    properties:
      - row_index: r
      - column_index: c
      - value: integer (digit 0-9)
      - location: (r, c) in a grid
relationships:
  - type: symmetry
    between: cell (r, c) and cell (r_sym, c)
    where: r_sym = R + (R - r)
  - type: source
    subject: axis_pattern
    object: output_grid non-background values (excluding axis row)
actions:
  - name: identify_axis_row
    input: input_grid
    output: axis_row_index R
  - name: extract_axis_pattern
    input: input_grid[R]
    output: axis_pattern P
  - name: initialize_output
    produces: output_grid (filled with background color 8)
  - name: copy_axis_row
    source: input_grid[R]
    destination: output_grid[R]
  - name: populate_output_cell
    inputs:
      - output_grid cell (r, c)
      - input_grid cell (r, c)
      - input_grid cell (r_sym, c)
      - input_grid cell (R, c) (axis value)
    condition:
      - r != R
      - input[R, c] != 6
      - input[r_sym, c] == input[R, c] # Based on Hypothesis 15
    effect: sets output_grid[r, c] = input[R, c]
```

## Natural Language Program

1.  Identify the horizontal row in the `input_grid` that contains the digit '6'. Let the index of this row be `R`. This is the 'axis row'.
2.  Create a new `output_grid` with the same dimensions as the `input_grid`, initially filled entirely with the background color '8'.
3.  Copy the entire axis row `R` from the `input_grid` to the `output_grid` at row `R`.
4.  Iterate through each row `r` of the `input_grid`, excluding the axis row `R`.
5.  For each row `r`, calculate the index of the symmetrically opposite row `r_sym = R + (R - r)`.
6.  If `r_sym` is outside the bounds of the grid (less than 0 or greater than or equal to the grid height), skip processing for this row `r` (its corresponding row in the `output_grid` remains background '8').
7.  If `r_sym` is within the grid bounds, iterate through each column `c` from 0 to the grid width minus 1.
8.  Get the value from the axis row at this column: `val_axis = input_grid[R, c]`.
9.  If `val_axis` is equal to '6', skip processing for this column `c` (the cell `output_grid[r, c]` remains background '8').
10. Get the value from the symmetric input row at this column: `val_sym = input_grid[r_sym, c]`.
11. Compare `val_sym` with `val_axis`. If they are equal (`val_sym == val_axis`), set the corresponding cell in the `output_grid` to the axis value: `output_grid[r, c] = val_axis`.
12. If `val_sym` is not equal to `val_axis`, the cell `output_grid[r, c]` remains background '8'.
13. After iterating through all rows `r` (except `R`) and all columns `c`, the `output_grid` is complete.
