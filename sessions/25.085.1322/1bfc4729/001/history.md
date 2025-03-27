
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 1
4 0 0 0 0 0 0 0 0 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 0 0 0 0 0 0 0 0 6
7 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
```

Okay, let's break down this task.

**Perception**

1.  **Input Grid:** The input grids are 10x10. They consist mostly of white pixels (0), with typically two distinct non-white pixels at different locations.
2.  **Output Grid:** The output grids are also 10x10. They contain rectangular "frames" (hollow rectangles) constructed from the colors found in the input grid. The interior of the frames remains white.
3.  **Color Correspondence:** Each non-white pixel in the input seems to generate a frame of the *same color* in the output.
4.  **Frame Structure:** The frames always span the entire width of the grid (columns 0 through 9). Their vertical position and extent vary.
5.  **Positional Logic:** The vertical definition (top and bottom rows) of each frame appears linked to the position (row `R` and column `C_idx`) of the corresponding non-white pixel in the input grid.
6.  **Rule Division:** There seems to be a conditional logic based on the input pixel's row index (`R`). A dividing line appears to be between row 4 and row 5.
    *   If the input pixel's row `R` is in the top half (0-4), the resulting frame uses row `R` as its bottom edge and row 0 as its top edge.
    *   If the input pixel's row `R` is in the bottom half (5-9), the resulting frame uses the input pixel's *column index* `C_idx` as its top edge and row 9 (the grid bottom) as its bottom edge.
7.  **Construction:** The output grid seems to be built by starting with a white grid and then drawing the borders (top row, bottom row, first column, last column) for each calculated frame.

**Facts**


```yaml
task_context:
  grid_size: [10, 10] # Both input and output grids are 10x10 in the examples.

input_elements:
  - object: background
    color: white (0)
  - object: trigger_pixel
    count: variable (typically 2 in examples)
    properties:
      - color: non-white (1-9)
      - location: (row R, column C_idx)

output_elements:
  - object: background
    color: white (0)
  - object: frame
    count: matches count of input trigger_pixels
    properties:
      - color: same as corresponding trigger_pixel
      - shape: rectangular border
      - extent:
          left_col: 0
          right_col: 9 # grid_width - 1
          top_row: determined by rule
          bottom_row: determined by rule

transformation_rules:
  - rule: Frame Generation
    applies_to: each input trigger_pixel
    details:
      - identify: pixel P with color C at (R, C_idx)
      - condition: check row index R relative to midpoint (4.5 for 10 rows)
      - if R <= 4:
          frame_top_row: 0
          frame_bottom_row: R
      - if R >= 5:
          frame_top_row: C_idx # Based on column index of input pixel
          frame_bottom_row: 9 # grid_height - 1
      - action: Draw Frame Border
        target: output grid (initialized white)
        color: C
        rows: [frame_top_row, frame_bottom_row]
        columns: [0, 9] # left_col, right_col
        pixels_to_draw:
          - row frame_top_row, all columns 0-9
          - row frame_bottom_row, all columns 0-9
          - column 0, all rows frame_top_row to frame_bottom_row
          - column 9, all rows frame_top_row to frame_bottom_row
```


**Natural Language Program**

1.  Create a new output grid with the same dimensions as the input grid (e.g., 10x10), and fill it entirely with white pixels (color 0).
2.  Iterate through each pixel of the input grid to find all non-white pixels.
3.  For each non-white pixel found:
    a.  Record its row index `R`, column index `C_idx`, and color `C`.
    b.  Determine the vertical range (top row `min_row`, bottom row `max_row`) for the frame:
        i.  If the row index `R` is 4 or less, set `min_row` to 0 and `max_row` to `R`.
        ii. If the row index `R` is 5 or more, set `min_row` to the pixel's column index `C_idx` and `max_row` to the last row index of the grid (9 for a 10-row grid).
    c.  Paint the border of this frame onto the output grid using color `C`:
        i.  Change the color of all pixels in row `min_row` (from column 0 to the last column) to `C`.
        ii. Change the color of all pixels in row `max_row` (from column 0 to the last column) to `C`.
        iii. Change the color of all pixels in column 0 (from row `min_row` to `max_row`) to `C`.
        iv. Change the color of all pixels in the last column (column 9 for a 10-column grid) (from row `min_row` to `max_row`) to `C`.
4.  After processing all non-white pixels from the input, the resulting output grid is the final answer.
