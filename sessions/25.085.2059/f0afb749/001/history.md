
## train_1

**input:**
```
2 0
0 0
```


**output:**
```
2 2 0 0
2 2 0 0
0 0 1 0
0 0 0 1
```


## train_2

**input:**
```
0 0 0 5 0
0 5 0 0 0
0 0 0 0 0
0 5 0 0 0
0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 5 5 0 0
0 1 0 0 0 0 5 5 0 0
0 0 5 5 0 0 0 0 1 0
0 0 5 5 0 0 0 0 0 1
1 0 0 0 1 0 0 0 0 0
0 1 0 0 0 1 0 0 0 0
0 0 5 5 0 0 1 0 0 0
0 0 5 5 0 0 0 1 0 0
0 0 0 0 1 0 0 0 1 0
0 0 0 0 0 1 0 0 0 1
```


## train_3

**input:**
```
0 0 0 0 0 3
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 3
0 0 0 0 0 0 0 0 0 0 3 3
1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0
```

Okay, let's break down this task.

**Perception:**

1.  **Grid Size Transformation:** In all examples, the output grid is exactly twice the height and twice the width of the input grid.
2.  **Pixel Mapping:** Each pixel in the input grid corresponds to a 2x2 block of pixels in the output grid. Specifically, the input pixel at `(row, col)` maps to the output block starting at `(2*row, 2*col)`.
3.  **Color Transformation Rule:**
    *   If an input pixel is **not** white (color 0), its color is duplicated across the entire corresponding 2x2 block in the output grid.
    *   If an input pixel **is** white (color 0), the corresponding 2x2 block in the output grid is filled with a specific pattern: blue (color 1) in the top-left and bottom-right cells, and white (color 0) in the top-right and bottom-left cells. This resembles a 2x2 identity matrix where '1' is replaced by the blue color.

**YAML Facts:**


```yaml
task_type: Grid Transformation

grid_properties:
  - relationship: output grid dimensions are 2x input grid dimensions (height and width).
  - initialization: Output grid can be conceptually initialized as white (0).

pixel_mapping:
  - input_pixel_coords: (r, c)
  - output_block_coords_top_left: (2*r, 2*c)
  - output_block_size: 2x2

transformation_rules:
  - condition: Input pixel color is non-white (value != 0).
    action: Fill the corresponding 2x2 output block with the input pixel's color.
    input_element: single non-white pixel
    output_element: 2x2 block of same color

  - condition: Input pixel color is white (value == 0).
    action: Fill the corresponding 2x2 output block with a pattern.
    pattern:
      - cell: (top-left of block) set to blue (1)
      - cell: (bottom-right of block) set to blue (1)
      - cell: (top-right of block) set to white (0)
      - cell: (bottom-left of block) set to white (0)
    input_element: single white pixel
    output_element: 2x2 block with blue identity pattern
```


**Natural Language Program:**

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Create a new output grid with dimensions `(2*H, 2*W)`, initialized with the white color (0).
3.  Iterate through each cell of the input grid, using row index `r` from 0 to `H-1` and column index `c` from 0 to `W-1`.
4.  For each input cell `(r, c)`:
    a.  Get the `input_color` at `input[r][c]`.
    b.  Calculate the top-left coordinates of the corresponding 2x2 block in the output grid: `out_r = 2 * r`, `out_c = 2 * c`.
    c.  Check the `input_color`:
        i.  If `input_color` is *not* white (0):
            Set the output cells `output[out_r][out_c]`, `output[out_r+1][out_c]`, `output[out_r][out_c+1]`, and `output[out_r+1][out_c+1]` to `input_color`.
        ii. If `input_color` *is* white (0):
            Set the output cell `output[out_r][out_c]` to blue (1).
            Set the output cell `output[out_r+1][out_c+1]` to blue (1).
            (The other two cells, `output[out_r+1][out_c]` and `output[out_r][out_c+1]`, remain white from the initialization).
5.  Return the completed output grid.
