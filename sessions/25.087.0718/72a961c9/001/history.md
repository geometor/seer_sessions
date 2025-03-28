
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 1 2 1 1 1 8 1 1 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 1 0 0 0 8 0 0 0
0 0 1 0 0 0 1 0 0 0
0 0 1 0 0 0 1 0 0 0
1 1 2 1 1 1 8 1 1 1
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
1 1 1 2 1 1 1
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 2 0 0 0
0 0 0 1 0 0 0
0 0 0 1 0 0 0
0 0 0 1 0 0 0
1 1 1 2 1 1 1
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
1 8 1 1 1 1
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0
0 1 0 0 0 0
0 1 0 0 0 0
1 8 1 1 1 1
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 8 1 1 1 8 1 2 1
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0
0 8 0 0 0 8 0 1 0
0 1 0 0 0 1 0 1 0
0 1 0 0 0 1 0 1 0
1 8 1 1 1 8 1 2 1
0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids consist primarily of a white background (0).
    *   Each input contains exactly one horizontal line composed of non-white pixels.
    *   Within this horizontal line, certain pixels act as triggers: red (2) and azure (8).
    *   The output grid is identical to the input grid, except for the addition of vertical columns extending upwards from the locations of the trigger pixels (red and azure).
    *   The colors used in the vertical column above a trigger pixel are copied from the horizontal line in the input grid, starting from the trigger pixel itself and proceeding rightwards along the line.
    *   The height of the vertical column added depends on the color of the trigger pixel: red (2) triggers a column of height 4, and azure (8) triggers a column of height 3.
    *   The vertical column starts one row above the horizontal line and extends upwards.
    *   The drawing of the vertical column is constrained by the top edge of the grid; it does not extend beyond row 0. The actual height of the drawn column might be less than the target height (4 or 3) if it hits the top edge or if the sequence of colors copied from the line runs out due to the right edge of the grid.

*   **Facts YAML:**
    
```yaml
    Grid:
      background_color: white (0)
      elements:
        - HorizontalLine
        - TriggerPixels
        - OutputColumns (derived)
    
    Objects:
      - type: HorizontalLine
        properties:
          - single instance per grid
          - composed of contiguous non-white pixels
          - located at a specific row `r_line`
          - contains TriggerPixels
      - type: TriggerPixel
        properties:
          - located within the HorizontalLine at `(r_line, c)`
          - color is either red (2) or azure (8)
          - defines the starting point and column for an OutputColumn
          - determines the target height of the OutputColumn (red=4, azure=3)
      - type: OutputColumn
        properties:
          - appears only in the output grid
          - vertical sequence of pixels
          - located at column `c` corresponding to a TriggerPixel
          - starts at row `r_line - 1` and extends upwards
          - colors are copied sequentially from the HorizontalLine, starting at `(r_line, c)` and moving right
          - target height depends on the TriggerPixel color (4 for red, 3 for azure)
          - actual height is limited by the target height, the top grid boundary (row 0), and the availability of colors from the HorizontalLine (right grid boundary)
    
    Relationships:
      - Each TriggerPixel (red or azure) in the input's HorizontalLine generates a corresponding OutputColumn in the output grid.
      - An OutputColumn is positioned directly above its generating TriggerPixel.
      - The colors in the OutputColumn mirror a segment of the HorizontalLine starting from the TriggerPixel.
      - The length (height) of the OutputColumn is determined primarily by the TriggerPixel's color, subject to grid boundaries.
    
    Actions:
      - Identify the HorizontalLine and its row `r_line`.
      - Locate all TriggerPixels (red=2, azure=8) within the HorizontalLine at positions `(r_line, c)`.
      - For each TriggerPixel:
        - Determine the target height `h` (4 if red, 3 if azure).
        - Extract the color sequence `S` of length up to `h` from the HorizontalLine, starting at column `c` and moving right.
        - Copy the input grid to the output grid.
        - Draw the sequence `S` vertically upwards into the output grid, starting at `(r_line - 1, c)`, ensuring not to draw above row 0. The k-th color in `S` (0-indexed) is placed at `(r_line - 1 - k, c)`.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Find the row index (`r_line`) of the single horizontal line containing non-white pixels.
    3.  Iterate through each column index `c` of the input grid width.
    4.  Check the pixel at `(r_line, c)` in the input grid.
    5.  If the pixel color is red (2):
        a.  Set the target height `h = 4`.
        b.  Extract the sequence of colors `S` from the input grid's horizontal line, starting at `(r_line, c)` and extending up to `h` pixels to the right (i.e., `input[r_line, c]` to `input[r_line, c + h - 1]`), stopping if the grid's right edge is reached.
        c.  Iterate from `k = 0` up to `len(S) - 1`.
        d.  Calculate the target row `r_target = r_line - 1 - k`.
        e.  If `r_target` is greater than or equal to 0 (within the grid's top boundary), set the pixel at `(r_target, c)` in the *output* grid to the color `S[k]`.
    6.  If the pixel color is azure (8):
        a.  Set the target height `h = 3`.
        b.  Extract the sequence of colors `S` from the input grid's horizontal line, starting at `(r_line, c)` and extending up to `h` pixels to the right (i.e., `input[r_line, c]` to `input[r_line, c + h - 1]`), stopping if the grid's right edge is reached.
        c.  Iterate from `k = 0` up to `len(S) - 1`.
        d.  Calculate the target row `r_target = r_line - 1 - k`.
        e.  If `r_target` is greater than or equal to 0 (within the grid's top boundary), set the pixel at `(r_target, c)` in the *output* grid to the color `S[k]`.
    7.  Return the modified output grid.
