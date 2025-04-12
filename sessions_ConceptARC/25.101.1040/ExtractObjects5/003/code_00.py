import numpy as np
from collections import deque

"""
The transformation identifies key objects in the input grid based on their bounding box dimensions relative to the largest square bounding box found.
1. Find all contiguous non-white objects and their bounding boxes (height H, width W).
2. Determine the maximum dimension 'M' such that at least one object has an MxM bounding box. If no square bounding boxes exist, M is treated as 0.
3. Filter the objects, selecting only those "key" objects where both H >= M-1 and W >= M-1.
4. If no key objects are selected, return an empty grid.
5. Determine the output square size 'S' by finding the minimum dimension (minimum of H or W) across all selected key objects.
6. For each selected key object, create a solid square of size SxS using the object's color.
7. Sort these SxS squares based on the horizontal position (minimum column index) of their corresponding original key objects in the input grid, from left to right.
8. Assemble the final output grid by arranging the sorted SxS squares horizontally next to each other.
"""


def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous objects of non-background color (0) in the grid.
    
    Args:
        grid: A numpy array representing the input grid.
        
    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its color, pixels (list of (r, c) tuples), and
        bounding box information (min_row, max_row, min_col, max_col, height, width).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'min_row': min_r, 'max_row': max_r,
                    'min_col': min_c, 'max_col': max_c,
                    'height': height, 'width': width
                })
    return objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid according to the specified object filtering,
    resizing, and assembly rules.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Find all objects and their properties
    all_objects = find_objects(input_np)
    if not all_objects:
        return [] # Return empty if no objects found

    # 2. Find the maximum dimension 'M' of square bounding boxes
    max_square_dim = 0
    for obj in all_objects:
        if obj['height'] == obj['width']:
            max_square_dim = max(max_square_dim, obj['height'])
            
    # Note: If max_square_dim remains 0, M-1 will be -1.
    # H >= -1 and W >= -1 will be true for all objects.

    # 3. Filter objects to select key objects (H >= M-1 and W >= M-1)
    filter_threshold = max_square_dim - 1
    key_objects = [
        obj for obj in all_objects 
        if obj['height'] >= filter_threshold and obj['width'] >= filter_threshold
    ]

    # 4. Handle case where no key objects are found
    if not key_objects:
        return [] 

    # 5. Determine output square size 'S' (minimum dimension among key objects)
    min_dim_key_objects = []
    for obj in key_objects:
        min_dim_key_objects.append(min(obj['height'], obj['width']))
    
    if not min_dim_key_objects: # Should not happen if key_objects is not empty, but safe check
         return []
         
    S = min(min_dim_key_objects)
    
    # Check for S=0 which would be invalid, implies an issue upstream
    if S <= 0:
        # This case likely indicates an issue with object finding or filtering
        # For example, if only 0-dimension objects were found, which shouldn't happen.
        # Returning empty seems safest.
        print(f"Warning: Calculated output size S={S} is invalid. Aborting.")
        return []


    # 6. Sort key objects by horizontal position (min_col)
    # Need to store the original object along with the square for sorting
    key_objects.sort(key=lambda obj: obj['min_col'])

    # 7. Create output squares
    output_squares = []
    for obj in key_objects:
        square = np.full((S, S), obj['color'], dtype=int)
        output_squares.append(square)

    # 8. Assemble the final output grid horizontally
    if not output_squares:
        # This case means key_objects was non-empty, but creating squares failed (e.g., S was invalid)
        # It might have been caught earlier, but double-check.
        return []
        
    output_grid_np = np.hstack(output_squares)
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid