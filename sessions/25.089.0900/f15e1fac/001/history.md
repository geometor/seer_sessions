
## train_1

**input:**
```
0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 0 8 0 0 0
0 8 0 0 0 8 0 0 0 2
0 8 0 0 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
0 8 0 0 0 8 0 0 0 0
8 0 0 0 8 0 0 0 0 2
8 0 0 0 8 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0
8 0 0 0 8 0 0 0 0 0
0 0 0 8 0 0 0 0 0 2
0 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0
```


## train_2

**input:**
```
0 8 0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 8 0 8 0 8 0 0
0 8 0 0 0 8 0 8 0 8 0 0
0 8 0 0 0 8 0 8 0 8 0 0
0 8 0 0 0 8 0 8 0 8 0 0
2 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
0 0 8 0 0 0 8 0 8 0 8 0
2 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
0 0 0 8 0 0 0 8 0 8 0 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0
```

*   **Perception:**
    *   The task involves transforming grids containing white (0), azure (8), and red (2) pixels.
    *   The transformation logic appears to depend on the initial positions of the azure and red pixels.
    *   Two distinct transformation modes are observed based on the input configuration:
        1.  **Mode 1 (Examples 1 & 2):** Triggered when azure pixels are present in the first row (row 0). Azure pixels in the first row define a vertical pattern. This pattern propagates downwards. When a row containing a red pixel (acting as a trigger) is encountered in the input, the pattern shifts one column to the left for subsequent rows. The propagated azure pattern only colors pixels that were originally white in the input grid; existing non-white pixels (like the red triggers) are preserved.
        2.  **Mode 2 (Example 3):** Triggered when no azure pixels are in the first row, but azure pixels *are* present in the first column (column 0). Each azure pixel in the first column at row `r` triggers the drawing of three horizontal, 4-pixel-wide azure blocks in the output: one starting at `(r, 0)`, one at `(r-1, 4)`, and one at `(r-2, 8)`. These blocks overwrite existing pixels in the output grid at their locations. All other pixels from the input grid (like the red pixels in Example 3) are preserved in their original positions unless overwritten by the drawn blocks.

*   **YAML Facts:**
    
```yaml
    task_type: grid_transformation
    colors_used:
      - white (0)
      - azure (8)
      - red (2)
    rules:
      - condition: Azure (8) pixels exist in the first row (row 0).
        mode: vertical_shift
        elements:
          - role: pattern_definition
            color: azure (8)
            location: first row (row 0)
            property: column indices define the initial pattern
          - role: trigger
            color: red (2)
            location: any row
            action: causes the pattern to shift left by 1 column in subsequent rows
          - role: background
            color: white (0)
            action: can be overwritten by the azure pattern
          - role: preserved_pixels
            color: non-white pixels from input (e.g., red triggers)
            action: are not overwritten by the azure pattern
        transformation:
          - Initialize output grid as a copy of the input.
          - Identify initial azure column pattern from row 0.
          - Iterate through rows top to bottom.
          - Maintain the current column pattern.
          - For each row `r`:
            - Apply the current pattern: for each column `c` in the pattern, if `input[r, c]` is white (0), set `output[r, c]` to azure (8).
            - Check if input row `r` contains any red (2) pixels.
            - If yes, update the pattern for subsequent rows by shifting all column indices left by 1 (discarding negative indices).
      - condition: No azure (8) pixels in row 0, but azure (8) pixels exist in the first column (col 0).
        mode: horizontal_blocks
        elements:
          - role: trigger
            color: azure (8)
            location: first column (col 0) at row `r`
            action: initiates drawing of three horizontal blocks
          - role: drawn_object
            color: azure (8)
            shape: horizontal block, 4 pixels wide
            placement:
              - Starts at (r, 0)
              - Starts at (r-1, 4) if r-1 >= 0
              - Starts at (r-2, 8) if r-2 >= 0
          - role: background/preserved_pixels
            color: all input pixels
            action: are preserved unless overwritten by the drawn azure blocks
        transformation:
          - Initialize output grid as a copy of the input.
          - Find all rows `r` where `input[r, 0]` is azure (8).
          - For each such `r`, draw the three specified 4-pixel horizontal azure blocks in the output grid, checking row boundary conditions (r-1 >= 0, r-2 >= 0). These blocks overwrite existing content.
      - condition: Fallback (neither of the above conditions met).
        transformation: Output grid is identical to the input grid. (Inferred, no examples provided).
    ```


*   **Natural Language Program:**
    1.  Examine the input grid. Check if any azure (8) pixels are present in the first row (row 0).
    2.  **If azure pixels are in the first row:**
        a.  Initialize the output grid as a copy of the input grid.
        b.  Determine the set of column indices containing azure pixels in the first row. This is the initial `current_pattern`.
        c.  Iterate through each row `r` from 0 to the grid height minus 1.
        d.  For the current row `r`, iterate through each column index `c` in the `current_pattern`. If the pixel at `input[r, c]` is white (0), set the corresponding pixel `output[r, c]` to azure (8).
        e.  Check if the input grid's row `r` contains any red (2) pixels.
        f.  If red pixels are present in row `r`, update the `current_pattern` for the *next* iteration (row `r+1`) by subtracting 1 from each column index and discarding any resulting negative indices. Otherwise, the `current_pattern` remains unchanged for the next row.
        g.  Proceed to the next row with the potentially updated `current_pattern`.
    3.  **If no azure pixels are in the first row:**
        a.  Check if any azure (8) pixels are present in the first column (column 0).
        b.  **If azure pixels are in the first column:**
            i.  Initialize the output grid as a copy of the input grid.
            ii. Find all row indices `r` such that `input[r, 0]` is azure (8).
            iii. For each such row index `r`:
                -   Draw a horizontal block of 4 azure pixels in the output grid from `(r, 0)` to `(r, 3)`.
                -   If `r-1` is a valid row index (>= 0), draw a horizontal block of 4 azure pixels from `(r-1, 4)` to `(r-1, 7)`.
                -   If `r-2` is a valid row index (>= 0), draw a horizontal block of 4 azure pixels from `(r-2, 8)` to `(r-2, 11)`.
                -   These drawing operations overwrite any previous content in those output grid cells.
        c.  **If no azure pixels are in the first column either:**
            i.  The output grid is identical to the input grid.
    4.  Return the final output grid.
