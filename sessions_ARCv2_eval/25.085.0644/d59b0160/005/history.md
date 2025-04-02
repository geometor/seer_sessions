
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies contiguous objects (using 8-directional connectivity) of non-background colors (not orange/7). 
An object is removed (replaced with the background color orange/7) if it meets two conditions:
1. It contains at least one white (0) pixel.
2. It does not touch any of the four borders of the grid.
Objects that do not meet both conditions remain unchanged.
"""

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid using 8-directional connectivity.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a single object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    # Define 8 directions (including diagonals)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(rows):
        for c in range(cols):
            # If the pixel is not background and not visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the object
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check all 8 neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc

                        # Check grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # If neighbor is part of the object (not background) and not visited
                            if grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                current_object.add((nr, nc))

                if current_object:
                    objects.append(current_object)
    return objects

def contains_color(grid, obj_coords, color_to_check):
    """Checks if any pixel in the object has the specified color."""
    for r, c in obj_coords:
        # Check bounds just in case, though obj_coords should be valid
        if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
            if grid[r, c] == color_to_check:
                return True
    return False

def touches_border(obj_coords, grid_shape):
    """Checks if any pixel in the object touches the grid border."""
    rows, cols = grid_shape
    for r, c in obj_coords:
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            return True
    return False

def transform(input_grid):
    """
    Applies the transformation rule: removes non-border-touching objects 
    containing white pixels by replacing them with the background color.
    """
    # Convert input list of lists to numpy array
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = grid.copy()
    rows, cols = grid.shape
    background_color = 7 # Orange
    white_color = 0      # White

    # Find all distinct objects (contiguous non-background pixels using 8-connectivity)
    objects = find_objects(grid, background_color)

    # Iterate through each found object
    for obj_coords in objects:
        # Check condition 1: Does the object contain white?
        has_white = contains_color(grid, obj_coords, white_color)

        # Check condition 2: Does the object touch the border?
        touches = touches_border(obj_coords, (rows, cols))

        # Apply the rule: If object contains white AND does NOT touch the border, remove it
        if has_white and not touches:
            # Replace object pixels with background color in the output grid
            for r, c in obj_coords:
                # Ensure coordinates are valid before writing (safety check)
                 if 0 <= r < rows and 0 <= c < cols:
                    output_grid[r, c] = background_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
4 7 1 3 7 7 7 9 6 4 7 7 7 7 7 7
7 7 7 3 7 7 7 4 5 9 7 7 0 0 0 7
2 7 7 3 7 7 7 0 0 0 7 7 0 4 0 7
3 3 3 3 7 7 7 0 0 0 7 7 0 0 1 7
7 7 7 7 7 7 7 6 5 0 7 7 0 2 0 7
7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7
7 7 7 0 0 0 0 9 0 0 5 7 7 7 7 7
7 7 7 0 0 9 0 2 9 0 0 7 7 7 0 0
7 7 7 2 0 0 0 0 0 0 0 7 7 7 1 4
7 7 7 0 0 1 0 4 0 0 8 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
0 0 0 0 0 0 0 1 7 0 0 0 0 7 0 0
9 5 0 9 0 0 8 6 7 9 0 0 8 7 6 0
0 4 2 6 0 0 0 0 7 0 6 0 5 7 0 0
2 0 0 0 6 0 0 0 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 2 2 0 7 0 8
```
Expected Output:
```
4 7 1 3 7 7 7 9 6 4 7 7 7 7 7 7
7 7 7 3 7 7 7 4 5 9 7 7 7 7 7 7
2 7 7 3 7 7 7 0 0 0 7 7 7 7 7 7
3 3 3 3 7 7 7 0 0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 6 5 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 4
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 9 0 0 8 7 6 0
7 7 7 7 7 7 7 7 7 0 6 0 5 7 0 0
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 2 2 0 7 0 8
```
Transformed Output:
```
4 7 1 3 7 7 7 9 6 4 7 7 7 7 7 7
7 7 7 3 7 7 7 4 5 9 7 7 7 7 7 7
2 7 7 3 7 7 7 0 0 0 7 7 7 7 7 7
3 3 3 3 7 7 7 0 0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 6 5 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 4
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
0 0 0 0 0 0 0 1 7 0 0 0 0 7 0 0
9 5 0 9 0 0 8 6 7 9 0 0 8 7 6 0
0 4 2 6 0 0 0 0 7 0 6 0 5 7 0 0
2 0 0 0 6 0 0 0 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 2 2 0 7 0 8
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.0

## Example 2:
Input:
```
7 9 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 3 7 7 0 0 0 7 7 7 0 0 0 7
5 7 6 3 7 7 1 0 0 7 7 7 6 0 4 7
3 3 3 3 7 7 0 5 0 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 9 0 7
7 7 7 7 7 7 2 0 6 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 8 0 7
7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 1 0 0 0 7 7 7 7 7 7 7 7
7 0 0 0 0 0 5 0 7 7 7 7 7 7 7 7
7 0 9 0 8 0 0 0 7 7 7 0 0 0 0 9
7 0 0 0 0 0 4 0 7 7 7 0 6 0 0 0
7 0 2 0 4 0 0 0 7 7 7 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7 7 0 0 5 1 0
7 7 7 7 7 7 7 7 7 7 7 8 0 0 0 0
```
Expected Output:
```
7 9 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 3 7 7 0 0 0 7 7 7 0 0 0 7
5 7 6 3 7 7 1 0 0 7 7 7 6 0 4 7
3 3 3 3 7 7 0 5 0 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 9 0 7
7 7 7 7 7 7 2 0 6 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 8 0 7
7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 1 0 0 0 7 7 7 7 7 7 7 7
7 0 0 0 0 0 5 0 7 7 7 7 7 7 7 7
7 0 9 0 8 0 0 0 7 7 7 7 7 7 7 7
7 0 0 0 0 0 4 0 7 7 7 7 7 7 7 7
7 0 2 0 4 0 0 0 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
7 9 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 3 7 7 7 7 7 7 7 7 7 7 7 7
5 7 6 3 7 7 7 7 7 7 7 7 7 7 7 7
3 3 3 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 9
7 7 7 7 7 7 7 7 7 7 7 0 6 0 0 0
7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7 7 0 0 5 1 0
7 7 7 7 7 7 7 7 7 7 7 8 0 0 0 0
```
Match: False
Pixels Off: 99
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 77.34375

## Example 3:
Input:
```
7 6 7 3 7 7 7 7 7 7 7 7 7 7 7 7
1 7 7 3 7 7 7 0 8 0 0 0 5 0 0 0
7 7 8 3 7 7 7 0 5 0 0 6 0 0 0 0
3 3 3 3 7 7 7 4 0 0 0 0 0 8 0 0
7 7 7 7 7 7 7 9 0 0 6 0 0 0 4 0
7 0 0 0 0 0 7 0 0 0 0 5 9 0 5 0
7 5 2 2 0 0 7 9 0 0 0 0 8 0 0 0
7 0 0 1 0 0 7 1 0 0 2 0 0 0 0 6
7 0 0 5 5 0 7 7 7 7 7 7 7 7 7 7
7 0 0 0 9 0 7 7 7 0 9 0 0 7 7 7
7 0 0 0 6 0 7 7 7 0 0 0 0 7 7 7
7 7 7 7 7 7 7 7 7 8 0 0 0 7 7 7
7 7 6 1 0 0 0 0 7 0 0 0 0 7 0 0
7 7 0 2 0 0 0 0 7 0 0 0 0 7 0 0
7 7 0 8 0 0 0 0 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```
Expected Output:
```
7 6 7 3 7 7 7 7 7 7 7 7 7 7 7 7
1 7 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 8 3 7 7 7 7 7 7 7 7 7 7 7 7
3 3 3 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7
7 5 2 2 0 0 7 7 7 7 7 7 7 7 7 7
7 0 0 1 0 0 7 7 7 7 7 7 7 7 7 7
7 0 0 5 5 0 7 7 7 7 7 7 7 7 7 7
7 0 0 0 9 0 7 7 7 0 9 0 0 7 7 7
7 0 0 0 6 0 7 7 7 0 0 0 0 7 7 7
7 7 7 7 7 7 7 7 7 8 0 0 0 7 7 7
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```
Transformed Output:
```
7 6 7 3 7 7 7 7 7 7 7 7 7 7 7 7
1 7 7 3 7 7 7 0 8 0 0 0 5 0 0 0
7 7 8 3 7 7 7 0 5 0 0 6 0 0 0 0
3 3 3 3 7 7 7 4 0 0 0 0 0 8 0 0
7 7 7 7 7 7 7 9 0 0 6 0 0 0 4 0
7 7 7 7 7 7 7 0 0 0 0 5 9 0 5 0
7 7 7 7 7 7 7 9 0 0 0 0 8 0 0 0
7 7 7 7 7 7 7 1 0 0 2 0 0 0 0 6
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```
Match: False
Pixels Off: 113
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 176.5625
