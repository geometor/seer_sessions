
## train_1

**input:**
```
0 0 0 8 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves processing each row of the input grid independently. In the input examples, certain rows contain exactly two pixels of the same non-white color, separated by white pixels. The transformation fills the white space *between* these two non-white pixels with the same color, effectively creating a horizontal line segment connecting the two original pixels. Rows that do not contain exactly two non-white pixels of the same color remain unchanged in the output. The size of the grid remains constant.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_dimensionality: 2D
      grid_size_constancy: True # Input and output grids have the same dimensions.
      background_color: 0 # white

    row_processing:
      dependency: Independent # Each row is processed based only on its own content.
      condition: Row must contain exactly two non-white pixels of the same color.
      action_if_condition_met: Fill the horizontal segment between the two non-white pixels (inclusive) with their color.
      action_if_condition_not_met: Copy the row unchanged.

    objects:
      - type: Pixel_Pair
        properties:
          - color: non-white (consistent within the pair, e.g., azure(8) or red(2))
          - count_per_row: Exactly 2
          - arrangement: Horizontal alignment within the same row
          - separation: Separated by one or more white (0) pixels.
      - type: Horizontal_Line_Segment
        description: A contiguous sequence of pixels of the same non-white color along a single row.

    transformation:
      type: Fill
      target: White pixels located horizontally between a Pixel_Pair.
      color_source: The color of the Pixel_Pair.
      outcome: Converts a Pixel_Pair separated by white space into a solid Horizontal_Line_Segment.

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each row of the input grid.
    3.  For the current row, find the indices and colors of all non-white pixels.
    4.  Check if there are exactly two non-white pixels in this row and if they have the same color (`C`).
    5.  If the condition in step 4 is met:
        a.  Let the column indices of these two pixels be `c1` and `c2`. Assume `c1 < c2`.
        b.  For every column index `c` from `c1` to `c2` (inclusive), set the pixel at the current row and column `c` in the output grid to color `C`.
    6.  If the condition in step 4 is not met, the row in the output grid remains unchanged (as it was copied in step 1).
    7.  After processing all rows, return the modified output grid.
