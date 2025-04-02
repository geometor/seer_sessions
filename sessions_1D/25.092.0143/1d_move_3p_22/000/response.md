*   **Perception**:
    *   The task operates on single-row grids (1x14).
    *   Each input grid contains a single contiguous block of a non-white color (green or orange) surrounded by white pixels.
    *   The output grid shows the same non-white block shifted three positions to the right compared to its position in the input grid.
    *   The space originally occupied by the block becomes white in the output.
    *   The size and color of the non-white block remain unchanged.

*   **Facts**:
    
```yaml
    task_type: object_motion
    grid_properties:
      - shape: horizontal_strip (1 row)
      - width: 14
      - height: 1
      - background_color: white (0)
    objects:
      - type: contiguous_horizontal_block
      - count: 1 per grid
      - color: non-white (varies: green (3), orange (7))
      - properties:
          - length: varies (4, 8, 5 pixels)
          - position: varies
    actions:
      - type: shift / translation
      - target: the non-white block
      - direction: horizontal (right)
      - magnitude: 3 pixels
    relationships:
      - the block moves relative to the grid boundaries
      - the original position of the block becomes the background color (white)
    invariants:
      - grid dimensions
      - block color
      - block size (length)
    ```


*   **Natural Language Program**:
    1.  Locate the contiguous horizontal segment (block) of non-white pixels within the input row. Record its color, starting index, and length.
    2.  Calculate the new starting index by adding 3 to the original starting index.
    3.  Create a new row of the same length as the input, filled entirely with white (0) pixels.
    4.  Copy the identified non-white block (using its original color and length) into the new row, starting at the calculated new starting index.
    5.  The resulting row is the output.