*   **Perception:**
    *   The input and output are grids of colored pixels.
    *   In all examples, the output grid is smaller than the input grid.
    *   The content of the output grid is identical to a portion of the input grid.
    *   Example 1 (3x6 -> 3x3): The output is the left half of the input. The width is halved.
    *   Example 2 (4x8 -> 4x4): The output is the left half of the input. The width is halved.
    *   Example 3 (6x2 -> 3x2): The output is the top half of the input. The height is halved.
    *   It appears the transformation involves selecting either the left half or the top half of the input grid.
    *   The choice between selecting the left half or the top half seems to depend on the relative dimensions (height and width) of the input grid. When the width is greater than the height (examples 1 and 2), the left half is kept. When the height is greater than the width (example 3), the top half is kept.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_output_relation: subset
    transformation_type: cropping

    observations:
      - input_grid: a 2D array of pixels
      - output_grid: a 2D array of pixels, always a subgrid of the input
      - dimension_comparison:
          - if input_width > input_height:
              action: keep the left half of the input grid
              output_width: input_width / 2
              output_height: input_height
          - if input_height >= input_width:  # Assuming equality follows the height rule based on example 3
              action: keep the top half of the input grid
              output_width: input_width
              output_height: input_height / 2
    properties:
      - The number of rows or columns is halved, depending on which dimension is larger.
      - Integer division seems implied for halving the dimension.
      - Pixel colors and their relative positions within the selected half are preserved.
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Compare the width (W) and height (H).
    3.  If the width (W) is greater than the height (H), the output grid consists of the pixels from the input grid located in columns 0 to (W/2) - 1 (integer division). The output grid has dimensions H x (W/2).
    4.  Otherwise (if the height (H) is greater than or equal to the width (W)), the output grid consists of the pixels from the input grid located in rows 0 to (H/2) - 1 (integer division). The output grid has dimensions (H/2) x W.