
Previous Code:
```python
"""
Transforms the input grid by removing non-background objects that touch the absolute border of the grid. 
An object is defined as a contiguous group of pixels of the same non-zero color (non-white), using 4-way connectivity.
A pixel touches the border if its row index is 0 or the maximum row index (height - 1), or its column index is 0 or the maximum column index (width - 1). 
If any pixel of an object touches the border, the entire object is removed (replaced with the background color 0 - white) in the output grid. 
Objects that do not touch any border remain unchanged. The output grid has the same dimensions as the input grid.
"""

import numpy as np
from collections import deque

def find_object(grid, start_row, start_col, visited):
    """
    Finds a connected object of the same color starting from (start_row, start_col) 
    using Breadth-First Search (BFS). Marks visited pixels for the found object 
    within the provided visited array.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        visited (np.array): A boolean grid indicating visited pixels (modified in place).

    Returns:
        tuple: (list of pixel coordinates [(r, c), ...], boolean indicating if it touches border)
               Returns (None, False) if the starting pixel is background (color 0) or 
               has already been visited as part of another object search.
    """
    rows, cols = grid.shape
    
    # Check if the starting point is out of bounds
    if not (0 <= start_row < rows and 0 <= start_col < cols):
        return None, False
        
    # Check if already visited or is background color (color 0)
    if visited[start_row, start_col] or grid[start_row, start_col] == 0:
        # Mark as visited if not already (e.g., if it's background) 
        # to avoid redundant checks by the caller.
        visited[start_row, start_col] = True 
        return None, False

    # Start BFS to find the connected component (object)
    color = grid[start_row, start_col]
    q = deque([(start_row, start_col)])
    object_pixels = []
    touches_border = False
    visited[start_row, start_col] = True # Mark the starting pixel as visited

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check if this pixel touches the absolute border (top, bottom, left, or right edge)
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            touches_border = True # Set the flag; it stays true if any part touches

        # Explore neighbors using 4-connectivity (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                 # Check if neighbor has the same color as the object and hasn't been visited yet
                if not visited[nr, nc] and grid[nr, nc] == color:
                    visited[nr, nc] = True # Mark visited when adding to queue to prevent cycles/revisits
                    q.append((nr, nc))

    # Return the list of pixels in the object and whether it touched the border
    return object_pixels, touches_border


def transform(input_grid):
    """
    Transforms the input grid according to the rule described in the module docstring.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid. 
    # Objects that are not removed will implicitly remain.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Keep track of visited pixels during object finding to ensure each pixel
    # is processed only once as part of exactly one object search.
    visited = np.zeros_like(input_grid, dtype=bool)

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If the pixel hasn't been visited yet (this check implicitly skips background
            # pixels after they are visited once by find_object, and prevents starting 
            # multiple searches for the same object)
            if not visited[r, c]:
                # Attempt to find an object starting from this pixel.
                # find_object handles checking if it's background (color 0), returning None.
                # It updates the 'visited' array for all pixels it processes (object or background).
                object_pixels, touches_border = find_object(input_grid, r, c, visited)
                
                # Check if a valid object was found (object_pixels is not None) 
                # AND this object touches the border
                if object_pixels is not None and touches_border:
                    # If the object touches the border, erase it from the output grid 
                    # by setting all its pixels to the background color (white, 0).
                    for pr, pc in object_pixels:
                        output_grid[pr, pc] = 0
                # No explicit 'else' is needed:
                # - If object_pixels is None, it was background or already visited; find_object marked it visited.
                # - If object_pixels is not None but touches_border is False, the object should
                #   remain unchanged, which it does because output_grid started as a copy.

    # Return the final modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 8 0 0 0
0 2 2 2 0 8 8 8 0 0
0 2 2 2 0 0 8 8 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 5 5 5 0
0 0 1 1 1 0 0 5 5 0
0 0 1 1 1 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 5 5 5 0
0 0 1 1 1 0 0 5 5 0
0 0 1 1 1 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 32.0

## Example 2:
Input:
```
6 6 0 0 0 0 4 4
0 0 0 0 0 0 4 4
0 0 4 0 0 0 4 4
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
7 7 0 0 0 2 0 0
7 7 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0
0 4 4 4 0 0 0 0
0 0 4 0 0 2 0 0
0 0 0 0 2 2 2 0
0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0
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
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 7 7 7 0
0 3 3 3 0 7 7 7 0
0 0 3 0 0 7 7 7 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 3 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 7 7 7 0 3 3 3 0
0 0 7 0 0 0 3 0 0
0 7 7 7 0 3 3 3 0
0 0 0 0 0 7 7 7 0
0 3 3 3 0 7 7 7 0
0 0 3 0 0 7 7 7 0
0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 22.22222222222223
