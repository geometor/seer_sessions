*   **Perception:**
    The task involves identifying specific, isolated single pixels in the input grid and replacing them with larger, hollow square patterns in the output grid. The color of the square depends on the color of the original isolated pixel. Other shapes or non-isolated pixels remain unchanged.

    1.  **Object Identification:** The key objects are single pixels (1x1 size) that are completely surrounded by the background color (white, 0). The colors of interest for these isolated pixels are red (2), green (3), and gray (5). Other objects, like the 2x2 magenta squares in train\_1, the blue 'L' shape in train\_2, or the yellow hollow square in train\_3, are also present but act as distractors or context, as they are not modified.
    2.  **Transformation:** When an isolated red, green, or gray pixel is found, it triggers a transformation. This pixel is conceptually replaced by a 4x4 hollow square.
    3.  **Color Mapping:** There's a specific mapping between the color of the isolated input pixel and the color of the output square:
        *   Red (2) pixel -> Yellow (4) square
        *   Green (3) pixel -> Blue (1) square
        *   Gray (5) pixel -> Magenta (6) square
    4.  **Placement:** The 4x4 hollow square is centered around the position of the original isolated pixel. If the original pixel was at `(row, col)`, the top-left corner of the 4x4 square is placed at `(row-1, col-1)`.
    5.  **Structure:** The output square is "hollow," meaning only its perimeter is colored; the inner 2x2 area retains the background color (white, 0).
    6.  **Persistence:** All parts of the input grid that are *not* isolated red, green, or gray pixels are copied directly to the output grid without modification.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    focus: isolated_pixels
    objects:
      - type: pixel
        color_constraints: [red, green, gray]
        property_constraints:
          - isolation: true  # All 8 neighbors must be background (white)
          - size: 1x1
      - type: shape
        description: Contiguous blocks of non-background color larger than 1x1. These are ignored.
      - type: background
        color: white
        description: The default grid color (0).
    actions:
      - name: find_isolated_pixels
        input: input_grid
        output: list_of_coordinates_and_colors
        description: Identify all pixels (r, c) where grid[r, c] is red, green, or gray, and all 8 neighbors are white.
      - name: map_color
        input: color_of_isolated_pixel (red, green, or gray)
        output: color_of_square (yellow, blue, or magenta)
        mapping:
          red: yellow
          green: blue
          gray: magenta
      - name: draw_hollow_square
        input: center_coordinate (r, c), square_color, output_grid
        output: modified_output_grid
        description: Draws a 4x4 hollow square of the specified color onto the output grid, centered at (r, c). The top-left corner is at (r-1, c-1). The perimeter is colored, the 2x2 interior is white. Handles grid boundaries.
      - name: copy_unchanged
        input: input_grid
        output: initial_output_grid
        description: Pixels not part of a transformation are copied. (Can be achieved by initializing output as a copy of input).
    relationships:
      - type: replacement
        description: An isolated pixel is replaced by a hollow square structure.
      - type: color_dependency
        description: The color of the replacement square depends on the color of the original isolated pixel.
      - type: spatial_dependency
        description: The position of the replacement square is centered on the position of the original isolated pixel.
    ```


*   **Natural Language Program:**
    1.  Create the output grid as a copy of the input grid.
    2.  Iterate through each cell `(r, c)` of the input grid, excluding the border rows/columns to simplify neighbor checking (or handle boundaries carefully if iterating over all cells).
    3.  For each cell `(r, c)`, check if it contains an isolated pixel:
        a.  Verify that the color of the pixel `input_grid[r, c]` is one of the trigger colors: red (2), green (3), or gray (5).
        b.  Verify that all 8 neighboring cells (at `(r-1, c-1)`, `(r-1, c)`, `(r-1, c+1)`, `(r, c-1)`, `(r, c+1)`, `(r+1, c-1)`, `(r+1, c)`, `(r+1, c+1)`) exist within the grid boundaries and contain the background color (white, 0).
    4.  If a cell `(r, c)` contains such an isolated trigger pixel:
        a.  Determine the target color for the output square based on the input pixel's color:
            *   If red (2), the target color is yellow (4).
            *   If green (3), the target color is blue (1).
            *   If gray (5), the target color is magenta (6).
        b.  Define the coordinates for the 4x4 bounding box centered at `(r, c)`. The top row is `r-1`, bottom row is `r+2`, left column is `c-1`, right column is `c+2`.
        c.  Draw the perimeter of this 4x4 box onto the *output grid* using the target color. Ensure drawing stays within the grid boundaries. Specifically, color the cells:
            *   Top edge: `(r-1, c-1)` to `(r-1, c+2)`
            *   Bottom edge: `(r+2, c-1)` to `(r+2, c+2)`
            *   Left edge (excluding corners): `(r, c-1)` and `(r+1, c-1)`
            *   Right edge (excluding corners): `(r, c+2)` and `(r+1, c+2)`
        d.  Ensure the 2x2 interior cells within the drawn square (`(r, c)`, `(r, c+1)`, `(r+1, c)`, `(r+1, c+1)`) are set to the background color (white, 0) in the output grid, if they fall within grid boundaries. *Correction:* Step 1 already copied the grid. Drawing the perimeter as described in 4c correctly creates the hollow effect, potentially overwriting the original pixel if it lies on the perimeter, which is fine. The central 2x2 area doesn't need explicit clearing if the drawing logic only paints the perimeter cells. Let's refine 4c: Paint all cells from `(r-1, c-1)` to `(r+2, c+2)` that are on the border of this 4x4 region.
    5.  After checking all cells in the input grid, return the modified output grid.