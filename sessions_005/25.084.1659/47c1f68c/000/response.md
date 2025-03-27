*   **Perception:**
    The task involves identifying central horizontal and vertical lines within the input grid. These lines act as axes of symmetry and also determine the color of the output shapes. A distinct shape, located in one quadrant (the top-left in all examples), is mirrored across these axes into the other three quadrants. The original central lines are then removed, resulting in a smaller output grid containing four identical shapes, all colored according to the original lines. The background color (white) is preserved.

*   **YAML Facts:**
    
```yaml
    task_type: symmetry_and_resizing
    elements:
      - type: grid
        properties:
          background_color: white (0)
      - type: lines
        properties:
          count: 2 (one horizontal, one vertical)
          role: defines symmetry axes, determines output color, defines quadrants
          location: intersect near the center, span the grid dimensions
          color: variable (azure, red, yellow in examples) - referred to as 'line_color'
      - type: shape
        properties:
          count: 1 (in examples)
          location: initially in one quadrant (top-left in examples)
          color: variable, different from 'line_color' and background - referred to as 'shape_color'
          role: object to be replicated via symmetry
    actions:
      - action: identify_lines
        inputs: input_grid
        outputs: horizontal_line_row, vertical_line_column, line_color
      - action: identify_shape
        inputs: input_grid, horizontal_line_row, vertical_line_column
        outputs: shape_pixels (relative coordinates and original color)
      - action: remove_lines
        inputs: input_grid, horizontal_line_row, vertical_line_column
        outputs: base_output_grid (size reduced by 1x1, lines removed)
      - action: mirror_shape
        inputs: shape_pixels, grid_dimensions (original), horizontal_line_row, vertical_line_column
        outputs: coordinates for three mirrored shapes
      - action: recolor_and_place_shapes
        inputs: base_output_grid, original_shape_pixels, mirrored_shape_coordinates, line_color
        outputs: final_output_grid
    relationships:
      - relationship: symmetry
        element1: shape
        element2: lines
        details: Shape is mirrored across both horizontal and vertical lines.
      - relationship: color_transfer
        element1: lines
        element2: shape (in output)
        details: The color of the lines ('line_color') becomes the color of all four shapes in the output grid.
      - relationship: resizing
        element1: input_grid
        element2: output_grid
        details: Output grid dimensions are (input_height - 1) x (input_width - 1) due to line removal.
    ```


*   **Natural Language Program:**
    1.  Identify the single, fully spanning horizontal line and the single, fully spanning vertical line within the input grid. Record their row index (`hr`), column index (`vc`), and color (`line_color`).
    2.  Identify all pixels belonging to shapes that are neither the background color (white) nor the `line_color`. Record their coordinates relative to the top-left corner.
    3.  Create a new output grid with dimensions (input_height - 1) x (input_width - 1), initially filled with the background color (white).
    4.  For each identified shape pixel at `(r, c)` in the input grid:
        a.  Calculate its position relative to the intersection of the lines: `(dr = r - hr, dc = c - vc)`.
        b.  Determine the corresponding positions in the four quadrants of the *output* grid (adjusting for the removed row/column):
            i.  Top-left: `(r, c)` maps to `(r, c)` if `r < hr` and `c < vc`.
            ii. Top-right: `(r, c)` maps to `(r, c - 1)` if `r < hr` and `c > vc`.
            iii. Bottom-left: `(r, c)` maps to `(r - 1, c)` if `r > hr` and `c < vc`.
            iv. Bottom-right: `(r, c)` maps to `(r - 1, c - 1)` if `r > hr` and `c > vc`.
        c.  Determine the mirrored positions based on `(dr, dc)`:
            i.  Original/Top-left Quadrant position maps from `(hr + dr, vc + dc)`.
            ii. Top-right Quadrant position maps from `(hr + dr, vc - dc)`.
            iii. Bottom-left Quadrant position maps from `(hr - dr, vc + dc)`.
            iv. Bottom-right Quadrant position maps from `(hr - dr, vc - dc)`.
        d.  For each of these four input-grid-relative positions `(mirrored_r, mirrored_c)`, calculate the corresponding output grid coordinates using the quadrant mapping logic from step 4b.
        e.  Set the color of these four calculated positions in the output grid to `line_color`.
    5.  Return the completed output grid.