Okay, let's break down this task.

## Perception

1.  **Input/Output Grids:** The task operates on grids of varying sizes containing pixels of different colors (0-9). The background is always white (0).
2.  **Key Elements:** The crucial elements in the input grids are the isolated, non-white pixels. There can be one or more such pixels.
3.  **Transformation:** The transformation involves extending lines from each non-white pixel towards the grid boundaries. Each non-white pixel generates exactly one vertical line and one horizontal line.
4.  **Line Generation:**
    *   A vertical line is drawn in the same column as the source pixel.
    *   A horizontal line is drawn in the same row as the source pixel.
    *   The color of the lines matches the color of the source pixel.
5.  **Directionality:** The direction of the lines (up/down, left/right) seems determined by the source pixel's proximity to the edges. The lines extend towards the *closer* edge.
    *   **Vertical:** If the pixel is closer to or equidistant from the top edge, the vertical line extends upwards from the top edge to the pixel's row. If it's closer to the bottom edge, the line extends downwards from the pixel's row to the bottom edge.
    *   **Horizontal:** If the pixel is closer to or equidistant from the left edge, the horizontal line extends leftwards from the left edge to the pixel's column. If it's closer to the right edge, the line extends rightwards from the pixel's column to the right edge.
6.  **Overlap:** The generated lines overwrite any existing pixels (including white background) in the output grid. The source pixel itself is part of both its vertical and horizontal lines.

## Facts


```yaml
task_context:
  description: "Draws vertical and horizontal lines extending from each non-white pixel to the nearest corresponding grid edge."
  grid_properties:
    - dimensions_vary: True
    - background_color: white (0)
    - content: Contains isolated non-white pixels.

identified_objects:
  - name: source_pixel
    description: "An individual pixel in the input grid with a color other than white (0)."
    properties:
      - position: (row, column)
      - color: (1-9)
      - grid_height: H
      - grid_width: W
      - distance_to_top_edge: row
      - distance_to_bottom_edge: H - 1 - row
      - distance_to_left_edge: column
      - distance_to_right_edge: W - 1 - column
    count_per_grid: varies (1 or more in examples)

actions:
  - name: identify_source_pixels
    input: input_grid
    output: list_of_source_pixels

  - name: determine_projection_directions
    input: source_pixel, grid_height, grid_width
    output: vertical_direction (up/down), horizontal_direction (left/right)
    logic: |
      vertical_direction = 'up' if distance_to_top_edge <= distance_to_bottom_edge else 'down'
      horizontal_direction = 'left' if distance_to_left_edge <= distance_to_right_edge else 'right'

  - name: draw_vertical_line
    input: output_grid, source_pixel, vertical_direction
    output: modified_output_grid
    logic: |
      Color pixels in the source_pixel's column with the source_pixel's color.
      If vertical_direction is 'up', color from row 0 to source_pixel.row (inclusive).
      If vertical_direction is 'down', color from source_pixel.row to grid_height - 1 (inclusive).

  - name: draw_horizontal_line
    input: output_grid, source_pixel, horizontal_direction
    output: modified_output_grid
    logic: |
      Color pixels in the source_pixel's row with the source_pixel's color.
      If horizontal_direction is 'left', color from column 0 to source_pixel.column (inclusive).
      If horizontal_direction is 'right', color from source_pixel.column to grid_width - 1 (inclusive).

relationships:
  - type: generation
    from: source_pixel
    to: vertical_line, horizontal_line
    details: "Each source pixel generates one vertical and one horizontal line of its own color."
  - type: dependency
    element: line_direction
    depends_on: source_pixel_position, grid_dimensions
    details: "The direction of projection depends on the relative distance of the source pixel to the grid edges."
  - type: composition
    element: output_grid
    composed_of: input_grid, all_generated_lines
    details: "The output grid starts as the input grid and is then modified by drawing all generated lines."

output_specification:
  - grid_size: Same as input grid size.
  - content: Input grid content overlaid with the generated vertical and horizontal lines originating from each source pixel.
```


## Natural Language Program

1.  Initialize the output grid as a direct copy of the input grid.
2.  Identify the locations (row, column) and colors of all pixels in the input grid that are not white (color 0). Let these be the "source pixels".
3.  For each identified source pixel at `(r, c)` with color `C`:
    a.  Determine the grid's height `H` and width `W`.
    b.  **Vertical Line:**
        i.  Compare the distance to the top edge (`r`) with the distance to the bottom edge (`H - 1 - r`).
        ii. If `r <= H - 1 - r` (closer to or equidistant from the top), draw a vertical line of color `C` in column `c` from row 0 up to and including row `r`.
        iii. Otherwise (closer to the bottom), draw a vertical line of color `C` in column `c` starting from row `r` down to and including row `H - 1`.
    c.  **Horizontal Line:**
        i.  Compare the distance to the left edge (`c`) with the distance to the right edge (`W - 1 - c`).
        ii. If `c <= W - 1 - c` (closer to or equidistant from the left), draw a horizontal line of color `C` in row `r` from column 0 up to and including column `c`.
        iii. Otherwise (closer to the right), draw a horizontal line of color `C` in row `r` starting from column `c` up to and including column `W - 1`.
4.  Return the final modified output grid.