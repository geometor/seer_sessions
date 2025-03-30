Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Input Grid:** The input grids are mostly white (0) with one or more isolated green (3) pixels.
2.  **Output Grid:** The output grids retain the original green pixels but add complex patterns around them. The background remains white where no patterns are added.
3.  **Pattern:** A consistent, complex pattern appears centered around each original green pixel. This pattern seems to be a fixed "stamp".
4.  **Stamp Details:** Let the green pixel be at `(r, c)`. The stamp affects a region roughly from `(r-2, c-2)` to `(r+2, c+2)`.
    *   Row `r-2`: A horizontal line of gray (5) pixels from `c-2` to `c+2`.
    *   Row `r-1`: Red (2) at `(r-1, c-2)`, gray (5) at `(r-1, c)`, red (2) at `(r-1, c+2)`. White (0) elsewhere in this row within the stamp's bounds.
    *   Row `r`: Red (2) at `(r, c-2)`, the original green (3) at `(r, c)`, red (2) at `(r, c+2)`. White (0) elsewhere.
    *   Row `r+1`: Red (2) at `(r+1, c-2)` and `(r+1, c+2)`. White (0) elsewhere.
    *   Row `r+2`: A horizontal line of azure (8) pixels from `c-2` to `c+2`.
5.  **Horizontal Lines:** In addition to the stamps, horizontal lines of red (2) pixels are drawn across the *entire width* of the grid. The row index for each red line seems related to the row index of a green pixel. Specifically, for a green pixel at `(r, c)`, a red line appears at row `r+2`.
6.  **Interaction/Overlap:** When multiple green pixels exist (Example 1), multiple stamps are placed, and multiple red lines are drawn. The key observation is how the red lines interact with the stamps. The red line at `r+2` overwrites existing pixels *except* for the azure (8) pixels that are part of *any* stamp pattern located at that same row `r+2`.

**YAML Fact Document:**


```yaml
task_description: Stamp a pattern centered on each green pixel and draw horizontal red lines based on green pixel locations, with specific overwrite rules.

grid_properties:
  - background_color: white (0)
  - grid_size: Variable (up to 30x30)

objects:
  - object: green_pixel
    color: 3 (green)
    property: location (row, column)
    role: trigger for pattern placement and line drawing

  - object: stamp_pattern
    size: 5x5 relative to center
    colors_used: [2 (red), 3 (green), 5 (gray), 8 (azure), 0 (white)]
    structure: Fixed spatial arrangement of colors relative to the center green pixel.
    property: centered_on: green_pixel location

  - object: horizontal_red_line
    color: 2 (red)
    property: row_index: derived from green_pixel row (r+2)
    property: length: spans the full width of the grid

actions:
  - action: find_green_pixels
    input: input_grid
    output: list of coordinates (r, c) of all green pixels

  - action: place_stamp
    input: output_grid, center_coordinate (r, c)
    effect: Overwrites pixels in the output_grid with the stamp_pattern centered at (r, c). Records the locations of azure (8) pixels placed.

  - action: draw_red_line
    input: output_grid, row_index R, set_of_azure_pixels
    effect: Iterates through columns C of row R. If (R, C) is not in set_of_azure_pixels, sets output_grid[R, C] to red (2).

relationships:
  - relationship: one_to_one
    subject: green_pixel
    verb: triggers
    object: stamp_pattern placement (centered on green_pixel)
  - relationship: one_to_one
    subject: green_pixel at (r, c)
    verb: determines
    object: horizontal_red_line row index (r+2)
  - relationship: overwrite_priority
    subject: horizontal_red_line
    verb: does not overwrite
    object: azure (8) pixels originating from any stamp_pattern
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Define the 5x5 `stamp_pattern` relative to a central coordinate:
    *   `(r-2, c-2)` to `(r-2, c+2)`: gray (5)
    *   `(r-1, c-2)`: red (2), `(r-1, c)`: gray (5), `(r-1, c+2)`: red (2)
    *   `(r, c-2)`: red (2), `(r, c)`: green (3), `(r, c+2)`: red (2)
    *   `(r+1, c-2)`: red (2), `(r+1, c+2)`: red (2)
    *   `(r+2, c-2)` to `(r+2, c+2)`: azure (8)
    *   Other relative coordinates within this 5x5 bounding box that are not explicitly mentioned are set to white (0).
3.  Find the coordinates `(r, c)` of all green (3) pixels in the `input_grid`. Store these `green_pixel_locations`.
4.  Create an empty set called `red_line_rows` to store the row indices where horizontal red lines should be drawn.
5.  Create an empty set called `azure_pixel_coordinates` to store the coordinates of all azure pixels placed by stamps.
6.  For each `(r, c)` in `green_pixel_locations`:
    a.  Add the row index `r + 2` to the `red_line_rows` set.
    b.  Apply the `stamp_pattern` centered at `(r, c)` onto the `output_grid`, overwriting existing values.
    c.  For each column `col` from `c - 2` to `c + 2`, add the coordinate `(r + 2, col)` to the `azure_pixel_coordinates` set.
7.  For each row index `R` in `red_line_rows`:
    a.  For each column index `C` from 0 to the width of the grid - 1:
        i.  If the coordinate `(R, C)` is *not* present in the `azure_pixel_coordinates` set, set the pixel value at `output_grid[R, C]` to red (2).
8.  Return the `output_grid`.