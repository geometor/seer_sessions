
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0
0 0 4 0 0 0 0 4 0 0
0 0 4 0 0 0 0 4 0 0
0 0 4 0 0 0 0 4 0 0
0 0 4 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 6 0
0 0 6 0 0 0 0 0 6 0
0 0 6 0 0 0 0 0 6 0
0 0 6 0 0 0 0 0 6 0
0 0 6 0 0 0 0 0 6 0
0 0 6 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception**

1.  **Input Analysis**: The input grids contain two parallel lines (either horizontal or vertical) composed of a single non-white color against a white background.
2.  **Output Analysis**: The output grids also contain two parallel lines of the *same* color as the input lines, but their orientation is rotated by 90 degrees compared to the input lines.
3.  **Transformation**: The transformation involves identifying the two parallel lines in the input, determining their color, orientation, and boundary coordinates. Then, it constructs two new lines in the output grid. These output lines have the same color as the input lines but are rotated 90 degrees. Crucially, the endpoints of the output lines are adjusted inwards by one pixel relative to the boundaries defined by the input lines.
4.  **Example 1 Specifics**: Input has two horizontal yellow lines. The output has two vertical yellow lines. The columns of the vertical lines correspond to the start and end columns of the input horizontal lines. The rows of the vertical lines span from one row below the top input line to one row above the bottom input line.
5.  **Example 2 Specifics**: Input has two vertical magenta lines. The output has two horizontal magenta lines. The rows of the horizontal lines correspond to the start and end rows of the input vertical lines. The columns of the horizontal lines span from one column to the right of the left input line to one column to the left of the right input line.

**Facts**


```yaml
task_description: Identify two parallel lines (horizontal or vertical) of the same color in the input grid and replace them with two parallel lines of the same color but rotated 90 degrees, with their span adjusted inwards by one unit relative to the original lines' boundaries.

elements:
  - object: parallel_lines
    count: 2
    properties:
      - color: non-white (consistent between the two lines)
      - orientation: either horizontal or vertical (consistent between the two lines)
      - location: defined by start and end coordinates (rows/columns)
  - object: background
    properties:
      - color: white (0)

relationships:
  - type: spatial
    description: The two lines are parallel and separated by background pixels.
  - type: transformation
    action: rotate_and_adjust
    input_object: parallel_lines (input)
    output_object: parallel_lines (output)
    details:
      - The orientation of the output lines is 90 degrees rotated from the input lines.
      - The color of the output lines is identical to the input lines.
      - The extent (length) and position of the output lines are derived from the input lines' boundaries, adjusted inwards by one pixel at each end of the span.

input_output_mapping:
  - case: input lines are horizontal
    input_properties:
      - color: C
      - row_top: R1
      - row_bottom: R2
      - col_start: C1
      - col_end: C2
    output_properties:
      - color: C
      - orientation: vertical
      - line1: col = C1, rows from R1+1 to R2-1
      - line2: col = C2, rows from R1+1 to R2-1
  - case: input lines are vertical
    input_properties:
      - color: C
      - col_left: C1
      - col_right: C2
      - row_start: R1
      - row_end: R2
    output_properties:
      - color: C
      - orientation: horizontal
      - line1: row = R1, cols from C1+1 to C2-1
      - line2: row = R2, cols from C1+1 to C2-1
```


**Natural Language Program**

1.  Identify all non-white pixels in the input grid.
2.  Group these pixels into connected objects (lines). Verify that there are exactly two such objects (lines) and that they share the same color and orientation (either both horizontal or both vertical).
3.  Determine the color (`C`) of these lines.
4.  Determine the orientation of the lines.
5.  **If the lines are horizontal:**
    a.  Find the row index of the top line (`R1`) and the bottom line (`R2`).
    b.  Find the starting column index (`C1`) and ending column index (`C2`) of the lines (these should be the same for both horizontal lines).
    c.  Create a new output grid of the same dimensions as the input, filled with white (0).
    d.  Draw a vertical line in the output grid using color `C` at column `C1`, spanning from row `R1 + 1` to `R2 - 1`.
    e.  Draw a second vertical line in the output grid using color `C` at column `C2`, spanning from row `R1 + 1` to `R2 - 1`.
6.  **If the lines are vertical:**
    a.  Find the column index of the left line (`C1`) and the right line (`C2`).
    b.  Find the starting row index (`R1`) and ending row index (`R2`) of the lines (these should be the same for both vertical lines).
    c.  Create a new output grid of the same dimensions as the input, filled with white (0).
    d.  Draw a horizontal line in the output grid using color `C` at row `R1`, spanning from column `C1 + 1` to `C2 - 1`.
    e.  Draw a second horizontal line in the output grid using color `C` at row `R2`, spanning from column `C1 + 1` to `C2 - 1`.
7.  Return the newly created output grid.
