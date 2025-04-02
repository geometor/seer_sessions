
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 2 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 2 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 2 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 2 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 4 4 4 4 2 0 0 0
0 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 2 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
2 0 0 0 4 0 0 0 0 0
2 0 0 4 4 4 0 0 0 0
2 0 4 4 4 4 2 0 0 0
2 4 4 4 4 4 4 4 0 0
2 0 4 4 4 4 2 0 0 0
2 0 0 4 4 4 0 0 0 0
2 0 0 0 4 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 2 0 3 3 2 3 0 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 2 2 2
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 2 0 3 3 2 3 0 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0
```

*   **Perception:**
    *   Each input grid contains exactly two red pixels (value 2). The rest of the grid contains other colors (azure, yellow, green) forming shapes, surrounded by a white background (value 0).
    *   The output grid is largely identical to the input grid, except that either the first row or the second column is entirely filled with red pixels.
    *   In examples 1 and 2, the two red pixels in the input share the same column index. In the output, the second column (index 1) is filled with red.
    *   In example 3, the two red pixels in the input share the same row index. In the output, the first row (index 0) is filled with red.
    *   The transformation rule depends on the relative positions of the two initial red pixels.

*   **YAML Facts:**
    
```yaml
    task_description: Modify a specific row or column based on the alignment of two existing red pixels.
    grid_properties:
      - dimensions: Varying (e.g., 10x10)
      - background_color: white (0)
    objects:
      - object: marker_pixels
        count: 2
        color: red (2)
        properties:
          - location: Coordinates (row, column)
          - alignment: Can be aligned horizontally (same row) or vertically (same column).
      - object: shapes
        count: 1 per example (implicitly defined by non-white, non-red pixels)
        color: Varies (azure (8), yellow (4), green (3))
        properties:
          - Contains the two red marker pixels.
    actions:
      - action: locate_markers
        input: input_grid
        output: coordinates of the two red pixels [(r1, c1), (r2, c2)]
      - action: check_alignment
        input: coordinates of red pixels
        output: alignment_type ('row' if r1 == r2, 'column' if c1 == c2)
      - action: modify_grid
        input: input_grid, alignment_type
        process:
          - Copy the input grid to create the output grid.
          - If alignment_type is 'row', set all pixels in the first row (index 0) of the output grid to red (2).
          - If alignment_type is 'column', set all pixels in the second column (index 1) of the output grid to red (2).
        output: modified_output_grid
    relationships:
      - The alignment (row or column) of the two red pixels determines which line (row 0 or column 1) is modified in the output.
      - If red pixels are in the same row, modify row 0.
      - If red pixels are in the same column, modify column 1.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid.
    2.  Find the coordinates (row and column indices) of the two pixels that have the color red (2). Let these coordinates be `(r1, c1)` and `(r2, c2)`.
    3.  Determine if the two red pixels are in the same row (`r1 == r2`) or the same column (`c1 == c2`).
    4.  If the red pixels are in the same row, modify the copied grid by changing the color of all pixels in the first row (row index 0) to red (2).
    5.  If the red pixels are in the same column, modify the copied grid by changing the color of all pixels in the second column (column index 1) to red (2).
    6.  Return the modified grid as the output.
