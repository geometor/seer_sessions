
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 7 0 7 0 0 0 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 0 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
0 7 0 7 0 0 7 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 6.0
