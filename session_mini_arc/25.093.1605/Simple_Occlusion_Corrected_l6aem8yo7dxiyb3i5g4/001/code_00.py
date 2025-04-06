import numpy as np
from collections import deque

"""
Identifies two distinct, vertically separated non-zero objects in a 5x5 input grid. 
Retains the upper object in its original position and color in the output grid.
Removes the lower object entirely.
Adds a single pixel to the output grid:
- Its color matches the upper object's color.
- Its row index is the same as the topmost row index of the original lower object.
- Its column index is the same as the column index of the upper object's anchor point 
  (top-most, left-most pixel).
All other cells in the output grid are set to the background color (0).
"""

def find_objects(grid):
    """
    Finds connected components of non-zero cells in the grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains:
        - 'pixels': A set of (row, col) tuples for the object's pixels.
        - 'color': The integer color of the object.
        - 'topmost_row': The minimum row index of the object.
        - 'anchor_point': The (row, col) tuple of the top-most, left-most pixel.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                # Found the start of a potential new object
                obj_color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_row = r
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    min_row = min(min_row, row) # Keep track of topmost row efficiently

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if neighbor is part of the object
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == obj_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                # Calculate anchor point (top-most, then left-most)
                top_pixels = [(row, col) for row, col in current_object_pixels if row == min_row]
                anchor_point = min(top_pixels, key=lambda item: item[1])
                            
                objects.append({
                    'pixels': current_object_pixels,
                    'color': obj_color,
                    'topmost_row': min_row,
                    'anchor_point': anchor_point
                })
                
    # Sort objects by topmost row to easily identify upper and lower
    objects.sort(key=lambda obj: obj['topmost_row'])
    
    return objects

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape
    
    # Initialize output grid with background color 0
    output_grid = np.zeros_like(input_grid)

    # 1. Identify the two non-zero objects
    objects = find_objects(input_grid)
    
    # Ensure exactly two objects were found as per problem description
    if len(objects) != 2:
        # Handle error case or unexpected input - returning empty for now
        # Or raise ValueError("Expected exactly two objects in the input grid.")
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning empty grid.")
        return np.zeros_like(input_grid).tolist()


    # 2. Determine upper and lower objects (already sorted by find_objects)
    upper_object = objects[0]
    lower_object = objects[1]

    # 3. Find properties of the upper object
    upper_color = upper_object['color']
    upper_pixels = upper_object['pixels']
    upper_anchor_col = upper_object['anchor_point'][1] # We only need the column

    # 4. Find the topmost row index of the lower object
    lower_topmost_row = lower_object['topmost_row']

    # 5. Output grid is already initialized

    # 6. Copy the upper object to the output grid
    for r, c in upper_pixels:
        if 0 <= r < rows and 0 <= c < cols: # Bounds check (good practice)
            output_grid[r, c] = upper_color

    # 7. Place the single anchor pixel
    new_pixel_row = lower_topmost_row
    new_pixel_col = upper_anchor_col
    if 0 <= new_pixel_row < rows and 0 <= new_pixel_col < cols: # Bounds check
        output_grid[new_pixel_row, new_pixel_col] = upper_color

    # Return the grid as a list of lists
    return output_grid.tolist()