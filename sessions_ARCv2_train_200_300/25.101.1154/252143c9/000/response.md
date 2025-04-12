## Perception

The task involves transforming an input grid into an output grid of the same dimensions.
Observing the examples, the orange color (7) appears to be a default or background color.
The input grids contain various colors, while the output grids are predominantly orange, with a single diagonal line segment composed of a different color.
The color and location of this diagonal line segment in the output seem determined by specific features of the input grid.
Specifically, the color of the line appears to be derived from the color of a non-orange pixel located closest to the geometric center of the input grid.
The line itself is an anti-diagonal (where row index + column index is constant).
The portion of the anti-diagonal that is drawn (i.e., the line segment) starts from the identified central pixel and extends towards one corner. The direction of extension seems dependent on the parity (even or odd) of the color of the central pixel.
All pixels not part of this drawn line segment are set to the background color (orange).

## Facts


```yaml
task_context:
  - description: Transform an input grid based on identifying a central feature and drawing a diagonal line.
  - grid_properties:
      - Input and output grids have the same dimensions.
      - Orange (7) acts as the background color in the output and is often the most frequent color in the input.

identified_objects:
  - object: Central Pixel
    description: The non-background pixel closest to the geometric center of the input grid.
    properties:
      - location: (r_c, c_c)
      - color: C (input[r_c][c_c])
      - constraints: Must not be the background color (orange=7). Ties in distance resolved by top-most, then left-most.
  - object: Background
    description: The default color used to fill the output grid initially.
    properties:
      - color: Orange (7)
  - object: Output Line Segment
    description: A segment of an anti-diagonal line drawn on the output grid.
    properties:
      - color: C (derived from the Central Pixel)
      - geometry: Anti-diagonal (r + c = r_c + c_c)
      - location: A subset of the full anti-diagonal, determined by the Central Pixel's location and color parity.

transformations:
  - action: Identify Background Color
    input: input_grid
    output: background_color (assumed Orange=7)
  - action: Calculate Geometric Center
    input: grid_dimensions (height, width)
    output: center_coords (center_r, center_c)
  - action: Find Central Pixel
    input: input_grid, background_color, center_coords
    output: central_pixel_location (r_c, c_c), central_pixel_color (C)
    details: Finds the non-background pixel closest to center_coords (Manhattan distance, tie-break with min row, then min col).
  - action: Initialize Output Grid
    input: grid_dimensions, background_color
    output: output_grid (filled with background_color)
  - action: Determine Line Segment Parameters
    input: central_pixel_location (r_c, c_c), central_pixel_color (C)
    output: anti_diagonal_sum (S = r_c + c_c), direction_rule (based on C parity)
  - action: Draw Line Segment
    input: output_grid, anti_diagonal_sum (S), central_pixel_location (r_c, c_c), central_pixel_color (C), direction_rule
    output: modified output_grid
    details: Iterates through grid cells (r, c). If r + c == S and the cell satisfies the direction rule (relative to (r_c, c_c) based on C's parity), set output[r][c] = C.

relationships:
  - The color of the Output Line Segment is determined by the color of the Central Pixel found in the input.
  - The location of the Output Line Segment is determined by the location of the Central Pixel (it lies on the anti-diagonal passing through it).
  - The extent and direction of the Output Line Segment along the anti-diagonal depend on the parity of the Central Pixel's color.
  - All pixels in the output grid not belonging to the Output Line Segment are set to the Background color.

```


## Natural Language Program

1.  Assume the background color is orange (7).
2.  Determine the dimensions (height H, width W) of the input grid.
3.  Calculate the coordinates of the geometric center of the grid: `center_r = (H - 1) / 2`, `center_c = (W - 1) / 2`.
4.  Find the pixel `(r_c, c_c)` in the input grid that is not the background color (orange=7) and has the minimum Manhattan distance `(|r - center_r| + |c - center_c|)` to the geometric center. If there are multiple pixels with the same minimum distance, choose the one with the smallest row index `r`. If there is still a tie, choose the one with the smallest column index `c`.
5.  Let `C` be the color of the identified pixel `input[r_c][c_c]`.
6.  Create a new output grid with the same dimensions (H, W) as the input grid, and fill it entirely with the background color (orange=7).
7.  Calculate the anti-diagonal sum `S = r_c + c_c`.
8.  Iterate through each cell `(r, c)` of the grid (from `r=0` to `H-1`, `c=0` to `W-1`).
9.  Check if the cell `(r, c)` lies on the target anti-diagonal, i.e., if `r + c == S`.
10. If it lies on the anti-diagonal, check the direction condition based on the parity of the color `C`:
    a.  If `C` is even: Check if `r <= r_c` AND `c >= c_c`. If true, set `output[r][c] = C`.
    b.  If `C` is odd: Check if `r >= r_c` AND `c <= c_c`. If true, set `output[r][c] = C`.
11. The final state of the new grid is the result.