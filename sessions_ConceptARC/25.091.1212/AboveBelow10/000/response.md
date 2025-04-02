Okay, let's analyze the provided examples.

## Perception

1.  **Input Structure:** Both input examples feature a grid primarily composed of the background color (white, 0). Within this background, there is a single, contiguous diagonal line formed by pixels of a single non-background color (yellow/4 in the first, green/3 in the second).
2.  **Output Structure:** The output grids retain the original diagonal line pixels. Additionally, areas adjacent to these diagonal pixels are filled with the same color. The pattern of filling differs between the two examples.
3.  **Transformation Pattern 1 (Example 1):** The diagonal line goes from the top-left towards the bottom-right. For each pixel on this line, all pixels in the *same row* to its *left* (including the original pixel's column) are changed to the line's color. This creates a filled right-angled triangle shape.
4.  **Transformation Pattern 2 (Example 2):** The diagonal line goes from the top-right towards the bottom-left. For each pixel on this line, all pixels in the *same row* to its *right* (including the original pixel's column) are changed to the line's color. Furthermore, all rows *below* the last row containing an original diagonal pixel are completely filled with the line's color.
5.  **Key Difference:** The primary difference seems linked to the direction of the input diagonal line. A down-right diagonal triggers a "fill-left" operation within rows. A down-left diagonal triggers a "fill-right" operation within rows *and* a "fill-below" operation for subsequent rows.

## Facts


```yaml
Input_Grid:
  - Objects:
      - Type: Background
        Color: white (0)
        Extent: Most of the grid
      - Type: Line
        Color: Non-white (yellow/4 or green/3)
        Shape: Diagonal (contiguous pixels)
        Properties:
          - Single color
          - Single contiguous line object
          - Direction: Down-right or Down-left
Output_Grid:
  - Objects:
      - Type: Background
        Color: white (0)
        Extent: Varies, potentially none in some rows/columns
      - Type: Filled_Region
        Color: Same as the input Line color
        Shape: Derived from the input Line
        Formation_Rule: Dependent on the input Line's direction
Relationships_and_Actions:
  - Identify: The single non-white color (C) in the input.
  - Identify: The positions (row, col) of all pixels with color C.
  - Determine: The direction of the diagonal line formed by pixels of color C.
    - If pixels follow (r, c), (r+1, c+1), ... -> Direction is Down-right.
    - If pixels follow (r, c), (r+1, c-1), ... -> Direction is Down-left.
  - Action (Conditional Fill):
    - IF Direction is Down-right:
        For each input pixel of color C at (r, c):
          Fill output grid row 'r' from column 0 to column 'c' (inclusive) with color C.
    - IF Direction is Down-left:
        For each input pixel of color C at (r, c):
          Fill output grid row 'r' from column 'c' to the last column (inclusive) with color C.
        Identify the maximum row index 'max_r' containing an input pixel of color C.
        Fill all output grid rows from 'max_r + 1' to the bottom row completely with color C.
  - State_Preservation: Pixels not explicitly changed retain their original color (which is white/0 in the background areas not affected by filling).
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the single non-background color (`C`) present in the input grid.
3.  Find all coordinates `(r, c)` of pixels with color `C`.
4.  Determine the primary direction of the diagonal line formed by these pixels:
    *   Check if the column index generally increases as the row index increases (Down-right diagonal).
    *   Check if the column index generally decreases as the row index increases (Down-left diagonal).
5.  **If the diagonal is Down-right:**
    *   Iterate through each coordinate `(r, c)` found in step 3.
    *   For the current coordinate `(r, c)`, change the color of all pixels in the output grid at row `r` from column 0 up to column `c` (inclusive) to color `C`.
6.  **If the diagonal is Down-left:**
    *   Find the maximum row index, `max_r`, among all coordinates found in step 3.
    *   Iterate through each coordinate `(r, c)` found in step 3.
    *   For the current coordinate `(r, c)`, change the color of all pixels in the output grid at row `r` from column `c` up to the rightmost column (inclusive) to color `C`.
    *   Iterate through all rows from `max_r + 1` down to the last row of the grid.
    *   For each of these rows, change the color of all pixels in that row to color `C`.
7.  Return the modified output grid.