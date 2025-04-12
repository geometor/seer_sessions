
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 3 3 3 3 3 3 3 0 0
6 0 3 3 0 0 0 0 3 0 0 6
0 0 3 0 0 6 0 0 3 0 0 0
0 0 3 3 0 6 0 6 3 0 6 0
0 0 0 3 0 0 0 0 3 0 0 0
6 0 0 3 0 0 6 0 0 3 0 0
0 0 3 3 0 0 0 0 0 3 0 0
0 0 0 3 3 3 0 0 0 3 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 6
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 4 4 0 0
0 0 4 4 0 0 1 0 0 0 4 0 4 0 0
0 0 4 0 4 0 0 0 0 0 0 0 4 0 0
0 4 0 0 4 0 0 0 0 4 0 0 0 4 0
4 0 1 0 4 4 0 0 0 4 0 0 0 4 0
4 4 0 0 0 4 4 4 4 0 0 0 4 4 0
0 4 4 0 0 0 0 0 0 0 0 0 4 0 0
0 0 4 4 0 1 0 0 0 0 0 4 4 0 0
0 0 0 4 4 0 0 1 0 0 0 4 0 0 0
0 0 0 0 4 0 0 0 0 0 4 4 0 0 0
0 0 0 0 4 0 0 0 0 4 0 0 0 1 0
0 1 0 0 0 0 4 4 4 4 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain a background color (white), pixels of one primary color (magenta in train_1, blue in train_2), and pixels/structures of a secondary color (green in train_1, yellow in train_2).
    *   The output grids are the same size as the input grids and retain the background color.
    *   The transformation involves filtering the primary color pixels based on their proximity to the secondary color pixels.
    *   Specifically, only the primary color pixels that are *not* adjacent (horizontally, vertically, or diagonally) to any secondary color pixel are kept in the output grid.
    *   All pixels of the secondary color are removed (turned into the background color) in the output.
    *   The positions of the preserved primary color pixels remain unchanged relative to the grid boundaries.

*   **Facts:**
    
```yaml
    task_type: filtering
    elements:
      - role: background
        color: white (0)
        persistence: maintained
      - role: target_pixels
        color: variable (magenta(6) in train_1, blue(1) in train_2)
        property: isolated_from_context
        action: kept if isolated, removed otherwise
      - role: context_pixels
        color: variable (green(3) in train_1, yellow(4) in train_2)
        property: defines_exclusion_zone
        action: removed
    relationships:
      - type: adjacency
        definition: 8-connectivity (horizontal, vertical, diagonal)
        between: target_pixels, context_pixels
        relevance: determines if a target_pixel is kept or removed
    grid_properties:
      - size: maintained between input and output
    ```


*   **Natural Language Program:**
    1.  Create a new grid with the same dimensions as the input grid, initialized with the background color (white).
    2.  Identify the 'target' color (the scattered, less numerous non-background color, e.g., magenta in train_1, blue in train_2).
    3.  Identify the 'context' color (the other non-background color, often forming larger structures, e.g., green in train_1, yellow in train_2).
    4.  Iterate through each pixel in the input grid at position (row, column).
    5.  If the current pixel's color is the 'target' color:
        a.  Examine all 8 neighboring pixels (including diagonals) of the current pixel in the input grid.
        b.  Check if *any* of these neighbors have the 'context' color.
        c.  If *none* of the neighbors have the 'context' color, set the pixel at (row, column) in the new grid to the 'target' color.
    6.  Output the new grid. (Pixels not explicitly set remain the background color).
