*   **Perception:**
    *   The input and output are always 1-dimensional grids (or 1xN grids) of the same size.
    *   Each input grid contains exactly one contiguous block of non-white pixels (e.g., red, gray, azure) surrounded by white pixels (color 0).
    *   The output grid contains the same contiguous block of non-white pixels as the input.
    *   The block of non-white pixels is shifted horizontally to the right in the output grid compared to its position in the input grid.
    *   The amount of the shift appears to be constant across all examples. In each case, the block shifts 3 positions to the right.
    *   The pixels in the positions vacated by the shift and the positions shifted into become white (color 0).

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D (or 1xN)
    grid_size_relation: input_height == output_height and input_width == output_width
    objects:
      - type: contiguous_block
        color: non-white (variable, e.g., red, gray, azure)
        count_in_input: 1
        count_in_output: 1
        properties:
          - location (start and end index)
          - color
          - length
    background_color: white (0)
    transformation:
      - action: horizontal_shift
        target: non-white_block
        direction: right
        magnitude: 3 positions
    invariance:
      - grid_size
      - color_of_the_block
      - length_of_the_block
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous block of non-white pixels in the input grid. Note its color, starting position (index), and length.
    2.  Create a new grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
    3.  Calculate the new starting position for the block by adding 3 to its original starting position.
    4.  Place the identified block of non-white pixels into the new grid, starting at the calculated new position.