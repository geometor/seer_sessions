
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 1 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 0 0 0 0 0 1
1 1 1 1 1 1 1
```


## train_2

**input:**
```
0 0 0
0 0 0
0 3 0
0 0 0
0 0 0
```


**output:**
```
3 3 3
3 0 3
3 0 3
3 0 3
3 3 3
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 6
```


## train_4

**input:**
```
0 0 0
0 2 0
0 0 0
```


**output:**
```
2 2 2
2 0 2
2 2 2
```

*   **Perception:**
    *   Each input grid contains a single pixel of a non-white color against a white background.
    *   The output grid has the same dimensions as the input grid.
    *   The output grid features a solid frame around its border.
    *   The color of the frame in the output grid is the same as the color of the single non-white pixel in the input grid.
    *   All pixels inside the frame in the output grid are white, regardless of the original content of the input grid in those positions.

*   **Facts:**
    
```yaml
    task_type: construction
    input_features:
      - grid_dimensions: variable (height H, width W)
      - background_color: white (0)
      - foreground_objects:
          - count: 1
          - shape: single pixel
          - color: non-white (variable, let's call it C)
          - position: variable
    output_features:
      - grid_dimensions: same as input (H x W)
      - background_color: white (0) (only in the interior if H>2 and W>2)
      - foreground_objects:
          - count: 1
          - shape: hollow rectangle (frame)
          - color: C (same as the input foreground pixel color)
          - position: fills the border (row 0, row H-1, column 0, column W-1)
    transformation:
      - identify the color (C) of the single non-white pixel in the input.
      - create an output grid of the same dimensions as the input.
      - fill the border pixels (top row, bottom row, leftmost column, rightmost column) of the output grid with color C.
      - fill all interior pixels (if any) of the output grid with white (0).
    relationships:
      - the output grid dimensions match the input grid dimensions.
      - the color of the output frame matches the color of the single non-white pixel in the input.
    ```


*   **Natural Language Program:**
    1.  Identify the dimensions (Height H, Width W) of the input grid.
    2.  Scan the input grid to find the single pixel that is not white (0). Let its color be C.
    3.  Create a new grid of dimensions H x W for the output.
    4.  Fill the top row (row 0) of the output grid with color C.
    5.  Fill the bottom row (row H-1) of the output grid with color C.
    6.  Fill the leftmost column (column 0) of the output grid with color C.
    7.  Fill the rightmost column (column W-1) of the output grid with color C.
    8.  Fill all remaining interior pixels (from row 1 to H-2 and column 1 to W-2, if H > 2 and W > 2) with white (0).
