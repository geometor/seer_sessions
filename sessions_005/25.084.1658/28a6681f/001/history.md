
## train_1

**input:**
```
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 3 0 3 1 1
0 0 0 0 0 3 0 3 1 1
0 0 0 0 2 3 0 3 1 1
0 0 0 0 2 3 0 3 1 1
0 2 2 2 2 3 3 3 1 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 0 0 3 1 1
0 0 0 0 0 3 1 3 1 1
0 0 0 0 0 3 1 3 1 1
0 0 0 0 2 3 1 3 1 1
0 0 0 0 2 3 1 3 1 1
0 2 2 2 2 3 3 3 1 1
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 1
0 0 3 0 0 0 0 1 1 1
0 0 3 0 0 0 0 1 1 1
0 0 3 0 0 0 1 1 1 1
0 0 3 0 0 3 1 1 1 1
0 0 3 0 0 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 3 3 3 5 5 5 5
```


**output:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 1 1 1 1 1 1 1
0 0 3 1 1 3 1 1 1 1
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 1 1 3 5 1 1 5
0 0 3 3 3 3 5 5 5 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
9 9 1 1 0 0 0 0 9 9
0 9 9 1 0 0 0 9 9 0
0 0 9 9 0 0 0 9 0 0
0 0 0 9 0 0 9 9 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 4 0 0 0 0
2 0 0 4 0 4 0 0 0 0
2 0 2 4 0 4 0 0 0 0
2 2 2 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
9 9 0 0 0 0 0 0 9 9
0 9 9 0 0 0 0 9 9 0
0 0 9 9 0 0 0 9 0 0
0 0 0 9 0 0 9 9 0 0
0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 4 0 0 0 0
2 0 0 4 1 4 0 0 0 0
2 1 2 4 1 4 0 0 0 0
2 2 2 4 4 4 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception**

1.  **Grid Structure:** The task operates on grids of colored pixels. The input and output grids have the same dimensions in all examples.
2.  **Color Palette:** The primary colors involved are `white` (0), `blue` (1), `red` (2), `green` (3), `yellow` (4), `gray` (5), `maroon` (9). Notably, `blue` (1) is the color used for the transformation output, while `white` (0) is the color being transformed. Other colors act as context or boundaries.
3.  **Transformation Focus:** The core transformation involves changing specific `white` (0) pixels to `blue` (1). All other pixels retain their original color from the input.
4.  **Spatial Relationship:** The change from `white` to `blue` depends on the horizontal neighbors of the `white` pixels. Specifically, `white` pixels that are horizontally "sandwiched" between non-`white` pixels within the same row are affected.
5.  **Horizontal Gaps:** The transformation identifies horizontal sequences (segments) of one or more `white` pixels. If such a sequence has a non-`white` pixel immediately to its left and a non-`white` pixel immediately to its right (both within the same row), the entire sequence of `white` pixels is filled with `blue` (1).
6.  **Consistency:** This pattern holds across all three training examples. The specific colors of the bounding non-`white` pixels do not matter, only that they are not `white` (0). The length of the `white` segment can be one or more pixels.

**Facts**


```yaml
task_elements:
  - type: grid
    properties:
      - dimensions: height and width (constant between input and output)
      - cells: pixels with color values (0-9)
  - type: pixel
    properties:
      - color: integer value 0-9
      - position: row and column index
      - role:
        - background: white (0)
        - fill_color: blue (1)
        - boundary_color: any non-white color (1-9)

transformation:
  - type: color_change
    input_color: white (0)
    output_color: blue (1)
    condition:
      - type: spatial_relationship
        scope: horizontal (within the same row)
        description: >
          A pixel changes color if it is white (0) AND it belongs to a
          contiguous horizontal sequence of one or more white (0) pixels
          that is immediately bounded on the left by a non-white (1-9) pixel
          AND immediately bounded on the right by a non-white (1-9) pixel.
      - type: completeness
        description: All pixels within the identified white sequence are changed.

invariance:
  - type: pixel_color
    description: >
      Pixels that are not white (0) in the input remain unchanged in the output.
  - type: pixel_color
    description: >
      White (0) pixels that do not meet the boundary condition remain unchanged.
  - type: grid_property
    description: Grid dimensions remain unchanged.

relationships:
  - type: adjacency
    direction: horizontal (left and right neighbors in the same row)
    relevance: >
      Crucial for determining which white (0) pixels are transformed.
      Only immediate left/right neighbors of a white segment matter.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the grid, from top to bottom.
3.  For the current row, scan from left to right to identify contiguous horizontal segments composed entirely of `white` (0) pixels.
4.  For each identified `white` segment:
    a.  Determine the column index of the pixel immediately to the left of the segment's start.
    b.  Determine the column index of the pixel immediately to the right of the segment's end.
    c.  Check if both these left and right bounding positions are within the grid's width boundaries.
    d.  If both positions are within bounds, check the color of the pixels at these bounding positions in the *input* grid.
    e.  If *both* the left bounding pixel and the right bounding pixel are non-`white` (have a color value from 1 to 9), then change the color of all pixels *within* the identified `white` segment in the *output* grid to `blue` (1).
5.  After iterating through all rows, the modified output grid is the result.
