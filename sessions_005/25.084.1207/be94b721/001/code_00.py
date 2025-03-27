import numpy as np
from collections import deque

"""
Identifies all distinct connected objects of non-background (non-0) colors in the input grid.
Calculates the size (pixel count) of each object.
Selects the object with the largest size. If there's a tie, the first one found is selected.
Determines the minimum bounding box enclosing the selected object.
Creates the output grid by cropping the input grid to this bounding box.
"""

def find_objects(grid):
    """
    Finds all connected objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'coords' (a set of (row, col) tuples), 'color' (int),
              and 'size' (int). Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            # If it's a non-background pixel and hasn't been visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Start Breadth-First Search (BFS) to find connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found object's details
                objects.append({'coords': obj_coords, 'color': color, 'size': len(obj_coords)})
    return objects

def get_bounding_box(coords):
    """
    Calculates the minimum bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples representing an object.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if coords is empty.
    """
    if not coords:
        return None 
    
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def transform(input_grid_list):
    """
    Transforms the input grid by finding the largest object and cropping the grid
    to its bounding box.

    Args:
        input_grid_list (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The cropped output grid containing the largest object.
                       Returns an empty list of lists if no objects are found.
    """
    # Convert input list of lists to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    
    # 1. Identify all objects and their properties (coordinates, color, size)
    objects = find_objects(input_grid)

    # Handle case where no objects are found in the input grid
    if not objects:
        # Return an empty grid representation
        return [[]] 
        
    # 2. Find the object with the largest size.
    #    In case of ties, max() returns the first one encountered.
    largest_object = max(objects, key=lambda obj: obj['size'])
    
    # 3. Determine the bounding box of the largest object
    bounding_box = get_bounding_box(largest_object['coords'])
    if bounding_box is None: # Should not happen if objects list is not empty
         return [[]] 
    min_r, min_c, max_r, max_c = bounding_box
    
    # 4. Crop the input grid using the bounding box coordinates.
    #    Numpy slicing includes the start index but excludes the end index,
    #    so we add 1 to max_r and max_c.
    output_grid_np = input_grid[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert the resulting numpy array back to a list of lists for the standard output format
    output_grid = output_grid_np.tolist()

    return output_grid