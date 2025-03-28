
## train_1

**input:**
```
3 3 3
3 3 3
3 3 3
```


**output:**
```
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
0 0 0 3 0 0 0 3 0 0 0 3 0 0 0
```


## train_2

**input:**
```
8 8
8 8
```


**output:**
```
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
0 0 8 0 0 8 0 0 8 0 0 8 0 0 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
2 2 2 2
2 2 2 2
2 2 2 2
2 2 2 2
```


**output:**
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```

*   **Perception**:
    *   The input is always a square grid filled entirely with a single, non-white color. The size of the square grid varies across examples (3x3, 2x2, 4x4).
    *   The output is always a larger, fixed-size 15x15 grid.
    *   The output grid consists of a white background (color 0) overlaid with a grid pattern.
    *   The lines forming the grid pattern in the output use the same color as the input grid.
    *   The position and spacing of the grid lines in the output depend on the dimensions of the input grid. Specifically, if the input grid is NxN:
        *   The first horizontal and vertical lines appear at index N (0-based).
        *   Subsequent lines appear with a spacing of N+1 pixels.
        *   Lines extend across the entire width or height of the 15x15 output grid.
    *   Pixels where horizontal and vertical lines intersect take the line color.

*   **Facts**:
    
```yaml
    task_type: grid_transformation
    input_characteristics:
      - object: input_grid
        type: 2D array
        properties:
          - shape: square (NxN)
          - content: uniform color (C), where C is not white (0)
          - N: varies (e.g., 2, 3, 4)
          - C: varies (e.g., green=3, azure=8, red=2)
    output_characteristics:
      - object: output_grid
        type: 2D array
        properties:
          - shape: fixed square (15x15)
          - content: pattern composed of two colors
          - background_color: white (0)
          - line_color: C (same as input_grid color)
          - pattern: grid lines
    transformation:
      - type: pattern generation
      - description: Creates a grid pattern on a fixed-size canvas based on input properties.
    relationships:
      - output_grid.line_color is determined by input_grid.color(C)
      - output_grid line positions are determined by input_grid.size(N):
          - first_line_index: N
          - line_spacing: N + 1
      - The output grid dimensions (15x15) are constant regardless of input size.
    ```


*   **Natural Language Program**:
    1.  Identify the dimensions (N x N) of the input grid. Let N be the width/height.
    2.  Identify the uniform color (C) filling the input grid.
    3.  Create a new 15x15 grid, and initialize all its pixels to white (color 0). This will be the output grid.
    4.  Calculate the indices for the horizontal and vertical lines:
        a.  Start with the index `current_index = N`.
        b.  While `current_index` is less than 15:
            i.  Record `current_index` as a line index.
            ii. Add `N + 1` to `current_index`.
        c.  Store the set of calculated line indices.
    5.  Iterate through the calculated line indices:
        a.  For each index `r` in the set, set all pixels in row `r` of the output grid to color C.
        b.  For each index `c` in the set, set all pixels in column `c` of the output grid to color C.
    6.  The resulting 15x15 grid is the final output.
