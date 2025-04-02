
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 2 2 2 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
2 2 2 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 3 0 0 0 4 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 3 0 0 0 4 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 3 0 0 0 0 0 0 0 0 0 4 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 0 3 0 3 0 0 0 0 0 0 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

*   **Input/Output Grids:** Both examples involve grids containing a white background (0) and distinct colored objects or groups of pixels. The output grids have the same dimensions as their corresponding input grids.
*   **Objects/Colors:**
    *   Example 1: Contains a solid 3x3 red (2) object and a solid 3x3 blue (1) object.
    *   Example 2: Contains multiple green (3) pixels and multiple yellow (4) pixels, arranged in patterns but not necessarily forming single contiguous blocks for each color overall.
*   **Transformation:** In both examples, the colored elements undergo a horizontal shift. Elements initially positioned on the left side of the grid's horizontal center move towards the left edge. Elements initially positioned on the right side move towards the right edge.
*   **Movement Details:**
    *   The vertical positions of all colored pixels remain unchanged.
    *   The relative horizontal positions *within* a group of the same color seem to be preserved. The entire group of pixels of a specific color moves as a single unit.
    *   The extent of the movement is such that the outermost pixel(s) of the color group align with the corresponding grid edge (leftmost pixel to column 0 for left-moving groups, rightmost pixel to the last column for right-moving groups).
*   **Key Factor:** The decision to move left or right appears to depend on the overall horizontal position of all pixels of a given color relative to the grid's horizontal center.

**Facts**


```yaml
task_description: Move groups of pixels of the same color horizontally to the nearest edge of the grid.
grid_properties:
  - background_color: white (0)
  - dimensions_preserved: true
objects:
  - type: color_group
    description: All pixels of a single non-background color are treated as a group.
    properties:
      - color: the specific non-background color (e.g., red, blue, green, yellow)
      - pixels: list of (row, col) coordinates for all pixels of that color
      - horizontal_bounding_box: defined by the minimum and maximum column indices (min_col, max_col) occupied by the group's pixels
      - horizontal_center: calculated as (min_col + max_col) / 2
relationships:
  - type: spatial
    description: The position of a color group relative to the grid's horizontal center determines its movement direction.
    grid_horizontal_center: calculated as (grid_width - 1) / 2
actions:
  - name: identify_color_groups
    input: input_grid
    output: list of color groups (color, pixels, bounding_box)
  - name: determine_movement
    input: color_group, grid_width
    output: horizontal_shift_amount
    logic:
      - if group_center < grid_center: shift = 0 - min_col
      - if group_center >= grid_center: shift = (grid_width - 1) - max_col
  - name: apply_shift
    input: color_group_pixels, horizontal_shift_amount
    output: shifted_pixel_coordinates
    logic: For each (row, col) in pixels, new coordinate is (row, col + shift)
  - name: reconstruct_output
    input: grid_dimensions, background_color, all_shifted_pixels_by_color
    output: output_grid
    logic: Create an empty grid and place the shifted pixels onto it.
```


**Natural Language Program**

1.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify all unique non-background colors present in the input grid.
3.  For each unique non-background color found:
    a.  Collect the coordinates `(row, col)` of all pixels matching this color in the input grid.
    b.  If no pixels of this color exist, skip to the next color.
    c.  Determine the minimum (`min_col`) and maximum (`max_col`) column indices among these collected coordinates.
    d.  Calculate the horizontal center of this color group: `group_center = (min_col + max_col) / 2.0`.
    e.  Calculate the horizontal center of the grid: `grid_center = (grid_width - 1) / 2.0`.
    f.  Compare `group_center` with `grid_center`.
    g.  If `group_center < grid_center`, the group moves left. Calculate the horizontal shift needed: `shift = 0 - min_col`.
    h.  Otherwise (if `group_center >= grid_center`), the group moves right. Calculate the horizontal shift needed: `shift = (grid_width - 1) - max_col`.
    i.  For every original pixel coordinate `(row, col)` collected in step 3a, calculate its new position `(new_row, new_col) = (row, col + shift)`.
    j.  Place the current color at the calculated `(new_row, new_col)` position in the output grid.
4.  After processing all unique colors, return the final output grid.
