
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 4 4 4 0 0 0 8
0 0 0 2 2 2 0 0 0 8
0 0 0 3 3 3 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
0 0 0 0 0 0 0 0 0 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 7 8 9 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided task examples.

## Perception

*   **`train_1` Example:**
    *   The input grid contains three horizontal lines (yellow, red, green), each 3 pixels wide, stacked vertically near the center. The background is white.
    *   The output grid is identical to the input, but with the addition of a solid azure vertical line filling the entire rightmost column.
    *   The primary input shapes are horizontal. The added feature is a vertical line on the right border. The color added (azure/8) is not present in the input colors (yellow/4, red/2, green/3).

*   **`train_2` Example:**
    *   The input grid contains a 4x4 block of colors (orange, azure, maroon, blue columns) roughly centered. The background is white.
    *   The output grid is identical to the input, but with the addition of a solid azure horizontal line filling the entire topmost row.
    *   The primary input shapes can be seen as vertical lines of distinct colors adjacent to each other. The added feature is a horizontal line on the top border. The color added (azure/8) *is* present in the input colors.

*   **Comparison & Pattern:**
    *   Both examples involve adding a single, solid-colored line to one of the grid's borders.
    *   The orientation of the added line seems opposite to the orientation of the primary shapes in the input (horizontal input shapes -> vertical output line; vertical input shapes -> horizontal output line).
    *   The position of the added line seems consistent based on the orientation: vertical lines are added to the rightmost column, and horizontal lines are added to the topmost row.
    *   The color of the added line is azure (8) in both cases. In `train_2`, azure is present in the input; in `train_1`, it is not. This suggests the added color might be consistently azure (8), regardless of input colors, but determined by the input shape orientation rule.

## Facts


```yaml
task_description: Add a single line of a specific color to one border of the grid, based on the orientation of shapes within the input grid.

examples:
  train_1:
    input:
      grid_size: [10, 10]
      background_color: white (0)
      objects:
        - shape: horizontal line
          color: yellow (4)
          location: rows=[4], cols=[3, 4, 5]
          size: [1, 3]
        - shape: horizontal line
          color: red (2)
          location: rows=[5], cols=[3, 4, 5]
          size: [1, 3]
        - shape: horizontal line
          color: green (3)
          location: rows=[6], cols=[3, 4, 5]
          size: [1, 3]
      dominant_orientation: horizontal
    output:
      grid_size: [10, 10]
      base_grid: same as input
      added_feature:
        shape: vertical line
        color: azure (8)
        location: rows=[0-9], cols=[9] (rightmost column)
        size: [10, 1]
      relationship: Added vertical line on the right border because input shapes were horizontal. Color is azure (8).

  train_2:
    input:
      grid_size: [10, 10]
      background_color: white (0)
      objects: # Can be viewed as a block or individual columns
        - shape: vertical line
          color: orange (7)
          location: rows=[3, 4, 5, 6], cols=[2]
          size: [4, 1]
        - shape: vertical line
          color: azure (8)
          location: rows=[3, 4, 5, 6], cols=[3]
          size: [4, 1]
        - shape: vertical line
          color: maroon (9)
          location: rows=[3, 4, 5, 6], cols=[4]
          size: [4, 1]
        - shape: vertical line
          color: blue (1)
          location: rows=[3, 4, 5, 6], cols=[5]
          size: [4, 1]
      dominant_orientation: vertical # Based on constituent lines
    output:
      grid_size: [10, 10]
      base_grid: same as input
      added_feature:
        shape: horizontal line
        color: azure (8)
        location: rows=[0], cols=[0-9] (topmost row)
        size: [1, 10]
      relationship: Added horizontal line on the top border because input shapes were vertical. Color is azure (8).

derived_rules:
  - rule: Determine the dominant orientation of non-background objects/shapes in the input grid.
    details: Check if connected non-background pixels form shapes that are wider than tall (horizontal) or taller than wide (vertical).
  - rule: If the dominant orientation is horizontal, add a vertical line of azure (8) color to the rightmost column of the grid.
  - rule: If the dominant orientation is vertical, add a horizontal line of azure (8) color to the topmost row of the grid.
  - rule: If orientation is ambiguous (e.g., square shapes), assume a default or apply tie-breaking (example suggests vertical takes precedence if components are vertical). The examples provided have clear or component-based orientation.
  - rule: The added color is always azure (8).
```


## Natural Language Program

1.  Analyze the input grid to identify all connected shapes formed by non-white pixels.
2.  Determine the primary orientation of these shapes:
    *   Calculate the width and height of the bounding box for each distinct non-white shape.
    *   If the shapes are predominantly wider than tall (sum of widths > sum of heights, or average width > average height), classify the dominant orientation as "horizontal".
    *   If the shapes are predominantly taller than wide, classify the dominant orientation as "vertical". (Consider constituent parts if a shape is complex, like the block in train_2 being composed of vertical lines). If shapes are square (width == height), potentially default to "vertical" based on `train_2`.
3.  Create the output grid by copying the input grid.
4.  Based on the determined dominant orientation:
    *   If "horizontal", fill the entire rightmost column of the output grid with azure (8).
    *   If "vertical", fill the entire topmost row of the output grid with azure (8).
5.  Return the modified grid.
