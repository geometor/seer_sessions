import numpy as np
from collections import deque

"""
Identifies a target color that forms exactly one contiguous object in the input grid. 
Finds the bounding box of this target object.
Extracts the subgrid corresponding to the bounding box.
Filters the extracted subgrid: keeps pixels of the target color and white (0), 
replaces all other colors with white (0).
The final filtered subgrid is the output.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.
        color (int): The color to search for.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples 
                   representing a contiguous object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                # Start BFS for a new object
                current_object = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_object.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_object.add((nr, nc))
                            q.append((nr, nc))
                
                objects.append(current_object)
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples.

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
    Transforms the input grid based on the described logic.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # --- Workflow ---
    
    # 1. Analyze the input grid to identify all unique non-white colors present.
    unique_colors = np.unique(input_np)
    non_white_colors = [color for color in unique_colors if color != 0]

    target_color = -1 # Initialize with an invalid value
    target_object_coords = None 

    # 2. For each unique non-white color, determine the number of distinct contiguous objects.
    # 3. Identify the 'target color' as the color that forms exactly one contiguous object.
    for color in non_white_colors:
        objects = find_objects(input_np, color)
        if len(objects) == 1:
            # Check if we already found a target color (ambiguous case, though not in examples)
            if target_color != -1:
                # Handle ambiguity if necessary, for now assume it won't happen based on examples
                # print(f"Warning: Multiple colors ({target_color}, {color}) form exactly one object.")
                pass # Or raise an error, or prioritize based on some rule
            target_color = color
            target_object_coords = objects[0]
            # Optimization: if we found one, we can potentially break if ambiguity isn't expected
            # break 
            
    # Handle case where no target color is found
    if target_color == -1:
        # Return empty grid or handle error as appropriate for the broader ARC context
        # Based on examples, this shouldn't happen. Maybe return the input? Or empty grid?
        # Let's return an empty grid for now.
        print("Warning: No color found that forms exactly one object.")
        return [] 

    # 4. Find the minimum bounding box of the target color object.
    min_row, max_row, min_col, max_col = get_bounding_box(target_object_coords)

    # 5. Determine the height and width of the output grid.
    # (Implicitly done by slicing)
    
    # 6. Create a new grid (the output grid) by extracting the subgrid.
    extracted_grid = input_np[min_row:max_row+1, min_col:max_col+1]
    
    # 7-11. Filter the extracted grid.
    output_grid = np.copy(extracted_grid)
    output_rows, output_cols = output_grid.shape
    for r in range(output_rows):
        for c in range(output_cols):
            pixel_color = extracted_grid[r, c]
            if pixel_color != target_color and pixel_color != 0:
                output_grid[r, c] = 0 # Replace non-target, non-white colors with white

    # 12. Return the resulting grid as a list of lists.
    return output_grid.tolist()