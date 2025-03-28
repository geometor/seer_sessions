"""
Identify the object (contiguous non-white pixels) in the input grid that contains at least one gray pixel (color 5). 
Determine the minimum bounding box for this object. 
Extract the portion of the input grid corresponding to this bounding box as the output grid.
If multiple instances of the shape containing gray exist, any instance can be chosen.
"""

import numpy as np
from collections import deque

def find_objects(grid, background_color=0, target_color=None):
    """
    Finds all connected objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color code for the background.
        target_color (int, optional): A specific color to check for within objects. 
                                     Defaults to None.

    Returns:
        list: A list of tuples. Each tuple contains:
              - A set of (row, col) coordinates belonging to the object.
              - A boolean indicating if the object contains the target_color (if specified).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                # Start a BFS to find the connected object
                q = deque([(r, c)])
                current_object_coords = set()
                contains_target = False
                
                while q:
                    row, col = q.popleft()
                    
                    if not (0 <= row < rows and 0 <= col < cols) or (row, col) in visited or grid[row, col] == background_color:
                        continue
                        
                    visited.add((row, col))
                    current_object_coords.add((row, col))
                    
                    if target_color is not None and grid[row, col] == target_color:
                        contains_target = True

                    # Add neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] != background_color:
                             q.append((nr, nc))

                objects.append((current_object_coords, contains_target))
                
    return objects

def get_bounding_box(coords):
    """
    Calculates the minimum bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col)
    """
    if not coords:
        return None
    
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), min(cols), max(rows), max(cols)


def transform(input_grid):
    """
    Finds the object containing gray (5) and extracts its bounding box.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Find all objects and check if they contain gray (color 5)
    all_objects = find_objects(input_grid_np, background_color=0, target_color=5)
    
    # Filter for objects containing gray
    target_objects = [obj_coords for obj_coords, contains_gray in all_objects if contains_gray]
    
    if not target_objects:
        # Should not happen based on examples, but handle defensively
        return [] 
        
    # Select the coordinates of the first found target object
    # (Examples suggest all gray-containing shapes are identical if multiple exist)
    selected_object_coords = target_objects[0]
    
    # Get the bounding box of the selected object
    min_r, min_c, max_r, max_c = get_bounding_box(selected_object_coords)
    
    # Extract the subgrid defined by the bounding box
    output_grid_np = input_grid_np[min_r : max_r + 1, min_c : max_c + 1]
    
    # Convert back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
