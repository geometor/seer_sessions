import numpy as np
from collections import deque

"""
The transformation identifies key objects based on their bounding box dimensions relative to the largest square bounding box present. It then creates output segments of a uniform size 'S' (derived from the minimum dimension of key objects). The content of each segment depends on whether the original key object's bounding box was exactly SxS (in which case the pattern is copied) or larger (in which case a solid square is created). These segments are assembled horizontally based on the original objects' left-to-right order.

1.  Identify all distinct, contiguous objects of non-white color in the input grid. Record color, bounding box (height H, width W), and leftmost column index (min_col) for each.
2.  Find the dimension M of the largest square bounding box (max H where H == W). Default M=0 if none.
3.  Select "key" objects where H >= M-1 and W >= M-1.
4.  If no key objects, output an empty grid.
5.  Determine the target size S = min(min(H, W)) for all key objects. Ensure S > 0.
6.  Sort key objects by min_col.
7.  Create S x S output segments:
    *   If H == S and W == S for a key object, extract the S x S pattern from the input grid at the object's location.
    *   Otherwise (H > S or W > S), create a solid S x S square of the object's color.
8.  Assemble segments horizontally in sorted order.
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
                    'pixels': obj_pixels, # Retained for potential future use, not strictly needed here
                    'min_row': min_r, 'max_row': max_r,
                    'min_col': min_c, 'max_col': max_c,
                    'height': height, 'width': width
                })
    return objects


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation logic to the input grid.
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
    min_dims_for_S = []
    for obj in key_objects:
        min_dims_for_S.append(min(obj['height'], obj['width']))
    
    if not min_dims_for_S: # Should not happen if key_objects is not empty
         return []
         
    S = min(min_dims_for_S)
    
    # Check for S=0 which would be invalid
    if S <= 0:
        print(f"Warning: Calculated output size S={S} is invalid. Aborting.")
        return []

    # 6. Sort key objects by horizontal position (min_col)
    key_objects.sort(key=lambda obj: obj['min_col'])

    # 7. Create output segments (S x S grids)
    output_segments = []
    for obj in key_objects:
        H = obj['height']
        W = obj['width']
        color = obj['color']
        
        # Conditional transformation based on object size vs target size S
        if H == S and W == S:
            # Extract the S x S pattern from the input grid
            min_r, min_c = obj['min_row'], obj['min_col']
            segment_grid = input_np[min_r : min_r + S, min_c : min_c + S]
        else:
            # Create a solid S x S square
            segment_grid = np.full((S, S), color, dtype=int)
            
        output_segments.append(segment_grid)

    # 8. Assemble the final output grid horizontally
    if not output_segments:
        # This case might occur if S was invalid or segment creation failed unexpectedly
        return []
        
    # Use hstack to concatenate the segments horizontally
    output_grid_np = np.hstack(output_segments)
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid