
## train_1

**input:**
```
0 5 0 5 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 5 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 2 2 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 2 0 2 2 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 2 2 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
5 0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 0 5 0 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 0 5 0 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 2 0 2 2 5
0 0 2 2 0 2 0 2 2 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 2 0 2 2 5
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 2 0 2 2 5
0 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   The input grids primarily consist of a white background (0) with some gray pixels (5).
    *   Gray pixels appear in the first row, forming a horizontal pattern.
    *   Gray pixels also appear sporadically in the last column of some rows below the first row.
    *   The output grids retain the original gray pixels from the input.
    *   Additionally, the output grids contain red pixels (2).
    *   The red pixels appear only in rows (excluding the first row) that have a gray pixel in the last column in the input grid.
    *   Within these specific rows, the red pixels replicate the horizontal pattern of the gray pixels found in the *first* row of the input grid, but only up to the second-to-last column. The gray pixel in the last column of these rows remains unchanged.

*   **YAML Facts**:
    
```yaml
    elements:
      - object: grid
        properties:
          - background_color: white (0)
          - contains: pixels
      - object: pixel
        properties:
          - color: [white (0), gray (5), red (2)]
          - position: (row, column)
      - object: pattern
        properties:
          - location: first row (row 0)
          - composition: sequence of gray (5) pixels
          - orientation: horizontal
      - object: trigger_pixel
        properties:
          - color: gray (5)
          - location: last column (column index = width - 1)
          - position: in rows below the first row (row index > 0)
    actions:
      - name: identify_pattern
        actor: system
        input: first row of the input grid
        output: horizontal pattern of gray pixels (excluding the last column)
      - name: identify_trigger_rows
        actor: system
        input: input grid (rows 1 to height-1)
        output: list of row indices containing a gray pixel in the last column
      - name: replicate_pattern
        actor: system
        input:
          - pattern from first row
          - trigger row index
        output: modification of the output grid row
        details: For each trigger row, iterate through columns 0 to width-2. If the pixel at (0, column) in the input is gray (5), change the pixel at (trigger_row_index, column) in the output grid to red (2).
      - name: copy_unchanged
        actor: system
        input: input grid
        output: output grid
        details: All pixels not modified by the replicate_pattern action retain their original color from the input grid. This includes the first row, rows without a trigger pixel, and the last column pixel of trigger rows.
    relationships:
      - type: dependency
        source: trigger_pixel in a row
        target: replication of the first row's pattern (in red) into that row
      - type: spatial
        details: The pattern replication occurs in the same columns as the original pattern in the first row, but in a different row (the trigger row).
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the horizontal pattern defined by the positions of gray (5) pixels in the first row (row 0) of the input grid, considering only columns from 0 up to the second-to-last column (width - 2).
    3.  Iterate through each subsequent row `r` of the input grid (from row 1 to height - 1).
    4.  Check if the pixel in the last column (column index = width - 1) of row `r` is gray (5).
    5.  If it is gray (5), then iterate through the columns `c` from 0 to width - 2:
        *   If the pixel at position (0, `c`) in the input grid is gray (5), change the pixel at position (`r`, `c`) in the output grid to red (2).
    6.  Leave all other pixels in the output grid unchanged from their initial copied state (which matches the input grid).
    7.  Return the modified output grid.
