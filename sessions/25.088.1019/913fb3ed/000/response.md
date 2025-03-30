*   **Perception of Elements:**
    *   The input grids are mostly white (0) with a few isolated, single non-white pixels.
    *   The non-white pixels observed in the inputs are green (3), red (2), and azure (8).
    *   The output grids retain the original non-white pixels at their locations.
    *   Each original non-white pixel in the input becomes the center of a 3x3 square in the output.
    *   The color of the surrounding pixels in the 3x3 square depends on the color of the central pixel according to a specific mapping:
        *   If the center is green (3), the surrounding pixels are magenta (6).
        *   If the center is red (2), the surrounding pixels are blue (1).
        *   If the center is azure (8), the surrounding pixels are yellow (4).
    *   The rest of the grid remains white (0).
    *   The transformations for multiple input pixels occur independently within the same grid.

*   **YAML Facts:**
    
```yaml
    task_description: "Create a 3x3 colored square around each non-white input pixel, preserving the original pixel color at the center."
    objects:
      - type: pixel
        properties:
          color: non-white (specifically green, red, azure observed)
          location: variable
          role: trigger_pixel
      - type: background
        properties:
          color: white (0)
          role: static
      - type: square
        properties:
          size: 3x3
          center_color: matches the trigger_pixel color
          border_color: determined by a specific mapping from the center_color
          role: generated_output_feature
    relationships:
      - type: centered_on
        subject: square
        object: trigger_pixel
      - type: color_mapping
        details:
          - input_color: green (3)
            output_color: magenta (6)
          - input_color: red (2)
            output_color: blue (1)
          - input_color: azure (8)
            output_color: yellow (4)
    actions:
      - name: identify_pixels
        input: input_grid
        target: non-white pixels
        output: list of trigger_pixel coordinates and colors
      - name: generate_square
        input: trigger_pixel (coordinate and color)
        process: >
          Determine the border color based on the trigger_pixel color using the color_mapping.
          Create a 3x3 square centered at the trigger_pixel coordinate.
          Fill the center of the square with the trigger_pixel color.
          Fill the 8 surrounding pixels of the square with the determined border color.
        output: 3x3 colored square pattern
      - name: overlay_squares
        input: output_grid (initially copy of input or white grid), list of generated_square patterns
        process: Place each generated square onto the output grid at the corresponding location.
        output: final_output_grid
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid or as an all-white grid of the same dimensions.
    2.  Iterate through each pixel of the input grid.
    3.  If a pixel is non-white (not color 0):
        a.  Identify its color (let's call it `center_color`) and its coordinates (row `r`, column `c`).
        b.  Determine the `border_color` based on the `center_color`:
            *   If `center_color` is green (3), `border_color` is magenta (6).
            *   If `center_color` is red (2), `border_color` is blue (1).
            *   If `center_color` is azure (8), `border_color` is yellow (4).
        c.  For the 8 neighboring pixels surrounding the coordinates (`r`, `c`) (i.e., pixels at `(r-1, c-1)`, `(r-1, c)`, `(r-1, c+1)`, `(r, c-1)`, `(r, c+1)`, `(r+1, c-1)`, `(r+1, c)`, `(r+1, c+1)`), change their color in the output grid to the determined `border_color`. Ensure these coordinates are within the grid boundaries.
        d.  Keep the pixel at (`r`, `c`) in the output grid with its original `center_color`.
    4.  Return the modified output grid.