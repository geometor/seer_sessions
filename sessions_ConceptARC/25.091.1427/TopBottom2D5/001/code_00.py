import numpy as np
from collections import deque

"""
Identify all distinct, connected objects of non-white pixels in the input grid. 
Determine the lowest row index reached by each object. Keep only the object(s) 
that reach the overall maximum lowest row index. Construct the output grid 
containing only these kept objects on a white background.
"""

def find_objects(grid):
    """
    Finds all connected objects of the same non-white color in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains:
            'color': The color of the object (int > 0).
            'pixels': A set of (row, col) tuples for the object's pixels.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            # If it's a non-white pixel and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            
                            nr, nc = row + dr, col + dc
                            
                            # Check grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor has the same color and not visited
                                if grid[nr, nc] == color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                                    
                if obj_pixels:
                    objects.append({'color': color, 'pixels': obj_pixels})
                    
    return objects

def get_lowest_row(obj):
    """Calculates the lowest row index for an object."""
    if not obj['pixels']:
        return -1 # Or some other indicator for empty objects
    return max(r for r, c in obj['pixels'])


def transform(input_grid):
    """
    Transforms the input grid by keeping only the object(s) that extend 
    to the lowest row(s).

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    
    # Find all distinct objects in the input grid
    objects = find_objects(input_grid)
    
    # If there are no objects, return a grid of the same size filled with white
    if not objects:
        return np.zeros_like(input_grid, dtype=int)
        
    # Calculate the lowest row index for each object
    lowest_rows = [(obj, get_lowest_row(obj)) for obj in objects]
    
    # Find the maximum lowest row index among all objects
    if not lowest_rows: # Should not happen if objects list is not empty, but good check
         return np.zeros_like(input_grid, dtype=int)
         
    max_lowest_row = -1
    for _, lowest_row in lowest_rows:
        if lowest_row > max_lowest_row:
            max_lowest_row = lowest_row

    # Filter objects: keep only those whose lowest row index matches the maximum
    kept_objects = [obj for obj, lowest_row in lowest_rows if lowest_row == max_lowest_row]
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros_like(input_grid, dtype=int)
    
    # Populate the output grid with the pixels of the kept objects
    for obj in kept_objects:
        color = obj['color']
        for r, c in obj['pixels']:
            output_grid[r, c] = color
            
    return output_grid