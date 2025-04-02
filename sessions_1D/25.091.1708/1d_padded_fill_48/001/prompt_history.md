
## train_1

**input:**
```
2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
```


## train_3

**input:**
```
7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain a white background (color 0) with a few scattered pixels of a single non-white color (red=2, azure=8, orange=7).
    *   In the rows containing non-white pixels, there are always exactly two such pixels.
    *   The output grids maintain the original positions of the non-white pixels.
    *   The key transformation is filling the horizontal space *between* the pair of non-white pixels in each relevant row with the same non-white color.
    *   Rows that were entirely white in the input remain entirely white in the output.
    *   The transformation acts independently on each row.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_features:
      - grid: 2D array of integers (0-9)
      - background_color: white (0)
      - foreground_objects:
          - type: isolated pixels
          - count_per_row_pattern: exactly two non-white pixels per row (if any non-white pixels are present in that row)
          - color: consistent non-white color within each example (e.g., red in train_1, azure in train_2)
    output_features:
      - grid: 2D array of integers (0-9)
      - background_color: white (0)
      - transformed_objects:
          - type: horizontal line segments
          - color: same as the non-white color from the input row
          - location: spans between the original pair of non-white pixels in each relevant row
    transformation_logic:
      - scope: row-wise
      - condition: process rows containing exactly two non-white pixels of the same color.
      - action: fill the segment between the leftmost and rightmost non-white pixel (inclusive) with that non-white color.
      - unchanged: rows with zero, one, or more than two non-white pixels, or pixels of different non-white colors, remain unchanged.
    relationships:
      - The output line segment's color is determined by the color of the pair of pixels in the input row.
      - The output line segment's start and end columns are determined by the column indices of the pair of pixels in the input row.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each row of the input grid.
    3.  For the current row, identify all non-white pixels, recording their color and column index.
    4.  Check if there are exactly two non-white pixels in the row and if they share the same color.
    5.  If the condition in step 4 is true:
        a.  Determine the non-white color (`fill_color`).
        b.  Find the minimum column index (`min_col`) among the two non-white pixels.
        c.  Find the maximum column index (`max_col`) among the two non-white pixels.
        d.  In the corresponding row of the output grid, set the color of all pixels from column `min_col` to `max_col` (inclusive) to `fill_color`.
    6.  If the condition in step 4 is false, leave the corresponding row in the output grid unchanged (it's already a copy from step 1).
    7.  Return the modified output grid.
