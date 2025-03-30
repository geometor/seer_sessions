*   **Perception of the elements:**
    *   The input and output grids are always the same size (10x10 in the examples).
    *   The grids have a dominant background color, which is azure (8).
    *   Each input grid contains one or more "foreground" pixels of a single color, different from the background.
    *   The transformation involves moving these foreground pixels within the grid. The background remains unchanged except where foreground pixels were moved from.
    *   The direction and distance of the movement depend solely on the *color* of the foreground pixels. All foreground pixels in a given grid move by the same amount in the same direction.

*   **YAML documenting facts:**
    
```yaml
    task: Shift foreground pixels based on their color.
    objects:
      - type: grid
        description: A 2D array of pixels.
      - type: background_pixel
        properties:
          color: azure (8)
          behavior: static
      - type: foreground_pixel
        properties:
          color: varies (orange(7), red(2), maroon(9), blue(1) in examples)
          behavior: moves based on its color
    relationships:
      - All foreground pixels within a single input grid share the same color.
      - The background pixel color fills the space previously occupied by moved foreground pixels.
    actions:
      - name: identify_foreground
        input: input_grid
        output: list of (row, col, color) for foreground pixels
      - name: determine_shift
        input: foreground_color
        output: (delta_row, delta_col) shift vector
        rules:
          - color: orange(7) -> shift: (-2, 0)  # Up 2
          - color: red(2)    -> shift: (0, -2)  # Left 2
          - color: maroon(9) -> shift: (+2, 0)  # Down 2
          - color: blue(1)   -> shift: (0, +1)  # Right 1
      - name: apply_shift
        input: input_grid, foreground_pixels, shift_vector
        output: output_grid
        steps:
          - Create a copy of the input grid for the output.
          - For each foreground pixel (row, col, color):
              - Set output_grid[row][col] to background_color (azure, 8).
              - Calculate new position: new_row = row + delta_row, new_col = col + delta_col.
              - Set output_grid[new_row][new_col] to foreground_color.
    ```


*   **Natural language program:**
    1.  Create the output grid as a copy of the input grid.
    2.  Identify the background color (azure, 8).
    3.  Find all pixels in the input grid that are *not* the background color. Record their positions (row, column) and their color. Assume all these non-background pixels have the same color. Let this color be `foreground_color`.
    4.  Determine the shift amount (change in row `delta_row`, change in column `delta_col`) based on the `foreground_color`:
        *   If `foreground_color` is orange (7), the shift is (-2, 0).
        *   If `foreground_color` is red (2), the shift is (0, -2).
        *   If `foreground_color` is maroon (9), the shift is (+2, 0).
        *   If `foreground_color` is blue (1), the shift is (0, +1).
        *   (Assume other colors, if encountered, follow an unknown but consistent rule or won't appear based on training examples).
    5.  Iterate through the recorded positions (row, col) of the foreground pixels found in step 3.
    6.  For each original position (row, col):
        a.  Set the pixel at (row, col) in the *output grid* to the background color (azure, 8).
        b.  Calculate the new position: `new_row = row + delta_row`, `new_col = col + delta_col`.
        c.  Set the pixel at (`new_row`, `new_col`) in the *output grid* to the `foreground_color`.
    7.  Return the final output grid.