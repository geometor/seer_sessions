
## train_1

**input:**
```
4 4 4 2 4 4 4
4 4 4 2 4 1 4
4 4 4 2 4 4 4
2 2 2 2 2 2 2
4 4 4 2 4 4 4
4 4 4 2 4 4 4
4 4 4 2 4 4 4
```


**output:**
```
4 4 4
4 1 4
4 4 4
```


## train_2

**input:**
```
8 8 3 8 8
8 8 3 8 8
3 3 3 3 3
8 8 3 8 8
4 8 3 8 8
```


**output:**
```
8 8
4 8
```


## train_3

**input:**
```
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 8 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
1 1 1 1 1 1 1 1 1 1 1
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
3 3 3 3 3 1 3 3 3 3 3
```


**output:**
```
3 3 3 3 3
3 3 3 3 3
3 8 3 3 3
3 3 3 3 3
3 3 3 3 3
```

## Perception

1.  **Input/Output Format:** Both input and output are 2D grids containing single-digit integers.
2.  **Separator Lines:** The input grids consistently feature one row and one column composed entirely of a single, repeating digit. These lines act as separators, dividing the grid.
3.  **Separator Digit Consistency:** The digit used in the separator row is always the same as the digit used in the separator column for a given input grid.
4.  **Subgrid Extraction:** The output grid is always a subgrid (quadrant) extracted from the input grid, relative to the separator lines. The separator lines themselves are excluded from the output.
5.  **Quadrant Selection:** The specific quadrant chosen for the output seems to depend on the value of the digit forming the separator lines. In the examples:
    *   Separator digit `1` or `2` results in the top-left quadrant being selected.
    *   Separator digit `3` results in the bottom-left quadrant being selected.

## Facts


```yaml
objects:
  - name: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: variable (rows x columns)
      - contains: separator_row, separator_column
  - name: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: smaller than input_grid
      - relationship: is a subgrid (quadrant) of input_grid
  - name: separator_row
    properties:
      - type: row within input_grid
      - composition: consists of a single repeated integer (separator_digit)
      - index: R
  - name: separator_column
    properties:
      - type: column within input_grid
      - composition: consists of a single repeated integer (separator_digit)
      - index: C
  - name: separator_digit
    properties:
      - type: integer
      - value: determines which quadrant is selected
      - relationship: same value for both separator_row and separator_column
  - name: quadrant
    properties:
      - type: subgrid of input_grid
      - location: defined relative to separator_row (index R) and separator_column (index C)
        - Top-Left: rows 0 to R-1, cols 0 to C-1
        - Top-Right: rows 0 to R-1, cols C+1 to end
        - Bottom-Left: rows R+1 to end, cols 0 to C-1
        - Bottom-Right: rows R+1 to end, cols C+1 to end
actions:
  - name: identify_separator_lines
    input: input_grid
    output: separator_row (index R), separator_column (index C), separator_digit (S)
    steps:
      - Find the row where all elements are identical. Record its index (R) and the repeated digit (S_row).
      - Find the column where all elements are identical. Record its index (C) and the repeated digit (S_col).
      - Verify S_row equals S_col. Set separator_digit (S) to this value.
  - name: select_quadrant
    input: separator_digit (S), separator_row_index (R), separator_column_index (C)
    output: coordinates of the target quadrant
    logic:
      - If S is 1 or 2, select the Top-Left quadrant (rows 0 to R-1, cols 0 to C-1).
      - If S is 3, select the Bottom-Left quadrant (rows R+1 to end, cols 0 to C-1).
      - (Rule may need extension for other separator digits).
  - name: extract_subgrid
    input: input_grid, quadrant_coordinates
    output: output_grid
    steps:
      - Copy the elements from the input_grid within the specified row and column ranges defined by the quadrant_coordinates.

relationships:
  - The output_grid is derived from the input_grid by identifying separator lines and extracting a specific quadrant based on the separator digit.
  - The separator_digit dictates the selection logic for the output quadrant.
```


## Natural Language Program

1.  Examine the input grid to find the row (`separator_row`) that consists of a single, repeated digit. Note the index (`R`) of this row and the value of the repeated digit (`S`).
2.  Examine the input grid to find the column (`separator_column`) that consists of the same repeated digit (`S`). Note the index (`C`) of this column.
3.  Based on the value of the `separator_digit` (`S`):
    *   If `S` is 1 or 2, select the **Top-Left** quadrant of the input grid. This quadrant includes all cells from row 0 up to (but not including) row `R`, and from column 0 up to (but not including) column `C`.
    *   If `S` is 3, select the **Bottom-Left** quadrant of the input grid. This quadrant includes all cells from the row after `R` (row `R+1`) to the last row, and from column 0 up to (but not including) column `C`.
4.  Construct the output grid using the cells from the selected quadrant.
