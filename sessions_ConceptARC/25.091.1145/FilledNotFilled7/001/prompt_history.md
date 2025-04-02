
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   Each input grid contains a single non-white color.
    *   The non-white pixels form one or more horizontal structures.
    *   The transformation modifies the area between the topmost and bottommost rows containing the non-white color.
    *   The specific modification depends on how many rows initially contain the non-white color within this vertical span.

*   **Fact Sheet:**
    
```yaml
    task_description: Modifies the vertical space between horizontal structures of the same color based on the number of initial structures.

    elements:
      - element: grid
        description: A 2D array of pixels with colors 0-9.
      - element: background
        properties:
          - color: white (0)
      - element: colored_region
        description: A collection of pixels sharing the same non-white color (C).
        properties:
          - color: C (where C is non-zero, e.g., red, green, orange)
          - bounding_box: Defined by min_row, max_row, min_col, max_col of pixels with color C.
          - rows_present: A list of row indices within the bounding_box that contain pixels of color C.
          - num_colored_rows: The count of unique row indices in rows_present.

    relationships:
      - relationship: spatial
        description: The colored_region exists within the grid, surrounded by the background. The transformation targets the rows between the min_row and max_row of the colored_region.
      - relationship: conditional
        description: The transformation type depends on the value of num_colored_rows.

    actions:
      - action: identify_colored_region
        description: Find all non-white pixels, verify they share a single color C, and determine their bounding_box (min_row, max_row, min_col, max_col).
      - action: count_colored_rows
        description: Count the number of distinct rows between min_row and max_row (inclusive) that contain color C.
      - action: fill_gap
        description: If num_colored_rows is 2, fill the rectangle defined by (min_row + 1 to max_row - 1, min_col to max_col) with color C.
        condition: num_colored_rows == 2
      - action: clear_middle
        description: If num_colored_rows is greater than 2, set the pixels in the rectangle defined by (min_row + 1 to max_row - 1, min_col to max_col) to white (0).
        condition: num_colored_rows > 2
      - action: copy_input
        description: The output grid starts as a copy of the input grid before modifications. Pixels outside the modified rectangle remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid. This copy will become the output grid.
    2.  Identify all pixels in the input grid that are not white (color 0). Verify that all these non-white pixels share the same color, let this color be C.
    3.  Determine the coordinates of the bounding box containing all pixels of color C: find the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`).
    4.  Count how many distinct rows between `min_row` and `max_row` (inclusive) contain at least one pixel of color C. Let this count be `num_colored_rows`.
    5.  If `num_colored_rows` equals 2:
        a.  Iterate through each row `r` from `min_row + 1` up to (but not including) `max_row`.
        b.  Iterate through each column `c` from `min_col` up to `max_col`.
        c.  Set the pixel at (`r`, `c`) in the output grid to color C.
    6.  If `num_colored_rows` is greater than 2:
        a.  Iterate through each row `r` from `min_row + 1` up to (but not including) `max_row`.
        b.  Iterate through each column `c` from `min_col` up to `max_col`.
        c.  Set the pixel at (`r`, `c`) in the output grid to white (color 0).
    7.  Return the modified output grid.
