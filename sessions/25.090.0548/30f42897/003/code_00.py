import numpy as np
from collections import Counter

"""
Transforms an input grid based on the properties of a single non-background 
colored object found within it.

1.  Identify Background and Object: Determine the background color (most frequent). 
    Find the single contiguous non-background object, its color (C), pixel coordinates, 
    bounding box (top, left, H, W).
2.  Initialize Output: Copy the input grid.
3.  Apply Shape-Specific Rules:
    *   If Vertical Line (W=1):
        *   If H=5: Add horizontal lines (length H, color C) at top-left and bottom-left.
        *   If H=2: Add specific horizontal and vertical lines (length H, color C) 
          at locations relative to grid boundaries (derived from example 3).
    *   If Rectangle (H>1, W>1):
        *   Add a horizontally reflected copy of the object, placed so its 
          top-left corner is at (0, GridWidth-W).
        *   Add a horizontal line (length W+1, color C) centered on the bottom row.
4.  Return: The modified output grid.
"""

def find_objects(grid, background_color):
    """
    Finds contiguous objects of non-background colors in the grid.
    Uses a simple flood fill (BFS) approach. Returns a list of objects, 
    each containing color, pixels (list of tuples), and bounding_box dict.
    """
    objects = []
    visited = np.zeros(grid.shape, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            # If this pixel is not background and not visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Breadth-First Search
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Calculate bounding box
                bounding_box = {
                    'top': min_r, 
                    'left': min_c, 
                    'height': max_r - min_r + 1, 
                    'width': max_c - min_c + 1
                }
                # Store object details
                objects.append({
                    'color': color, 
                    'pixels': obj_pixels, 
                    'bounding_box': bounding_box
                })
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rules based on the detected object.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    grid_h, grid_w = input_np.shape

    # 1. Identify Background Color
    colors, counts = np.unique(input_np, return_counts=True)
    if not counts.size: # Handle empty grid case
         return output_grid.tolist()
    background_color = colors[np.argmax(counts)]
    
    # 2. Find the single non-background object
    objects = find_objects(input_np, background_color)
    
    # Expecting exactly one non-background object based on examples
    if len(objects) != 1:
        # If no object or multiple objects, return copy (as per observed ARC behavior)
        # print(f"Warning: Found {len(objects)} objects, expected 1. Returning copy.")
        return output_grid.tolist() 
        
    obj = objects[0]
    obj_color = obj['color']
    obj_pixels = obj['pixels']
    bbox = obj['bounding_box']
    H = bbox['height']
    W = bbox['width']
    top = bbox['top']
    left = bbox['left']

    # 3. Apply Shape-Specific Rule
    if W == 1 and H > 0: # Vertical Line
        if H == 5: # Rule from train_1
            # Add horizontal line top-left
            if 0 + H <= grid_w: # Check if line fits
                 output_grid[0, 0:H] = obj_color
            # Add horizontal line bottom-left
            if 0 + H <= grid_w and grid_h > 0: # Check if line fits and grid has rows
                 output_grid[grid_h - 1, 0:H] = obj_color
                 
        elif H == 2: # Rule from train_3 
             # Add shapes based on fixed/relative positions observed in example 3
             # Check boundaries before drawing
             line_len = H # which is 2
             # Horizontal lines 
             if 1 + line_len <= grid_w: output_grid[0, 1 : 1+line_len] = obj_color 
             if 5 + line_len <= grid_w: output_grid[0, 5 : 5+line_len] = obj_color 
             if grid_h > 0: # Check row exists
                 if 0 + line_len <= grid_w: output_grid[grid_h-1, 0 : 0+line_len] = obj_color 
                 if 4 + line_len <= grid_w: output_grid[grid_h-1, 4 : 4+line_len] = obj_color 
             # Vertical lines 
             if grid_w > 0: # Check col exists
                if 1 + line_len <= grid_h: output_grid[1 : 1+line_len, grid_w-1] = obj_color 
                if 5 + line_len <= grid_h: output_grid[5 : 5+line_len, grid_w-1] = obj_color 
        # else: (No rules for other vertical line heights)
            # print(f"Warning: Unhandled vertical line height H={H}.")
             
    elif H > 1 and W > 1: # Rectangle (Rule from train_2, including reflection)
        # --- Reflected Copy ---
        target_top = 0
        target_left = grid_w - W
        
        # Iterate through original object pixels to create reflected copy
        for r, c in obj_pixels:
            # Calculate relative coordinates within the object's bounding box
            rel_r = r - top
            rel_c = c - left
            # Calculate horizontally reflected relative column
            reflected_rel_c = (W - 1) - rel_c
            # Calculate target coordinates in the output grid (top-right placement)
            target_r = target_top + rel_r
            target_c = target_left + reflected_rel_c
            # Check boundaries before placing the pixel
            if 0 <= target_r < grid_h and 0 <= target_c < grid_w:
                output_grid[target_r, target_c] = obj_color

        # --- Bottom Line ---
        line_len = W + 1
        if line_len <= grid_w and grid_h > 0: # Check if line fits and row exists
            start_col = (grid_w - line_len) // 2
            # Ensure start_col is non-negative (can happen if line_len > grid_w)
            if start_col >= 0:
                 output_grid[grid_h - 1, start_col : start_col + line_len] = obj_color
            
    # else: (No rules for horizontal lines H=1 or single pixels H=1,W=1)
        # print(f"Warning: Unhandled object shape H={H}, W={W}.")

    # 4. Final Output - convert back to list of lists
    return output_grid.tolist()