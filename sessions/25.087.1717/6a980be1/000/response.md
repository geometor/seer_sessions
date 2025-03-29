*   **Perception:**
    *   All examples feature an input grid with a single-color border (Azure-8, Yellow-4, Magenta-6) surrounding a primarily white (0) content area.
    *   The content area contains a central pattern composed mainly of Green (3) and Red (2) pixels.
    *   The output grid typically has the same dimensions as the input grid (Example 1's output dimension seems anomalous in the prompt, assuming it should be 18x19 like its input based on other examples).
    *   The output grid removes the original border.
    *   The core Green/Red pattern from the input's content area is preserved in the output.
    *   The key transformation involves changing the background pixels (originally white or the border color) based on the content of each row within the pattern's extent, and handling rows outside the pattern's extent distinctly.
    *   Specifically, for rows within the pattern's vertical span: if the row contains Red (2) pixels in the input, the background in the output row becomes the original border color; otherwise, the background becomes white (0).
    *   For rows outside the pattern's vertical span (relevant in Example 2 where the pattern doesn't fill the height), the output rows are filled with a repeating horizontal pattern using white (0) and the original border color.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_properties:
        - input_output_size_match: true # Assuming example 1 output size was a typo
        - input_has_border: true
        - border_width: 1
        - output_has_border: false
        - background_color: 0 # white
      key_colors:
        - border_color: # Varies per example (8, 4, 6) - identifies the input border
            role: determines_fill_color_1
        - pattern_color_1: 3 # green - structural element
            role: part_of_preserved_pattern
        - pattern_color_2: 2 # red - conditional trigger
            role: determines_row_background_fill
        - background_fill_color_1: # Same as border_color
            role: fills_background_on_red_presence
        - background_fill_color_2: 0 # white
            role: fills_background_on_red_absence_or_outside_pattern

    transformation:
      - action: identify_border_color
        input: input_grid[0, 0]
        output: border_color
      - action: identify_pattern_vertical_span
        input: input_grid content area (excluding border)
        criteria: rows containing any non-white pixels
        output: min_pattern_row, max_pattern_row
      - action: initialize_output_grid
        size: same as input grid
        initial_value: # determined by row position relative to pattern span
      - action: preserve_pattern
        input: input_grid content area
        output: output_grid
        filter: copy non-white pixels to the same coordinates
      - action: fill_row_backgrounds_within_span
        target: rows from min_pattern_row to max_pattern_row
        condition: check presence of red (2) in the corresponding input row (content area)
        logic:
          - if red present: fill white/border pixels in output row with border_color
          - if red absent: fill white/border pixels in output row with white (0)
      - action: fill_row_backgrounds_outside_span # Only if min_pattern_row > 0 or max_pattern_row < height - 1
        target: rows 0 to min_pattern_row - 1 AND rows max_pattern_row + 1 to height - 1
        logic: fill row with repeating horizontal pattern [white, border_color, border_color]
      - action: handle_original_border_rows_if_pattern_is_full_height # if min_pattern_row = 1 and max_pattern_row = height - 2
        target: rows 0 and height - 1
        logic: fill row with white (0)

    relationships:
      - border_color (input) determines fill_color_1 (output)
      - presence of red (2) in input row triggers use of fill_color_1 for that row's background
      - absence of red (2) in input row triggers use of fill_color_2 (white) for that row's background
      - vertical span of the non-white pattern determines which rows use conditional fill vs pattern fill
    ```


*   **Natural Language Program:**
    1.  Identify the border color by looking at a corner pixel (e.g., top-left) of the input grid.
    2.  Create a new grid (output) of the same dimensions as the input grid.
    3.  Find the minimum and maximum row indices (`min_r`, `max_r`) that contain any non-background (non-white) pixels within the input grid's content area (i.e., excluding the 1-pixel border).
    4.  Iterate through each row index `r` from 0 to the height of the grid minus 1.
    5.  **Case 1: Row `r` is within the pattern's vertical span (`min_r <= r <= max_r`).**
        *   Check if the input grid's row `r` contains any red (2) pixels within the content columns (between column 1 and width-2).
        *   If red (2) is present: Set the background fill color for this output row to be the identified border color.
        *   If red (2) is absent: Set the background fill color for this output row to be white (0).
        *   Iterate through each column index `c` from 0 to the width of the grid minus 1.
        *   If the pixel `input[r, c]` is part of the original non-white pattern (i.e., not white and not the border color, typically green or red), copy `input[r, c]` to `output[r, c]`.
        *   Otherwise (if `input[r, c]` was white or the border color), set `output[r, c]` to the background fill color determined for this row.
    6.  **Case 2: Row `r` is outside the pattern's vertical span (`r < min_r` or `r > max_r`).**
        *   Determine if this case applies because the pattern is "short" (like Example 2) or because we are processing the original top/bottom border rows of a "tall" pattern (like Examples 1 and 3). This can be checked by seeing if `min_r > 1` or `max_r < height - 2`.
        *   If the pattern is "short": Fill the output row `r` by repeating the horizontal pattern `[white, border_color, border_color]` across the columns.
        *   If the pattern is "tall" (meaning `min_r = 1` and `max_r = height - 2`, and we are currently processing row 0 or row height-1): Fill the output row `r` entirely with white (0).
    7.  Return the completed output grid.