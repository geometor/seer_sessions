*   **Perception:**
    *   The input grids contain a white background (color 0) with a few isolated, non-white pixels.
    *   The output grids retain the original non-white pixels in their positions.
    *   For each original non-white pixel, a horizontal pattern is generated to its right, extending to the edge of the grid.
    *   This pattern alternates between gray (color 5) and the color of the original pixel. The pattern always starts with gray immediately to the right of the original pixel.
    *   The white background pixels remain unchanged unless overwritten by the generated pattern.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        description: A 2D array of pixels with integer values representing colors.
      - object: background_pixel
        property: color
        value: 0 (white)
      - object: colored_pixel
        property: color
        value: Any color except 0 (non-white)
        description: Isolated pixels in the input grid.
      - object: generated_pattern
        property: structure
        value: Horizontal sequence
        property: content
        value: Alternating sequence of gray (5) and the color of the source colored_pixel.
        relationship: Starts immediately to the right of a colored_pixel and extends to the right edge of the grid.
        property: starting_color
        value: gray (5)

    actions:
      - action: locate
        actor: system
        input: input_grid
        output: coordinates and color of each colored_pixel
      - action: generate_pattern
        actor: system
        input:
          - location (row, col) of a colored_pixel
          - color of the colored_pixel
          - grid_width
        process: |
          For each column 'c_new' from 'col + 1' to 'grid_width - 1':
          If ('c_new' - ('col' + 1)) is even, set the pixel at (row, c_new) to gray (5).
          If ('c_new' - ('col' + 1)) is odd, set the pixel at (row, c_new) to the color of the colored_pixel.
        output: Modified row segment containing the pattern.
      - action: construct_output
        actor: system
        input:
          - input_grid
          - all generated_patterns for each colored_pixel
        process: Start with a copy of the input grid. Overlay the generated_patterns onto the corresponding rows.
        output: output_grid
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each row (`r`) and column (`c`) of the input grid.
    3.  If the pixel at (`r`, `c`) is not white (color is not 0):
        a.  Let the color of this pixel be `original_color`.
        b.  Iterate through the columns `c_new` from `c + 1` to the last column index of the grid.
        c.  Determine the color to place at (`r`, `c_new`):
            i.  If the horizontal distance `(c_new - c)` is odd, set the color to gray (5).
            ii. If the horizontal distance `(c_new - c)` is even, set the color to `original_color`.
        d.  Update the pixel at (`r`, `c_new`) in the output grid with the determined color.
    4.  Return the final output grid.