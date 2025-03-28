import numpy as np
from collections import deque

"""
The transformation identifies a dividing line (a full row or column of a single non-background color) in the input grid. 
It then finds the four distinct colored objects present in the grid, excluding the background (color 0) and the divider color.
For each object, it determines its bounding box and extracts the top-left 3x3 subgrid (crop). 
The objects are categorized as Top-Left, Top-Right, Bottom-Left, or Bottom-Right based on their position relative to the dividing line.
Finally, a 6x6 output grid is constructed by placing the 3x3 crop of each object into the corresponding quadrant:
- Top-Left object crop -> Output[0:3, 0:3]
- Top-Right object crop -> Output[0:3, 3:6]
- Bottom-Left object crop -> Output[3:6, 0:3]
- Bottom-Right object crop -> Output[3:6, 3:6]
"""

def find_divider(grid):
    """
    Finds a horizontal or vertical line of a single non-background color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (color, orientation ('h' or 'v'), index) or (None, None, None) if not found.
    """
    height, width = grid.shape

    # Check for horizontal divider
    for r in range(height):
        first_color = grid[r, 0]
        if first_color != 0 and np.all(grid[r, :] == first_color):
            return first_color, 'h', r

    # Check for vertical divider
    for c in range(width):
        first_color = grid[0, c]
        if first_color != 0 and np.all(grid[:, c] == first_color):
            return first_color, 'v', c

    return None, None, None

def find_objects(grid, ignore_colors):
    """
    Finds all contiguous objects of colors not in ignore_colors.

    Args:
        grid (np.ndarray): The input grid.
        ignore_colors (set): A set of colors to ignore (background, divider).

    Returns:
        list: A list of dictionaries, each representing an object with 
              'color', 'pixels' (list of (r, c) tuples), and 'bbox' 
              (min_row, max_row, min_col, max_col).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if not visited[r, c] and color not in ignore_colors:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check neighbors (orthogonal)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, max_r, min_c, max_c)
                })
                
    return objects

def get_crop(grid, bbox):
    """
    Extracts the top-left 3x3 crop of an object based on its bounding box.
    Pads with background color (0) if the object is smaller or near the edge.
    """
    min_r, _, min_c, _ = bbox
    height, width = grid.shape
    crop = np.zeros((3, 3), dtype=grid.dtype)
    
    for r_offset in range(3):
        for c_offset in range(3):
            source_r, source_c = min_r + r_offset, min_c + c_offset
            if 0 <= source_r < height and 0 <= source_c < width:
                 # Check if the source pixel actually belongs to the object
                 # This prevents grabbing parts of adjacent objects if bbox overlaps
                 # Note: This check isn't strictly necessary if find_objects guarantees
                 # non-overlapping bounding boxes for distinct objects, or if we only care
                 # about the top-left region regardless of exact object shape.
                 # Sticking to the simpler interpretation: grab 3x3 from bbox start.
                 crop[r_offset, c_offset] = grid[source_r, source_c]
            # else: it remains 0 (background) due to initialization
            
    return crop

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules:
    1. Find the divider line.
    2. Find the four objects (excluding divider and background).
    3. Extract the 3x3 top-left crop of each object's bounding box.
    4. Categorize objects relative to the divider (TL, TR, BL, BR).
    5. Assemble the crops into a 6x6 output grid.
    """
    input_grid = np.array(input_grid)
    
    # 1. Find the divider line
    divider_color, divider_orient, divider_idx = find_divider(input_grid)
    if divider_color is None:
        # Handle error case if necessary, though examples suggest a divider always exists
        print("Error: Divider not found.") 
        return None # Or raise an exception

    # 2. Find the four objects
    ignore_colors = {0, divider_color}
    objects = find_objects(input_grid, ignore_colors)
    
    if len(objects) != 4:
         # Handle error case if necessary
         print(f"Error: Expected 4 objects, found {len(objects)}.")
         return None # Or raise an exception

    # 3. Get crops and 4. Categorize objects
    categorized_crops = {}
    
    if divider_orient == 'v': # Vertical divider at column divider_idx
        left_objs = sorted([obj for obj in objects if obj['bbox'][3] < divider_idx], key=lambda o: o['bbox'][0])
        right_objs = sorted([obj for obj in objects if obj['bbox'][2] > divider_idx], key=lambda o: o['bbox'][0])
        
        if len(left_objs) == 2 and len(right_objs) == 2:
            categorized_crops['TL'] = get_crop(input_grid, left_objs[0]['bbox'])
            categorized_crops['BL'] = get_crop(input_grid, left_objs[1]['bbox'])
            categorized_crops['TR'] = get_crop(input_grid, right_objs[0]['bbox'])
            categorized_crops['BR'] = get_crop(input_grid, right_objs[1]['bbox'])
        else:
             print(f"Error: Incorrect object distribution around vertical divider. Left: {len(left_objs)}, Right: {len(right_objs)}")
             return None

    elif divider_orient == 'h': # Horizontal divider at row divider_idx
        top_objs = sorted([obj for obj in objects if obj['bbox'][1] < divider_idx], key=lambda o: o['bbox'][2])
        bottom_objs = sorted([obj for obj in objects if obj['bbox'][0] > divider_idx], key=lambda o: o['bbox'][2])
        
        if len(top_objs) == 2 and len(bottom_objs) == 2:
            categorized_crops['TL'] = get_crop(input_grid, top_objs[0]['bbox'])
            categorized_crops['TR'] = get_crop(input_grid, top_objs[1]['bbox'])
            categorized_crops['BL'] = get_crop(input_grid, bottom_objs[0]['bbox'])
            categorized_crops['BR'] = get_crop(input_grid, bottom_objs[1]['bbox'])
        else:
            print(f"Error: Incorrect object distribution around horizontal divider. Top: {len(top_objs)}, Bottom: {len(bottom_objs)}")
            return None
            
    # 5. Assemble the output grid
    output_grid = np.zeros((6, 6), dtype=input_grid.dtype)
    
    if 'TL' in categorized_crops:
        output_grid[0:3, 0:3] = categorized_crops['TL']
    if 'TR' in categorized_crops:
        output_grid[0:3, 3:6] = categorized_crops['TR']
    if 'BL' in categorized_crops:
        output_grid[3:6, 0:3] = categorized_crops['BL']
    if 'BR' in categorized_crops:
        output_grid[3:6, 3:6] = categorized_crops['BR']

    return output_grid.tolist() # Return as list of lists per ARC standard
