```python
import numpy as np
from collections import deque

"""
Identify the largest green object (color 3). 
Retain this object and any other object that is directly adjacent (including diagonals) to it.
Remove all other objects by changing their pixels to white (0).
"""

def find_objects(grid):
    """
    Identifies all connected objects of the same non-white color in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys 'color' (int) and 'pixels' (list of (row, col) tuples).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If the pixel is not white (0), hasn't been visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = row + dr, col + dc
                            
                            # Check boundaries
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is same color and not visited
                                if grid[nr, nc] == color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                                    
                objects.append({'color': color, 'pixels': obj_pixels})
                
    return objects

def get_adjacent_pixels(pixels, grid_shape):
    """
    Finds all unique pixels adjacent (including diagonals) to a given set of pixels.

    Args:
        pixels: A list or set of (row, col) tuples representing the object's pixels.
        grid_shape: A tuple (height, width) of the grid.

    Returns:
        A set of (row, col) tuples representing adjacent pixel coordinates.
    """
    height, width = grid_shape
    adjacent_coords = set()
    pixel_set = set(pixels) # For efficient checking if a neighbor belongs to the object itself

    for r, c in pixels:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r + dr, c + dc
                
                # Check boundaries and ensure it's not part of the object itself
                if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in pixel_set:
                    adjacent_coords.add((nr, nc))
                    
    return adjacent_coords


def transform(input_grid):
    """
    Transforms the input grid by keeping the largest green object and its adjacent objects.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # 1. Identify all distinct objects
    all_objects = find_objects(input_grid)
    
    # 2. Find all green objects
    green_objects = [obj for obj in all_objects if obj['color'] == 3]
    
    # Handle case where there are no green objects
    if not green_objects:
        # If no green object, maybe clear everything or return input?
        # Examples suggest a green object exists. Let's assume it does.
        # If strict adherence to rule needed for no green object, could return all white.
        # For now, let's proceed assuming one exists as per examples.
        # Alternative: return np.zeros_like(input_grid)
         return input_grid # Or maybe raise an error? Or return all white grid?

    # 3. Find the largest green object
    largest_green_object = max(green_objects, key=lambda obj: len(obj['pixels']))
    largest_green_pixels_set = set(largest_green_object['pixels'])

    # 4. Determine the adjacency zone around the largest green object
    adjacency_zone = get_adjacent_pixels(largest_green_pixels_set, (height, width))
    
    # 5. Iterate through all objects and remove non-adjacent ones (excluding the largest green)
    objects_to_remove = []
    for obj in all_objects:
        current_obj_pixels_set = set(obj['pixels'])
        
        # Skip the largest green object itself
        if current_obj_pixels_set == largest_green_pixels_set:
            continue
            
        # Check if any pixel of the current object is in the adjacency zone
        is_adjacent = False
        for pixel in current_obj_pixels_set:
            if pixel in adjacency_zone:
                is_adjacent = True
                break
        
        # If the object is not adjacent, mark it for removal
        if not is_adjacent:
            objects_to_remove.append(obj)

    # 6. Modify the output grid by removing marked objects
    for obj in objects_to_remove:
        for r, c in obj['pixels']:
            output_grid[r, c] = 0 # Change to white background color

    return output_grid
```