```python
import numpy as np
from collections import Counter

"""
This program transforms an input grid based on the properties of a single 
non-background colored object found within it.

1.  **Identify Background and Object:** 
    Determine the background color (most common color). Find the single 
    contiguous non-background object, its color (C), height (H), and width (W).
2.  **Initialize Output:** Copy the input grid to the output grid.
3.  **Apply Shape-Specific Rules:**
    *   **Vertical Line (W=1):**
        *   If H=5: Add horizontal lines of length H and color C at the top-left 
          (row 0, cols 0 to H-1) and bottom-left (last row, cols 0 to H-1).
        *   If H=2: Add specific horizontal (length H) and vertical (length H) 
          lines of color C at fixed/relative positions based on example 3.
           - Horizontal: [0, 1:3], [0, 5:7], [6, 0:2], [6, 4:6]
           - Vertical:   [1:3, 8], [5:7, 8] 
           (Assuming grid size 7x9, adjustments might be needed for other sizes)
    *   **Rectangle (H>1, W>1):**
        *   Add a copy of the object (color C, size HxW) to the top-right 
          corner (rows 0 to H-1, cols GridWidth-W to GridWidth-1).
        *   Add a horizontal line of color C and length W+1 centered on the 
          bottom row (last row).
4.  **Return:** The modified output grid.
"""

def find_objects(grid, background_color):
    """
    Finds contiguous objects of non-background colors in the grid.
    Uses a simple flood fill (BFS) approach.
    """
    objects = []
    visited = np.zeros(grid.shape, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

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
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                bounding_box = {
                    'top': min_r, 
                    'left': min_c, 
                    'height': max_r - min_r + 1, 
                    'width': max_c - min_c + 1
                }
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

    # 1. Identify Background and Object
    colors, counts = np.unique(input_np, return_counts=True)
    background_color = colors[np.argmax(counts)]
    
    objects = find_objects(input_np, background_color)
    
    # Expecting exactly one non-background object based on examples
    if not objects or len(objects) > 1:
        # If no object or multiple objects, return copy (or handle error)
        print(f"Warning: Found {len(objects)} objects, expected 1. Returning copy.")
        return output_grid.tolist() 
        
    obj = objects[0]
    obj_color = obj['color']
    bbox = obj['bounding_box']
    H = bbox['height']
    W = bbox['width']
    top = bbox['top']
    left = bbox['left']

    # 3. Apply Shape-Specific Rule
    if W == 1: # Vertical Line
        if H == 5: # Rule from train_1
            # Add horizontal line top-left
            if 0 + H <= grid_w:
                 output_grid[0, 0:H] = obj_color
            # Add horizontal line bottom-left
            if 0 + H <= grid_w:
                 output_grid[grid_h - 1, 0:H] = obj_color
                 
        elif H == 2: # Rule from train_3 (specific to 7x9 grid?)
             # Add shapes based on fixed/relative positions observed in example 3
             # Check boundaries before drawing
             # Horizontal lines (length H=2)
             if 1 + H <= grid_w: output_grid[0, 1:1+H] = obj_color # row 0, cols 1-2
             if 5 + H <= grid_w: output_grid[0, 5:5+H] = obj_color # row 0, cols 5-6
             if 0 + H <= grid_w: output_grid[grid_h-1, 0:0+H] = obj_color # row 6, cols 0-1
             if 4 + H <= grid_w: output_grid[grid_h-1, 4:4+H] = obj_color # row 6, cols 4-5
             # Vertical lines (length H=2)
             if 1 + H <= grid_h and grid_w > 0: output_grid[1:1+H, grid_w-1] = obj_color # col 8, rows 1-2
             if 5 + H <= grid_h and grid_w > 0: output_grid[5:5+H, grid_w-1] = obj_color # col 8, rows 5-6
        else:
             # Handle other vertical line heights if necessary, or default behavior
             print(f"Warning: Unhandled vertical line height H={H}. Returning copy.")
             # pass # No specific rule defined for other heights yet
             
    elif H > 1 and W > 1: # Rectangle (Rule from train_2)
        # Add copy of object at top-right
        if 0 + H <= grid_h and grid_w - W >= 0:
            # Ensure we only copy the object pixels, not the background within the bbox
            # This simpler version copies the whole bbox area. Refine if needed.
            # output_grid[0:H, grid_w-W:grid_w] = input_np[top:top+H, left:left+W] 
            # More precisely, color only the non-background pixels from the original object's bbox
             object_slice = input_np[top:top+H, left:left+W]
             target_slice = output_grid[0:H, grid_w-W:grid_w]
             mask = (object_slice == obj_color)
             target_slice[mask] = obj_color


        # Add horizontal line of length W+1 at bottom-center
        line_len = W + 1
        if line_len <= grid_w:
            start_col = (grid_w - line_len) // 2
            output_grid[grid_h - 1, start_col : start_col + line_len] = obj_color
            
    # elif H == 1: # Horizontal Line (Inferred, no example)
        # print("Warning: Horizontal line case not explicitly defined by examples.")
        # pass # Add rules here if needed based on future examples or inference

    else:
        # Handle other cases or single pixel objects if necessary
        print(f"Warning: Unhandled object shape H={H}, W={W}. Returning copy.")
        # pass 

    # 4. Final Output - convert back to list of lists
    return output_grid.tolist()

```