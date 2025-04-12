
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

Okay, let's break down the task based on the provided examples.

## Perception

1.  **Input/Output Structure:** Both input and output are 2D grids of pixels, representing colors. The grid dimensions remain the same between input and output for each example.
2.  **Content:** The grids contain a background color (white, 0) and one or more groups of pixels of other colors (e.g., red, blue, green, yellow). These colored pixels often form distinct shapes or patterns.
3.  **Transformation:** The core transformation involves moving specific groups of colored pixels horizontally.
4.  **Movement Pattern:**
    *   The group of pixels belonging to the color that appears furthest to the left in the input grid is moved to the absolute left edge (column 0) of the output grid.
    *   The group of pixels belonging to the color that appears furthest to the right in the input grid is moved to the absolute right edge (last column) of the output grid.
5.  **Preservation:**
    *   The vertical position of each moved pixel group is preserved.
    *   The internal shape and relative arrangement of pixels within each moved color group are preserved.
    *   Pixels not belonging to the identified leftmost or rightmost color groups are not present in the output; the corresponding areas become background (white).
    *   The background color (white) fills any space not occupied by the moved color groups.

## Facts


```yaml
task_description: Horizontally translate the leftmost color group to the left edge and the rightmost color group to the right edge of the grid.

elements:
  - element: grid
    properties:
      - height: integer (constant within a pair)
      - width: integer (constant within a pair)
      - pixels: 2D array of color values (0-9)
  - element: color_group
    description: All pixels of a specific non-background color in the input grid.
    properties:
      - color: integer (1-9)
      - pixels: list of (row, column) coordinates
      - bounding_box:
          min_row: integer
          max_row: integer
          min_col: integer
          max_col: integer

relationships:
  - type: spatial
    description: Determine the overall leftmost and rightmost extent of non-background pixels.
    properties:
      - min_overall_col: minimum column index containing any non-background pixel
      - max_overall_col: maximum column index containing any non-background pixel
  - type: identity
    description: Identify the color(s) present at the overall minimum and maximum columns.
    properties:
      - leftmost_colors: set of colors present in the min_overall_col
      - rightmost_colors: set of colors present in the max_overall_col

actions:
  - action: create_output_grid
    origin: input grid dimensions
    target: output grid
    properties:
      - dimensions: same as input grid
      - initial_fill: background color (white, 0)
  - action: translate_horizontally
    origin: input grid pixels for specific colors
    target: output grid
    conditions:
      - Applies to colors identified as leftmost_colors.
      - Applies to colors identified as rightmost_colors.
    properties:
      - direction: left (for leftmost_colors), right (for rightmost_colors)
      - destination_edge: column 0 (for leftmost_colors), column width-1 (for rightmost_colors)
      - preservation: maintains vertical position (row index) and relative horizontal positions within the color group.
    details:
      - For each leftmost_color:
          shift = 0 - min_col for that color
          Each pixel (r, c) moves to (r, c + shift)
      - For each rightmost_color:
          shift = (grid_width - 1) - max_col for that color
          Each pixel (r, c) moves to (r, c + shift)

```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with the background color (white, 0).
2.  Identify all distinct non-background colors present in the input grid.
3.  For each distinct non-background color, find all coordinates `(row, column)` where it appears. Group these coordinates by color.
4.  Determine the overall minimum column index (`min_overall_col`) occupied by any non-background pixel across the entire input grid.
5.  Identify the set of colors (`leftmost_colors`) that have at least one pixel located at `min_overall_col`.
6.  Determine the overall maximum column index (`max_overall_col`) occupied by any non-background pixel across the entire input grid.
7.  Identify the set of colors (`rightmost_colors`) that have at least one pixel located at `max_overall_col`.
8.  For each color in the `leftmost_colors` set:
    a.  Find the minimum column index (`min_col_for_this_color`) among all pixels *of this specific color*.
    b.  Calculate the horizontal shift required to move this color group to the left edge: `shift = 0 - min_col_for_this_color`.
    c.  Iterate through all input coordinates `(r, c)` corresponding to this color. Place this color at the coordinate `(r, c + shift)` in the output grid.
9.  For each color in the `rightmost_colors` set:
    a.  Find the maximum column index (`max_col_for_this_color`) among all pixels *of this specific color*.
    b.  Get the width of the grid (`grid_width`).
    c.  Calculate the horizontal shift required to move this color group to the right edge: `shift = (grid_width - 1) - max_col_for_this_color`.
    d.  Iterate through all input coordinates `(r, c)` corresponding to this color. Place this color at the coordinate `(r, c + shift)` in the output grid. (Note: If a color is in both `leftmost_colors` and `rightmost_colors`, its pixels might be written twice, potentially overwriting based on the order of steps 8 and 9, but the final position will depend on the applied shift).
10. Return the completed output grid.
