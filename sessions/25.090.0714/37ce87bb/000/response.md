*   **Perception:** The input grids contain a background of orange (7) pixels and one or more vertical lines composed of azure (8) or red (2) pixels. The output grids are identical to the input grids, except for the addition of a new vertical gray (5) line. The position and vertical extent of this gray line depend on the properties of the rightmost vertical line object in the input and the total number of vertical line objects.

*   **Facts YAML:**
    
```yaml
    background_color: 7 # orange
    input_object_colors: [2, 8] # red, azure
    output_object_color: 5 # gray
    objects:
      - type: vertical_line
        properties:
          - color: 2 # red
          - color: 8 # azure
          - column_index
          - start_row
          - end_row
    actions:
      - identify_vertical_lines: Find all contiguous vertical segments of non-background colors.
      - find_rightmost_line: Determine the vertical line with the highest column index.
      - count_lines: Count the total number of identified vertical lines.
      - calculate_new_column: New column index = column index of rightmost line + 2.
      - determine_new_line_extent:
          condition: Color of the rightmost line.
          condition_value_1: Red (2)
          result_1: Start row = End row = End row of the rightmost line.
          condition_value_2: Azure (8)
          sub_condition: Total number of vertical lines.
          sub_condition_value_1: 2
          sub_result_1: Start row = max(0, Start row of the rightmost line - 2), End row = End row of the rightmost line.
          sub_condition_value_2: 3
          sub_result_2: Start row = max(0, Start row of the rightmost line - 1), End row = End row of the rightmost line.
      - draw_line: Add a vertical line of gray (5) pixels at the calculated column and row extent onto a copy of the input grid.
    relationships:
      - The position (column) of the new gray line is relative to the rightmost input vertical line (+2 columns).
      - The vertical extent (start/end rows) of the new gray line depends on the color and start/end rows of the rightmost input vertical line, and sometimes the total count of vertical lines.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct vertical line objects in the input grid. A vertical line object consists of contiguous pixels of the same non-orange color (red or azure) all located in the same column.
    2.  If no vertical line objects are found, return the input grid unchanged.
    3.  Determine the vertical line object with the largest column index (the "rightmost line"). Note its color (`color_R`), column index (`col_R`), topmost row index (`start_R`), and bottommost row index (`end_R`).
    4.  Count the total number of vertical line objects identified (`num_objects`).
    5.  Calculate the column index for the new gray line: `col_G = col_R + 2`.
    6.  Calculate the end row for the new gray line: `end_G = end_R`.
    7.  Calculate the start row for the new gray line (`start_G`) based on the color of the rightmost line and the total number of lines:
        *   If `color_R` is red (2), set `start_G = end_G`.
        *   If `color_R` is azure (8):
            *   If `num_objects` is 2, set `start_G = max(0, start_R - 2)`.
            *   If `num_objects` is 3, set `start_G = max(0, start_R - 1)`.
            *   (Assume behavior for other counts is undefined by examples, proceed only if count is 2 or 3 when rightmost is azure).
    8.  Create a copy of the input grid.
    9.  If `col_G` is a valid column index within the grid's width, draw a vertical line of gray (5) pixels in column `col_G` from row `start_G` to `end_G` (inclusive) onto the copied grid.
    10. Return the modified grid.