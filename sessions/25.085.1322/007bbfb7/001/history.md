
## train_1

**input:**
```
6 6 0
6 0 0
0 6 6
```


**output:**
```
6 6 0 6 6 0 0 0 0
6 0 0 6 0 0 0 0 0
0 6 6 0 6 6 0 0 0
6 6 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0
0 0 0 6 6 0 6 6 0
0 0 0 6 0 0 6 0 0
0 0 0 0 6 6 0 6 6
```


## train_2

**input:**
```
4 0 4
0 0 0
0 4 0
```


**output:**
```
4 0 4 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
```


## train_3

**input:**
```
0 0 0
0 0 2
2 0 2
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 2
2 0 2 0 0 0 2 0 2
```


## train_4

**input:**
```
2 2 2
0 0 0
0 2 2
```


**output:**
```
2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 2 2
```


## train_5

**input:**
```
0 7 7
7 7 7
0 7 7
```


**output:**
```
0 0 0 0 7 7 0 7 7
0 0 0 7 7 7 7 7 7
0 0 0 0 7 7 0 7 7
0 7 7 0 7 7 0 7 7
7 7 7 7 7 7 7 7 7
0 7 7 0 7 7 0 7 7
0 0 0 0 7 7 0 7 7
0 0 0 7 7 7 7 7 7
0 0 0 0 7 7 0 7 7
```

**Perception**

1.  **Input/Output Size:** All input grids are 3x3. All output grids are 9x9. This indicates a scaling factor of 3 in both height and width.
2.  **Output Structure:** The 9x9 output grid appears to be constructed as a 3x3 arrangement of smaller 3x3 subgrids.
3.  **Pattern Mapping:** The content of each 3x3 subgrid in the output depends on the value of the corresponding pixel in the 3x3 input grid.
4.  **Rule:**
    *   If a pixel in the input grid at position `(r, c)` is *not* white (color 0), then the 3x3 subgrid in the output grid starting at position `(r * 3, c * 3)` is a direct copy of the *entire* original input grid.
    *   If a pixel in the input grid at position `(r, c)` *is* white (color 0), then the 3x3 subgrid in the output grid starting at position `(r * 3, c * 3)` is filled entirely with white (color 0).

**Facts**


```yaml
task_type: grid_transformation
input_properties:
  shape: [3, 3] # Inferred from examples, potentially variable
  element_type: color_value (0-9)
output_properties:
  shape: [9, 9] # Input height * 3, Input width * 3
  element_type: color_value (0-9)
transformation:
  type: conditional_tiling
  scale_factor: 3
  grid_division:
    meta_grid_rows: 3 # Same as input height
    meta_grid_cols: 3 # Same as input width
    subgrid_rows: 3 # Same as input height
    subgrid_cols: 3 # Same as input width
  condition:
    based_on: value of corresponding input pixel at (row // 3, col // 3)
    if_true (input pixel != white(0)):
      action: copy the entire input grid into the output subgrid
    if_false (input pixel == white(0)):
      action: fill the output subgrid with white(0)
```


**Natural Language Program**

1.  Get the input grid and determine its height (H) and width (W).
2.  Create a new output grid with dimensions (H \* 3) x (W \* 3). Initialize all pixels in the output grid to white (0).
3.  Iterate through each pixel of the input grid using its row index `r` (from 0 to H-1) and column index `c` (from 0 to W-1).
4.  For the current input pixel `input_grid[r][c]`:
    *   Check if its value is not white (0).
    *   If it is *not* white:
        *   Calculate the top-left corner coordinates of the corresponding subgrid in the output grid: `start_row = r * 3`, `start_col = c * 3`.
        *   Copy the entire original input grid into the output grid, starting at `(start_row, start_col)` and filling the H x W area from that point.
    *   If the input pixel *is* white (0), do nothing (the corresponding area in the output grid is already initialized to white).
5.  Return the completed output grid.
