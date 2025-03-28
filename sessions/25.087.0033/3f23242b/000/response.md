*   **Perception:**
    The task involves identifying specific trigger pixels in the input grid and drawing a predefined, complex pattern centered around each trigger pixel in the output grid. The input grids contain one or more green (3) pixels scattered on a white (0) background. The output grid has the same dimensions as the input. For every green pixel in the input, a specific multi-colored structure is drawn in the output, centered at the location of the original green pixel. This structure consists of gray (5), red (2), and azure (8) pixels arranged in lines and specific points relative to the center. A key feature is a horizontal red line segment at the bottom of the structure that extends left and right from the main body of the structure all the way to the vertical edges of the grid. If there are multiple green pixels, the corresponding structures are drawn independently for each, potentially overwriting the background. The examples suggest that the structures themselves don't overlap in ways that cause ambiguity, other than potentially sharing the background color. The original green pixel is preserved at its location within the drawn structure.

*   **Facts:**
    
```yaml
    task_context:
      problem_type: pattern_drawing
      grid_size_relation: input and output grids share the same dimensions.
      background_color: white (0)

    input_elements:
      - object: trigger_pixel
        color: green (3)
        count: 1 or more
        properties:
          - location: (r, c) - coordinates vary per instance.

    output_elements:
      - object: composite_structure
        count: one for each input trigger_pixel
        properties:
          - centered at the (r, c) coordinates of the corresponding trigger_pixel.
        components:
          - type: pixel # Center anchor
            color: green (3)
            relative_location: (0, 0) corresponding to input (r, c)
          - type: h_line # Top gray line
            color: gray (5)
            relative_location: row -2, columns -2 to +2
            length: 5
          - type: pixel # Center gray dot
            color: gray (5)
            relative_location: (-1, 0)
          - type: v_line # Left red line
            color: red (2)
            relative_location: column -2, rows -1 to +2
            length: 4
          - type: v_line # Right red line
            color: red (2)
            relative_location: column +2, rows -1 to +2
            length: 4
          - type: pixel # Left red dot
            color: red (2)
            relative_location: (0, -2)
          - type: pixel # Right red dot
            color: red (2)
            relative_location: (0, +2)
          - type: h_line # Bottom azure line
            color: azure (8)
            relative_location: row +2, columns -2 to +2
            length: 5
          - type: h_line_segment # Bottom left red extension
            color: red (2)
            relative_location: row +2, from grid_left_edge (col 0) to column -3
          - type: h_line_segment # Bottom right red extension
            color: red (2)
            relative_location: row +2, from column +3 to grid_right_edge (col width-1)

    actions:
      - action: identify_triggers
        input: input_grid
        target_color: green (3)
        output: list of coordinates [(r1, c1), (r2, c2), ...]
      - action: render_structure
        input: trigger coordinate (r, c), grid dimensions
        process: For a given trigger coordinate, draw all components of the composite_structure relative to (r, c) onto the grid. Respect grid boundaries.
        output: modifies the grid state by drawing pixels.

    relationships:
      - Each green pixel in the input mandates the drawing of one complete composite_structure in the output.
      - The structure is rigidly defined relative to the green pixel's location.
      - The red extension lines (h_line_segment) always span from the structure's edge (cols c-3 and c+3) to the respective grid boundary along the row r+2.
      - The final output grid is the superposition of all drawn structures onto the initial grid state (which is identical to the input).
    ```


*   **Natural Language Program:**
    1.  Create the output grid by making a copy of the input grid.
    2.  Identify all locations (rows `r`, columns `c`) in the input grid that contain a green (3) pixel.
    3.  For each identified location (`r`, `c`):
        a.  Calculate the absolute coordinates for each component of the predefined structure based on its relative position to (`r`, `c`).
        b.  For each calculated coordinate `(row, col)` and its associated color:
            i.  Check if `(row, col)` is within the bounds of the grid.
            ii. If it is within bounds, set the color of the pixel at `(row, col)` in the output grid to the component's color.
        c.  Specifically, draw the following components (checking boundaries for each pixel):
            -   Gray (5) pixels: `(r-2, c-2)` through `(r-2, c+2)`, and `(r-1, c)`.
            -   Red (2) pixels: `(r-1, c-2)` through `(r+2, c-2)`, `(r-1, c+2)` through `(r+2, c+2)`, `(r, c-2)`, `(r, c+2)`.
            -   Azure (8) pixels: `(r+2, c-2)` through `(r+2, c+2)`.
            -   Red (2) pixels (extensions): all pixels in row `r+2` from column 0 to `c-3` (inclusive), and all pixels in row `r+2` from column `c+3` to the last column index (inclusive).
            -   Ensure the pixel at (`r`, `c`) remains green (3) (it should be preserved from the initial copy unless explicitly overwritten, which the defined structure doesn't do).
    4.  Return the fully modified output grid.