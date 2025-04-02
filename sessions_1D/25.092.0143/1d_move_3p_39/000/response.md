*   **Perception:**
    *   The task operates on 1-dimensional grids (or 1xN grids).
    *   Each input grid contains a single contiguous block of a non-white color (magenta or red in the examples) against a white background (color 0).
    *   The output grid has the same dimensions as the input grid.
    *   The non-white block in the output is identical in color and length to the block in the input.
    *   The key transformation is the horizontal shifting of this non-white block. In all provided examples, the block shifts exactly 3 positions to the right.
    *   The grid cells not occupied by the shifted block are filled with the background color (white, 0).

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # or 1xN 2D
    background_color: 0 # white
    objects:
      - type: contiguous_block
        color: non-zero # variable (magenta, red)
        properties:
          - length: variable (7, 3, 6)
          - start_index: variable (1, 0, 0)
    action:
      - type: shift
        direction: right
        magnitude: 3 positions
        target: the non-zero contiguous_block
    output_grid:
      - dimensions: same as input
      - content: background_color filled grid with the shifted object placed at its new location
    relationships:
      - object_position_output = object_position_input + 3
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input grid. Note its color, length, and starting position (index).
    2.  Determine the dimensions of the input grid.
    3.  Create a new output grid of the same dimensions, initially filled entirely with the background color (white, 0).
    4.  Calculate the new starting position for the block by adding 3 to its original starting position.
    5.  Place the identified block (with its original color and length) into the output grid, starting at the calculated new position.