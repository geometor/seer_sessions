
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 4 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 2 2 2 2 0
0 0 0 0 0 2 2 2 2 0
0 0 0 0 4 0 0 0 0 4
```

*   **Perception:**
    *   The input and output grids have the same dimensions.
    *   The grids contain white (0), yellow (4), and red (2) pixels. White acts as the background.
    *   In the input grids, there are sets of four yellow pixels arranged at the corners of rectangles.
    *   The output grids retain the original yellow pixels from the input.
    *   Additionally, the output grids contain red pixels that fill the rectangular area strictly *inside* the boundaries defined by each set of four yellow corner pixels.
    *   If the area inside a rectangle defined by yellow corners is empty (i.e., the corners are adjacent either horizontally or vertically), no red pixels are added for that rectangle.
    *   There can be multiple, non-overlapping sets of yellow corners and corresponding red filled areas within a single grid.

*   **Facts:**
    
```yaml
    task_description: "Fill the interior area defined by rectangular arrangements of four yellow pixels with red pixels."
    elements:
      - element: "grid"
        description: "A 2D array of pixels representing colors."
        properties:
          - size: "Variable height and width (up to 30x30)."
          - background_color: "white (0)"
      - element: "pixel"
        description: "A single cell within the grid."
        properties:
          - color: "An integer from 0 to 9, mapped to specific colors."
      - element: "marker_pixel"
        description: "A yellow (4) pixel in the input grid."
        properties:
          - color: "yellow (4)"
      - element: "marker_set"
        description: "A set of four yellow pixels forming the corners of a rectangle."
        properties:
          - count: 4
          - arrangement: "Rectangular corners, e.g., (r1, c1), (r1, c2), (r2, c1), (r2, c2)"
      - element: "fill_pixel"
        description: "A red (2) pixel added to the output grid."
        properties:
          - color: "red (2)"
      - element: "filled_area"
        description: "A rectangular region filled with red pixels in the output grid."
        properties:
          - boundary: "Defined by a marker_set."
          - location: "Strictly inside the boundary defined by the marker_set."
    relationships:
      - type: "defines"
        source: "marker_set"
        target: "filled_area"
        details: "The four yellow pixels of a marker_set define the boundaries of the area to be filled."
      - type: "contains"
        source: "output grid"
        target: "marker_pixel"
        details: "All original yellow marker pixels from the input are present in the output."
      - type: "contains"
        source: "output grid"
        target: "fill_pixel"
        details: "Red fill pixels are added to the output grid within the defined filled_area."
    actions:
      - action: "identify"
        actor: "system"
        target: "marker_set"
        details: "Locate all sets of four yellow pixels forming rectangles in the input grid."
      - action: "calculate_bounds"
        actor: "system"
        input: "marker_set"
        output: "min_row, max_row, min_col, max_col"
        details: "Determine the minimum and maximum row and column indices for the rectangle defined by a marker_set."
      - action: "fill"
        actor: "system"
        target: "grid cells"
        details: "Change the color of specific grid cells to red (2)."
        condition: "Cells must be within the calculated bounds (row > min_row, row < max_row, col > min_col, col < max_col)."
      - action: "copy"
        actor: "system"
        source: "input grid"
        target: "output grid"
        details: "Initialize the output grid as a copy of the input grid before filling."
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Find all yellow (4) pixels in the input grid.
    3.  Identify all unique sets of four yellow pixels that form the corners of a rectangle. Let the corners of one such rectangle be `(r1, c1)`, `(r1, c2)`, `(r2, c1)`, and `(r2, c2)`, where `r1` and `r2` are the row indices and `c1` and `c2` are the column indices.
    4.  For each identified rectangle:
        a.  Determine the minimum row (`min_r = min(r1, r2)`), maximum row (`max_r = max(r1, r2)`), minimum column (`min_c = min(c1, c2)`), and maximum column (`max_c = max(c1, c2)`).
        b.  Iterate through all grid cells `(r, c)`.
        c.  If a cell's row `r` is strictly greater than `min_r` and strictly less than `max_r`, AND its column `c` is strictly greater than `min_c` and strictly less than `max_c`, change the color of that cell `(r, c)` in the output grid to red (2).
    5.  Return the modified output grid.
