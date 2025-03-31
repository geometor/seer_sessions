
## train_1

**input:**
```
7 7 7 7 7 7 7 7 1 7 2 7 7 9 7
7 7 7 7 7 7 7 7 1 7 4 7 9 7 7
7 7 7 7 7 7 7 7 1 3 7 7 7 7 7
7 7 7 7 7 7 7 7 1 7 7 4 7 7 5
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
7 7 7 7 7 7 7 7 1 7 7 7 7 7 7
7 7 7 7 7 7 7 7 1 7 7 7 7 7 7
7 7 7 7 7 7 7 7 1 7 7 7 7 7 7
7 7 7 7 7 7 7 7 1 7 7 7 7 7 7
7 7 7 7 7 7 7 7 1 7 7 7 7 7 7
```


**output:**
```
7 7 7 9 7 7 2 7 1 7 2 7 7 9 7
7 7 7 7 9 7 4 7 1 7 4 7 9 7 7
7 7 7 7 7 7 7 3 1 3 7 7 7 7 7
7 7 5 7 7 4 7 7 1 7 7 4 7 7 5
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
7 7 5 7 7 4 7 7 1 7 7 4 7 7 5
7 7 7 7 7 7 7 3 1 3 7 7 7 7 7
7 7 7 7 9 7 4 7 1 7 4 7 9 7 7
7 7 7 9 7 7 2 7 1 7 2 7 7 9 7
7 7 7 7 7 7 7 7 1 7 7 7 7 7 7
```


## train_2

**input:**
```
1 7 7 7 6 7 7 7 7 7 7
2 2 7 7 6 7 7 7 7 7 7
0 4 7 7 6 7 7 7 7 7 7
7 4 7 7 6 7 7 7 7 7 7
7 8 7 7 6 7 7 7 7 7 7
6 6 6 6 6 6 6 6 6 6 6
7 7 7 7 6 7 7 7 7 7 7
7 7 7 7 6 7 7 7 7 7 7
7 7 7 7 6 7 7 7 7 7 7
7 7 7 7 6 7 7 7 7 7 7
7 7 7 7 6 7 7 7 7 7 7
```


**output:**
```
1 7 7 7 6 7 7 7 1 7 7
2 2 7 7 6 7 7 2 2 7 7
0 4 7 7 6 7 7 4 0 7 7
7 4 7 7 6 7 7 4 7 7 7
7 8 7 7 6 7 7 8 7 7 7
6 6 6 6 6 6 6 6 6 6 6
7 8 7 7 6 7 7 8 7 7 7
7 4 7 7 6 7 7 4 7 7 7
0 4 7 7 6 7 7 4 0 7 7
2 2 7 7 6 7 7 2 2 7 7
1 7 7 7 6 7 7 7 1 7 7
```


## train_3

**input:**
```
7 7 7 3 8 0 7 1
7 7 7 3 7 7 6 7
7 7 7 3 0 2 7 0
7 7 7 3 7 7 7 7
3 3 3 3 3 3 3 3
7 7 7 3 7 7 7 7
7 7 7 3 7 7 7 7
7 7 7 3 7 7 7 7
```


**output:**
```
7 0 8 3 8 0 7 1
6 7 7 3 7 7 6 7
7 2 0 3 0 2 7 0
7 7 7 3 7 7 7 7
3 3 3 3 3 3 3 3
7 7 7 3 7 7 7 7
7 2 0 3 0 2 7 0
6 7 7 3 7 7 6 7
```

*   **Perception:**
    *   Each input grid contains a background color (orange - 7 in all examples).
    *   There are two lines (one horizontal, one vertical) of the same, non-background color, which intersect. This color differs between examples (blue-1, magenta-6, green-3). These lines act as axes of reflection.
    *   In the input, non-background, non-axis colored pixels ("content pixels") are predominantly located in one of the four quadrants defined by the intersection of the axis lines.
    *   The output grid retains the original axis lines and the content pixels in their original quadrant.
    *   The output grid is completed by reflecting the content pixels from the original quadrant into the other three quadrants, using the axis lines as mirrors. The background color is ignored during reflection (i.e., reflected pixels overwrite the background color, but background color pixels do not overwrite existing content pixels in other quadrants if reflection were done naively).

*   **YAML Facts:**
    
```yaml
    task_description: Reflect content from one quadrant into the other three across intersecting axis lines.
    
    elements:
      - object: grid
        description: A 2D array of colored pixels.
      - object: background_pixel
        property:
          color: orange (7) in examples, but likely the most frequent color overall excluding axis lines.
          role: Fills empty space.
      - object: axis_lines
        property:
          color: Varies per example (blue-1, magenta-6, green-3), but consistent within an example for both horizontal and vertical lines.
          shape: One horizontal line and one vertical line intersecting within the grid.
          role: Define the center and axes for reflection.
      - object: content_pixels
        property:
          color: Any color other than the background and axis colors.
          location: Primarily located in one quadrant defined by the axis lines in the input.
          role: The pattern to be reflected.
      - object: source_quadrant
        property:
          location: The quadrant containing the content_pixels in the input grid.
          relationship: Defined relative to the intersection of the axis_lines.
      - object: target_quadrants
        property:
          location: The three quadrants other than the source_quadrant.
          relationship: Defined relative to the intersection of the axis_lines.
    
    transformation:
      - action: identify_background_color
        description: Determine the most frequent color (likely background).
      - action: identify_axis_lines
        description: Find the single horizontal and single vertical lines composed of the same, non-background color. Determine their intersection point and axis color.
      - action: identify_source_quadrant
        description: Locate the quadrant (relative to the axis intersection) containing the majority of non-background, non-axis pixels in the input.
      - action: reflect_content
        description: Copy the pattern of content_pixels from the source_quadrant into the other three quadrants by reflecting across the axis_lines.
        details:
          - Reflect horizontally across the vertical axis line.
          - Reflect vertically across the horizontal axis line.
          - Reflect diagonally (or sequentially horizontally then vertically) across the intersection point.
        constraints:
          - Only reflect content_pixels (ignore background and axis colors when sourcing the pattern).
          - Reflected pixels overwrite the background color in the target quadrants.
          - The original axis lines and the source quadrant content remain unchanged.
      - output: The grid containing the original axis lines, the original source quadrant content, and the reflected content in the other three quadrants.
    ```


*   **Natural Language Program:**
    1.  Identify the background color (typically the most frequent color).
    2.  Identify the color that forms both a single continuous horizontal line and a single continuous vertical line within the grid; this is the 'axis color', and the lines are the 'axis lines'. Determine the row index of the horizontal axis line and the column index of the vertical axis line. Their intersection point defines the center.
    3.  Define the four quadrants of the grid based on the axis lines.
    4.  Identify the 'source quadrant' in the input grid, which is the quadrant containing pixels that are neither the background color nor the axis color ('content pixels'). Assume there is only one such source quadrant.
    5.  Create the output grid, initially identical to the input grid.
    6.  For each content pixel located at `(row, col)` within the source quadrant:
        a.  Calculate the horizontally reflected position across the vertical axis line. Place the content pixel's color at this reflected position in the output grid.
        b.  Calculate the vertically reflected position across the horizontal axis line. Place the content pixel's color at this reflected position in the output grid.
        c.  Calculate the diagonally reflected position (across both axes). Place the content pixel's color at this reflected position in the output grid.
    7.  Ensure the original axis lines and the content pixels within the source quadrant remain unchanged in the output grid. The reflections should only overwrite the background color in the target quadrants.
