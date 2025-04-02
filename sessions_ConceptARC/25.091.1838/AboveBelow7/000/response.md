Okay, let's break down the task based on the examples provided.

## Perception

1.  **Input Structure:** The input grids contain distinct shapes made of non-white pixels set against a white background.
2.  **Objects:** In `train_1`, we see two distinct objects: a yellow horizontal line and a green hollow rectangle below it. In `train_2`, we see a complex red shape and multiple disconnected azure shapes located above the red shape. It appears that objects are grouped by color.
3.  **Color Grouping:** All pixels of the same non-white color seem to act as a single unit or group, even if they form disconnected shapes (like the azure pixels in `train_2`).
4.  **Transformation:** The core transformation appears to be a vertical rearrangement of these color groups. In `train_1`, the yellow group (line) and the green group (rectangle) swap their vertical positions. In `train_2`, the azure group (all azure pixels collectively) and the red group swap their vertical positions.
5.  **Spacing:** The relative vertical spacing *between* the bounding boxes of the color groups seems to be preserved during the swap. For instance, in `train_1`, the yellow line is directly above the green rectangle (0 rows gap), and in the output, the green rectangle is directly above the yellow line (0 rows gap). Similarly, in `train_2`, the lowest azure pixel is directly above the highest red pixel, and in the output, the lowest red pixel is directly above the highest azure pixel.
6.  **Internal Structure:** The internal structure and relative positions of pixels within each color group remain unchanged.
7.  **Horizontal Position:** The horizontal position of each color group appears unchanged relative to the grid boundaries.

## Facts


```yaml
task_type: object_manipulation

elements:
  - role: background
    properties:
      color: white
      value: 0
  - role: color_group
    description: A collection of all pixels sharing the same non-background color. Acts as a single unit for transformation.
    properties:
      color: any non-white color (e.g., yellow, green, red, azure)
      value: 1-9
      shape: Can be contiguous or non-contiguous, simple or complex.
      vertical_extent: Defined by the minimum and maximum row indices occupied by pixels of this color.
      horizontal_extent: Defined by the minimum and maximum column indices occupied by pixels of this color.

relationships:
  - type: vertical_ordering
    description: Color groups are ordered vertically based on their topmost pixel row index.
    between: [color_group, color_group]
  - type: vertical_spacing
    description: The number of background rows separating the bounding boxes of vertically adjacent color groups.
    between: [color_group, color_group]

actions:
  - name: identify_color_groups
    input: input_grid
    output: list of color_groups with their properties (pixels, color, vertical_extent)
  - name: determine_vertical_order
    input: list of color_groups
    output: ordered list of color_groups (top to bottom)
  - name: reverse_vertical_order
    input: ordered list of color_groups
    output: list of color_groups in reversed vertical order
  - name: calculate_vertical_shifts
    input: original_order, reversed_order, original_vertical_spacing
    output: vertical shift amount for each color_group
    description: Calculates how many rows each group needs to move up or down to achieve the reversed order while preserving inter-group spacing.
  - name: apply_shifts
    input: input_grid, color_groups, vertical_shifts
    output: output_grid
    description: Creates the output grid by moving pixels of each color group according to the calculated vertical shift.

goal: Reverse the vertical order of the distinct color groups found in the input grid, preserving their internal structure, horizontal positions, and the vertical spacing between them.
```


## Natural Language Program

1.  Identify all unique non-background colors present in the input grid.
2.  For each unique non-background color, determine the set of all pixel coordinates belonging to that color. Treat this set as a single "color group".
3.  For each color group, calculate its vertical bounding box by finding the minimum and maximum row indices occupied by its pixels.
4.  Determine the initial vertical order of the color groups based on their minimum row indices (topmost group first).
5.  Calculate the vertical gaps (number of rows) between the bounding boxes of consecutive groups in the initial order.
6.  Determine the target vertical order by reversing the initial order of the color groups.
7.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
8.  Iterate through the color groups in their target vertical order (which is the reversed order). For each group:
    a.  Calculate the target top row for the current group. This will be the row immediately below the bottom row of the previously placed group (or row 0 if it's the first group being placed), plus the original vertical gap that existed *above* this group in the *initial* ordering.
    b.  Calculate the vertical shift required for this group: `shift = target_top_row - original_min_row`.
    c.  For every pixel belonging to the current color group in the input grid, place its color into the output grid at `(original_row + shift, original_column)`.
9.  Return the completed output grid.