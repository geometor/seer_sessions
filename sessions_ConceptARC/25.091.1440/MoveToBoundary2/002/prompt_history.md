
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 7 0 0 0 7 0 0 7 0
0 7 0 0 0 7 0 0 7 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7
0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input/Output:** Both are grids of pixels, primarily white (0) with scattered orange (7) pixels.
2.  **Content:** The orange pixels form distinct shapes or objects (connected components). These objects can be single pixels, lines (vertical or horizontal), or more complex shapes.
3.  **Transformation:** The core transformation involves shifting the orange pixels either downwards or rightwards. The direction of the shift seems to depend on the overall characteristics of the orange shapes present in the input grid.
4.  **Shift Mechanism (Vertical):** When shifting downwards (as seen in examples 1 and 3), it appears to operate column by column. All orange pixels within a specific column are shifted down by the same amount. This amount is determined by the lowest orange pixel in that column; it's shifted so that it ends up on the bottom-most row of the grid. Columns without any orange pixels remain unchanged.
5.  **Shift Mechanism (Horizontal):** When shifting rightwards (as seen in example 2), it appears to operate row by row. All orange pixels within a specific row are shifted right by the same amount. This amount is determined by the rightmost orange pixel in that row; it's shifted so that it ends up in the rightmost column of the grid. Rows without any orange pixels remain unchanged.
6.  **Condition for Shift Direction:** The choice between vertical and horizontal shift seems related to the dominant orientation of the orange objects. By calculating the total height and total width of all distinct orange objects, we can determine the mode:
    *   If the sum of object heights is greater than or equal to the sum of object widths, vertical gravity is applied.
    *   If the sum of object heights is less than the sum of object widths, horizontal gravity is applied.

**YAML Facts:**


```yaml
Grid:
  Type: 2D Array
  Colors:
    - White (0): Background
    - Orange (7): Foreground Objects
Objects:
  Definition: Contiguous block of orange pixels (using 4-connectivity, not diagonal).
  Properties:
    - Position: (row, column) coordinates of constituent pixels.
    - Shape: Variable (pixels, lines, L-shapes, bars, etc.).
    - BoundingBox: Defined by min/max row and column indices.
    - Height: Max row - min row + 1
    - Width: Max col - min col + 1
Transformation:
  Type: Conditional Shift (Gravity)
  Condition:
    - Calculate TotalHeight = Sum of heights of all distinct orange objects.
    - Calculate TotalWidth = Sum of widths of all distinct orange objects.
    - If TotalHeight >= TotalWidth: Apply Vertical Gravity
    - If TotalHeight < TotalWidth: Apply Horizontal Gravity
  Actions:
    - Vertical Gravity:
        Scope: Per Column
        Rule: Shift all orange pixels in a column downwards.
        Shift Amount (for column c): `grid_height - 1 - max_row_index_of_orange_in_column_c`
        Result: Lowest orange pixel in each column moves to the bottom row.
    - Horizontal Gravity:
        Scope: Per Row
        Rule: Shift all orange pixels in a row rightwards.
        Shift Amount (for row r): `grid_width - 1 - max_col_index_of_orange_in_row_r`
        Result: Rightmost orange pixel in each row moves to the rightmost column.
  Output Grid:
    - Start with an all-white grid of the same dimensions as the input.
    - Place the shifted orange pixels onto this grid.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but with all pixels set to white (0).
2.  Identify all distinct orange (7) objects in the input grid, considering pixels connected horizontally or vertically (not diagonally) as part of the same object.
3.  For each identified orange object, calculate its height (number of rows it spans) and width (number of columns it spans).
4.  Sum the heights of all objects to get `TotalHeight`.
5.  Sum the widths of all objects to get `TotalWidth`.
6.  Determine the transformation direction based on the sums:
    *   **If `TotalHeight` is greater than or equal to `TotalWidth` (Vertical Gravity):**
        a.  Iterate through each column `c` from left to right (index 0 to `grid_width - 1`).
        b.  Find all orange pixels located in the current column `c` in the input grid.
        c.  If no orange pixels are found in this column, continue to the next column.
        d.  If orange pixels exist, find the maximum row index (`max_r`) among them.
        e.  Calculate the downward shift amount `s = grid_height - 1 - max_r`.
        f.  For every orange pixel originally at `(r, c)` in the input grid's column `c`, set the pixel at `(r + s, c)` in the output grid to orange (7).
    *   **If `TotalHeight
```python
import numpy as np
from collections import deque

"""
Identify all distinct orange (7) objects (4-connected components) in the input grid.
Calculate the total height and total width spanned by all orange objects.
If total height >= total width, apply vertical gravity:
  For each column, find the lowest orange pixel. Calculate the shift needed to move this pixel to the bottom row.
  Shift all orange pixels in that column down by this amount.
If total height < total width, apply horizontal gravity:
  For each row, find the rightmost orange pixel. Calculate the shift needed to move this pixel to the rightmost column.
  Shift all orange pixels in that row right by this amount.
The output grid contains only the shifted orange pixels on a white background.
"""

def find_objects(grid, color_to_find=7):
    """
    Finds all connected components of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color_to_find (int): The color of the objects to find.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'pixels': set of (row, col) tuples for the object's pixels.
              'min_r', 'max_r', 'min_c', 'max_c': Bounding box coordinates.
              'height': Height of the bounding box.
              'width': Width of the bounding box.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_to_find and (r, c) not in visited:
                # Start BFS to find a new object
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_pixels.add((r, c))
                min_r, max_r, min_c, max_c = r, r, c, c

                while q:
                    curr_r, curr_c = q.popleft()

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color_to_find and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))

                if obj_pixels:
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    objects.append({
                        'pixels': obj_pixels,
                        'min_r': min_r, 'max_r': max_r,
                        'min_c': min_c, 'max_c': max_c,
                        'height': height, 'width': width
                    })
    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies conditional gravity (vertical or horizontal) to orange objects in the grid.

    Args:
        input_grid (np.ndarray): The 2D input grid.

    Returns:
        np.ndarray: The transformed 2D output grid.
    """
    rows, cols = input_grid.shape
    orange_color = 7
    background_color = 0

    # Find all orange objects and their properties
    objects = find_objects(input_grid, orange_color)

    # Calculate total height and width
    total_height = sum(obj['height'] for obj in objects)
    total_width = sum(obj['width'] for obj in objects)

    # Initialize output grid with background color
    output_grid = np.full_like(input_grid, background_color)

    # Get all orange pixel coordinates from the input grid
    orange_pixels_input = np.argwhere(input_grid == orange_color) # list of [row, col]

    if not orange_pixels_input.size > 0: # Handle empty input grid case
        return output_grid

    # Determine gravity direction
    if total_height >= total_width:
        # Apply Vertical Gravity (column-wise)
        for c in range(cols):
            # Find orange pixels in this column
            col_pixels = orange_pixels_input[orange_pixels_input[:, 1] == c]
            if col_pixels.size > 0:
                # Find the lowest orange pixel in this column
                max_r = np.max(col_pixels[:, 0])
                # Calculate shift amount
                shift = rows - 1 - max_r
                # Apply shift to all orange pixels in this column
                for r, _ in col_pixels:
                    output_grid[r + shift, c] = orange_color
    else:
        # Apply Horizontal Gravity (row-wise)
        for r in range(rows):
            # Find orange pixels in this row
            row_pixels = orange_pixels_input[orange_pixels_input[:, 0] == r]
            if row_pixels.size > 0:
                # Find the rightmost orange pixel in this row
                max_c = np.max(row_pixels[:, 1])
                # Calculate shift amount
                shift = cols - 1 - max_c
                # Apply shift to all orange pixels in this row
                for _, c in row_pixels:
                    output_grid[r, c + shift] = orange_color

    return output_grid
```
