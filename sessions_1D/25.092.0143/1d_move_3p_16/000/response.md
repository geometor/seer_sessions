*   **Perception:**
    *   The input and output are single-row grids (1D arrays) of pixels.
    *   Each input contains exactly one contiguous block of non-white pixels, surrounded by white (0) pixels.
    *   The non-white blocks have different colors (red, gray) and lengths across the examples.
    *   In the output, the non-white block has been shifted horizontally to the right.
    *   The amount of shift appears consistent across all examples. In train\_1, the red block (2 2 2) starts at index 11 and moves to start at index 14 (shift of 3). In train\_2, the gray block starts at index 4 and moves to start at index 7 (shift of 3). In train\_3, the gray block starts at index 1 and moves to start at index 4 (shift of 3).
    *   The size of the grid remains the same.
    *   The color and length of the non-white block remain unchanged.
    *   The positions previously occupied by the block become white (0) in the output, and the block overwrites the white pixels at its new location.

*   **YAML Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Effectively 1 row
    background_color: 0 # white
    objects:
      - type: contiguous_block
        properties:
          color: non-zero (variable: 2/red, 5/gray)
          shape: horizontal_line
          length: variable (3, 12, 15)
          count_per_example: 1
    actions:
      - type: translation
        direction: horizontal_right
        magnitude: 3 positions
        target: the_non-white_object
    relationships:
      - object_moves_relative_to_grid
      - vacated_space_becomes_background
      - grid_size_constant
      - object_properties_constant (color, length)
    ```


*   **Natural Language Program:**
    1.  Identify the input grid (a single row).
    2.  Locate the contiguous sequence (block) of non-white pixels. Determine its color, starting index, and length.
    3.  Create a new output grid of the same size as the input grid, initially filled with the background color (white, 0).
    4.  Calculate the new starting index for the block by adding 3 to its original starting index.
    5.  Place the identified block (using its original color and length) into the output grid, starting at the calculated new index.