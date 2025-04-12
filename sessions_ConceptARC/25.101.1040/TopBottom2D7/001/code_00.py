import numpy as np
from collections import deque

"""
Identifies all contiguous non-white objects in the input grid.
Determines the topmost row index for each object.
Selects the object with the minimum topmost row index (highest in the grid).
Creates the output grid by extracting the pixels corresponding to the selected object, 
cropped to its minimum bounding box.
"""

def _find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous objects of the same non-background color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'pixels' (list of (row, col) tuples),
        'min_row', 'max_row', 'min_col', 'max_col'.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-white and not visited
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                current_object_pixels = []
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform BFS to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))

                    # Update bounding box
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds, color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                # Store the found object
                objects.append({
                    'color': color,
                    'pixels': current_object_pixels,
                    'min_row': min_r,
                    'max_row': max_r,
                    'min_col': min_c,
                    'max_col': max_c
                })
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the highest object (minimum top row)
    and returning that object cropped to its bounding box.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the cropped highest object.
    """
    
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify all contiguous groups of non-white pixels (objects)
    objects = _find_objects(grid_np)

    # Handle cases with no objects found
    if not objects:
        return [] 

    # 2. & 3. Find the object with the minimum topmost row index
    highest_object = min(objects, key=lambda obj: obj['min_row'])

    # 4. Determine the bounding box of the selected object
    min_r = highest_object['min_row']
    max_r = highest_object['max_row']
    min_c = highest_object['min_col']
    max_c = highest_object['max_col']
    obj_color = highest_object['color']
    obj_pixels = set(highest_object['pixels']) # Use set for faster lookup

    # 5. Create a new output grid with dimensions matching the bounding box size
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    output_grid_np = np.zeros((height, width), dtype=int) # Initialize with background color 0

    # 6. Copy the pixels of the selected object into the output grid
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
             # Check if the pixel in the original grid belongs to the selected object
            if (r, c) in obj_pixels:
                 # Calculate relative coordinates for the output grid
                out_r = r - min_r
                out_c = c - min_c
                output_grid_np[out_r, out_c] = obj_color # Use the object's color

    # Convert the numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid