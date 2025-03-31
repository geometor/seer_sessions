*   **Perception:**
    *   The input grid contains a white background, two distinct vertical red lines (color 2) usually near the left and right edges, and several azure pixels (color 8) scattered between the red lines.
    *   The output grid retains the original red lines. New horizontal lines appear, primarily composed of azure (8) pixels, with some yellow (4) pixels.
    *   The azure pixels in the input act as markers or triggers. They are located on rows that are part of one of the red vertical line segments.
    *   Each input azure pixel seems to generate two horizontal lines in the output:
        1.  A line on the *same row* as the input azure pixel. This line starts from the red line on the same side as the azure pixel and extends towards the column of the azure pixel. The pixel at the azure pixel's original coordinates becomes yellow (4), and the pixels between the red line and the yellow pixel become azure (8).
        2.  A line on the *corresponding row* of the *opposite* red line segment. This line starts from the opposite red line and extends fully across the gap towards the first red line, filling the space between the two red lines (exclusive) with azure (8) pixels.
    *   The "corresponding row" is determined by the relative position within the red line segment. For example, if an azure pixel is on the 2nd row of the left red segment, the corresponding row on the right segment is the 2nd row of that segment.

*   **YAML Facts:**
    
```yaml
    elements:
      - object: background
        color: white (0)
        role: static_canvas
      - object: red_line_segment
        color: red (2)
        shape: vertical_line
        count: 2 (one left, one right)
        properties:
          - spans_multiple_rows
          - define_boundaries_for_line_drawing
        role: boundary/anchor
      - object: azure_marker
        color: azure (8)
        shape: pixel
        count: variable (>=1)
        location: within_rows_spanned_by_a_red_line_segment
        role: trigger
      - object: generated_same_side_line
        color: azure (8)
        shape: horizontal_line_segment
        role: output_element
        relationship:
          - starts_adjacent_to_source_red_line
          - extends_towards_trigger_column
          - exists_on_same_row_as_trigger
      - object: generated_yellow_endpoint
        color: yellow (4)
        shape: pixel
        role: output_element
        location: at_the_original_coordinates_of_an_azure_marker
        relationship: terminates_generated_same_side_line
      - object: generated_opposite_side_line
        color: azure (8)
        shape: horizontal_line_segment
        role: output_element
        relationship:
          - starts_adjacent_to_target_red_line
          - extends_towards_source_red_line
          - fills_space_between_red_lines
          - exists_on_row_corresponding_to_trigger_row_in_target_segment

    actions:
      - identify: locate the two vertical red line segments and their row ranges.
      - identify: locate all azure marker pixels.
      - for_each: azure marker pixel at (r, c):
          - determine: which red segment (source) row 'r' belongs to, and identify the other segment (target).
          - generate_same_side:
              - draw: horizontal line in row 'r' starting adjacent to the source red line.
              - fill: with azure (8) pixels up to, but not including, column 'c'.
              - place: yellow (4) pixel at (r, c).
          - generate_opposite_side:
              - calculate: the corresponding row 'r_target' in the target segment's row range.
              - draw: horizontal line in row 'r_target' starting adjacent to the target red line.
              - fill: with azure (8) pixels across the entire width between the two red lines (exclusive of the columns containing the red lines).
      - copy: retain the original red lines in the output.
      - maintain: keep the background white where no lines are drawn.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, but remove all azure (8) pixels from the copy, reverting them to white (0).
    2.  Identify the two vertical red (2) line segments. Record their column indices (`col_left`, `col_right`) and their starting and ending row indices (`row_start_left`, `row_end_left`, `row_start_right`, `row_end_right`).
    3.  Find all azure (8) pixels in the *original input* grid.
    4.  For each found azure pixel at input coordinates (`r`, `c`):
        a.  **Determine Source/Target:** Check if row `r` falls within the range [`row_start_left`, `row_end_left`].
            *   If yes, the left segment is the 'source' and the right is the 'target'. Set `source_col = col_left`, `target_col = col_right`, `source_row_start = row_start_left`, `target_row_start = row_start_right`.
            *   If no (meaning `r` is in the right segment's range), the right segment is the 'source' and the left is the 'target'. Set `source_col = col_right`, `target_col = col_left`, `source_row_start = row_start_right`, `target_row_start = row_start_left`.
        b.  **Generate Same-Side Line:**
            *   Place a yellow (4) pixel in the output grid at (`r`, `c`).
            *   Determine the range of columns to fill with azure (8):
                *   If source is left (`source_col = col_left`), fill columns from `col_left + 1` to `c - 1` in row `r` with azure (8).
                *   If source is right (`source_col = col_right`), fill columns from `c + 1` to `col_right - 1` in row `r` with azure (8).
        c.  **Generate Opposite-Side Line:**
            *   Calculate the relative row index within the source segment: `relative_row = r - source_row_start`.
            *   Calculate the corresponding row index in the target segment: `r_target = target_row_start + relative_row`.
            *   Determine the range of columns to fill with azure (8) in row `r_target`: Fill columns from `min(col_left, col_right) + 1` to `max(col_left, col_right) - 1` with azure (8).
    5.  The final output grid contains the original red lines and the newly generated yellow and azure pixels.