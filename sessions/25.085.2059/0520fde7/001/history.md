
## train_1

**input:**
```
1 1 0 5 0 1 0
0 0 1 5 1 1 1
1 1 0 5 0 1 0
```


**output:**
```
0 2 0
0 0 2
0 2 0
```


## train_2

**input:**
```
1 0 0 5 0 1 0
0 1 0 5 1 1 1
1 0 0 5 0 0 0
```


**output:**
```
0 0 0
0 2 0
0 0 0
```


## train_3

**input:**
```
0 0 1 5 0 0 0
1 1 0 5 1 0 1
0 1 1 5 1 0 1
```


**output:**
```
0 0 0
2 0 0
0 0 2
```

*   **Perception:**
    *   The input grids consistently have 3 rows and 7 columns.
    *   A vertical line of gray pixels (color 5) is always present in the 4th column (index 3), acting as a central separator.
    *   Blue pixels (color 1) appear on both the left and right sides of the gray line.
    *   White pixels (color 0) act as the background.
    *   The output grids are always 3x3.
    *   The output grids contain only white (0) and red (2) pixels.
    *   The position of red pixels in the output seems related to the positions of blue pixels in the input, specifically where blue pixels appear symmetrically mirrored across the central gray line within the same row.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_grid:
      properties:
        height: 3
        width: 7
        colors_present: [white, blue, gray]
      objects:
        - type: dividing_line
          color: gray
          position: column 3 (0-indexed)
          shape: vertical line
        - type: pattern_pixels
          color: blue
          position: variable, located on either side of the dividing_line
    output_grid:
      properties:
        height: 3
        width: 3
        colors_present: [white, red]
      objects:
        - type: marker_pixels
          color: red
          position: determined by input pattern
          relationship_to_input: marks positions where blue pixels exist symmetrically across the gray line in the input.
    transformation:
      dimensionality_change: input width 7 -> output width 3
      color_mapping: blue (1) in specific symmetric configurations -> red (2), all others -> white (0)
      logic:
        - identify the central gray line column index (gc = 3).
        - determine the width of the left side (lw = gc) and right side (rw = input_width - gc - 1).
        - the output width is max(lw, rw). In this case, lw=3, rw=3, so output width is 3.
        - for each row 'i':
          - compare the pattern of blue pixels in columns 0 to lw-1 with the pattern of blue pixels in columns gc+1 to gc+rw.
          - for each column index 'j' from 0 to output_width-1:
            - check if input[i, j] is blue AND input[i, gc + 1 + j] is blue.
            - if both conditions are true, the output grid cell [i, j] becomes red (2).
            - otherwise, the output grid cell [i, j] remains white (0).
    ```


*   **Natural Language Program:**
    1.  Create a new output grid with the same number of rows as the input grid and a width equal to the number of columns to the left of the central gray line (which is also equal to the number of columns to the right of the gray line in these examples, specifically 3 columns). Initialize this output grid with white pixels (0).
    2.  Identify the column index of the vertical gray line (color 5) in the input grid. Let this be `gray_col_index`.
    3.  Iterate through each row `i` of the input grid (from top to bottom).
    4.  For each row `i`, iterate through the columns `j` from 0 up to (but not including) `gray_col_index`. This corresponds to iterating through the columns of the left side of the input grid and simultaneously the columns of the output grid.
    5.  Inside this loop, check if the pixel at `(i, j)` in the input grid is blue (1) AND the pixel at `(i, gray_col_index + 1 + j)` in the input grid (the corresponding mirrored position on the right side) is also blue (1).
    6.  If both pixels are blue, set the pixel at `(i, j)` in the output grid to red (2).
    7.  If the condition in step 5 is not met, the pixel at `(i, j)` in the output grid remains white (0).
    8.  After iterating through all rows and relevant columns, the resulting output grid is complete.
