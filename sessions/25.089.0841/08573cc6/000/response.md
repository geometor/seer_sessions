*   **Perception:**
    *   The input grids contain exactly three non-white pixels.
    *   Two pixels are located at the top-left corner: input[0,0] and input[0,1]. Their colors determine the 'fill' and 'outline' colors for a shape to be drawn in the output.
    *   A single blue pixel (color 1) is located elsewhere in the input grid. Its position serves as an 'anchor' point for drawing the shape in the output grid.
    *   The output grid is initially white (all 0s).
    *   A specific shape template is selected based on the combination of the fill color (from input[0,0]) and outline color (from input[0,1]). Each training example demonstrates a different shape corresponding to a different color pair.
    *   This selected shape is drawn onto the output grid using the identified fill and outline colors.
    *   The drawing is positioned relative to the anchor point found in the input.
    *   The pixel at the anchor location in the output grid retains the blue color (1), overriding any fill or outline color that the template might specify for that relative position.

*   **Facts:**
    
```yaml
    task_elements:
      - element: input_grid
        description: A 2D grid containing pixels with colors 0-9.
        properties:
          - size: variable height and width (up to 30x30).
          - content: Mostly white (0) with three significant non-white pixels.
      - element: significant_pixels
        description: The three non-white pixels in the input grid that determine the output.
        properties:
          - pixel_fill_color:
              location: [0, 0]
              role: Defines the fill color for the output shape.
          - pixel_outline_color:
              location: [0, 1]
              role: Defines the outline color for the output shape.
          - pixel_anchor:
              color: 1 (blue)
              location: variable coordinates [r_anchor, c_anchor]
              role: Defines the anchor point for positioning the shape in the output.
      - element: output_grid
        description: A 2D grid representing the transformed input.
        properties:
          - size: Same dimensions as the input grid.
          - content: Initially white (0), then a shape is drawn onto it.
      - element: shape_template
        description: A predefined pattern of relative coordinates specifying fill and outline pixels.
        properties:
          - identity: Determined by the combination of fill_color and outline_color.
          - structure: Consists of relative coordinates for fill pixels and outline pixels.
          - examples_observed:
              - fill_color: 5 (gray), outline_color: 6 (magenta) -> "T" shape
              - fill_color: 3 (green), outline_color: 2 (red) -> "H" shape
              - fill_color: 5 (gray), outline_color: 3 (green) -> "Key/F" shape
    actions:
      - action: identify_colors_and_anchor
        inputs: input_grid
        outputs: fill_color, outline_color, anchor_location [r_anchor, c_anchor]
        steps:
          - Read color at input_grid[0, 0] -> fill_color.
          - Read color at input_grid[0, 1] -> outline_color.
          - Find coordinates [r_anchor, c_anchor] of the pixel with color 1.
      - action: select_shape_template
        inputs: fill_color, outline_color
        outputs: specific_shape_template
        description: Choose the appropriate shape based on the color pair. Requires a mapping from (fill, outline) pairs to shape templates.
      - action: draw_shape
        inputs: output_grid, specific_shape_template, fill_color, outline_color, anchor_location [r_anchor, c_anchor]
        outputs: modified_output_grid
        steps:
          - Initialize output_grid with all white (0) pixels.
          - For each relative coordinate [dr, dc] defined as 'fill' in the specific_shape_template:
              - Calculate absolute coordinate [r, c] = [r_anchor + dr, c_anchor + dc].
              - If [r, c] is within the grid bounds and is not the anchor location:
                  - Set output_grid[r, c] = fill_color.
          - For each relative coordinate [dr, dc] defined as 'outline' in the specific_shape_template:
              - Calculate absolute coordinate [r, c] = [r_anchor + dr, c_anchor + dc].
              - If [r, c] is within the grid bounds and is not the anchor location:
                  - Set output_grid[r, c] = outline_color.
          - Set output_grid[r_anchor, c_anchor] = 1 (blue).
    ```


*   **Natural Language Program:**
    1.  Identify the fill color (`C_fill`) from the input grid pixel at coordinate (0, 0).
    2.  Identify the outline color (`C_outline`) from the input grid pixel at coordinate (0, 1).
    3.  Find the coordinates (`r_anchor`, `c_anchor`) of the single blue pixel (color 1) in the input grid.
    4.  Determine which predefined shape template corresponds to the specific pair (`C_fill`, `C_outline`). Store this template, which consists of sets of relative coordinates for fill pixels and outline pixels (relative to a conceptual center, e.g., (0,0)).
    5.  Create a new output grid of the same dimensions as the input grid, initialized with all white pixels (color 0).
    6.  Iterate through the relative fill coordinates (`dr`, `dc`) defined in the selected shape template:
        a.  Calculate the target absolute coordinates: `r = r_anchor + dr`, `c = c_anchor + dc`.
        b.  Check if the target coordinates (`r`, `c`) are within the bounds of the output grid.
        c.  If they are within bounds and (`r`, `c`) is *not* the anchor location (`r_anchor`, `c_anchor`), set the pixel at (`r`, `c`) in the output grid to `C_fill`.
    7.  Iterate through the relative outline coordinates (`dr`, `dc`) defined in the selected shape template:
        a.  Calculate the target absolute coordinates: `r = r_anchor + dr`, `c = c_anchor + dc`.
        b.  Check if the target coordinates (`r`, `c`) are within the bounds of the output grid.
        c.  If they are within bounds and (`r`, `c`) is *not* the anchor location (`r_anchor`, `c_anchor`), set the pixel at (`r`, `c`) in the output grid to `C_outline`.
    8.  Finally, set the pixel at the anchor coordinates (`r_anchor`, `c_anchor`) in the output grid to blue (color 1), ensuring it remains blue regardless of the shape template.
    9.  Return the completed output grid.