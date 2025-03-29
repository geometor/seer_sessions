```python
import numpy as np
from collections import deque

"""
Identify all connected objects of the same non-white color in the input grid.
Calculate the area (number of pixels) for each object.
Find the object with the largest area.
Extract the bounding box containing the largest object.
Create an output grid with the dimensions of the bounding box.
Copy the largest object into the output grid, preserving its shape and relative position within the bounding box, using the original color. Fill the rest of the output grid with white (0).
"""

def find_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start BFS to find a connected object
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_pixels.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_bounding_box(obj_pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        obj_pixels (set): A set of (row, col) tuples representing an object.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if no pixels.
    """
    if not obj_pixels:
        return None
    
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Identifies the largest object of a single non-white color in the input grid
    and extracts it into a new grid representing its bounding box.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Find the non-white color present in the grid
    unique_colors = np.unique(grid)
    target_color = -1
    for color in unique_colors:
        if color != 0:
            target_color = color
            break
            
    if target_color == -1:
        # Handle case with only background color or empty grid
        # Based on examples, this shouldn't happen, but good practice.
        # Returning an empty grid or a 1x1 white grid might be options.
        # Let's return a 1x1 white grid for now.
         return [[0]] 

    # Find all objects of the target color
    objects = find_objects(grid, target_color)
    
    if not objects:
        # No objects of the target color found
         return [[0]]

    # Find the object with the largest area (most pixels)
    largest_object = max(objects, key=len)
    
    # Get the bounding box of the largest object
    min_r, min_c, max_r, max_c = get_bounding_box(largest_object)
    
    # Calculate output grid dimensions
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1
    
    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Copy the largest object pixels to the output grid, adjusting coordinates
    for r, c in largest_object:
        output_r = r - min_r
        output_c = c - min_c
        output_grid[output_r, output_c] = target_color
        
    # Convert back to list of lists for the required output format
    return output_grid.tolist()

```