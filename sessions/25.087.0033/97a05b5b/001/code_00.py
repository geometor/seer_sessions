import numpy as np
from collections import deque

"""
Identify the largest contiguous red object (MainRedObject) in the input grid.
Identify all other smaller, contiguous, non-red, non-white objects (StampObjects).
Extract the shape and color pattern of each StampObject relative to its bounding box.
Identify contiguous white areas (WhiteHoles) within the bounding box of the MainRedObject.
For each WhiteHole, find a StampObject with the exact same shape (set of relative pixel coordinates).
If a match is found, fill the WhiteHole in the MainRedObject area with the color pattern of the matching StampObject.
The final output is the modified MainRedObject area, cropped to its bounding box.
"""

def find_objects(grid, colors_to_find=None, ignore_colors=None, connectivity=1):
    """
    Finds contiguous objects of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set, optional): Set of colors to look for. If None, finds all colors not in ignore_colors.
        ignore_colors (set, optional): Set of colors to ignore. Defaults to {0} (white).
        connectivity (int): 1 for 4-way connectivity, 2 for 8-way connectivity.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'pixels': set of (row, col) tuples.
              'color': the color of the object.
              'bbox': tuple (min_row, min_col, max_row, max_col).
    """
    if ignore_colors is None:
        ignore_colors = {0}
        
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    if connectivity == 1:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 2:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 1 or 2")

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if visited[r, c] or color in ignore_colors or (colors_to_find is not None and color not in colors_to_find):
                continue

            obj_pixels = set()
            q = deque([(r, c)])
            visited[r, c] = True
            min_r, min_c = r, c
            max_r, max_c = r, c

            while q:
                curr_r, curr_c = q.popleft()
                obj_pixels.add((curr_r, curr_c))
                min_r = min(min_r, curr_r)
                min_c = min(min_c, curr_c)
                max_r = max(max_r, curr_r)
                max_c = max(max_c, curr_c)

                for dr, dc in deltas:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       not visited[nr, nc] and grid[nr, nc] == color:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            objects.append({
                'pixels': obj_pixels,
                'color': color,
                'bbox': (min_r, min_c, max_r, max_c)
            })
            
    return objects

def get_relative_pattern(grid, pixels, bbox):
    """Calculates the shape (relative coords) and pattern (relative coords -> color)."""
    min_r, min_c, _, _ = bbox
    shape = frozenset((r - min_r, c - min_c) for r, c in pixels)
    pattern = {(r - min_r, c - min_c): grid[r, c] for r, c in pixels}
    return shape, pattern

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.
    """
    input_arr = np.array(input_grid, dtype=int)
    rows, cols = input_arr.shape
    
    # 1. Find the largest contiguous red object (MainRedObject)
    red_objects = find_objects(input_arr, colors_to_find={2})
    if not red_objects:
        # Handle case where no red object is found (return empty or original?)
        # Based on examples, seems like a red object is always present.
        # Let's assume an error or return empty grid for now.
        return [] 
        
    main_red_object = max(red_objects, key=lambda obj: len(obj['pixels']))
    main_bbox = main_red_object['bbox']
    min_r, min_c, max_r, max_c = main_bbox
    
    # 2. Create the initial output grid by copying the MainRedObject area
    output_arr = input_arr[min_r:max_r+1, min_c:max_c+1].copy()
    out_rows, out_cols = output_arr.shape

    # 3. Find all StampObjects (non-red, non-white) in the *input* grid
    # We ignore the main red object pixels during search to avoid including parts of it if stamps touch it.
    temp_input_arr = input_arr.copy()
    for r, c in main_red_object['pixels']:
         temp_input_arr[r,c] = -1 # Mark red object pixels as temporary ignore value
         
    stamp_objects_raw = find_objects(temp_input_arr, ignore_colors={0, 2, -1}) # Ignore white, red, and marked pixels
    
    # 4. Extract shapes and patterns of StampObjects
    stamp_patterns = {}
    for stamp in stamp_objects_raw:
        shape, pattern = get_relative_pattern(input_arr, stamp['pixels'], stamp['bbox']) # Use original grid for colors
        # If multiple stamps have the same shape, the last one found will overwrite previous ones.
        # This seems acceptable based on the task description.
        stamp_patterns[shape] = pattern 

    # 5. Identify WhiteHoles within the *output* grid (cropped MainRedObject area)
    hole_objects = find_objects(output_arr, colors_to_find={0}, ignore_colors=None) # Find white objects in the cropped area

    # 6. Match WhiteHoles to StampObjects by shape and fill
    for hole in hole_objects:
        hole_min_r, hole_min_c, _, _ = hole['bbox'] # Bbox relative to output_arr
        
        # Calculate the shape of the hole relative to its own bounding box
        hole_shape = frozenset((r - hole_min_r, c - hole_min_c) for r, c in hole['pixels'])

        # 7. Check if a StampObject matches the hole shape
        if hole_shape in stamp_patterns:
            matched_pattern = stamp_patterns[hole_shape]
            
            # 8. Fill the hole in the output grid using the matched pattern
            for (dr, dc), color in matched_pattern.items():
                # Coordinates are relative to the stamp's bbox, which matches the hole's bbox
                out_r, out_c = hole_min_r + dr, hole_min_c + dc
                # Ensure coordinates are within the bounds of the output array
                if 0 <= out_r < out_rows and 0 <= out_c < out_cols:
                    # Check if the target pixel is actually part of the hole we are filling
                    # This prevents accidentally overwriting parts of the red frame if the stamp
                    # pattern's bounding box extends beyond the hole pixels.
                    if output_arr[out_r, out_c] == 0 and (out_r, out_c) in hole['pixels']:
                         output_arr[out_r, out_c] = color

    # Convert the final numpy array back to a list of lists
    return output_arr.tolist()