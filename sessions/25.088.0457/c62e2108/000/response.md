*   **Perception:** The task involves modifying an input grid based on the locations of specific colored objects. There are always one or more "pattern" objects (non-white, non-blue colors like azure, red, green) and several blue lines (horizontal or vertical). The output grid retains the original pattern objects but adds lines of the pattern object's color. These new lines seem to correspond to the locations of the original blue lines and also to the boundary rows and columns of the original pattern objects.

*   **YAML Facts:**
    
```yaml
    task_description: Modify the grid by adding horizontal and vertical lines based on existing objects and blue lines.
    
    elements:
      - type: grid
        properties:
          background_color: white (0)
      - type: object
        name: pattern_object
        properties:
          color: any color except white (0) or blue (1)
          shape: variable (e.g., 'H' shape in examples)
          contiguous: true
          count: one or more per input grid
      - type: object
        name: boundary_marker
        properties:
          color: blue (1)
          shape: horizontal line (1 pixel thick) or vertical line (1 pixel thick)
          contiguous: true
          count: multiple per input grid (can be zero horizontal or zero vertical)
    
    relationships:
      - relation: defines_fill_location
        subject: boundary_marker (blue line)
        object: output grid modification
        details: The row index of a horizontal blue line indicates a row to be filled in the output. The column index of a vertical blue line indicates a column to be filled in the output.
      - relation: defines_fill_location
        subject: pattern_object
        object: output grid modification
        details: The minimum and maximum row indices (bounding box) of a pattern object indicate rows to be filled in the output. The minimum and maximum column indices (bounding box) of a pattern object indicate columns to be filled in the output.
      - relation: determines_fill_color
        subject: pattern_object
        object: output grid modification
        details: The color of a pattern object is used as the fill color for the rows and columns associated with that pattern object and the associated boundary markers.
    
    actions:
      - action: identify
        target: pattern_objects
        criteria: contiguous pixels with color not white (0) and not blue (1)
        result: list of pattern objects, each with color and bounding box (min_row, min_col, max_row, max_col)
      - action: identify
        target: horizontal_boundary_markers
        criteria: horizontal lines of blue (1) pixels
        result: list of row indices
      - action: identify
        target: vertical_boundary_markers
        criteria: vertical lines of blue (1) pixels
        result: list of column indices
      - action: create_output
        source: input grid
        steps:
          - Initialize output grid as a copy of the input grid.
          - For each identified pattern_object:
            - Get its color C and bounding box (min_r, min_c, max_r, max_c).
            - For each identified horizontal_boundary_marker row index `hr`: Fill row `hr` of the output grid entirely with color C.
            - For each identified vertical_boundary_marker column index `vc`: Fill column `vc` of the output grid entirely with color C.
            - Fill row `min_r` of the output grid entirely with color C.
            - Fill row `max_r` of the output grid entirely with color C.
            - Fill column `min_c` of the output grid entirely with color C.
            - Fill column `max_c` of the output grid entirely with color C.
            - Note: Fills from different patterns or steps overwrite previous fills in the same location.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, contiguous objects in the input grid that are not white (0) or blue (1). These are the "Pattern Objects". For each Pattern Object, record its color and its bounding box (minimum row, minimum column, maximum row, maximum column).
    2.  Identify all horizontal lines composed entirely of blue (1) pixels. Record the row index of each such line.
    3.  Identify all vertical lines composed entirely of blue (1) pixels. Record the column index of each such line.
    4.  Initialize the output grid as an exact copy of the input grid.
    5.  Iterate through each identified Pattern Object:
        a.  Let C be the color of the current Pattern Object.
        b.  Let (min_row, min_col, max_row, max_col) be the bounding box of the current Pattern Object.
        c.  For each recorded horizontal blue line row index `r`, fill the entire row `r` in the output grid with color C.
        d.  For each recorded vertical blue line column index `c`, fill the entire column `c` in the output grid with color C.
        e.  Fill the entire row `min_row` in the output grid with color C.
        f.  Fill the entire row `max_row` in the output grid with color C.
        g.  Fill the entire column `min_col` in the output grid with color C.
        h.  Fill the entire column `max_col` in the output grid with color C.
    6.  The final state of the output grid after processing all Pattern Objects is the result. (Note: Later fills overwrite earlier fills if they target the same pixel).