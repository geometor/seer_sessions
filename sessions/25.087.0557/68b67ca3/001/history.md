
## train_1

**input:**
```
2 0 2 0 1 0
0 0 0 0 0 0
2 0 1 0 0 0
0 0 0 0 0 0
3 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
2 2 1
2 1 0
3 0 0
```


## train_2

**input:**
```
3 0 0 0 2 0
0 0 0 0 0 0
8 0 0 0 8 0
0 0 0 0 0 0
0 0 1 0 0 0
0 0 0 0 0 0
```


**output:**
```
3 0 2
8 0 8
0 1 0
```


## train_3

**input:**
```
1 0 0 0 0 0
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
6 0 0 0 6 0
0 0 0 0 0 0
```


**output:**
```
1 0 0
0 2 0
6 0 6
```

**Perception**

1.  **Grid Structure:** The input grids are consistently 6x6, while the output grids are 3x3.
2.  **Pixel Content:** The input grids feature a sparse pattern where non-white pixels (colors other than 0) appear primarily at intersections of even-numbered rows (0, 2, 4) and even-numbered columns (0, 2, 4). Odd-numbered rows and columns (1, 3, 5) consist entirely of white pixels (0).
3.  **Transformation:** The transformation involves selecting specific pixels from the input grid to form the output grid. The output grid seems to be a downsampled version of the input grid.
4.  **Mapping:** Comparing the input and output grids reveals a consistent mapping: the pixel at position (r, c) in the 3x3 output grid corresponds to the pixel at position (2*r, 2*c) in the 6x6 input grid.
5.  **Color Preservation:** The colors of the selected pixels are preserved exactly from the input to the output. White pixels (0) are also copied if they are at the sampled locations.

**Facts**


```yaml
task_type: grid_transformation
input_grid:
  size: 6x6
  properties:
    - Contains various colors (0-9).
    - White pixels (0) act as background.
    - Non-white pixels are primarily located at coordinates (row, col) where both row and col are even numbers (0, 2, 4).
    - Odd-numbered rows and columns are entirely white (0).
output_grid:
  size: 3x3
  properties:
    - Contains colors sampled from the input grid.
transformation:
  type: sampling
  description: Selects pixels from the input grid based on their coordinates.
mapping_rule:
  input_coord: (row_in, col_in)
  output_coord: (row_out, col_out)
  relationship: row_in = row_out * 2, col_in = col_out * 2
color_handling: Colors are preserved during sampling.
```


**Natural Language Program**

1.  Create a new grid with dimensions 3x3, initialized with a default color (e.g., white/0).
2.  Iterate through each row index `r_out` from 0 to 2 and each column index `c_out` from 0 to 2 of the output grid.
3.  For each output grid cell at (`r_out`, `c_out`), identify the corresponding source cell in the input grid using the coordinates (`r_in = r_out * 2`, `c_in = c_out * 2`).
4.  Copy the color value from the input grid cell at (`r_in`, `c_in`) to the output grid cell at (`r_out`, `c_out`).
5.  Return the populated 3x3 output grid.
