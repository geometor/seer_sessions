import numpy as np
from collections import deque

"""
The transformation identifies all distinct connected objects composed of non-background colors (green '3' and maroon '9') using orthogonal adjacency. For each object, it calculates the count of maroon pixels (`maroon_count`) and the total pixel count (`total_size`), and identifies its top-left pixel coordinate. It then selects a single object for removal based on a hierarchical criteria: 
1. Minimum `maroon_count`.
2. If tied, maximum `total_size`.
3. If still tied, the object whose top-most, left-most pixel appears first (minimum row index, then minimum column index).
Finally, it creates the output grid by copying the input grid and changing all pixels of the selected object to the background color (white '0').
"""

def find_objects(grid):
    """
    Identifies all distinct connected objects of non-background pixels in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains:
        'pixels': A set of (row, col) tuples for the object.
        'maroon_count': Integer count of maroon (9) pixels.
        'total_size': Integer count of all pixels.
        'top_left': Tuple (row, col) of the top-most, left-most pixel.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If pixel is non-background (not 0) and not visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_pixels = set()
                maroon_count = 0
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Track top-left for this object

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.add((curr_r, curr_c))

                    # Update top-left tracking: find min row, then min col for that row
                    if curr_r < min_r:
                        min_r, min_c = curr_r, curr_c
                    elif curr_r == min_r and curr_c < min_c:
                        min_c = curr_c

                    # Count maroon pixels
                    if grid[curr_r, curr_c] == 9:
                        maroon_count += 1

                    # Explore neighbors (orthogonal: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, non-background color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store object details after BFS completes for this object
                objects.append({
                    'pixels': current_object_pixels,
                    'maroon_count': maroon_count,
                    'total_size': len(current_object_pixels),
                    'top_left': (min_r, min_c)
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # 1. Identify all objects and calculate their properties
    objects = find_objects(grid)
    
    # Handle edge case: If no non-background objects found, return the original grid
    if not objects:
        # Ensure output is list of lists
        return grid.tolist() 
        
    # 2. Select Target Object: Filter by Minimum Maroon Count
    min_maroon_count = min(obj['maroon_count'] for obj in objects)
    candidates = [obj for obj in objects if obj['maroon_count'] == min_maroon_count]
    
    target_object = None
    # 3. If only one candidate after step 2, it's the target
    if len(candidates) == 1:
        target_object = candidates[0]
    else:
        # 4. Tie-breaker 1: Filter by Maximum Size (if necessary)
        max_total_size = max(obj['total_size'] for obj in candidates)
        candidates = [obj for obj in candidates if obj['total_size'] == max_total_size]
        
        # 5. If only one candidate after step 4, it's the target
        if len(candidates) == 1:
            target_object = candidates[0]
        else:
            # 6. Tie-breaker 2: Filter by Position (if necessary)
            # Sort remaining candidates by top_left coordinate (row first, then column)
            candidates.sort(key=lambda obj: (obj['top_left'][0], obj['top_left'][1]))
            # The first object after sorting is the target
            target_object = candidates[0] 

    # 7. Generate Output grid: Create a copy of the input grid
    output_grid = grid.copy()
    
    # 8. Modify Output grid: Change pixels of the target object to white (0)
    for r, c in target_object['pixels']:
        output_grid[r, c] = 0
        
    # Convert output numpy array back to list of lists for the required format
    return output_grid.tolist()