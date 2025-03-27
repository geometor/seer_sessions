*   **Perception**
    *   The output grid is always larger than the input grid.
    *   Comparing the dimensions, the output grid's height and width are exactly double the input grid's height and width.
    *   Observing the pixel colors, each pixel in the input grid appears to be expanded into a 2x2 block of the same color in the corresponding position in the output grid.
    *   For an input pixel at row `r` and column `c` with color `X`, the output grid has a 2x2 block of color `X` covering rows `2*r` and `2*r + 1`, and columns `2*c` and `2*c + 1`.
    *   The transformation essentially zooms in or scales up the input grid by a factor of 2.

*   **Facts**
    
```yaml
    task_description: Scale the input grid by a factor of 2x.
    grid_relationship:
      - type: scaling
        input: input_grid
        output: output_grid
        scale_factor_height: 2
        scale_factor_width: 2
    pixel_transformation:
      - scope: each pixel in the input grid
        action: replace
        details: |
          Replace the input pixel at position (row `r`, column `c`)
          with a 2x2 block of the same color in the output grid.
          The top-left corner of this 2x2 block in the output grid
          is at position (row `r*2`, column `c*2`).
    objects:
      - id: input_grid
        properties:
          - height: H
          - width: W
      - id: output_grid
        properties:
          - height: H * 2
          - width: W * 2
      - id: pixel
        properties:
          - position: (row, column)
          - color: C
    ```


*   **Natural Language Program**
    1.  Determine the height (`H`) and width (`W`) of the input grid.
    2.  Create a new output grid with height `H * 2` and width `W * 2`.
    3.  Iterate through each pixel in the input grid at position (row `r`, column `c`), where `r` ranges from 0 to `H-1` and `c` ranges from 0 to `W-1`.
    4.  Get the color (`C`) of the input pixel at `(r, c)`.
    5.  In the output grid, fill the 2x2 block defined by the top-left corner `(r * 2, c * 2)` and the bottom-right corner `(r * 2 + 1, c * 2 + 1)` with the color `C`.
    6.  Return the completed output grid.