
## train_1

**input:**
```
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 0 0 0 4 0 0
0 0 0 4 4 4 4 4 0 0
```


**output:**
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 2 2 2 2 2 2 2 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```

Okay, let's analyze the task based on the provided examples.

**Perception**

The input grids contain one or more distinct, closed shapes made of non-white pixels (Red, Yellow, Orange) on a white background. These shapes enclose regions of the white background pixels. The core transformation involves identifying these enclosed white regions and filling them with a new color. The specific color used for filling depends on the color of the shape that encloses the region. Crucially, the rule mapping the enclosing color to the fill color appears to change based on the *total number of distinct non-white colors* present in the shapes within the input grid.

In the first example, there are two distinct shape colors (Red, Yellow). Red shapes enclose areas filled with Green, and Yellow shapes enclose areas filled with Orange.

In the second example, there are three distinct shape colors (Red, Yellow, Orange). Here, Red shapes enclose areas filled with Orange, Yellow shapes enclose areas filled with Green, and Orange shapes enclose areas filled with Green.

This suggests two different color-filling rules, selected based on whether two or three (or more) distinct non-white colors form the shapes in the input grid.

**Facts**


```yaml
elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: background
    properties:
      - color: white (0)
  - type: shape
    description: A contiguous block of non-white pixels.
    properties:
      - color: [red (2), yellow (4), orange (7), ...]
      - connectivity: Assumed 8-way adjacency for shape pixels.
  - type: enclosed_region
    description: A contiguous region of white (0) pixels that does not touch the grid border and is entirely surrounded by pixels of a single shape/color.
    properties:
      - color: white (0)
      - connectivity: Assumed 8-way adjacency for region pixels.
      - status: enclosed (boolean)
      - enclosing_color: The color of the single shape surrounding the region.
      - border_touching: (boolean) True if any pixel is on the grid edge.

grid_properties:
  - name: distinct_shape_colors
    description: The set of unique non-white colors present in the shapes of the input grid.
  - name: num_distinct_shape_colors
    description: The count of unique non-white colors.

transformation:
  - action: identify_shapes
    description: Locate all contiguous non-white shapes.
  - action: count_distinct_colors
    description: Determine the number of unique colors used in the identified shapes.
  - action: identify_white_regions
    description: Locate all contiguous white (0) regions.
  - action: check_enclosure
    description: For each white region, determine if it is enclosed.
    criteria:
      - Must not touch the grid border.
      - All adjacent (8-way) non-white pixels must belong to a single shape and have the same color.
  - action: determine_enclosing_color
    description: Identify the color of the shape enclosing a white region.
  - action: apply_fill_rule
    description: Select a fill color based on the enclosing color and the total number of distinct shape colors in the grid.
    rules:
      - condition: num_distinct_shape_colors <= 2
        mapping:
          - input_color: red (2)
            output_color: green (3)
          - input_color: yellow (4)
            output_color: orange (7)
          # Add other colors if observed in more examples
      - condition: num_distinct_shape_colors >= 3
        mapping:
          - input_color: red (2)
            output_color: orange (7)
          - input_color: yellow (4)
            output_color: green (3)
          - input_color: orange (7)
            output_color: green (3)
          # Add other colors if observed in more examples
  - action: fill_region
    description: Change the color of the pixels within an enclosed white region to the determined fill color.

output_constraints:
  - The grid dimensions remain unchanged.
  - The original shapes remain unchanged in color and position.
  - Only the enclosed white regions are modified.
  - Background pixels not part of an enclosed region remain white.
```


**Natural Language Program**

1.  **Analyze Input Shapes:** Identify all contiguous shapes formed by non-white pixels in the input grid. Determine the set of unique colors present in these shapes and count how many distinct colors there are (`num_distinct_shape_colors`).
2.  **Identify Candidate Regions:** Find all contiguous regions of white (0) pixels in the input grid.
3.  **Check for Enclosure:** For each white region identified:
    a.  Verify that no pixel in the region lies on the border of the grid.
    b.  Examine all pixels directly adjacent (including diagonals) to the white region.
    c.  Confirm that all adjacent pixels that are *not* white share the exact same single color (`enclosing_color`).
    d.  If both conditions (a and c) are met, the white region is considered "enclosed".
4.  **Determine Fill Rule:** Based on the `num_distinct_shape_colors` calculated in step 1:
    a.  If `num_distinct_shape_colors` is 2 or less, use Rule Set A: Red(2) fills Green(3), Yellow(4) fills Orange(7).
    b.  If `num_distinct_shape_colors` is 3 or more, use Rule Set B: Red(2) fills Orange(7), Yellow(4) fills Green(3), Orange(7) fills Green(3).
5.  **Apply Filling:** Create a copy of the input grid to serve as the output. For every white region identified as "enclosed" in step 3:
    a.  Determine the appropriate `fill_color` using the selected Rule Set (A or B) and the `enclosing_color` found in step 3c.
    b.  Change the color of all pixels within that enclosed region to the determined `fill_color` in the output grid.
6.  **Finalize Output:** Return the modified grid. Pixels that were not part of an enclosed white region retain their original color from the input grid.
