
## train_1

**input:**
```
1 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 2 0 0
0 2 0 0 2 0
0 0 2 0 0 2
2 0 0 2 0 0
0 2 0 0 2 0
0 0 2 0 0 2
```


**output:**
```
2 0 0 5 0 0
0 2 0 0 5 0
0 0 2 0 0 5
2 0 0 2 0 0
0 2 0 0 2 0
0 0 2 0 0 2
```


## train_3

**input:**
```
0 4 0 4 0 4
4 4 0 4 0 4
0 0 0 4 0 4
4 4 4 4 0 4
0 0 0 0 0 4
4 4 4 4 4 4
```


**output:**
```
0 5 0 4 0 4
5 5 0 4 0 4
0 0 0 4 0 4
4 4 4 4 0 4
0 0 0 0 0 4
4 4 4 4 4 4
```


## train_4

**input:**
```
0 8 8 8 0 0
8 8 0 0 0 8
0 0 0 8 8 8
0 8 8 8 0 0
8 8 0 0 0 8
0 0 0 8 8 8
```


**output:**
```
0 5 5 5 0 0
5 5 0 0 0 8
0 0 0 8 8 8
0 8 8 8 0 0
8 8 0 0 0 8
0 0 0 8 8 8
```

## Perception

The task involves transforming an input grid into an output grid of the same dimensions. The transformation selectively changes the color of one specific object within the grid to
```python
import numpy as np
from collections import deque

"""
Identifies the object containing the uppermost, leftmost non-white pixel in the input grid and changes the color of all pixels belonging to that object to gray (5). All other pixels remain unchanged. An object is defined as a contiguous group of pixels of the same non-white color, where contiguity includes diagonal adjacency.
"""

def find_connected_object(grid, start_row, start_col):
    """
    Finds all connected pixels of the same color as the starting pixel,
    using BFS (includes diagonal adjacency).

    Args:
        grid (np.array): The input grid.
        start_row (int): The row index of the starting pixel.
        start_col (int): The column index of the starting pixel.

    Returns:
        set: A set of (row, col) tuples representing the coordinates of the object's pixels.
             Returns an empty set if the starting pixel is white (0).
    """
    rows, cols = grid.shape
    target_color = grid[start_row, start_col]

    # If the starting pixel is white, it's not part of a colored object
    if target_color == 0:
        return set()

    object_pixels = set()
    queue = deque([(start_row, start_col)])
    visited = set([(start_row, start_col)])
    object_pixels.add((start_row, start_col))

    while queue:
        r, c = queue.popleft()

        # Check all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the center pixel itself
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc

                # Check bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor has the target color and hasn't been visited
                    if grid[nr, nc] == target_color and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        object_pixels.add((nr, nc))
                        queue.append((nr, nc))

    return object_pixels


def transform(input_grid):
    """
    Transforms the input grid by changing the color of the top-leftmost
    non-white object to gray (5).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    first_pixel_found = False
    object_coords = set()

    # Find the uppermost, leftmost non-white pixel
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0: # Found the first non-white pixel
                # Find all pixels belonging to the object connected to this pixel
                object_coords = find_connected_object(input_grid, r, c)
                first_pixel_found = True
                break # Stop searching columns
        if first_pixel_found:
            break # Stop searching rows

    # If an object was found, change its color to gray (5) in the output grid
    if object_coords:
        for r, c in object_coords:
            output_grid[r, c] = 5

    return output_grid
```
