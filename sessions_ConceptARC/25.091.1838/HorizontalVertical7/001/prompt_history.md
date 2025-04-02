
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
    *   Each input grid contains a background of white pixels (0).
    *   Within the background, there is a larger shape composed of a non-white, non-red color (azure - 8, yellow - 4, green - 3).
    *   Inside this larger shape, there are exactly two red pixels (2).
    *   The transformation depends on the relative positions of these two red pixels.
    *   If the two red pixels share the same column index, the first column of the output grid is filled entirely with red pixels. The rest of the output grid matches the input grid. (Examples 1 & 2)
    *   If the two red pixels share the same row index, the first row of the output grid is filled entirely with red pixels. The rest of the output grid matches the input grid. (Example 3)
    *   The original colors and positions of all other pixels (excluding the first row/column modification) are preserved in the output.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    components:
      - role: background
        color: white (0)
        location: surrounds the main shape
      - role: main_shape
        color: variable (azure, yellow, green)
        description: a contiguous block of non-white, non-red pixels
        location: within the background
      - role: key_pixels
        color: red (2)
        count: 2
        location: inside the main_shape
        relationship: their relative positions (same row or same column) determine the output modification
    transformation:
      condition:
        - check: if the two red pixels share the same column index
          action: fill the first column (index 0) of the output grid with red (2)
        - check: if the two red pixels share the same row index
          action: fill the first row (index 0) of the output grid with red (2)
      preserve_content: all pixels from the input grid are copied to the output grid, except for the modified first row or first column.
    grid_properties:
      size: input and output grids have the same dimensions.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the initial output grid.
    2.  Identify the coordinates (row and column indices) of all red pixels (color 2) in the input grid. There will be exactly two such pixels. Let their coordinates be (r1, c1) and (r2, c2).
    3.  Compare the row indices: check if r1 is equal to r2.
    4.  Compare the column indices: check if c1 is equal to c2.
    5.  If the column indices are the same (c1 == c2), modify the output grid by setting all pixels in the first column (column index 0) to red (2).
    6.  If the row indices are the same (r1 == r2), modify the output grid by setting all pixels in the first row (row index 0) to red (2).
    7.  Return the modified output grid.
