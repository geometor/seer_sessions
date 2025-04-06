
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids of integers, representing colors (0 typically being the background). The grid dimensions vary between examples.
2.  **Core Transformation:** The output grid is largely identical to the input grid, with some specific cells changing color from 0 to a non-zero color. The transformation adds new colored points based on a pattern derived from the input.
3.  **Key Feature - Bottom Row:** The bottom row of the input grid seems critical. It contains patterns of non-zero colors that determine the transformation.
4.  **Source Identification:** Within the bottom row, there appears to be a "source" element. This source is characterized by its color and its central position within a contiguous block of non-zero colors in that row.
    *   In `train_1`, the source is the central '1' from the `1 1 1` block.
    *   In `train_2`, the source is the central '3' from the `3` block.
    *   In `train_3`, the source is the central '4' from the `4 4 4` block.
    *   In `train_4`, the source is the central '4' from the `4` block.
5.  **Projection Pattern:** New points are added in the rows *above* the source cell. These points use the *source color*. They form a symmetrical pattern expanding upwards and outwards from the source cell's column.
6.  **Projection Rule Dependency:** The exact pattern (the "slope" of the diagonal projection) depends on the *length* of the contiguous block containing the source color in the bottom row.
    *   If the block length is 1 (e.g., `train_2`, `train_4`), the projection seems to follow one rule (`abs(horizontal_offset) = vertical_offset - 1`).
    *   If the block length is greater than 1 (e.g., `train_1`, `train_3`, which have length 3), the projection follows another rule (`abs(horizontal_offset) = vertical_offset`).
7.  **No Overwriting:** The added points only change cells that were originally 0 (background color). Existing non-zero cells from the input are preserved.

**YAML Facts:**


```yaml
task_description: Projecting a pattern upwards from a source element in the bottom row.

elements:
  - object: grid
    properties:
      - type: 2D array of integers (colors)
      - size: variable rows and columns
  - object: cell
    properties:
      - coordinates: (row, column)
      - color: integer (0 is background)
  - object: bottom_row
    properties:
      - location: last row of the grid
      - contains: patterns of non-zero colors
  - object: source_block
    properties:
      - location: within the bottom row
      - type: contiguous horizontal sequence of non-zero cells
      - centrality: typically the single centrally located block
      - length: number of cells in the block
  - object: source_cell
    properties:
      - location: central cell within the source_block
      - coordinates: (R, C) where R is the last row index
      - color: X (the color value of the cell)
  - object: projected_points
    properties:
      - location: cells above the source_cell (row < R)
      - color: same as source_color X
      - condition: only added if the target cell is initially background color (0)
      - pattern: symmetrical around the source_cell's column C

relationships:
  - type: dependency
    from: projected_points.location
    to: source_cell.location
    details: Points (r, c) are generated based on (R, C).
  - type: dependency
    from: projected_points.color
    to: source_cell.color
    details: Projected points take the color X.
  - type: dependency
    from: projected_points.pattern
    to: source_block.length (L)
    details: |
      The relationship between vertical distance (k = R - r) and horizontal distance (d = abs(c - C)) depends on L.
      If L == 1, then d = k - 1.
      If L > 1, then d = k.
  - type: constraint
    on: projected_points
    details: Projection starts from k=2 (i.e., r = R - 2), not the row immediately above (k=1). Projection occurs only within grid boundaries.

actions:
  - action: identify_source
    steps:
      - locate bottom row R
      - find contiguous non-zero blocks in row R
      - select the central block
      - find the central cell (R, C) and its color X within that block
      - determine block length L
  - action: project_pattern
    steps:
      - copy input grid to output grid
      - determine projection rule based on L (d = k-1 or d = k)
      - iterate k from 2 up to R
      - calculate target row r = R - k
      - calculate target columns c1 = C - d, c2 = C + d
      - for each target (r, c):
        - check if (r, c) is within grid bounds
        - check if output[r][c] is 0
        - if both true, set output[r][c] = X
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Identify the index of the bottom row, `R`.
3.  Analyze the bottom row (`input_grid[R]`) to find the centrally located contiguous block of non-zero colored cells.
4.  Determine the column index `C` and color `X` of the central cell within this central block.
5.  Measure the length `L` of
