
## train_1

**input:**
```
0 5 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
5 0 0 0 0 5
0 0 0 0 0 0
```


**output:**
```
8 5 0 0 0 8 8 5 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
5 8 0 0 0 5 5 8 0 0 0 5
8 8 0 0 0 8 8 8 0 0 0 8
8 5 0 0 0 8 8 5 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
5 8 0 0 0 5 5 8 0 0 0 5
8 8 0 0 0 8 8 8 0 0 0 8
```


## train_2

**input:**
```
2 0 0
0 0 0
0 0 2
```


**output:**
```
2 0 8 2 0 8
8 0 8 8 0 8
8 0 2 8 0 2
2 0 8 2 0 8
8 0 8 8 0 8
8 0 2 8 0 2
```


## train_3

**input:**
```
0 4
0 0
```


**output:**
```
0 4 0 4
0 8 0 8
0 4 0 4
0 8 0 8
```

## Perception

1.  **Input/Output Format:** The input and output are both 2D grids containing numerical digits.
2.  **Grid Size:** The output grid's dimensions (height and width) are exactly double the input grid's dimensions.
3.  **Tiling:** The output grid appears to be constructed by tiling a modified version of the input grid in a 2x2 pattern.
4.  **Color/Value Transformation:**
    *   The original non-zero values from the input grid seem to be preserved in their corresponding positions within the modified grid before tiling.
    *   A new value, '8', appears in the output.
    *   The value '0' from the input can either remain '0' or be replaced by '8' in the modified grid.
5.  **Transformation Logic:** The key transformation happens *before* tiling. It involves analyzing the columns of the input grid. If a column in the input grid contains *any* non-zero value, then all the '0's within that same column are replaced by '8's in the modified grid. The original non-zero values in that column are kept. If a column contains only '0's, it remains unchanged in the modified grid.
6.  **Final Output Construction:** The modified grid (same dimensions as the input) is then repeated 2 times horizontally and 2 times vertically to form the final output grid.

## Facts


```yaml
elements:
  - object: input_grid
    properties:
      - type: 2D array of integers
      - dimensions: H x W
      - contains: cells with values (0 or non-zero integers like 2, 4, 5)
  - object: intermediate_grid
    properties:
      - type: 2D array of integers
      - dimensions: H x W (same as input_grid)
      - derived_from: input_grid
      - contains: cells with values (0, 8, or original non-zero integers)
  - object: output_grid
    properties:
      - type: 2D array of integers
      - dimensions: (2*H) x (2*W)
      - derived_from: intermediate_grid
      - structure: 2x2 tiling of intermediate_grid
  - object: column
    properties:
      - part_of: input_grid, intermediate_grid
      - contains: sequence of cell values
      - state: contains_non_zero (boolean)
  - object: cell
    properties:
      - value: integer (0, 2, 4, 5, 8)
      - position: (row, column)

actions:
  - name: create_intermediate_grid
    actor: system
    input: input_grid
    output: intermediate_grid
    steps:
      - Iterate through each column index `j` from 0 to W-1.
      - Check if any cell `input_grid[i][j]` (for any `i`) is non-zero.
      - If non-zero exists in the column:
        - For each row `i` from 0 to H-1:
          - If `input_grid[i][j]` is non-zero, set `intermediate_grid[i][j] = input_grid[i][j]`.
          - If `input_grid[i][j]` is 0, set `intermediate_grid[i][j] = 8`.
      - If only zeros exist in the column:
        - For each row `i` from 0 to H-1:
          - Set `intermediate_grid[i][j] = 0`.
  - name: tile_grid
    actor: system
    input: intermediate_grid
    output: output_grid
    steps:
      - Create an output grid with dimensions (2*H) x (2*W).
      - Copy the `intermediate_grid` into the top-left quadrant (rows 0 to H-1, cols 0 to W-1).
      - Copy the `intermediate_grid` into the top-right quadrant (rows 0 to H-1, cols W to 2*W-1).
      - Copy the `intermediate_grid` into the bottom-left quadrant (rows H to 2*H-1, cols 0 to W-1).
      - Copy the `intermediate_grid` into the bottom-right quadrant (rows H to 2*H-1, cols W to 2*W-1).

relationships:
  - output_grid is a 2x2 tiling of intermediate_grid.
  - intermediate_grid is derived from input_grid based on column content.
  - A cell's value in intermediate_grid depends on the values in the corresponding column of input_grid.
```


## Natural Language Program

1.  Initialize an `intermediate_grid` with the same dimensions as the `input_grid`.
2.  For each column in the `input_grid`:
    a.  Check if the column contains any non-zero value.
    b.  If it does contain a non-zero value:
        i.  Copy the non-zero values from the `input_grid` column to the corresponding positions in the `intermediate_grid` column.
        ii. Replace all the zero ('0') values in that `input_grid` column with eight ('8') in the corresponding positions in the `intermediate_grid` column.
    c.  If the column contains only zero ('0') values:
        i.  Copy the column of zeros directly to the corresponding column in the `intermediate_grid`.
3.  Create the `output_grid` with dimensions twice the height and twice the width of the `input_grid`.
4.  Tile the `intermediate_grid` into the `output_grid` in a 2x2 pattern, filling all four quadrants of the `output_grid`.
