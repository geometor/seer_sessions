
## train_1

**input:**
```
0 2 0 1 0 0 0 0 0 0
0 0 0 0 0 2 0 1 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 2 0 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 1 0 0 0 1 0 0
0 2 0 0 0 2 0 1 0 0
0 2 0 0 0 2 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 2 0 0 0 0 2 0 0 2
0 2 0 0 0 0 2 0 0 2
0 0 0 0 1 0 2 0 0 0
0 0 0 0 1 0 2 0 0 0
0 0 1 0 1 0 2 0 1 0
0 0 1 0 1 0 0 0 1 0
```


## train_2

**input:**
```
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 2 0 0 1 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 1 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0
0 2 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 2
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 1 0 0 0 2 0 0 1 0
0 1 0 0 0 0 0 0 1 0
```

Okay, let's analyze the provided example pair (train_2).

**Perception:**

1.  **Grid Structure:** Both input and output grids are 10x10.
2.  **Key Feature:** A solid horizontal gray line (color 5) exists in row index 5 (the 6th row) in both input and output. This line divides the grid into an upper region (rows 0-4) and a lower region (rows 6-9).
3.  **Objects:** The primary objects are individual pixels of blue (color 1) and red (color 2) scattered on a white background (color 0), distinct from the gray line.
4.  **Transformation:** The transformation involves adding new pixels of the same color (blue or red) vertically, creating vertical lines originating from the initial colored pixels.
5.  **Color-Specific Behavior:**
    *   **Red Pixels:** Appear to extend vertically *towards* the central gray line. If a red pixel is above the gray line, it fills downwards until the row just above the gray line. If it's below the gray line, it fills upwards until the row just below the gray line. The original red pixel remains.
    *   **Blue Pixels:** Appear to extend vertically *towards* the nearest horizontal edge of the grid (top edge - row 0, or bottom edge - row 9). If a blue pixel is closer to the top edge, it fills upwards to row 0. If it's closer to the bottom edge, it fills downwards to row 9. The original blue pixel remains.
6.  **Static Elements:** The white background pixels and the gray line remain unchanged.

**YAML Facts:**


```yaml
task_context:
  grid_dimensions: 10x10
  static_elements:
    - type: line
      color: gray
      orientation: horizontal
      location: row_index 5
    - type: background
      color: white
  dynamic_objects:
    - type: pixel
      color: red
    - type: pixel
      color: blue
rules:
  - description: Apply transformation to each non-gray, non-white pixel individually.
  - action: create_vertical_path
    target_objects:
      - color: red
      - color: blue
    details:
      - condition: object_color is red
        target_destination: adjacent_row_to_gray_line
        path_filling: Fill empty cells (white) in the same column between the object's initial row and the target row (exclusive of gray line row) with red color.
        direction: towards_gray_line (downwards if above, upwards if below)
        keep_original: true
      - condition: object_color is blue
        target_destination: nearest_horizontal_grid_boundary (row 0 or row 9)
        path_filling: Fill empty cells (white) in the same column between the object's initial row and the target row (inclusive) with blue color.
        direction: towards_nearest_boundary (upwards for top, downwards for bottom)
        keep_original: true

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the row index of the horizontal gray line.
3.  Iterate through each cell (pixel) of the input grid.
4.  If a cell contains a red pixel:
    a.  Determine its row (`r`) and column (`c`).
    b.  If the red pixel's row `r` is above the gray line's row (`gray_row`), fill all cells from row `r` down to row `gray_row - 1` in column `c` of the output grid with red.
    c.  If the red pixel's row `r` is below the gray line's row (`gray_row`), fill all cells from row `r` up to row `gray_row + 1` in column `c` of the output grid with red.
5.  If a cell contains a blue pixel:
    a.  Determine its row (`r`) and column (`c`).
    b.  Find the grid height (`H`).
    c.  Determine the distance to the top edge (`r`) and the bottom edge (`H - 1 - r`).
    d.  If the distance to the top edge is less than or equal to the distance to the bottom edge, fill all cells from row 0 up to row `r` in column `c` of the output grid with blue.
    e.  Otherwise (if closer to the bottom edge), fill all cells from row `r` down to row `H - 1` in column `c` of the output grid with blue.
6.  Leave all gray and white pixels unchanged from the input grid (this is implicitly handled by initializing the output as a copy and only modifying based on red/blue pixels).
7.  Return the modified output grid.
