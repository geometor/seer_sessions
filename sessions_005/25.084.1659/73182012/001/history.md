
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 5 5 2 2 5 5 0 0 0
0 0 0 5 3 3 3 3 5 0 0 0
0 0 2 2 3 1 1 3 2 2 0 0
0 0 2 2 3 1 1 3 2 2 0 0
0 0 0 5 3 3 3 3 5 0 0 0
0 0 0 5 5 2 2 5 5 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2
0 5 5 2
0 5 3 3
2 2 3 1
```


## train_2

**input:**
```
0 0 0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0
0 2 3 1 1 3 2 0 0 0 0 0
2 2 1 0 0 1 2 2 0 0 0 0
2 2 1 0 0 1 2 2 0 0 0 0
0 2 3 1 1 3 2 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2
0 0 2 2
0 2 3 1
2 2 1 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 7 7 0
0 0 0 0 7 2 2 3 3 2 2 7
0 0 0 0 7 2 8 8 8 8 2 7
0 0 0 0 0 3 8 0 0 8 3 0
0 0 0 0 0 3 8 0 0 8 3 0
0 0 0 0 7 2 8 8 8 8 2 7
0 0 0 0 7 2 2 3 3 2 2 7
0 0 0 0 0 7 7 0 0 7 7 0
```


**output:**
```
0 7 7 0
7 2 2 3
7 2 8 8
0 3 8 0
```

*   **Perception**:
    *   The input grids contain patterns composed of various colors, often surrounded by a white (0) background.
    *   The output grids are consistently 4x4 in size.
    *   The output grid appears to be a direct sub-section (subgrid) extracted from the input grid.
    *   By comparing the pixel values, the output grid corresponds exactly to a specific 4x4 region within the input grid.
    *   In each example, the extracted 4x4 region starts at the top-left corner of the bounding box containing all non-white pixels in the input grid.

*   **Facts**:
    
```yaml
    task_type: extraction
    input_properties:
      - description: Input grid containing a pattern, usually surrounded by white pixels (0).
      - grid_size: Variable (e.g., 12x12 in examples).
      - colors_present: Variable, includes white (0) and others (1-9).
    output_properties:
      - description: Output grid is a 4x4 subgrid extracted from the input.
      - grid_size: Fixed (4x4).
      - content: Directly copied pixel values from a specific region of the input.
    transformation:
      - type: subgrid_extraction
      - parameters:
          - size: 4x4
          - anchor_point: Top-left corner of the bounding box of all non-white pixels in the input grid.
      - relationship: The output grid is `input[min_row : min_row + 4, min_col : min_col + 4]`, where `(min_row, min_col)` are the minimum row and column indices containing non-white pixels.
    objects:
      - id: main_pattern
        description: The collection of all non-white pixels in the input grid.
        properties:
          - bounding_box: The smallest rectangle containing all non-white pixels.
          - top_left_corner: Coordinates (min_row, min_col) of the bounding box.
      - id: extracted_subgrid
        description: The 4x4 section of the input grid that forms the output.
        relationship: Located at the `top_left_corner` of the `main_pattern`.
    ```


*   **Natural Language Program**:
    1.  Identify all non-white pixels (pixels with values 1 through 9) in the input grid.
    2.  Determine the bounding box that encloses all these non-white pixels. Find the minimum row index (`min_row`) and minimum column index (`min_col`) among these pixels. This defines the top-left corner of the bounding box.
    3.  Extract a 4x4 subgrid from the input grid, starting at the coordinates (`min_row`, `min_col`). This subgrid covers rows from `min_row` to `min_row + 3` and columns from `min_col` to `min_col + 3`.
    4.  The extracted 4x4 subgrid is the output grid.
