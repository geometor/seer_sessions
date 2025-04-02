Okay, I will analyze the provided examples and generate the requested deliverables.

## Perception

1.  **Input/Output Structure:** Both inputs and outputs are 2D grids of pixels with integer values representing colors. The grid dimensions can vary.
2.  **Background:** The background color in both examples is white (0).
3.  **Objects:** Each input grid contains a single, solid-colored rectangular object.
    *   Example 1: A 3x3 green (3) square.
    *   Example 2: A 6x5 red (2) rectangle (taller than wide).
4.  **Transformation:** The transformation involves adding a line of pixels extending from the original object to one edge of the grid. The original object remains unchanged in the output.
5.  **Line Color:** The added line uses the same color as the object in the input grid.
6.  **Line Direction and Placement:**
    *   In Example 1 (square object, 3x3), a *horizontal* line is added. It starts one pixel to the right of the object's right edge and extends all the way to the right edge of the grid. It is placed in the *middle row* of the original object (row index 2).
    *   In Example 2 (tall rectangle, 6x5), a *vertical* line is added. It starts one pixel below the object's bottom edge and extends all the way to the bottom edge of the grid. It is placed in the *middle column* of the original object (column index 3).
7.  **Rule Inference:** The direction of the added line appears to depend on the aspect ratio of the input object.
    *   If the object's width is greater than or equal to its height (like the square in Ex 1), the line is horizontal, extending rightwards from the middle row.
    *   If the object's height is greater than its width (like the tall rectangle in Ex 2), the line is vertical, extending downwards from the middle column.
8.  **Position Calculation:** The "middle" row/column seems to be calculated using integer division (e.g., for height 3, middle row index is `1 + 3 // 2 = 2`; for width 5, middle column index is `1 + 5 // 2 = 3`).

## Facts


```yaml
Task: Add a line extending from a central point of an existing object to a grid edge.

Input_Features:
  - Grid: 2D array of integers (colors).
  - Background_Color: white (0).
  - Objects:
    - Contains exactly one solid-colored, non-white rectangular object.
    - Object_Color: Varies (green(3), red(2) in examples).
    - Object_Shape: Rectangular (can be square or non-square).
    - Object_Properties: Bounding box (top_row, bottom_row, left_col, right_col), height, width.

Output_Features:
  - Grid: Same dimensions as the input grid.
  - Original_Object: Preserved from the input grid.
  - Added_Element: A single straight line (horizontal or vertical).
    - Line_Color: Same as the Object_Color from the input.
    - Line_Origin: Starts adjacent to the original object.
    - Line_Extent: Extends to one edge of the grid (right or bottom).

Transformation_Rules:
  - Identify the single non-white rectangular object in the input grid.
  - Determine the object's bounding box, height, width, and color.
  - Compare the object's width and height:
    - If width >= height:
      - Action: Draw a horizontal line.
      - Row: object_top_row + object_height // 2 (middle row).
      - Start_Column: object_right_col + 1.
      - End_Column: grid_width - 1 (right edge).
      - Color: object_color.
    - If height > width:
      - Action: Draw a vertical line.
      - Column: object_left_col + object_width // 2 (middle column).
      - Start_Row: object_bottom_row + 1.
      - End_Row: grid_height - 1 (bottom edge).
      - Color: object_color.
  - Result: Output grid is the input grid with the added line.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find the non-white (color > 0) pixels in the input grid.
3.  Identify the single contiguous rectangular object formed by these pixels. Determine its color, its bounding box (top_row, bottom_row, left_col, right_col), its height (`bottom_row - top_row + 1`), and its width (`right_col - left_col + 1`).
4.  Compare the object's width and height.
5.  **If** the object's width is greater than or equal to its height:
    a.  Calculate the target row index: `target_row = top_row + height // 2`.
    b.  Iterate through columns from `col = right_col + 1` to the last column index (`grid_width - 1`).
    c.  Set the pixel at `(target_row, col)` in the output grid to the object's color.
6.  **Else (if** the object's height is greater than its width):
    a.  Calculate the target column index: `target_col = left_col + width // 2`.
    b.  Iterate through rows from `row = bottom_row + 1` to the last row index (`grid_height - 1`).
    c.  Set the pixel at `(row, target_col)` in the output grid to the object's color.
7.  Return the modified output grid.