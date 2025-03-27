
## train_1

**input:**
```
9 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 3
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 7
```


**output:**
```
9 0 0 0 0 0 0 3 0 0
0 9 0 0 0 0 0 0 3 0
0 0 9 0 0 0 8 0 0 3
0 0 0 9 0 8 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 8 0 7 0 0 0 0
0 0 8 0 0 0 7 0 0 0
0 8 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
```


## train_2

**input:**
```
0 0 2 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
```


**output:**
```
0 0 2 0 0 6 0 0 0 0
0 2 0 0 0 0 6 0 0 0
2 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6
0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0
```


## train_3

**input:**
```
0 0 0 6 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 0 8 0 0 0 0
0 0 6 0 0 0 8 0 0 0
0 6 4 0 0 0 0 8 0 0
6 0 0 4 0 0 0 0 8 0
0 0 0 0 4 0 0 0 0 8
0 0 0 0 9 4 0 0 0 0
0 0 0 9 0 0 4 0 0 0
0 0 9 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids consist of a white background (value 0) with a few scattered, isolated pixels of various non-white colors.
    *   The output grids retain the original colored pixels from the input.
    *   Additional colored pixels appear in the output, forming diagonal lines extending from each of the original colored pixels.
    *   These lines always extend downwards and to the left.
    *   The color of each line matches the color of the original pixel it originates from.
    *   The lines terminate when they reach either the bottom edge or the left edge of the grid.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    background_color: white
    input_elements:
      - type: isolated_pixels
        properties:
          - color: non-white (various)
          - quantity: multiple per grid
    output_elements:
      - type: isolated_pixels
        properties:
          - same as input pixels
      - type: diagonal_lines
        properties:
          - direction: down-left (increase row, decrease column)
          - origin: each non-white pixel from the input
          - color: matches the origin pixel's color
          - termination: stops at grid boundary (bottom edge or left edge)
    relationship: each non-white pixel in the input generates a diagonal line segment in the output, starting one step down-left from the pixel and continuing until a grid edge is met. The original pixel is preserved.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each cell (row `r`, column `c`) of the input grid.
    3.  If the cell at (`r`, `c`) contains a non-white color `C`:
        a.  Initialize the current position for line drawing to (`r + 1`, `c - 1`).
        b.  While the current position (`current_r`, `current_c`) is within the grid boundaries (i.e., `current_r` is less than the grid height and `current_c` is greater than or equal to 0):
            i.  Set the color of the cell at (`current_r`, `current_c`) in the output grid to `C`.
            ii. Update the current position to (`current_r + 1`, `current_c - 1`).
    4.  Return the modified output grid.
