
## train_1

**input:**
```
0 0 0 0 0 0
1 1 1 1 1 0
0 0 0 0 0 0
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0
1 1 1 1 1 0
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


## train_2

**input:**
```
0 6 0 0 0 0
0 6 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 3 3 3 3 0
0 0 0 0 0 0
```


**output:**
```
0 6 0 0 0 0
0 6 0 0 0 0
0 6 0 0 0 0
0 6 0 0 0 0
3 3 3 3 3 0
0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 0 0
0 0 0 0 7 7
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 7 7
0 0 0 0 0 0
```


## train_4

**input:**
```
0 8 0 0 0 0
0 8 0 9 9 9
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0
0 8 9 9 9 9
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception of Elements

1.  **Grid Structure:** The inputs and outputs are 2D grids of colored pixels (represented by integers 0-9). White (0) acts as the background.
2.  **Objects:** In each input grid, there are exactly two distinct non-white objects. These objects always appear to be straight lines, either perfectly horizontal or perfectly vertical. One line is always horizontal, and the other is always vertical.
3.  **Colors:** The lines have specific colors (blue, red, magenta, green, yellow, orange, azure, maroon) that are preserved from input to output.
4.  **Transformation:** The core transformation involves one of the two lines extending its length. The other line remains unchanged.
5.  **Extension Direction:** Vertical lines, when they extend, always extend downwards. Horizontal lines, when they extend, always extend rightwards.
6.  **Extension Trigger & Length:** The key is determining *which* line extends and by *how much*.
    *   It appears the horizontal line extends only if it is located entirely to the right of the vertical line (Example 4). In this case, it extends by one pixel to the right.
    *   In all other cases (horizontal line is left of, intersects, or touches the vertical line), the vertical line extends downwards.
    *   The length of the vertical extension depends on its position relative to the horizontal line:
        *   If the vertical line is entirely above the horizontal line, it extends downwards until it reaches the row immediately preceding the horizontal line's row (Examples 2 & 3).
        *   If the vertical line intersects, touches, or is entirely below the horizontal line, it extends downwards by exactly one pixel (Example 1).

## YAML Facts


```yaml
task_description: Identify a single vertical line and a single horizontal line in the input grid, then extend one of them based on their relative positions.

grid_properties:
  - background_color: white (0)
  - dimensions: variable (e.g., 6x6 in examples)

objects:
  - name: vertical_line
    count: 1
    properties:
      - shape: vertical line segment
      - color: non-white (variable, e.g., red, magenta, yellow, azure)
      - location: defined by a single column index and a range of row indices
  - name: horizontal_line
    count: 1
    properties:
      - shape: horizontal line segment
      - color: non-white (variable, different from vertical_line, e.g., blue, green, orange, maroon)
      - location: defined by a single row index and a range of column indices

relationships_and_actions:
  - relationship: relative_position
    between: [vertical_line, horizontal_line]
    types:
      - horizontal_line is entirely to the right of vertical_line column
      - horizontal_line is not entirely to the right (left of, intersects, touches)
      - vertical_line is entirely above horizontal_line row
      - vertical_line intersects, touches, or is below horizontal_line row
  - action: extend_line
    target: EITHER vertical_line OR horizontal_line (mutually exclusive)
    conditions_and_rules:
      - condition: horizontal_line is entirely to the right of vertical_line
        action_details:
          - target: horizontal_line
          - direction: rightwards
          - length: 1 pixel
      - condition: horizontal_line is NOT entirely to the right of vertical_line
        action_details:
          - target: vertical_line
          - direction: downwards
          - length:
              - if vertical_line is entirely above horizontal_line: extend until the row just before horizontal_line's row
              - otherwise: extend by 1 pixel

output_specification: A grid identical to the input, except for the extension applied to the selected line according to the rules. The color of the extended portion matches the color of the line being extended.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all contiguous non-white pixels belonging to the vertical line object. Record its color, its single column index (`C_v`), and its minimum and maximum row indices (`R_v_min`, `R_v_max`).
3.  Identify all contiguous non-white pixels belonging to the horizontal line object. Record its color, its single row index (`R_h`), and its minimum and maximum column indices (`C_h_min`, `C_h_max`).
4.  Check if the horizontal line is entirely to the right of the vertical line by comparing `C_h_min` and `C_v`.
5.  **If `C_h_min` is greater than `C_v`:**
    *   Determine the coordinates of the new pixel to add: (`R_h`, `C_h_max + 1`).
    *   Set the color of this pixel in the output grid to the color of the horizontal line.
6.  **Else (if `C_h_min` is less than or equal to `C_v`):**
    *   Check if the vertical line is entirely above the horizontal line by comparing `R_v_max` and `R_h`.
    *   **If `R_v_max` is less than `R_h`:**
        *   Iterate through the rows from `R_v_max + 1` up to `R_h - 1`.
        *   For each row `r` in this range, set the color of the pixel at (`r`, `C_v`) in the output grid to the color of the vertical line.
    *   **Else (if `R_v_max` is greater than or equal to `R_h`):**
        *   Determine the coordinates of the new pixel to add: (`R_v_max + 1`, `C_v`).
        *   Set the color of this pixel in the output grid to the color of the vertical line.
7.  Return the modified output grid.
