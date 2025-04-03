
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

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are 2D grids (matrices) of digits. They appear to be 6x6 in all examples.
2.  **Grid Content:** The grids contain a background digit '0' and non-zero digits forming lines.
3.  **Structure:** Each input grid features exactly one continuous vertical line composed of a single non-zero digit and one or more continuous horizontal lines, each composed of a single non-zero digit.
4.  **Transformation Focus:** The changes between input and output occur exclusively at the intersection points where the vertical line crosses a horizontal line.
5.  **Change Rule:** The digit at an intersection point in the output grid is determined by comparing the digit present at that intersection in the input grid with the digits of the intersecting lines. Specifically, the digit at the intersection is *swapped* with the digit of the *other* line crossing that point. If the input intersection has the vertical line's digit, the output gets the horizontal line's digit, and vice-versa.

**YAML Facts:**


```yaml
task_description: Modify the values at the intersections of a single vertical line and one or more horizontal lines within a grid.
grid_properties:
  dimensions: 6x6
  background_value: 0
objects:
  - name: vertical_line
    properties:
      orientation: vertical
      continuity: continuous
      value: non-zero digit (V)
      location: specific column index (col_v)
  - name: horizontal_line
    properties:
      orientation: horizontal
      continuity: continuous
      value: non-zero digit (H)
      location: specific row index (row_h)
      count: one or more per grid
  - name: intersection
    properties:
      location: coordinates (row_h, col_v)
      input_value: input_grid[row_h][col_v] (will be either V or H)
      output_value: determined by the transformation rule
relationships:
  - type: intersects
    subject: vertical_line
    object: horizontal_line
    at: intersection point (row_h, col_v)
transformation_rule:
  - scope: operates only on intersection points
  - condition: Check the value at the intersection point in the input grid.
  - action:
      if input_value == value of horizontal_line (H):
        set output_value = value of vertical_line (V)
      elif input_value == value of vertical_line (V):
        set output_value = value of horizontal_line (H)
  - default: all non-intersection points remain unchanged.

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the vertical line: Find the column index (`col_v`) and the non-zero digit (`val_v`) that forms a continuous vertical line.
3.  Identify all horizontal lines: For each row, check if it contains a continuous horizontal line. Store the row index (`row_h`) and the non-zero digit (`val_h`) for each identified horizontal line.
4.  Iterate through each identified horizontal line (`row_h`, `val_h`).
5.  Determine the coordinates of the intersection point: `(row_h, col_v)`.
6.  Read the value at the intersection point from the *input* grid: `input_val = input_grid[row_h][col_v]`.
7.  Compare the `input_val` with the values of the intersecting lines (`val_h` and `val_v`).
8.  If `input_val` is equal to the horizontal line's value (`val_h`), update the *output* grid at the intersection `(row_h, col_v)` with the vertical line's value (`val_v`).
9.  If `input_val` is equal to the vertical line's value (`val_v`), update the *output* grid at the intersection `(row_h, col_v)` with the horizontal line's value (`val_h`).
10. After checking all intersections, return the modified output grid.
```python
"""
Transforms an input grid by identifying a single vertical line and one or more
horizontal lines. At each intersection point between the vertical line and a
horizontal line, the value at that point in the input grid is swapped:
if the intersection point initially holds the value of the horizontal line,
it's replaced with the value of the vertical line in the output grid, and
vice-versa. All other grid points remain unchanged.
"""

import numpy as np
import copy

def _find_vertical_line(grid):
    """Finds the column index and value of the single vertical line."""
    rows, cols = grid.shape
    for j in range(cols):
        column = grid[:, j]
        non_zeros = column[column != 0]
        unique_non_zeros = np.unique(non_zeros)
        # A vertical line is defined by having exactly one unique non-zero value
        if len(unique_non_zeros) == 1:
            return j, unique_non_zeros[0]
    return None, None # Should not happen based on problem description

def _find_horizontal_lines(grid):
    """Finds the row indices and values of all horizontal lines."""
    rows, cols = grid.shape
    h_lines = []
    for i in range(rows):
        row = grid[i, :]
        non_zeros = row[row != 0]
        unique_non_zeros = np.unique(non_zeros)
        # A horizontal line is defined by having exactly one unique non-zero value
        if len(unique_non_zeros) == 1:
            h_lines.append((i, unique_non_zeros[0]))
    return h_lines

def transform(input_grid):
    """
    Applies the intersection swap transformation to the input grid.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A new 2D numpy array with the transformation applied.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid)

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid_np)

    # Find the vertical line properties (column index, value)
    col_v, val_v = _find_vertical_line(input_grid_np)
    if col_v is None:
        # Handle case where no vertical line is found (though unlikely per problem)
        return output_grid

    # Find all horizontal lines properties (list of (row index, value))
    horizontal_lines = _find_horizontal_lines(input_grid_np)

    # Iterate through each identified horizontal line
    for row_h, val_h in horizontal_lines:
        # Determine the intersection point coordinates
        intersection_row = row_h
        intersection_col = col_v

        # Get the value at the intersection point in the *input* grid
        input_val = input_grid_np[intersection_row, intersection_col]

        # Apply the swap logic based on the input value at the intersection
        # Only swap if the intersection point actually contains one of the line values
        if input_val == val_h:
            # If input is horizontal value, output becomes vertical value
            output_grid[intersection_row, intersection_col] = val_v
        elif input_val == val_v:
            # If input is vertical value, output becomes horizontal value
            output_grid[intersection_row, intersection_col] = val_h
        # If input_val is 0 or some other unexpected value, it remains unchanged
        # due to the initial deep copy.

    return output_grid.tolist() # Convert back to list of lists if needed
```
