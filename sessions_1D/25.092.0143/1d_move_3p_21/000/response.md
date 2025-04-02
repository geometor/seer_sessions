*   **Perception:** The task involves manipulating 1D grids (or rows). Each input grid contains a single contiguous block of a non-white color surrounded by white pixels (color 0). The output grid is the same size as the input, but the colored block has been shifted horizontally to the right by a fixed amount. The specific color of the block changes between examples (orange, gray, magenta), but the transformation logic remains the same. The background remains white.

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D # or 1xN 2D
    background_color: 0 # white
    objects:
      - object_type: contiguous_block
        properties:
          color: non_white # varies per example (7, 5, 6)
          shape: horizontal_line
          location: defined by start and end indices
    actions:
      - action_type: horizontal_shift
        target_object: contiguous_block
        direction: right
        amount: 3 positions
        constraints:
          - preserves_color
          - preserves_length
          - background_pixels_become_white
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input grid. Determine its color, start index, and end index.
    2.  Calculate the new start index by adding 3 to the original start index.
    3.  Calculate the new end index by adding 3 to the original end index.
    4.  Create a new output grid of the same size as the input grid, initially filled entirely with the background color (white, 0).
    5.  Copy the identified non-white block (preserving its color and length) into the output grid, starting at the calculated new start index and ending at the calculated new end index.