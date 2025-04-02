
## train_1

**input:**
```
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
```


**output:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
```

**Perception**

1.  **Grid Structure:** The input and output are 2D grids of varying dimensions (Example 1 & 2: 7x9, Example 3: 8x9). The background color is consistently white (0).
2.  **Core Elements:** The key elements are the non-white pixels within each row. Their presence, count, position, and color dictate the transformation.
3.  **Row Independence:** The transformation process operates independently on each row. The changes in one row do not affect any other row.
4.  **Transformation Logic:** The transformation involves filling segments of rows horizontally based on the non-white pixels present in the input row.
5.  **Conditional Filling:** There are two distinct filling behaviors based on the *number* of non-white pixels in a row:
    *   **Single Non-White Pixel:** If a row contains exactly one non-white pixel, the output row is filled with that pixel's color starting from its column index and extending all the way to the right edge of the grid. Pixels to the left remain white.
    *   **Multiple Non-White Pixels:** If a row contains two or more non-white pixels, the output row is filled *between* the column index of the leftmost non-white pixel and the column index of the rightmost non-white pixel (inclusive). The color used for filling is the color of the *leftmost* non-white pixel in that row. Pixels outside this horizontal segment remain white.
    *   **No Non-White Pixels:** If a row contains only white pixels, the output row remains unchanged (all white).

**Facts**

```
yaml
task_type: grid_transformation
grid_properties:
  - background_color: 0 (white)
  - dimensions_vary: true # Seen 7x9 and 8x9
processing_granularity: row-wise # Each row processed independently
objects:
  - type: pixel
    attributes:
      - color: integer 0-9
      - position: (row_index, column_index)
  - type: non_white_pixel
    description: A pixel with color > 0.
    attributes:
      - color
      - position
row_analysis:
  - identify: non_white_pixels_in_row
    properties:
      - locations: list of (column_index, color) pairs
      - count: number of non_white_pixels
      - leftmost_pixel: pixel with minimum column_index (if count > 0)
      - rightmost_pixel: pixel with maximum column_index (if count > 0)
transformation_rule:
  - scope: per_row
  - conditions:
      - if: count == 0
        action: output_row = input_row (all white)
      - if: count == 1
        action:
          - get: color C and column index Col of the single non_white_pixel
          - fill: output_row from Col to grid_width-1 with C
          - keep: output_row from 0 to Col-1 as white
      - if: count > 1
        action:
          - get: color C and column index MinCol of leftmost_pixel
          - get: column index MaxCol of rightmost_pixel
          - fill: output_row from MinCol to MaxCol (inclusive) with C
          - keep: output_row outside [MinCol, MaxCol] as white

