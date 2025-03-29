Okay, let's break down the transformation for this task.

**Perception**

1.  **Input Grid:** The input grid consists primarily of a single background color (azure=8, maroon=9, or orange=7). Scattered within this background are a few isolated pixels of blue (1). These blue pixels appear as distinct points.
2.  **Output Grid:** The output grid retains the same dimensions and background color as the input. The key changes occur around the locations of the original blue pixels.
3.  **Transformation Pattern:** For each original blue pixel in the input:
    *   A horizontal line of blue (1) is drawn across the entire width of the grid at the row of the original blue pixel.
    *   A vertical line of blue (1) is drawn across the entire height of the grid at the column of the original blue pixel.
    *   The original blue pixel's location is replaced with a red pixel (2).
    *   The four diagonally adjacent pixels to the red pixel are changed to green (3).
4.  **Overlapping:** When lines or patterns from different source pixels overlap:
    *   Intersections of horizontal and vertical blue lines remain blue (1).
    *   The red (2) center pixel overwrites any blue line passing through it.
    *   The green (3) diagonal pixels overwrite any blue line passing through them. This suggests the red and green pixels are applied *after* the blue lines are drawn.

**Facts**


```yaml
task_context:
  grid_properties:
    - dimensions_preserved: True # Output grid has same height/width as input
    - background_color_preserved: True # The dominant color in input remains in output where no pattern is drawn
  objects:
    - object_type: background
      description: The single dominant color filling most of the input grid. Color varies between examples (azure=8, maroon=9, orange=7).
    - object_type: source_pixel
      color: blue (1)
      description: Isolated single pixels in the input grid. Their locations trigger the transformation.
    - object_type: horizontal_line
      color: blue (1)
      description: Drawn in the output grid across the full width at the row of each source_pixel.
    - object_type: vertical_line
      color: blue (1)
      description: Drawn in the output grid across the full height at the column of each source_pixel.
    - object_type: center_marker
      color: red (2)
      description: Replaces the source_pixel location in the output grid.
    - object_type: diagonal_markers
      color: green (3)
      description: Placed at the four diagonal neighbors of the center_marker in the output grid.
  relationships_and_actions:
    - action: identify
      actor: system
      target: source_pixels (color blue=1) in the input grid.
      result: A list of coordinates (row, col) for each source_pixel.
    - action: initialize_output
      actor: system
      source: input_grid
      result: Output grid starts as a copy of the input grid.
    - action: draw_lines
      actor: system
      trigger: Each identified source_pixel coordinate (r, c).
      target: output_grid
      details:
        - Draw a horizontal line of blue (1) at row r.
        - Draw a vertical line of blue (1) at column c.
      note: Lines overwrite the initial background/source pixels. Intersections of lines are blue (1).
    - action: place_markers
      actor: system
      trigger: Each identified source_pixel coordinate (r, c).
      target: output_grid
      details:
        - Place a center_marker (red=2) at (r, c).
        - Place diagonal_markers (green=3) at (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1), checking for grid boundaries.
      note: These markers overwrite any existing color (including blue lines) at their locations. This action occurs after draw_lines.

```


**Natural Language Program**

1.  Create the output grid with the same dimensions as the input grid and copy the contents of the input grid into it.
2.  Identify the row and column coordinates of all pixels in the input grid that have the color blue (1). Store these as a list of source coordinates.
3.  For each source coordinate `(r, c)` found in step 2:
    a.  Iterate through all columns `j` from 0 to the grid's width minus 1. Set the color of the pixel at `(r, j)` in the output grid to blue (1).
    b.  Iterate through all rows `i` from 0 to the grid's height minus 1. Set the color of the pixel at `(i, c)` in the output grid to blue (1).
4.  For each source coordinate `(r, c)` found in step 2:
    a.  Set the color of the pixel at `(r, c)` in the output grid to red (2).
    b.  Define the four diagonal neighbor coordinates: `(r-1, c-1)`, `(r-1, c+1)`, `(r+1, c-1)`, `(r+1, c+1)`.
    c.  For each diagonal neighbor coordinate `(nr, nc)`:
        i.  Check if `nr` is within the row boundaries (0 to height-1) and `nc` is within the column boundaries (0 to width-1).
        ii. If the coordinate `(nr, nc)` is within the grid boundaries, set the color of the pixel at `(nr, nc)` in the output grid to green (3).