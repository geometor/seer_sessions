
## train_1

**input:**
```
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
2 2 2 2 2 2
0 0 0 0 1 0
0 0 0 0 1 0
```


**output:**
```
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
2 2 2 2 1 2
0 0 0 0 1 0
0 0 0 0 1 0
```


## train_2

**input:**
```
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
4 3 4 4 4 4
0 3 0 0 0 0
0 3 0 0 0 0
```


**output:**
```
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
4 4 4 4 4 4
0 3 0 0 0 0
0 3 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 8 0
0 0 0 0 8 0
7 7 7 7 7 7
0 0 0 0 8 0
0 0 0 0 8 0
0 0 0 0 8 0
```


**output:**
```
0 0 0 0 8 0
0 0 0 0 8 0
7 7 7 7 8 7
0 0 0 0 8 0
0 0 0 0 8 0
0 0 0 0 8 0
```


## train_4

**input:**
```
0 8 0 0 0 0
5 8 5 5 5 5
0 8 0 0 0 0
5 5 5 5 5 5
0 8 0 0 0 0
0 8 0 0 0 0
```


**output:**
```
0 8 0 0 0 0
5 5 5 5 5 5
0 8 0 0 0 0
5 8 5 5 5 5
0 8 0 0 0 0
0 8 0 0 0 0
```

*   **Perception:** The input grids contain patterns resembling horizontal and vertical lines or structures against a white background. These structures intersect at specific points. The transformation modifies the color of the pixel at these intersection points. The rule for modification depends on the original color of the intersection pixel relative to the colors of the intersecting horizontal and vertical structures.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        attributes:
          - background_color: white (0)
      - object: horizontal_structure
        attributes:
          - located_in: row
          - color: dominant non-white color in the row (H_color)
      - object: vertical_structure
        attributes:
          - located_in: column
          - color: dominant non-white color in the column (V_color)
      - object: intersection_point
        attributes:
          - location: coordinates (r, c) where a horizontal structure in row r meets a vertical structure in column c
          - original_color: color of the pixel at (r, c) in the input grid
    relationships:
      - type: intersection
        between: [horizontal_structure, vertical_structure]
        at: intersection_point
    actions:
      - action: determine_structure_color
        on: [horizontal_structure, vertical_structure]
        details: Find the most frequent non-white color within the row/column.
      - action: modify_color
        on: intersection_point
        details: Change the color based on original_color, H_color, and V_color.
    transformation_rule:
      - condition: If original_color equals H_color
        effect: Change intersection_point color to V_color.
      - condition: If original_color equals V_color
        effect: Change intersection_point color to H_color.
      - condition: Otherwise (original_color is neither H_color nor V_color, e.g., background)
        effect: Change intersection_point color to V_color (vertical color takes precedence).
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all rows containing horizontal structures (rows with at least one non-white pixel). For each such row `r`, determine its characteristic horizontal color (`H_color`) by finding the most frequent non-white color in that row.
    3.  Identify all columns containing vertical structures (columns with at least one non-white pixel). For each such column `c`, determine its characteristic vertical color (`V_color`) by finding the most frequent non-white color in that column.
    4.  Iterate through every row `r` identified in step 2 and every column `c` identified in step 3. The cell at coordinates `(r, c)` is considered an intersection point.
    5.  For each intersection point `(r, c)`:
        a.  Retrieve the original color of this point from the input grid (`Original_color`).
        b.  Retrieve the horizontal color `H_color` associated with row `r`.
        c.  Retrieve the vertical color `V_color` associated with column `c`.
        d.  Compare `Original_color` with `H_color` and `V_color`.
        e.  If `Original_color` is the same as `H_color`, update the color of the cell `(r, c)` in the output grid to `V_color`.
        f.  Else if `Original_color` is the same as `V_color`, update the color of the cell `(r, c)` in the output grid to `H_color`.
        g.  Otherwise (if `Original_color` is neither `H_color` nor `V_color`), update the color of the cell `(r, c)` in the output grid to `V_color`.
```python
"""
Transformation Rule Natural Language Description:

1. Initialize the output grid as a copy of the input grid.
2. For each cell (r, c) in the grid:
   a. Determine the dominant non-white color (H_color) of row r. If row r contains only white (0), H_color is considered non-existent.
   b. Determine the dominant non-white color (V_color) of column c. If column c contains only white (0), V_color is considered non-existent.
   c. If both H_color and V_color exist, then the cell (r, c) is an intersection point.
   d. For each intersection point (r, c):
      i. Get the original color of this point from the input grid (Original_color).
      ii. If Original_color is the same as H_color, update the color of the cell (r, c) in the output grid to V_color.
      iii. Else if Original_color is the same as V_color, update the color of the cell (r, c) in the output grid to H_color.
      iv. Otherwise (if Original_color is neither H_color nor V_color, including if it's white), update the color of the cell (r, c) in the output grid to V_color.
3. Return the modified output grid.
"""

import numpy as np
from collections import Counter

def get_dominant_color(line: np.ndarray) -> int | None:
    """
    Finds the most frequent non-white (non-zero) color in a 1D numpy array (row or column).
    Returns the dominant color (int) or None if the line contains only white (0) pixels.
    If there's a tie for the most frequent non-white color, it returns one of the tied colors.
    """
    non_white_pixels = line[line != 0]
    if non_white_pixels.size == 0:
        return None  # No non-white pixels
    
    count = Counter(non_white_pixels)
    # most_common(1) returns a list of tuples [(element, count)]
    dominant_color, _ = count.most_common(1)[0]
    return int(dominant_color) # Ensure return type is int

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    At the intersection of a horizontal and a vertical structure, the color
    of the intersection pixel is modified based on its original color relative
    to the dominant colors of the intersecting structures.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = input_np.copy()
    height, width = input_np.shape

    # Pre-calculate dominant colors for all rows and columns to avoid redundant calculations
    h_colors = {}
    for r in range(height):
        h_color = get_dominant_color(input_np[r, :])
        if h_color is not None:
            h_colors[r] = h_color

    v_colors = {}
    for c in range(width):
        v_color = get_dominant_color(input_np[:, c])
        if v_color is not None:
            v_colors[c] = v_color

    # Iterate through potential intersection points
    for r in h_colors:
        for c in v_colors:
            # This cell (r, c) is an intersection point
            h_color = h_colors[r]
            v_color = v_colors[c]
            original_color = input_np[r, c]

            # Apply the transformation rule
            if original_color == h_color:
                output_np[r, c] = v_color
            elif original_color == v_color:
                 output_np[r, c] = h_color
            else:
                # Covers cases where original_color is background (0) or another color
                # The rule specifies to use V_color in the 'otherwise' case.
                 output_np[r, c] = v_color

    # Convert the result back to a list of lists
    return output_np.tolist()

```
