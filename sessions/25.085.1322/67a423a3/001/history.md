
## train_1

**input:**
```
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
8 8 8 8 6 8 8 8
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
```


**output:**
```
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
0 0 0 4 4 4 0 0
8 8 8 4 6 4 8 8
0 0 0 4 4 4 0 0
0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0
```


## train_2

**input:**
```
0 3 0 0
2 2 2 2
0 3 0 0
0 3 0 0
```


**output:**
```
4 4 4 0
4 2 4 2
4 4 4 0
0 3 0 0
```


## train_3

**input:**
```
0 0 1 0 0 0
0 0 1 0 0 0
9 9 1 9 9 9
0 0 1 0 0 0
0 0 1 0 0 0
0 0 1 0 0 0
```


**output:**
```
0 0 1 0 0 0
0 4 4 4 0 0
9 4 1 4 9 9
0 4 4 4 0 0
0 0 1 0 0 0
0 0 1 0 0 0
```

Okay, let's break down this task.

## Perception

1.  **Input Structure:** Each input grid contains exactly one continuous horizontal line and one continuous vertical line (or vertically aligned elements that clearly define a column) of solid, non-white colors. The rest of the grid is typically white (0).
2.  **Output Structure:** The output grid is largely identical to the input grid, except for modifications within a 3x3 area.
3.  **Intersection:** The horizontal and vertical lines intersect at a single point in each example.
4.  **Modification Area:** A 3x3 square area centered on the intersection point is the focus of the transformation.
5.  **Core Transformation:** The primary change is filling the 3x3 area with yellow (4).
6.  **Conditional Preservation:** Some pixels within the 3x3 area retain their original colors from the input grid, overriding the yellow fill. This preservation depends on:
    *   The position of the pixel relative to the intersection center (center, horizontal neighbor, vertical neighbor, corner).
    *   The specific colors of the original horizontal and vertical lines.
7.  **Specific Color Rules:**
    *   The center pixel `(r, c)` retains its original input color *unless* the vertical line's color is green (3). If the vertical line is green, the center becomes yellow.
    *   The horizontal neighbors `(r, c-1)` and `(r, c+1)` retain their original input colors *unless* the horizontal line's color is azure (8). If the horizontal line is azure, these neighbors become yellow.
    *   The vertical neighbors `(r-1, c)` and `(r+1, c)` and the corner pixels within the 3x3 area always become yellow (or stay yellow if filled).

## Facts


```yaml
task_description: Modifies a 3x3 area around the intersection of a horizontal and a vertical line based on the specific colors of those lines.

elements:
  - object: horizontal_line
    description: A continuous horizontal line of a single non-white color.
    properties:
      - color: color_h (The color of the horizontal line, e.g., 8, 2, 9)
      - row_index: r (The row index of the horizontal line)
  - object: vertical_line
    description: A continuous vertical line (or distinct vertical elements in a single column) of a single non-white color.
    properties:
      - color: color_v (The color of the vertical line, e.g., 6, 3, 1)
      - column_index: c (The column index of the vertical line)
  - object: intersection
    description: The single pixel where the conceptual horizontal and vertical lines cross.
    properties:
      - coordinates: (r, c)
  - object: modification_area
    description: A 3x3 square grid region centered at the intersection point (r, c).
  - object: fill_color
    description: The primary color used to modify the area.
    properties:
      - color_value: 4
      - color_name: yellow

transformation_logic:
  - step: Identify Lines and Intersection
    details: Find the horizontal line (color `color_h`, row `r`) and vertical line (color `color_v`, column `c`). The intersection is at `(r, c)`.
  - step: Initialize Output
    details: Create the output grid as a direct copy of the input grid.
  - step: Fill Area Yellow
    details: Iterate through all coordinates `(i, j)` within the 3x3 square centered at `(r, c)`. If `(i, j)` is within the grid bounds, set `output[i, j]` to yellow (4).
  - step: Conditional Restoration (Center)
    details: Check the vertical line color `color_v`. If `color_v` is NOT green (3), restore the pixel at the intersection `(r, c)` in the output grid to its original color from the input grid (`input[r, c]`).
  - step: Conditional Restoration (Horizontal Neighbors)
    details: Check the horizontal line color `color_h`. If `color_h` is NOT azure (8), restore the pixels at the horizontal neighbors `(r, c-1)` and `(r, c+1)` in the output grid to their original colors from the input grid (`input[r, c-1]` and `input[r, c+1]`, respectively), provided these coordinates are within the grid bounds.

assumptions:
  - Each input grid contains exactly one discernible horizontal line and one vertical line/structure made of non-background colors.
  - These lines intersect at exactly one point.
  - The 3x3 modification area calculation respects grid boundaries.
```


## Natural Language Program

1.  **Identify Lines:** Scan the input grid to find the row index (`r`) and color (`color_h`) of the unique horizontal line, and the column index (`c`) and color (`color_v`) of the unique vertical line (or distinct vertical structure).
2.  **Copy Grid:** Create a new grid (`output_grid`) identical to the `input_grid`.
3.  **Fill 3x3 Area:** Define the 3x3 area centered at coordinates `(r, c)`. For each pixel `(i, j)` within this 3x3 area (from `r-1` to `r+1` and `c-1` to `c+1`), if `(i, j)` is within the grid's boundaries, set the color of `output_grid[i, j]` to yellow (4).
4.  **Check Center Pixel:** Examine the vertical line's color, `color_v`. If `color_v` is not equal to green (3), then set the color of the center pixel `output_grid[r, c]` back to its original value from `input_grid[r, c]`.
5.  **Check Horizontal Neighbors:** Examine the horizontal line's color, `color_h`. If `color_h` is not equal to azure (8), then:
    *   If the coordinate `(r, c-1)` is within the grid boundaries, set `output_grid[r, c-1]` back to its original value from `input_grid[r, c-1]`.
    *   If the coordinate `(r, c+1)` is within the grid boundaries, set `output_grid[r, c+1]` back to its original value from `input_grid[r, c+1]`.
6.  **Return Result:** The final `output_grid` is the result of the transformation.
