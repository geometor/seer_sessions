
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
```


## train_3

**input:**
```
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain mostly white pixels (0) and a few isolated non-white pixels (blue=1, green=3, orange=7).
    *   In each example, the non-white pixels appear in different rows but seem to maintain a consistent column alignment within that example.
    *   The output grids retain the same dimensions as the input grids.
    *   The transformation operates row by row.
    *   For each row in the input grid:
        *   If the row contains only white pixels, the corresponding output row is identical (all white).
        *   If the row contains a non-white pixel, locate the column index of that pixel. The output row is modified such that all pixels from that column index to the rightmost column are filled with the color of the non-white pixel found in the input row. All pixels to the left of that starting column index remain white.
    *   The color of the non-white pixel in the input row determines the color used for filling in the output row.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    transformation_scope: row-wise
    background_color: 0 # white
    objects:
      - type: pixel
        properties:
          - color (non-zero)
          - position (row_index, column_index)
    row_processing:
      condition: presence of a non-white pixel in the input row
      action:
        - identify the first non-white pixel from left to right
        - record its color (C) and column index (idx)
        - generate output row:
          - pixels from column 0 to idx-1 are set to white (0)
          - pixels from column idx to the last column are set to color C
      fallback (if no non-white pixel):
        - copy the input row to the output row (all white)
    grid_properties:
      - dimensions remain constant between input and output
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output grid with the same dimensions as the input grid.
    2.  Iterate through each row of the input grid, keeping track of the row index.
    3.  For the current row:
        a.  Initialize a variable `first_non_white_col` to -1 and `fill_color` to 0 (white).
        b.  Scan the row from left to right (column 0 to the last column).
        c.  If a non-white pixel is encountered at column `c`:
            i.  Set `first_non_white_col` to `c`.
            ii. Set `fill_color` to the color of the pixel at `(row_index, c)`.
            iii. Stop scanning the current row (break the inner loop).
        d.  Construct the corresponding row for the output grid:
            i.  If `first_non_white_col` is -1 (meaning the input row was all white), fill the output row entirely with white (0).
            ii. If `first_non_white_col` is not -1, fill the output row from column `first_non_white_col` to the last column with `fill_color`. Fill columns 0 to `first_non_white_col - 1` with white (0).
    4.  Return the completed output grid.
