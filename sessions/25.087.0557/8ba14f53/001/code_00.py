import numpy as np
from collections import deque

"""
The transformation identifies the two distinct, non-white colored objects in the 4x9 input grid. 
It calculates the number of pixels (count) for each object. 
Based on a comparison of these counts and their relative difference or absolute value, 
it selects one of six predefined 3x3 patterns to construct the output grid, using the colors of the left and right objects.

1. Find the two connected components (objects) of non-white colors in the input grid.
2. For each object, determine its color, pixel count, and its leftmost column index.
3. Identify the object on the left (smaller minimum column index) and the object on the right. Let their colors be C_left, C_right and counts be N_left, N_right, respectively.
4. Compare N_left and N_right:
    a. If N_left > N_right:
        - If N_left - N_right == 1: Use Pattern GT1: [[L,L,L],[R,R,R],[0,0,0]]
        - If N_left - N_right >= 2: Use Pattern GT2: [[L,L,L],[L,0,0],[R,R,0]]
    b. If N_left < N_right:
        - If N_right - N_left >= 4: Use Pattern LT1: [[L,0,0],[R,R,R],[R,R,R]]
        - If N_right - N_left == 3: Use Pattern LT2: [[L,L,0],[R,R,R],[0,0,0]]
    c. If N_left == N_right:
        - If N_left >= 8: Use Pattern EQ1: [[L,L,L],[R,R,0],[0,0,0]]
        - If N_left < 8: Use Pattern EQ2: [[L,0,0],[R,0,0],[0,0,0]]
5. Create a 3x3 numpy array and fill it according to the selected pattern, substituting L for C_left and R for C_right.
6. Return the resulting 3x3 grid.
"""

def find_objects(grid):
    """
    Finds connected components of non-white colors in the grid.
    Returns a list of objects, each represented as a dictionary containing
    'color', 'pixels' (set of coordinates), 'count', and 'min_col'.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_col = c
                
                while q:
                    row, col = q.popleft()
                    pixels.add((row, col))
                    min_col = min(min_col, col)
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': pixels,
                    'count': len(pixels),
                    'min_col': min_col
                })
                
    # Sort objects by their leftmost column to easily identify left/right
    objects.sort(key=lambda obj: obj['min_col'])
    return objects

def transform(input_grid):
    """
    Applies the transformation rule based on object counts and positions.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Find the two non-white objects
    objects = find_objects(input_grid_np)
    
    # Ensure exactly two objects are found (as per task examples)
    if len(objects) != 2:
        # Handle unexpected cases, perhaps return empty or original grid?
        # For now, let's assume the structure holds and raise error or return default
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning empty grid.")
        return np.zeros((3, 3), dtype=int).tolist() 
        
    obj_left = objects[0]
    obj_right = objects[1]
    
    c_left = obj_left['color']
    c_right = obj_right['color']
    n_left = obj_left['count']
    n_right = obj_right['count']

    # Initialize the 3x3 output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Apply patterns based on count comparison
    if n_left > n_right:
        if n_left - n_right == 1: # Pattern GT1 (e.g., train_3)
            output_grid[0, :] = c_left
            output_grid[1, :] = c_right
        else: # Pattern GT2 (e.g., train_4) (n_left - n_right >= 2)
            output_grid[0, :] = c_left
            output_grid[1, 0] = c_left
            output_grid[2, 0] = c_right
            output_grid[2, 1] = c_right
            
    elif n_left < n_right:
        if n_right - n_left >= 4: # Pattern LT1 (e.g., train_1)
             output_grid[0, 0] = c_left
             output_grid[1, :] = c_right
             output_grid[2, :] = c_right
        else: # Pattern LT2 (e.g., train_6) (n_right - n_left == 3)
             output_grid[0, 0] = c_left
             output_grid[0, 1] = c_left
             output_grid[1, :] = c_right

    else: # n_left == n_right
        if n_left >= 8: # Pattern EQ1 (e.g., train_2)
            output_grid[0, :] = c_left
            output_grid[1, 0] = c_right
            output_grid[1, 1] = c_right
        else: # Pattern EQ2 (e.g., train_5) (n_left < 8)
            output_grid[0, 0] = c_left
            output_grid[1, 0] = c_right

    return output_grid.tolist()
