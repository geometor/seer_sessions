**Perception:**

The task involves transforming a small grid based on the position of a single red pixel (value 2). The input grid always contains exactly one red pixel, and the rest are white (value 0). The output grid is the same size as the input grid but contains up to four different colored pixels: green (3), magenta (6), azure (8), and orange (7), placed at specific locations relative to the position of the input red pixel. The original red pixel location becomes white in the output. The placement of the output pixels depends on whether the calculated position falls within the grid boundaries.

**YAML Facts:**


```yaml
task_description: Place four specific colors diagonally adjacent to the position of the input red pixel, if within bounds.
grid_properties:
  size: Fixed 3x5 for all examples shown. Assumed to be consistent for the test case.
  background_color: white (0)

input_elements:
  - object: marker_pixel
    color: red (2)
    count: 1
    properties:
      - position: (row, col) varies between examples.

output_elements:
  - object: output_pixel_green
    color: green (3)
    count: 0 or 1
    relationship: Placed at (input_row - 1, input_col - 1) relative to the red marker_pixel, if within grid bounds.
  - object: output_pixel_magenta
    color: magenta (6)
    count: 0 or 1
    relationship: Placed at (input_row - 1, input_col + 1) relative to the red marker_pixel, if within grid bounds.
  - object: output_pixel_azure
    color: azure (8)
    count: 0 or 1
    relationship: Placed at (input_row + 1, input_col - 1) relative to the red marker_pixel, if within grid bounds.
  - object: output_pixel_orange
    color: orange (7)
    count: 0 or 1
    relationship: Placed at (input_row + 1, input_col + 1) relative to the red marker_pixel, if within grid bounds.

transformation_rules:
  - action: find_marker
    input: input grid
    target: red (2) pixel
    output: coordinates (input_row, input_col) of the red pixel.
  - action: generate_output_grid
    input: dimensions of the input grid
    output: an empty grid (all white pixels) of the same dimensions.
  - action: place_pixels
    inputs:
      - output grid from previous step
      - coordinates (input_row, input_col) of the red marker
    process:
      - Calculate target coordinates for green: (input_row - 1, input_col - 1)
      - Calculate target coordinates for magenta: (input_row - 1, input_col + 1)
      - Calculate target coordinates for azure: (input_row + 1, input_col - 1)
      - Calculate target coordinates for orange: (input_row + 1, input_col + 1)
      - For each calculated coordinate (target_row, target_col):
        - Check if target_row is within the grid height bounds [0, height-1].
        - Check if target_col is within the grid width bounds [0, width-1].
        - If both are within bounds, place the corresponding color (green, magenta, azure, or orange) at (target_row, target_col) in the output grid.
    output: The final output grid with placed pixels.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid's dimensions, filled entirely with white pixels (0).
2.  Locate the coordinates (row `R`, column `C`) of the single red pixel (2) in the input grid.
3.  Define the four target relative positions and their corresponding colors:
    *   Green (3) at relative position (-1, -1)
    *   Magenta (6) at relative position (-1, +1)
    *   Azure (8) at relative position (+1, -1)
    *   Orange (7) at relative position (+1, +1)
4.  For each of the four defined relative positions (`dr`, `dc`) and their color `Col`:
    a.  Calculate the absolute target coordinates: `target_row = R + dr`, `target_col = C + dc`.
    b.  Check if `target_row` is greater than or equal to 0 and less than the height of the grid.
    c.  Check if `target_col` is greater than or equal to 0 and less than the width of the grid.
    d.  If both conditions (4b and 4c) are true, set the pixel at (`target_row`, `target_col`) in the output grid to the color `Col`.
5.  Return the final output grid.