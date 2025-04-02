*   **Perception**: The input and output grids are single rows (1D arrays). Each input grid contains a contiguous block of a single non-white color (red or gray) and a single maroon pixel, with the rest being white pixels. The output grid shows the same non-white block and the maroon pixel, but the position of the non-white block has changed. The block appears to have moved horizontally to the right until its rightmost pixel is immediately adjacent to the left side of the maroon pixel. The size and color of the block, the position of the maroon pixel, and the overall grid dimensions remain unchanged.

*   **Facts**:
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D # Represented as 1xN or Nx1
    components:
      - object:
          description: A contiguous horizontal block of a single color (not white=0, not maroon=9).
          examples:
            - color: red (2), size: 3 pixels (train_1)
            - color: gray (5), size: 12 pixels (train_2)
            - color: gray (5), size: 15 pixels (train_3)
          properties:
            - is_contiguous
            - horizontal_orientation
            - color_is_uniform
            - color_is_not_white
            - color_is_not_maroon
      - marker:
          description: A single pixel of maroon color (9).
          properties:
            - size: 1 pixel
            - color: maroon (9)
            - position_is_static_relative_to_grid
      - background:
          description: White pixels (0) filling the rest of the grid.
    action:
      type: translation
      direction: horizontal_right
      target_object: the non-white, non-maroon block
      reference_object: the maroon pixel
      termination_condition: The rightmost pixel of the target object becomes horizontally adjacent (left neighbor) to the marker pixel.
    constraints:
      - Only one non-white, non-maroon block exists.
      - Only one maroon pixel exists.
      - The grid dimensions remain constant.
      - The color and size of the block remain constant.
      - The position of the maroon pixel remains constant.
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous horizontal block of a single color that is neither white (0) nor maroon (9). Let this be the 'moving block'.
    2.  Identify the single maroon (9) pixel. Let this be the 'marker'.
    3.  Determine the starting column index of the marker pixel.
    4.  Determine the width (number of pixels) of the moving block.
    5.  Calculate the target starting column index for the moving block such that its rightmost pixel is at `marker_column_index - 1`. The target starting column index is `marker_column_index - block_width`.
    6.  Create a new grid of the same dimensions as the input, initialized with white (0) pixels.
    7.  Place the maroon (9) marker pixel at its original column index in the new grid.
    8.  Place the moving block (using its original color and width) into the new grid, starting at the calculated target starting column index.