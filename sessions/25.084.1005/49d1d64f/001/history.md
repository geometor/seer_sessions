
## train_1

**input:**
```
1 8 4
8 3 8
```


**output:**
```
0 1 8 4 0
1 1 8 4 4
8 8 3 8 8
0 8 3 8 0
```


## train_2

**input:**
```
1 2
3 8
```


**output:**
```
0 1 2 0
1 1 2 2
3 3 8 8
0 3 8 0
```


## train_3

**input:**
```
2 1 4
8 0 2
3 2 8
```


**output:**
```
0 2 1 4 0
2 2 1 4 4
8 8 0 2 2
3 3 2 8 8
0 3 2 8 0
```

**Perception**

1.  **Input and Output:** The task takes a smaller grid as input and produces a larger grid as output.
2.  **Size Transformation:** The output grid's dimensions are consistently 2 units larger than the input grid in both height and width (output\_height = input\_height + 2, output\_width = input\_width + 2).
3.  **Core Preservation:** The original input grid is preserved and located exactly in the center of the output grid, offset by one pixel from all edges.
4.  **Border Creation:** A border of width 1 is added around the central input grid.
5.  **Border Filling Pattern:**
    *   The four corner cells of the output grid are always `white` (0).
    *   The top border row (excluding corners) is filled with the colors from the *first* row of the input grid.
    *   The bottom border row (excluding corners) is filled with the colors from the *last* row of the input grid.
    *   The left border column (excluding corners) is filled with the colors from the *first* column of the input grid.
    *   The right border column (excluding corners) is filled with the colors from the *last* column of the input grid.
    *   This effectively "copies" or "extrudes" the edge pixels of the input grid outwards to form the border, except for the corners which are fixed to `white`.

**Facts**


```yaml
task: frame_edges_with_white_corners
description: Expands the input grid by adding a border, copying edge pixels outwards, and setting corners to white.

elements:
  - object: input_grid
    properties:
      - type: 2D array of integers (colors)
      - dimensions: height H, width W
  - object: output_grid
    properties:
      - type: 2D array of integers (colors)
      - dimensions: height H+2, width W+2

relationships:
  - type: containment
    description: The input_grid is placed in the center of the output_grid, starting at row 1, column 1 (0-indexed).
  - type: border_generation
    properties:
      - border_width: 1 pixel
      - corners: All four corners (output[0,0], output[0, W+1], output[H+1, 0], output[H+1, W+1]) are set to 'white' (0).
      - top_edge: output_grid row 0, columns 1 to W, are copied from input_grid row 0, columns 0 to W-1.
      - bottom_edge: output_grid row H+1, columns 1 to W, are copied from input_grid row H-1, columns 0 to W-1.
      - left_edge: output_grid column 0, rows 1 to H, are copied from input_grid column 0, rows 0 to H-1.
      - right_edge: output_grid column W+1, rows 1 to H, are copied from input_grid column W-1, rows 0 to H-1.

actions:
  - action: resize
    actor: system
    input: input_grid
    output: output_grid shell (initially maybe all white)
    details: Create a new grid with dimensions H+2, W+2.
  - action: copy_center
    actor: system
    input: input_grid
    target: output_grid[1:H+1, 1:W+1]
    details: Copy the entire input_grid to the central region of the output_grid.
  - action: fill_border
    actor: system
    input: input_grid edges
    target: output_grid border cells (excluding corners)
    details: Copy the corresponding edge rows/columns from the input_grid to the border cells.
  - action: set_corners
    actor: system
    target: output_grid corners
    details: Set the four corner cells of the output_grid to 'white' (0).

```


**Natural Language Program**

1.  Determine the height (H) and width (W) of the input grid.
2.  Create a new output grid with height H+2 and width W+2.
3.  Copy the input grid into the center of the output grid, specifically into the region defined by rows 1 to H (inclusive) and columns 1 to W (inclusive).
4.  Fill the border of the output grid:
    a.  Copy the first row of the input grid (input\_grid\[0, :]) into the top border row of the output grid, excluding the corners (output\_grid\[0, 1:W+1]).
    b.  Copy the last row of the input grid (input\_grid\[H-1, :]) into the bottom border row of the output grid, excluding the corners (output\_grid\[H+1, 1:W+1]).
    c.  Copy the first column of the input grid (input\_grid\[:, 0]) into the left border column of the output grid, excluding the corners (output\_grid\[1:H+1, 0]).
    d.  Copy the last column of the input grid (input\_grid\[:, W-1]) into the right border column of the output grid, excluding the corners (output\_grid\[1:H+1, W+1]).
5.  Set the four corner cells of the output grid (at indices [0, 0], [0, W+1], [H+1, 0], and [H+1, W+1]) to `white` (0).
6.  Return the completed output grid.
