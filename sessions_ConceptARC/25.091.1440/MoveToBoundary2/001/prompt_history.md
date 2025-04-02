
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input/Output:** Both are grids of pixels, primarily white (0) with scattered orange (7) pixels.
2.  **Content:** The orange pixels form distinct shapes or objects (connected components). These objects can be single pixels, lines (vertical or horizontal), or more complex shapes.
3.  **Transformation:** The core transformation involves shifting the orange pixels either downwards or rightwards. The direction of the shift seems to depend on the overall characteristics of the orange shapes present in the input grid.
4.  **Shift Mechanism (Vertical):** When shifting downwards (as seen in examples 1 and 3), it appears to operate column by column. All orange pixels within a specific column are shifted down by the same amount. This amount is determined by the lowest orange pixel in that column; it's shifted so that it ends up on the bottom-most row of the grid. Columns without any orange pixels remain unchanged.
5.  **Shift Mechanism (Horizontal):** When shifting rightwards (as seen in example 2), it appears to operate row by row. All orange pixels within a specific row are shifted right by the same amount. This amount is determined by the rightmost orange pixel in that row; it's shifted so that it ends up in the rightmost column of the grid. Rows without any orange pixels remain unchanged.
6.  **Condition for Shift Direction:** The choice between vertical and horizontal shift seems related to the dominant orientation of the orange objects. By calculating the total height and total width of all distinct orange objects, we can determine the mode:
    *   If the sum of object heights is greater than or equal to the sum of object widths, vertical gravity is applied.
    *   If the sum of object heights is less than the sum of object widths, horizontal gravity is applied.

**YAML Facts:**


```yaml
Grid:
  Type: 2D Array
  Colors:
    - White (0): Background
    - Orange (7): Foreground Objects
Objects:
  Definition: Contiguous block of orange pixels (using 4-connectivity, not diagonal).
  Properties:
    - Position: (row, column) coordinates of constituent pixels.
    - Shape: Variable (pixels, lines, L-shapes, bars, etc.).
    - BoundingBox: Defined by min/max row and column indices.
    - Height: Max row - min row + 1
    - Width: Max col - min col + 1
Transformation:
  Type: Conditional Shift (Gravity)
  Condition:
    - Calculate TotalHeight = Sum of heights of all distinct orange objects.
    - Calculate TotalWidth = Sum of widths of all distinct orange objects.
    - If TotalHeight >= TotalWidth: Apply Vertical Gravity
    - If TotalHeight < TotalWidth: Apply Horizontal Gravity
  Actions:
    - Vertical Gravity:
        Scope: Per Column
        Rule: Shift all orange pixels in a column downwards.
        Shift Amount (for column c): `grid_height - 1 - max_row_index_of_orange_in_column_c`
        Result: Lowest orange pixel in each column moves to the bottom row.
    - Horizontal Gravity:
        Scope: Per Row
        Rule: Shift all orange pixels in a row rightwards.
        Shift Amount (for row r): `grid_width - 1 - max_col_index_of_orange_in_row_r`
        Result: Rightmost orange pixel in each row moves to the rightmost column.
  Output Grid:
    - Start with an all-white grid of the same dimensions as the input.
    - Place the shifted orange pixels onto this grid.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but with all pixels set to white (0).
2.  Identify all distinct orange (7) objects in the input grid, considering pixels connected horizontally or vertically (not diagonally) as part of the same object.
3.  For each identified orange object, calculate its height (number of rows it spans) and width (number of columns it spans).
4.  Sum the heights of all objects to get `TotalHeight`.
5.  Sum the widths of all objects to get `TotalWidth`.
6.  Determine the transformation direction based on the sums:
    *   **If `TotalHeight` is greater than or equal to `TotalWidth` (Vertical Gravity):**
        a.  Iterate through each column `c` from left to right (index 0 to `grid_width - 1`).
        b.  Find all orange pixels located in the current column `c` in the input grid.
        c.  If no orange pixels are found in this column, continue to the next column.
        d.  If orange pixels exist, find the maximum row index (`max_r`) among them.
        e.  Calculate the downward shift amount `s = grid_height - 1 - max_r`.
        f.  For every orange pixel originally at `(r, c)` in the input grid's column `c`, set the pixel at `(r + s, c)` in the output grid to orange (7).
    *   **If `TotalHeight
