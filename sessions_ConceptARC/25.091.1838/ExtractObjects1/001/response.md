```python
import numpy as np
from collections import deque

"""
Identify all contiguous objects of non-background (non-white) color in the input grid. 
Determine the size (number of pixels) of each object. Find the object with the largest size. 
Calculate the minimum bounding box that encloses this largest object. 
Extract (crop) the portion of the input grid defined by this bounding box to create the output grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a list of (row, col) coordinates.
              Returns an empty list if no non-background pixels are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-background (not 0) and hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_coords = []
                object_color = grid[r, c]
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == object_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box for a list of coordinates.

    Args:
        obj_coords (list): A list of (row, col) tuples representing the object pixels.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if obj_coords is empty.
    """
    if not obj_coords:
        return None
        
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by finding the largest non-background object 
    and cropping the grid to its bounding box.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the cropped output grid. 
                  Returns an empty array if no objects are found.
    """
    # Convert input list of lists to numpy array if necessary
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid, dtype=int)

    # 1. Find all non-background objects
    objects = find_objects(input_grid)

    # Handle case with no objects
    if not objects:
        # Based on examples, this case might not happen, but returning empty seems reasonable
        return np.array([[]], dtype=int) 

    # 2. Calculate sizes and find the largest object
    largest_object = max(objects, key=len)

    # 3. Calculate the bounding box of the largest object
    bbox = get_bounding_box(largest_object)
    if bbox is None: # Should not happen if objects list was not empty
         return np.array([[]], dtype=int)
         
    min_row, max_row, min_col, max_col = bbox

    # 4. Crop the input grid using the bounding box coordinates
    # Note: Slicing in numpy is exclusive for the end index, so add 1
    output_grid = input_grid[min_row : max_row + 1, min_col : max_col + 1]

    return output_grid
```