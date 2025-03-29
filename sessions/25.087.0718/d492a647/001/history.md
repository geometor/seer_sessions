
## train_1

**input:**
```
5 0 5 0 5 5 5 5 5 5 5 0 5 0 5 5
0 5 5 0 5 5 5 0 5 0 0 5 0 0 5 5
5 5 5 0 0 0 0 0 0 0 0 0 0 5 5 0
5 5 0 0 0 0 0 0 0 0 0 5 0 5 5 0
5 0 5 0 0 0 0 0 0 0 0 5 5 5 0 0
5 5 5 0 0 0 0 3 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 0 0 0 0 5 5 0 5 0
0 5 5 0 0 0 0 0 0 0 0 0 5 5 5 5
0 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5
0 5 5 5 0 5 5 5 5 5 0 5 0 5 0 0
5 5 5 5 0 5 0 5 0 0 0 5 0 5 0 0
0 5 5 0 0 5 0 5 0 0 0 0 5 5 0 5
5 5 0 5 5 5 5 5 5 0 5 5 5 5 0 5
```


**output:**
```
5 0 5 0 5 5 5 5 5 5 5 0 5 0 5 5
0 5 5 3 5 5 5 3 5 3 0 5 0 3 5 5
5 5 5 0 0 0 0 0 0 0 0 0 0 5 5 0
5 5 0 3 0 3 0 3 0 3 0 5 0 5 5 3
5 0 5 0 0 0 0 0 0 0 0 5 5 5 0 0
5 5 5 3 0 3 0 3 0 3 0 3 0 5 0 3
0 5 0 0 0 0 0 0 0 0 0 5 5 0 5 0
0 5 5 3 0 3 0 3 0 3 0 3 5 5 5 5
0 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5
0 5 5 5 0 5 5 5 5 5 0 5 0 5 0 3
5 5 5 5 0 5 0 5 0 0 0 5 0 5 0 0
0 5 5 3 0 5 0 5 0 3 0 3 5 5 0 5
5 5 0 5 5 5 5 5 5 0 5 5 5 5 0 5
```


## train_2

**input:**
```
0 0 5 0 5 5 5 0 5 0 5 5 5
5 5 0 5 0 0 5 5 0 5 5 5 5
5 0 5 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 1 0 0 0 0 0 5 5
0 5 5 0 0 0 0 0 0 0 0 5 5
0 5 5 0 0 0 0 0 0 0 0 0 5
5 0 5 0 0 0 0 0 0 0 0 0 5
5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5
0 0 5 5 0 5 0 5 0 5 5 5 5
5 5 5 0 5 5 5 5 5 5 5 5 5
5 5 0 5 0 5 5 5 5 0 5 0 5
```


**output:**
```
0 1 5 1 5 5 5 1 5 1 5 5 5
5 5 0 5 0 0 5 5 0 5 5 5 5
5 1 5 1 0 1 0 1 0 1 0 1 0
5 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 1 0 1 0 1 0 1 0 5 5
0 5 5 0 0 0 0 0 0 0 0 5 5
0 5 5 1 0 1 0 1 0 1 0 1 5
5 0 5 0 0 0 0 0 0 0 0 0 5
5 5 5 1 0 1 0 1 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0 0 5 5
0 1 5 5 0 5 0 5 0 5 5 5 5
5 5 5 0 5 5 5 5 5 5 5 5 5
5 5 0 5 0 5 5 5 5 1 5 1 5
```

*   **Perception:**
    *   The input and output are grids of the same dimensions.
    *   The grids contain pixels of three main colors: white (0), gray (5), and one other "target" color (green=3 in train_1, blue=1 in train_2).
    *   Gray pixels typically form an outer border or structure and remain unchanged between input and output.
    *   The input grid contains exactly one pixel of the "target" color, located somewhere within the grid.
    *   The transformation involves changing *some* of the white (0) pixels to the "target" color.
    *   The rule for changing a white pixel seems to depend on the coordinates (row and column indices) of the pixel and the coordinates of the single "target" color pixel found in the input.
    *   Specifically, a white pixel is changed to the target color if its row parity (odd/even) matches the row parity of the input target pixel, AND its column parity (odd/even) matches the column parity of the input target pixel.
    *   All non-white pixels (gray and the original target pixel) remain unchanged in the output.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    components:
      - item: grid
        properties:
          - dimensions: height, width (consistent between input and output)
          - background_color: white (0)
          - frame_color: gray (5) (generally unchanged)
          - target_color_pixel:
              count: 1 per input grid
              role: defines the color to paint with and the parity rule
              value: non-white, non-gray color (e.g., green=3, blue=1)
              location: (target_row, target_col)
      - item: pixel
        properties:
          - color: (0-9)
          - location: (row, col)
          - parity:
              row_parity: odd or even based on row index
              col_parity: odd or even based on col index
    transformation:
      action: conditional_color_change
      condition:
        - applies_to: pixels with input color white (0)
        - rule: change color to target_color IF (pixel.row_parity == target_color_pixel.row_parity) AND (pixel.col_parity == target_color_pixel.col_parity)
      unchanged:
        - pixels with input color gray (5)
        - the original target_color_pixel
        - white pixels not meeting the parity condition
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Scan the input grid to find the single pixel that is neither white (0) nor gray (5). Record its color as the `target_color` and its location as (`target_row`, `target_col`).
    3.  Determine the parity (odd or even) of `target_row`. Let this be `target_row_parity`.
    4.  Determine the parity (odd or even) of `target_col`. Let this be `target_col_parity`.
    5.  Iterate through each pixel of the input grid at location (`r`, `c`).
    6.  Check if the color of the input pixel at (`r`, `c`) is white (0).
    7.  If it is white, determine the parity of the current row `r` (`current_row_parity`) and the parity of the current column `c` (`current_col_parity`).
    8.  Compare the parities: If `current_row_parity` matches `target_row_parity` AND `current_col_parity` matches `target_col_parity`, then change the color of the pixel at location (`r`, `c`) in the *output* grid to the `target_color`.
    9.  If the input pixel is not white, or if the parities do not match the target parities, the corresponding pixel in the output grid retains its original color (from the initial copy).
    10. Return the final output grid.
