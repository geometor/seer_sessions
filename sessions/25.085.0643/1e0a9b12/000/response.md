*   **Perception of Task Elements:**
    *   The input and output are grids of the same dimensions.
    *   The grids contain pixels of different colors, including white (0) which acts as background/empty space.
    *   Non-white pixels in the input grid appear to move downwards in the output grid.
    *   The horizontal position (column) of each non-white pixel is preserved.
    *   The downward movement stops when a pixel reaches the bottom edge of the grid or lands on top of another non-white pixel within the same column.
    *   Essentially, gravity acts independently on each column, causing the non-white pixels to stack up at the bottom.

*   **Facts:**
    
```yaml
    task_type: gravity_compaction
    element_type: pixels
    properties:
      - color: integer value 0-9
      - position: (row, column)
    objects:
      - type: non-white_pixel
        description: Pixels with color values 1 through 9. These are subject to movement.
      - type: white_pixel
        description: Pixels with color value 0. These represent empty space.
    relationships:
      - type: vertical_adjacency
        description: Pixels directly above or below each other in the same column.
      - type: grid_boundary
        description: The bottom edge of the grid acts as a boundary.
    actions:
      - name: fall
        actor: non-white_pixel
        effect: Changes the row position downwards.
        constraint: Movement is restricted to the pixel's original column.
      - name: stop
        trigger: non-white_pixel reaches the bottom row or lands on another non-white_pixel in the same column.
      - name: stack
        effect: Non-white pixels within a column form a contiguous vertical block at the bottom of that column in the output.
    grid_properties:
      - dimensions: height and width remain constant between input and output.
      - background: white (0) pixels fill the space not occupied by fallen non-white pixels.
    ```


*   **Natural Language Program:**
    1.  Create a new grid (output grid) with the same dimensions as the input grid, initially filled entirely with the white color (0).
    2.  Iterate through each column of the input grid, from left to right.
    3.  For the current column, identify all non-white pixels and record their colors in the order they appear from top to bottom.
    4.  Take the recorded list of non-white pixel colors for the current column.
    5.  Place these colors back into the corresponding column of the output grid, starting from the bottom row and moving upwards, filling the cells consecutively without leaving any white gaps between them.
    6.  After processing all columns, the output grid represents the final state.