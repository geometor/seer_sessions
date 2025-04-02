
## train_1

**input:**
```
2 2 2 0 3 3 3 0 4 4 4
2 0 2 0 3 0 3 0 4 0 4
2 2 2 0 3 3 3 0 4 4 4
```


**output:**
```
2 2 2 0 3 3 3 0 4 4 4
2 0 2 0 3 0 3 0 4 0 4
2 2 2 0 3 3 3 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 3 3 3 0 4 4 4
2 0 2 0 3 0 3 0 4 0 4
2 2 2 0 3 3 3 0 4 4 4
```


## train_2

**input:**
```
6 6 6 6
6 6 6 6
0 0 0 0
7 7 7 7
7 7 7 7
0 0 0 0
0 0 0 0
9 9 9 9
9 9 9 9
```


**output:**
```
6 6 6 6 0 6 6 6 6
6 6 6 6 0 6 6 6 6
0 0 0 0 0 0 0 0 0
7 7 7 7 0 7 7 7 7
7 7 7 7 0 7 7 7 7
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
9 9 9 9 0 9 9 9 9
9 9 9 9 0 9 9 9 9
```

*   **Perception:**
    *   The input grids in both examples contain distinct colored shapes or blocks, often separated by white pixels.
    *   The output grid always contains two copies of the input grid.
    *   A separator, consisting entirely of white pixels (0), is inserted between these two copies.
    *   The orientation of the duplication and the nature of the separator (row or column) depend on the dimensions of the input grid.
    *   In `train_1`, the input is wider (11x3) than tall. The output duplicates the input vertically, placing one copy above the other, separated by a single row of white pixels. The output dimensions are (2 * height + 1) x width = 7x11.
    *   In `train_2`, the input is taller (9x4) than wide. The output duplicates the input horizontally, placing one copy next to the other, separated by a single column of white pixels. The output dimensions are height x (2 * width + 1) = 9x9.
    *   The rule appears to be: if the input width is greater than or equal to its height, duplicate vertically with a white row separator. If the input height is greater than its width, duplicate horizontally with a white column separator.

*   **Facts:**
    
```yaml
    task_context:
      - name: input_grid
        description: A 2D grid of pixels with varying dimensions and colored patterns.
      - name: output_grid
        description: A transformed 2D grid derived from the input grid.

    transformation_details:
      - name: duplication
        description: The entire input grid is duplicated exactly once.
      - name: separator
        description: A single line (row or column) of white pixels (0) is inserted between the two copies of the input grid.
        properties:
          - color: white (0)
          - thickness: 1 pixel
      - name: orientation_condition
        description: The orientation of duplication and the type of separator depend on the input grid's dimensions (height H, width W).
        conditions:
          - if: W >= H
            action: Duplicate vertically.
            separator_type: Row.
            output_dimensions: (2*H + 1) x W
          - if: H > W
            action: Duplicate horizontally.
            separator_type: Column.
            output_dimensions: H x (2*W + 1)

    object_relationships:
      - description: The output grid consists of two identical copies of the input grid structure, separated by a line of white pixels.
      - description: The placement of the copies and the separator (horizontal row vs. vertical column) is determined by comparing the input grid's width and height.
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Compare the width and height.
    3.  **If the width is greater than or equal to the height (W >= H):**
        a.  Create a new grid with dimensions (2 * H + 1) rows and W columns.
        b.  Copy the input grid into the top H rows of the new grid (rows 0 to H-1).
        c.  Fill the row at index H with white pixels (0).
        d.  Copy the input grid into the bottom H rows of the new grid (rows H+1 to 2*H).
    4.  **If the height is greater than the width (H > W):**
        a.  Create a new grid with dimensions H rows and (2 * W + 1) columns.
        b.  Copy the input grid into the left W columns of the new grid (columns 0 to W-1).
        c.  Fill the column at index W with white pixels (0).
        d.  Copy the input grid into the right W columns of the new grid (columns W+1 to 2*W).
    5.  Return the new grid as the output.
