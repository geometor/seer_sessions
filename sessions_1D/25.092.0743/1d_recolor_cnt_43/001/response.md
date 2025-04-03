```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects composed of azure (8) pixels in the input grid.
Contiguous means sharing a side (horizontally or vertically).
For each azure object, count the number of pixels it contains (its size).
Recolor the object in the output grid based on its size according to the following map:
- Size 1: Change color to red (2).
- Size 2: Change color to blue (1).
- Size 3: Change color to magenta (6).
Objects of other sizes, if any, remain azure (8).
The background (white, 0) and the shape/position of objects are preserved.
"""

def find_connected_pixels(grid, start_row, start_col, target_color, visited):
    """
    Finds all connected pixels of a target color starting from a given point using BFS.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        target_color (int): The color of the pixels to find.
        visited (set): A set of (row, col) tuples already visited.

    Returns:
        list: A list of (row, col) tuples representing the connected component.
              Returns an empty list if the start pixel is not the target color
              or has already been visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_row < rows and 0 <= start_col < cols) or \
       grid[start_row, start_col] != target_color or \
       (start_row, start_col) in visited:
        return []

    object_pixels = []
    q = deque([(start_row, start_col)])
    visited.add((start_row, start_col))

    while q:
        r, c = q.popleft()
        object_pixels.append((r, c))

        # Check orthogonal neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, target color, and if visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == target_color and \
               (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))

    return object_pixels


def transform(input_grid):
    """
    Transforms the input grid by recoloring azure (8) objects based on their size.
    Size 1 -> Red (2)
    Size 2 -> Blue (1)
    Size 3 -> Magenta (6)
    Other sizes remain azure (8).

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = input_np.copy()
    rows, cols = input_np.shape
    
    # Keep track of pixels already processed as part of an object
    visited = set()
    
    # Define the target color to find objects of
    target_color = 8
    
    # Define the mapping from object size to output color
    color_map = {
        1: 2,  # Size 1 -> Red
        2: 1,  # Size 2 -> Blue
        3: 6   # Size 3 -> Magenta
    }

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is the target color and hasn't been visited yet
            if input_np[r, c] == target_color and (r, c) not in visited:
                # Find all connected pixels forming the object starting from (r, c)
                current_object_pixels = find_connected_pixels(input_np, r, c, target_color, visited)
                
                # If an object was found (should always be true if we enter here)
                if current_object_pixels:
                    object_size = len(current_object_pixels)
                    
                    # Determine the output color based on the object's size
                    # If the size is not in the map, default to the original target color
                    output_color = color_map.get(object_size, target_color)
                    
                    # Recolor all pixels belonging to this object in the output grid
                    for obj_r, obj_c in current_object_pixels:
                        output_grid[obj_r, obj_c] = output_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()

```