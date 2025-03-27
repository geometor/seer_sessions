*   **Perception:**
    *   Each input grid has a unique, non-white colored pixel at the top-left corner (0,0). Let's call this the "control pixel".
    *   The rest of the grid (excluding row 0 and column 0, which are mostly white except for the control pixel) contains various colored shapes or patterns against a white background.
    *   Comparing inputs and outputs, the primary transformation appears to be a vertical (downward) shift of the grid content, excluding the control pixel.
    *   The amount of the downward shift seems to be determined by the color (value) of the control pixel.
    *   The control pixel itself remains unchanged in the output grid at position (0,0).
    *   When the content is shifted down, the rows at the top (below row 0) that become empty are filled with the background color (white, 0).
    *   Content shifted beyond the bottom boundary of the grid is lost.
    *   Example 1 shows the case where the input and output are identical, suggesting a shift of 0 rows corresponds to the control pixel color (maroon, 9).
    *   Other examples show different shift amounts based on the control pixel's color: Yellow (4) causes a 3-row shift, Magenta (6) causes a 2-row shift, and Orange (7) causes a 5-row shift.

*   **Facts:**
    
```yaml
    task_elements:
      - element: grid
        description: A 2D array of pixels with colors 0-9.
      - element: control_pixel
        description: The pixel located at position (0, 0) in the input grid. Its value determines the transformation.
        properties:
          - location: (0, 0)
          - value: N (a color value from 0-9)
      - element: grid_content
        description: All pixels in the input grid excluding the control_pixel at (0,0).
        properties:
          - shapes: Various colored patterns and blocks.
          - background: Primarily white (0).

    transformation:
      - action: read_control_pixel
        input: control_pixel
        output: value N
      - action: determine_shift_amount
        input: value N
        output: shift_amount S
        logic: Based on a specific mapping derived from examples - {4: 3, 6: 2, 7: 5, 9: 0}. If N is not in this set, the behavior is undefined by the examples, but 0 shift might be a default (as seen for N=9).
      - action: shift_grid_content
        input: grid_content
        parameter: shift_amount S
        output: shifted_grid_content
        logic: >
          Each pixel at input coordinates (r, c) where r > 0 is moved to output coordinates (r + S, c),
          provided r + S is less than the grid height. Pixels shifted beyond the grid boundary are discarded.
      - action: construct_output_grid
        input:
          - control_pixel (original)
          - shifted_grid_content
        output: final_output_grid
        logic: >
          Create a new grid of the same dimensions as the input, initialized with white (0).
          Place the original control_pixel at (0, 0).
          Place the shifted_grid_content into the appropriate rows (from row S+1 downwards).
          Rows 1 to S will remain white.

    relationships:
      - The value N of the control_pixel dictates the vertical shift amount S applied to the rest of the grid content (rows 1 onwards). The mapping observed is {Yellow(4): 3, Magenta(6): 2, Orange(7): 5, Maroon(9): 0}.
    ```


*   **Natural Language Program:**
    1.  Identify the control pixel at position (0, 0) in the input grid and read its value, `N`.
    2.  Determine the downward shift amount, `S`, based on the value `N` using the following mapping: if `N` is 4, `S` is 3; if `N` is 6, `S` is 2; if `N` is 7, `S` is 5; if `N` is 9, `S` is 0. (Assume `S` is 0 for any other value of `N` not seen in examples, or handle as an error).
    3.  Create a new output grid with the same dimensions as the input grid, and fill it entirely with the background color (white, 0).
    4.  Copy the value `N` from the input grid's control pixel (0, 0) to the output grid's position (0, 0).
    5.  Iterate through the input grid's rows `r` from 1 to `height - 1` and columns `c` from 0 to `width - 1`.
    6.  For each pixel at `(r, c)`, calculate the target row `target_r = r + S`.
    7.  If `target_r` is less than the grid height, copy the pixel value from input `(r, c)` to the output grid at `(target_r, c)`.
    8.  Return the newly constructed output grid.