
## train_1

**input:**
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 1 1 0 0 2 0
0 1 1 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 1 1 2 0
0 0 0 1 1 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```


## train_2

**input:**
```
0 0 0 0 2 0
0 1 0 0 2 0
0 1 1 0 2 0
0 1 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```


**output:**
```
0 0 0 0 2 0
0 0 1 0 2 0
0 0 1 1 2 0
0 0 1 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 1 1 0 2 0
0 0 1 1 0 0 2 0
0 0 0 1 1 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 1 1 2 0
0 0 0 1 1 0 2 0
0 0 0 0 1 1 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```


## train_4

**input:**
```
0 0 0 0 0 0
0 1 1 1 1 1
0 1 0 0 0 1
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 1 1 1 1 1
0 1 0 0 0 1
2 2 2 2 2 2
0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain three colors: white (0) as the background, blue (1) forming an object, and red (2) forming a line.
    *   The red object is always a straight line, either vertical or horizontal.
    *   The blue object is a distinct shape that does not touch the red line.
    *   In the output grid, the red line and the white background remain unchanged.
    *   The blue object moves its position. The shape of the blue object remains the same.
    *   The direction and distance of the blue object's movement seem to depend on the orientation of the red line and the relative position of the blue object to the red line.
    *   When the red line is vertical, the blue object moves 1 step horizontally away from the line (to the right in the examples).
    *   When the red line is horizontal, the blue object moves 2 steps vertically away from the line (downwards in the example).

*   **YAML Facts:**
    
```yaml
    task_description: Move a blue object away from a red line based on the line's orientation.
    elements:
      - object: background
        color: white (0)
        role: static_canvas
      - object: primary_shape
        color: blue (1)
        role: movable_object
        properties:
          - shape: variable (L-shape, plus, compound, U-shape in examples)
          - contiguity: contiguous block of blue pixels
      - object: constraint_line
        color: red (2)
        role: static_constraint
        properties:
          - shape: straight line (vertical or horizontal)
          - contiguity: contiguous block of red pixels
    relationships:
      - type: spatial
        description: The blue object is positioned relative to the red line (left/right or above/below).
      - type: interaction
        description: The red line dictates the movement of the blue object.
    actions:
      - action: identify_objects
        inputs: [input_grid]
        outputs: [blue_object_pixels, red_object_pixels]
      - action: determine_line_orientation
        inputs: [red_object_pixels]
        outputs: [orientation (vertical/horizontal)]
      - action: determine_relative_position
        inputs: [blue_object_pixels, red_object_pixels, orientation]
        outputs: [relative_pos (left/right/above/below)]
      - action: calculate_shift
        inputs: [orientation, relative_pos]
        outputs: [shift_vector (dx, dy)]
        logic:
          - if orientation is vertical, shift is (1, 0) if relative_pos is left, (-1, 0) if right.
          - if orientation is horizontal, shift is (0, 2) if relative_pos is above, (0, -2) if below.
      - action: apply_shift
        inputs: [input_grid, blue_object_pixels, shift_vector]
        outputs: [output_grid]
        logic: Create a new grid, copy the red line and background from the input, place the blue object at the shifted coordinates.
    ```


*   **Natural Language Program:**
    1.  Identify the set of coordinates occupied by the blue pixels (color 1) representing the blue object.
    2.  Identify the set of coordinates occupied by the red pixels (color 2) representing the red line.
    3.  Determine the orientation of the red line:
        *   If all red pixels share the same column index, the line is vertical.
        *   If all red pixels share the same row index, the line is horizontal.
    4.  Determine the shift vector (change in row `dy`, change in column `dx`):
        *   If the red line is vertical:
            *   Determine the column index of the red line (`red_col`).
            *   Find the average column index of the blue object pixels (`blue_avg_col`).
            *   If `blue_avg_col` < `red_col` (blue is left), set the shift vector to `(dx=1, dy=0)`.
            *   If `blue_avg_col` > `red_col` (blue is right), set the shift vector to `(dx=-1, dy=0)`.
        *   If the red line is horizontal:
            *   Determine the row index of the red line (`red_row`).
            *   Find the average row index of the blue object pixels (`blue_avg_row`).
            *   If `blue_avg_row` < `red_row` (blue is above), set the shift vector to `(dx=0, dy=2)`.
            *   If `blue_avg_row` > `red_row` (blue is below), set the shift vector to `(dx=0, dy=-2)`.
    5.  Create the output grid, identical in size to the input grid and initially filled with the background color (white, 0).
    6.  Copy the red line from the input grid to the output grid at its original position.
    7.  For each blue pixel at coordinate `(row, col)` in the input grid, place a blue pixel at `(row + dy, col + dx)` in the output grid.
```python
import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Moves a blue (1) object relative to a red (2) line.
If the red line is vertical, the blue object moves 1 step horizontally away from the line.
If the red line is horizontal, the blue object moves 2 steps vertically away from the line.
The red line and white (0) background remain unchanged.
"""

def find_object_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def determine_line_orientation_and_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[str, int]]:
    """
    Determines if the pixels form a vertical or horizontal line.
    Returns the orientation ('vertical' or 'horizontal') and the fixed coordinate (column or row index).
    Returns None if the pixels don't form a straight line or are empty.
    """
    if not pixels:
        return None

    rows = {r for r, c in pixels}
    cols = {c for r, c in pixels}

    if len(cols) == 1:
        # All pixels share the same column -> vertical line
        return 'vertical', list(cols)[0]
    elif len(rows) == 1:
        # All pixels share the same row -> horizontal line
        return 'horizontal', list(rows)[0]
    else:
        # Not a straight line
        return None

def calculate_average_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[float, float]]:
    """Calculates the average row and column index for a set of pixels."""
    if not pixels:
        return None
    
    avg_row = sum(r for r, c in pixels) / len(pixels)
    avg_col = sum(c for r, c in pixels) / len(pixels)
    return avg_row, avg_col

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by moving the blue object away from the red line.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Find blue and red pixels
    blue_pixels = find_object_pixels(input_grid, 1)
    red_pixels = find_object_pixels(input_grid, 2)

    # If no blue object or no red line, return the original grid
    if not blue_pixels or not red_pixels:
        return input_grid.copy() # Return a copy to avoid modifying original

    # Determine red line orientation and position
    line_info = determine_line_orientation_and_position(red_pixels)
    if line_info is None:
         # Red pixels don't form a line, return original
        return input_grid.copy()
    orientation, line_pos = line_info

    # Calculate average position of the blue object
    avg_blue_pos = calculate_average_position(blue_pixels)
    if avg_blue_pos is None: # Should not happen if blue_pixels is not empty
        return input_grid.copy()
    blue_avg_row, blue_avg_col = avg_blue_pos

    # Determine the shift vector (dx, dy)
    dx = 0
    dy = 0
    if orientation == 'vertical':
        red_col = line_pos
        # If blue object is to the left (smaller avg col), move right (dx=1)
        # If blue object is to the right (larger avg col), move left (dx=-1)
        dx = 1 if blue_avg_col < red_col else -1
        dy = 0
    elif orientation == 'horizontal':
        red_row = line_pos
        # If blue object is above (smaller avg row), move down (dy=2)
        # If blue object is below (larger avg row), move up (dy=-2)
        dy = 2 if blue_avg_row < red_row else -2
        dx = 0

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid)

    # Copy the red line from the input to the output
    for r, c in red_pixels:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 2

    # Apply the shift to the blue pixels and place them in the output grid
    for r, c in blue_pixels:
        new_r, new_c = r + dy, c + dx
        # Check bounds before placing the pixel
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = 1
        # else: pixel moves off grid - do nothing based on examples

    return output_grid
```
