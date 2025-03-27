
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 0 0 0
3 3 3 3 3 0 0 0 0
3 3 3 3 0 0 0 0 0
2 2 2 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 2 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 0 0
3 3 3 3 0 0 0
3 3 3 0 0 0 0
2 2 0 0 0 0 0
1 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 0 0 0
3 3 3 3 3 0 0 0 0
2 2 2 2 0 0 0 0 0
1 1 1 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain a single horizontal line of red pixels (color 2) against a white background (color 0). The line always starts at the leftmost column (column 0).
    *   The output grids retain the original red line and the grid dimensions.
    *   Two new shapes are added to the output grid:
        *   A green shape (color 3) appears above the red line. It resembles a right-angled triangle with its right angle at the top-left corner relative to the shape itself. Its base sits one row above the red line, and it extends upwards and rightwards. The width of the green shape increases by one pixel for each row further up from the red line.
        *   A blue shape (color 1) appears below the red line. It resembles a right-angled triangle with its right angle at the bottom-left corner relative to the shape itself. Its top sits one row below the red line, and it extends downwards and leftwards (though it always starts at column 0). The width of the blue shape decreases by one pixel for each row further down from the red line.
    *   The sizes and specific positions of the green and blue shapes are determined by the position and length of the original red line.

*   **Facts:**
    
```yaml
    elements:
      - object: input_grid
        description: A 2D grid of pixels, primarily white (0).
      - object: red_line
        description: A single contiguous horizontal line of red pixels (2) within the input_grid.
        properties:
          - color: 2 (red)
          - orientation: horizontal
          - contiguity: contiguous pixels
          - location: defined by a starting row (R) and columns (C to C+L-1). Observed C is always 0.
          - length: L (number of red pixels)
      - object: output_grid
        description: A 2D grid of pixels, same dimensions as input_grid. Contains the original red_line plus added shapes.
        properties:
          - dimensions: same height and width as input_grid
      - object: green_shape
        description: A shape made of green pixels (3) added to the output_grid above the red_line.
        properties:
          - color: 3 (green)
          - location: occupies rows 0 to R-1.
          - geometry: In row 'r' (where r < R), it occupies columns 0 to (L + R - r - 1). Forms a triangle-like shape expanding upwards and rightwards.
        relationship: Anchored vertically above the red_line, starting horizontally at column 0. Its dimensions depend on the red_line's length (L) and row (R).
      - object: blue_shape
        description: A shape made of blue pixels (1) added to the output_grid below the red_line.
        properties:
          - color: 1 (blue)
          - location: occupies rows starting from R+1 downwards.
          - geometry: In row 'r' (where r > R), it occupies columns 0 to (L - (r - R) - 1), provided the number of columns is positive. Forms a triangle-like shape shrinking downwards, starting from column 0.
        relationship: Anchored vertically below the red_line, starting horizontally at column 0. Its dimensions depend on the red_line's length (L) and row (R).
    actions:
      - action: identify
        actor: self
        target: red_line
        purpose: Find the location (row R, starting column C) and length (L) of the horizontal red line in the input_grid. (Note: C is always 0 in examples).
      - action: copy
        actor: self
        source: input_grid
        target: output_grid
        purpose: Initialize the output_grid as a copy of the input_grid.
      - action: draw
        actor: self
        target: output_grid
        object: green_shape
        parameters: R, L
        purpose: Add green pixels (3) to the output_grid in rows 0 to R-1. For each row 'r', fill columns 0 to (L + R - r - 1).
      - action: draw
        actor: self
        target: output_grid
        object: blue_shape
        parameters: R, L
        purpose: Add blue pixels (1) to the output_grid in rows R+1 downwards. For each row 'r', fill columns 0 to (L - (r - R) - 1), stopping when the calculated width is zero or less.
    ```


*   **Natural Language Program:**
    1.  Create the output grid by copying the input grid.
    2.  Identify the horizontal red line (color 2) in the input grid. Determine its row index `R`, its starting column index `C` (which is 0), and its length `L`.
    3.  Generate the green shape (color 3) above the red line: Iterate through each row `r` from 0 up to `R - 1`. In each row `r`, change the color of the pixels from column 0 up to column `C + L + R - r - 1` (inclusive) to green (3).
    4.  Generate the blue shape (color 1) below the red line: Iterate through each row `r` starting from `R + 1` downwards, continuing as long as the calculated width is positive. Calculate the width for the current row `r` as `width = L - (r - R)`. If `width > 0`, change the color of the pixels in row `r` from column `C` (which is 0) up to column `C + width - 1` (inclusive) to blue (1). If `width <= 0`, stop adding blue pixels for this and subsequent rows.
    5.  Return the modified output grid.
