
## train_1

**input:**
```
0 0 0 0 0 0
1 1 1 1 1 0
0 0 0 0 0 0
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0
1 1 1 1 1 0
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
0 0 0 2 0 0
```


## train_2

**input:**
```
0 6 0 0 0 0
0 6 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 3 3 3 3 0
0 0 0 0 0 0
```


**output:**
```
0 6 0 0 0 0
0 6 0 0 0 0
0 6 0 0 0 0
0 6 0 0 0 0
3 3 3 3 3 0
0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 0 0
0 0 0 0 7 7
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 7 7
0 0 0 0 0 0
```


## train_4

**input:**
```
0 8 0 0 0 0
0 8 0 9 9 9
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 8 0 0 0 0
0 8 9 9 9 9
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception of Elements

1.  **Grid Structure:** The inputs and outputs are 2D grids of colored pixels (represented by integers 0-9). White (0) acts as the background.
2.  **Objects:** In each input grid, there are exactly two distinct non-white objects. These objects always appear to be straight lines, either perfectly horizontal or perfectly vertical. One line is always horizontal, and the other is always vertical.
3.  **Colors:** The lines have specific colors (blue, red, magenta, green, yellow, orange, azure, maroon) that are preserved from input to output.
4.  **Transformation:** The core transformation involves one of the two lines extending its length. The other line remains unchanged.
5.  **Extension Direction:** Vertical lines, when they extend, always extend downwards. Horizontal lines, when they extend, always extend rightwards.
6.  **Extension Trigger & Length:** The key is determining *which* line extends and by *how much*.
    *   It appears the horizontal line extends only if it is located entirely to the right of the vertical line (Example 4). In this case, it extends by one pixel to the right.
    *   In all other cases (horizontal line is left of, intersects, or touches the vertical line), the vertical line extends downwards.
    *   The length of the vertical extension depends on its position relative to the horizontal line:
        *   If the vertical line is entirely above the horizontal line, it extends downwards until it reaches the row immediately preceding the horizontal line's row (Examples 2 & 3).
        *   If the vertical line intersects, touches, or is entirely below the horizontal line, it extends downwards by exactly one pixel (Example 1).

## YAML Facts


```yaml
task_description: Identify a single vertical line and a single horizontal line in the input grid, then extend one of them based on their relative positions.

grid_properties:
  - background_color: white (0)
  - dimensions: variable (e.g., 6x6 in examples)

objects:
  - name: vertical_line
    count: 1
    properties:
      - shape: vertical line segment
      - color: non-white (variable, e.g., red, magenta, yellow, azure)
      - location: defined by a single column index and a range of row indices
  - name: horizontal_line
    count: 1
    properties:
      - shape: horizontal line segment
      - color: non-white (variable, different from vertical_line, e.g., blue, green, orange, maroon)
      - location: defined by a single row index and a range of column indices

relationships_and_actions:
  - relationship: relative_position
    between: [vertical_line, horizontal_line]
    types:
      - horizontal_line is entirely to the right of vertical_line column
      - horizontal_line is not entirely to the right (left of, intersects, touches)
      - vertical_line is entirely above horizontal_line row
      - vertical_line intersects, touches, or is below horizontal_line row
  - action: extend_line
    target: EITHER vertical_line OR horizontal_line (mutually exclusive)
    conditions_and_rules:
      - condition: horizontal_line is entirely to the right of vertical_line
        action_details:
          - target: horizontal_line
          - direction: rightwards
          - length: 1 pixel
      - condition: horizontal_line is NOT entirely to the right of vertical_line
        action_details:
          - target: vertical_line
          - direction: downwards
          - length:
              - if vertical_line is entirely above horizontal_line: extend until the row just before horizontal_line's row
              - otherwise: extend by 1 pixel

output_specification: A grid identical to the input, except for the extension applied to the selected line according to the rules. The color of the extended portion matches the color of the line being extended.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all contiguous non-white pixels belonging to the vertical line object. Record its color, its single column index (`C_v`), and its minimum and maximum row indices (`R_v_min`, `R_v_max`).
3.  Identify all contiguous non-white pixels belonging to the horizontal line object. Record its color, its single row index (`R_h`), and its minimum and maximum column indices (`C_h_min`, `C_h_max`).
4.  Check if the horizontal line is entirely to the right of the vertical line by comparing `C_h_min` and `C_v`.
5.  **If `C_h_min` is greater than `C_v`:**
    *   Determine the coordinates of the new pixel to add: (`R_h`, `C_h_max + 1`).
    *   Set the color of this pixel in the output grid to the color of the horizontal line.
6.  **Else (if `C_h_min` is less than or equal to `C_v`):**
    *   Check if the vertical line is entirely above the horizontal line by comparing `R_v_max` and `R_h`.
    *   **If `R_v_max` is less than `R_h`:**
        *   Iterate through the rows from `R_v_max + 1` up to `R_h - 1`.
        *   For each row `r` in this range, set the color of the pixel at (`r`, `C_v`) in the output grid to the color of the vertical line.
    *   **Else (if `R_v_max` is greater than or equal to `R_h`):**
        *   Determine the coordinates of the new pixel to add: (`R_v_max + 1`, `C_v`).
        *   Set the color of this pixel in the output grid to the color of the vertical line.
7.  Return the modified output grid.
```python
import numpy as np
from typing import Tuple, Dict, List, Optional

"""
Identifies a single vertical line and a single horizontal line in the input grid. 
Then, based on their relative positions, extends one of the lines.
- If the horizontal line is entirely to the right of the vertical line's column, the horizontal line extends one pixel to the right.
- Otherwise, the vertical line extends downwards. 
  - If the vertical line is entirely above the horizontal line's row, it extends down to the row just above the horizontal line.
  - Otherwise (if the vertical line intersects, touches, or is below the horizontal line), it extends down by exactly one pixel.
"""

def find_objects(grid: np.ndarray) -> List[Dict]:
    """
    Finds contiguous objects of the same non-background color in the grid.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    "color": color,
                    "pixels": obj_pixels,
                    "min_r": min_r,
                    "max_r": max_r,
                    "min_c": min_c,
                    "max_c": max_c,
                    "height": max_r - min_r + 1,
                    "width": max_c - min_c + 1
                })
    return objects


def find_lines(grid: np.ndarray) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Identifies the single vertical and single horizontal line among found objects.
    """
    objects = find_objects(grid)
    vertical_line = None
    horizontal_line = None

    for obj in objects:
        if obj['width'] == 1 and obj['height'] > 0: # Must have height > 0
             if vertical_line is None: # Take the first one found
                 vertical_line = obj
             else:
                 # Error handling/assumption check: should only be one vertical line
                 pass
        elif obj['height'] == 1 and obj['width'] > 0: # Must have width > 0
             if horizontal_line is None: # Take the first one found
                horizontal_line = obj
             else:
                 # Error handling/assumption check: should only be one horizontal line
                 pass
                 
    # Basic sanity check - ensure lines are not single points unless grid is 1x1 etc.
    # The logic width > 0 and height > 0 handles the case of single points being lines
    # but we rely on the problem constraints ensuring lines are actual lines of length > 0

    return vertical_line, horizontal_line


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the line extension transformation based on relative positions.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the vertical and horizontal lines
    vertical_line, horizontal_line = find_lines(input_grid)

    # Check if both lines were found (as expected by the problem description)
    if vertical_line is None or horizontal_line is None:
        # Should not happen based on examples, but return original grid if lines aren't found
        print("Warning: Could not find both a vertical and horizontal line.")
        return output_grid

    # Extract properties for easier access
    v_color = vertical_line['color']
    v_col = vertical_line['min_c'] # Since width is 1, min_c == max_c
    v_min_row = vertical_line['min_r']
    v_max_row = vertical_line['max_r']

    h_color = horizontal_line['color']
    h_row = horizontal_line['min_r'] # Since height is 1, min_r == max_r
    h_min_col = horizontal_line['min_c']
    h_max_col = horizontal_line['max_c']

    # Rule 1: Check if the horizontal line is entirely to the right of the vertical line
    if h_min_col > v_col:
        # Extend the horizontal line one pixel to the right
        extend_col = h_max_col + 1
        if extend_col < width: # Check boundary
            output_grid[h_row, extend_col] = h_color
    else:
        # Rule 2: Horizontal line is not entirely to the right, so extend the vertical line
        
        # Rule 2a: Check if the vertical line is entirely above the horizontal line
        if v_max_row < h_row:
            # Extend downwards until the row just before the horizontal line
            for r in range(v_max_row + 1, h_row):
                 if r < height: # Check boundary
                    output_grid[r, v_col] = v_color
        else:
            # Rule 2b: Vertical line intersects, touches, or is below the horizontal line
            # Extend downwards by exactly one pixel
            extend_row = v_max_row + 1
            if extend_row < height: # Check boundary
                 output_grid[extend_row, v_col] = v_color

    return output_grid
```
