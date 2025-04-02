
## train_1

**input:**
```
0 6 0 0 0 6
0 6 0 0 8 6
0 6 0 0 0 6
0 6 0 0 0 6
0 6 0 0 0 6
0 6 0 0 0 6
```


**output:**
```
0 6 0 0 0 6
0 6 0 8 0 6
0 6 0 0 0 6
0 6 0 0 0 6
0 6 0 0 0 6
0 6 0 0 0 6
```


## train_2

**input:**
```
0 0 0 0 0 0
3 3 3 3 3 3
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 7 0
3 3 3 3 3 3
```


**output:**
```
0 0 0 0 0 0
3 3 3 3 3 3
0 0 0 0 0 0
0 0 0 0 7 0
0 0 0 0 0 0
3 3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 6 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
```


**output:**
```
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 6 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
0 4 0 0 0 0 0 4
```

*   **Perception:**
    *   The input grid always contains a white background (color 0).
    *   There are always two parallel lines (either horizontal or vertical) of a single color that span the full width or height of the grid, respectively. These lines are identical in both the input and output grids.
    *   There is exactly one pixel of a unique color (different from the background and the lines) located somewhere strictly *between* the two parallel lines in the input grid.
    *   In the output grid, this unique pixel has moved from its original position. The background and the parallel lines remain unchanged.
    *   The movement of the unique pixel is always along the axis perpendicular to the parallel lines (i.e., horizontal movement for vertical lines, vertical movement for horizontal lines).
    *   The destination position of the unique pixel is the central row (if lines are horizontal) or central column (if lines are vertical) within the space *strictly between* the two parallel lines. The pixel's coordinate along the axis parallel to the lines remains unchanged.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: background
        color: white (0)
        shape: occupies most of the grid
        state: static
      - element: parallel_lines
        count: 2
        properties:
          - same_color (not white)
          - orientation: either horizontal or vertical
          - span: full width or height of the grid
          - parallel: constant distance apart
        state: static
      - element: moving_pixel
        count: 1
        properties:
          - unique_color (not white, not line color)
          - location: strictly between the parallel_lines in the input
        state: dynamic (changes position)
    transformation:
      action: move
      target: moving_pixel
      rule:
        - Identify the orientation (horizontal/vertical) of the parallel_lines.
        - Determine the axis of movement (perpendicular to the lines).
        - Define the region (rows or columns) strictly between the parallel_lines.
        - Calculate the central row/column index within this region.
        - The moving_pixel's new position retains its original coordinate along the axis *parallel* to the lines.
        - The moving_pixel's new position adopts the calculated central index along the axis *perpendicular* to the lines.
      static_elements:
        - background
        - parallel_lines
    ```


*   **Natural Language Program:**
    1.  Identify the background color (white, 0).
    2.  Find the two parallel lines by locating rows or columns completely filled with the same non-background color. Note their color, orientation (horizontal/vertical), and indices (row or column numbers).
    3.  Locate the single pixel whose color is different from both the background and the parallel lines. Note its initial coordinates (row, column) and color.
    4.  Determine the axis of movement, which is perpendicular to the orientation of the parallel lines.
        *   If lines are horizontal (spanning width), movement is vertical.
        *   If lines are vertical (spanning height), movement is horizontal.
    5.  Find the indices of the two parallel lines, let them be `idx1` and `idx2`. Assume `idx1 < idx2`.
    6.  Calculate the central index (`center_idx`) for the space *strictly between* the lines: `center_idx = idx1 + 1 + floor(((idx2 - idx1 - 1) - 1) / 2)`.
    7.  Create the output grid as a copy of the input grid.
    8.  Clear the original position of the moving pixel in the output grid (set it to the background color, 0).
    9.  Set the color of the pixel at the new position in the output grid to the color of the moving pixel.
        *   If movement is vertical (horizontal lines), the new position is (`center_idx`, original_column).
        *   If movement is horizontal (vertical lines), the new position is (original_row, `center_idx`).
