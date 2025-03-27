
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 5 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 0 3
0 0 0 0 0 3 0 3 5 3
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 5 2 0 2 5 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 0 2 0 2 0 2
0 2 0 2 5 2 0 2 5 2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 5 4 0 4 5
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 0 4 0
0 0 0 0 4 0 4 5 4 0
```

*   **Perception:**
    *   The input grid contains a single non-white pixel located somewhere along the bottom row.
    *   The output grid displays a repeating vertical pattern originating from the column of the input pixel.
    *   The pattern consists of solid vertical lines of the input pixel's color alternating with columns containing a single gray pixel.
    *   The vertical position of the gray pixel alternates between the top and bottom rows for successive gray columns.

*   **YAML Facts:**
    
```yaml
    task_description: Generate a vertical pattern based on a single input pixel.
    input_properties:
      - grid_size: 10x10 (constant across examples)
      - background_color: white (0)
      - objects:
          - name: trigger_pixel
            count: 1
            pixels:
              - location: bottom row (row 9)
              - color: varies (green, red, yellow in examples)
            properties:
              - defines the starting column (X) and pattern color (C)
    output_properties:
      - grid_size: 10x10 (same as input)
      - background_color: white (0)
      - generated_pattern:
          - starts_at_column: X (from trigger_pixel)
          - extends_to: right edge of the grid
          - columns:
              - type: colored_line
                column_indices: X, X+2, X+4, ... (within grid bounds)
                color: C (from trigger_pixel)
                fill: entire column
              - type: gray_marker
                column_indices: X+1, X+3, X+5, ... (within grid bounds)
                color: gray (5)
                location: alternates between top (row 0) and bottom (row 9)
                  - Top (row 0) for columns X+1, X+5, X+9, ...
                  - Bottom (row 9) for columns X+3, X+7, X+11, ...
                background: white (0) for the rest of the column
    relationship: The position and color of the single non-white pixel in the input determine the starting point, color, and structure of the vertical pattern in the output.
    ```


*   **Natural Language Program:**
    1.  Identify the single non-white pixel in the input grid. Let its color be `C` and its column index be `X`.
    2.  Create a new output grid of the same dimensions as the input grid, initially filled with white (0).
    3.  Iterate through the columns `j` from `X` to the last column index (width - 1).
    4.  Calculate the offset `offset = j - X`.
    5.  If `offset` is an even number (0, 2, 4, ...):
        *   Fill the entire column `j` of the output grid with color `C`.
    6.  If `offset` is an odd number (1, 3, 5, ...):
        *   Check the position for the gray pixel based on the offset:
            *   If `(offset // 2)` is an even number (meaning offset is 1, 5, 9, ...), set the pixel at row 0 and column `j` to gray (5).
            *   If `(offset // 2)` is an odd number (meaning offset is 3, 7, 11, ...), set the pixel at the last row (height - 1) and column `j` to gray (5).
