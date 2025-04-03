```python
import numpy as np
from collections import deque

"""
Identifies all distinct contiguous objects (groups of connected pixels of the same non-background color) 
in the input grid using 4-directional connectivity (up, down, left, right). 
It then determines the object with the largest size (most pixels). 
Finally, it creates an output grid of the same dimensions as the input, filled with the background color (white, 0), 
and copies only the pixels belonging to the largest identified object from the input grid onto the output grid, 
preserving their original color and location. If multiple objects share the same maximum size, 
any one of them may be chosen (the implementation picks the first one encountered during the scan).
"""

def _find_contiguous_objects(grid):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (row, col) tuples), and 'size'.
    """
    height, width = grid.shape
    visited = set()
    objects = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and (r, c) not in visited:
                # Start BFS for a new object
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    obj_pixels.append((curr_r, curr_c))

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, color match, and if visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'size': len(obj_pixels)
                })
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous non-background object.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid with only the largest object.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    background_color = 0

    # Initialize output grid with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Find all contiguous non-background objects
    objects = _find_contiguous_objects(grid_np)

    # If no objects found, return the empty grid
    if not objects:
        return output_grid.tolist() # Return as list of lists per ARC standard if needed

    # Find the largest object
    largest_object = None
    max_size = -1
    for obj in objects:
        if obj['size'] > max_size:
            max_size = obj['size']
            largest_object = obj
            
    # If a largest object was found (should always be true if objects is not empty)
    if largest_object:
        # Copy the pixels of the largest object to the output grid
        object_color = largest_object['color']
        for r, c in largest_object['pixels']:
            output_grid[r, c] = object_color

    # Return the output grid, converting back to list of lists if necessary
    # The ARC framework often expects list of lists.
    return output_grid.tolist() 

```