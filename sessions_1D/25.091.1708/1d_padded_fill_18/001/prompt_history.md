
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0
```


## train_3

**input:**
```
0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    The input grids are primarily composed of the background color white (0), with a few scattered pixels of a single non-background color (azure (8), blue (1), or orange (7) in the examples). The non-background pixels appear in distinct rows. The output grids retain the same dimensions as the input. The transformation operates row by row. For each row in the input grid that contains non-background pixels, the output grid fills the horizontal segment between the leftmost and rightmost occurrences of that non-background color in that row with the same color. Rows containing only the background color remain unchanged.

*   **Facts**:
    
```yaml
    task_type: shape_completion
    scope: row-wise
    objects:
      - type: background_pixel
        color: white (0)
      - type: colored_pixel
        color: non-white (e.g., azure, blue, orange)
        properties:
          - row_index
          - column_index
    actions:
      - identify_rows_with_colored_pixels
      - for_each_identified_row:
          - find_colored_pixel_color: C
          - find_min_column_index: min_col
          - find_max_column_index: max_col
          - fill_horizontal_segment:
              from: (row_index, min_col)
              to: (row_index, max_col)
              color: C
    relationships:
      - pixels within the same row
      - leftmost and rightmost colored pixels define the bounds of the filled segment in a row
    state_changes:
      - background_pixels within the identified horizontal segment [min_col, max_col] in a relevant row change to the colored_pixel_color C.
      - colored_pixels remain the same color.
      - background_pixels outside the identified segments remain white.
      - rows with only background_pixels remain unchanged.
    assumptions:
      - Within a single row containing colored pixels, all colored pixels share the same color.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each row of the input grid.
    3.  For the current row, identify the indices of all columns containing non-white pixels.
    4.  If no non-white pixels are found in the current row, proceed to the next row.
    5.  If non-white pixels are found:
        a.  Determine the color (`C`) of the first non-white pixel encountered in the row (based on the assumption that all non-white pixels in a relevant row share the same color).
        b.  Find the minimum column index (`min_col`) among the non-white pixels in this row.
        c.  Find the maximum column index (`max_col`) among the non-white pixels in this row.
        d.  In the corresponding row of the output grid, change the color of all pixels from column `min_col` to `max_col` (inclusive) to color `C`.
    6.  After processing all rows, return the modified output grid.
