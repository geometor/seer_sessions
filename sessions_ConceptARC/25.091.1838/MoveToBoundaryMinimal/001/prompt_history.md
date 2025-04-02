
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 3 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 3 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
```


## train_2

**input:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves moving a single, uniquely colored pixel towards a line of a different color. The background is white (0). The line acts as a barrier, and the single pixel stops one cell away from it. The movement is either purely horizontal or purely vertical.

*   **YAML Facts:**
    
```yaml
    task_description: Move a single pixel towards a line barrier until adjacent.
    
    elements:
      - type: grid
        description: Input and output are 2D grids of pixels with integer values 0-9 representing colors.
      - type: background_pixel
        value: 0
        color: white
        description: The most common pixel color, filling empty space.
      - type: mover_pixel
        description: A single pixel of a unique color (not background, not barrier color).
        properties:
          - color: Varies (green in example 1, magenta in example 2).
          - count: Always 1 in the input grid.
          - role: Moves towards the barrier.
      - type: barrier_line
        description: A contiguous line (horizontal or vertical) of pixels of the same color (not background, not mover color).
        properties:
          - color: Varies (yellow in example 1, green in example 2).
          - count: Greater than 1.
          - shape: Straight line (horizontal or vertical).
          - role: Acts as a destination/boundary for the mover pixel.
    
    relationships:
      - type: adjacency
        description: The mover pixel stops in the cell directly adjacent (sharing an edge, not diagonal) to the barrier line, one step away.
      - type: movement
        description: The mover pixel translates across the grid towards the barrier line.
        properties:
          - direction: Orthogonal (horizontal or vertical) along the shortest path to the barrier.
          - distance: Determined by the initial position and the position adjacent to the barrier.
    
    actions:
      - action: identify_elements
        description: Distinguish the background, the single mover pixel, and the barrier line based on color and count/shape.
      - action: determine_target_position
        description: Calculate the final position for the mover pixel.
          - If the barrier is vertical at column `c_b`, the target column is `c_b - 1` (if mover is left) or `c_b + 1` (if mover is right). The row remains the same.
          - If the barrier is horizontal at row `r_b`, the target row is `r_b - 1` (if mover is above) or `r_b + 1` (if mover is below). The column remains the same.
      - action: update_grid
        description: Create the output grid by setting the mover pixel's original location to the background color and its calculated target position to the mover pixel's color. All other pixels remain unchanged.
    
    constraints:
      - Assumes exactly one 'mover' pixel (count=1, non-background, non-barrier color).
      - Assumes exactly one 'barrier' line (contiguous line, non-background, non-mover color).
      - Assumes the mover pixel is not already adjacent to the barrier.
      - Assumes the background color is white (0).
    ```


*   **Natural Language Program:**
    1.  Identify the background color (white, 0).
    2.  Identify all non-background pixels.
    3.  Find the pixel color that appears exactly once; this is the 'mover' pixel. Record its color and initial coordinates (row_start, col_start).
    4.  Identify the remaining non-background pixels; these form the 'barrier' line. Determine if the barrier is horizontal (all pixels have the same row) or vertical (all pixels have the same column). Record the barrier's row or column coordinate.
    5.  Determine the target coordinates (row_end, col_end) for the 'mover' pixel:
        *   If the barrier is vertical at column `col_barrier`:
            *   The target row is `row_start`.
            *   The target column is `col_barrier - 1` if `col_start < col_barrier`, otherwise `col_barrier + 1`.
        *   If the barrier is horizontal at row `row_barrier`:
            *   The target column is `col_start`.
            *   The target row is `row_barrier - 1` if `row_start > row_barrier`, otherwise `row_barrier + 1`.
    6.  Create the output grid as a copy of the input grid.
    7.  Set the pixel at the 'mover' pixel's initial coordinates (row_start, col_start) in the output grid to the background color (white, 0).
    8.  Set the pixel at the calculated target coordinates (row_end, col_end) in the output grid to the 'mover' pixel's color.
