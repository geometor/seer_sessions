```python
import numpy as np
from collections import Counter
import itertools

"""
Transforms an input grid based on identifying internal white rectangular areas, 
determining a target size based on the mode dimensions of these areas, 
overlaying the contents of these areas onto a target-sized canvas, and finally 
cropping any surrounding whitespace.

1.  Identify all distinct, maximal rectangular blocks composed entirely of white 
    pixels (color 0) that are located inside the single-pixel outer border of 
    the input grid.
2.  For each identified white rectangle, determine its height and width.
3.  Find the most common height (Mode Height) and the most common width 
    (Mode Width) among all identified white rectangles.
4.  Prepare an intermediate canvas grid with dimensions Mode Height x Mode Width, 
    initially filled entirely with white pixels (0).
5.  Iterate through each identified white rectangle from the input grid:
    a. Extract the content grid (pixels from the input grid within the 
       rectangle's bounds).
    b. Create a temporary grid, also of size Mode Height x Mode Width, filled 
       with white pixels (0).
    c. Place the extracted content onto the top-left corner of this temporary 
       grid. Crop the content if it's larger than Mode Height x Mode Width; 
       pad with white if it's smaller.
    d. Overlay the temporary grid onto the intermediate canvas grid: For each 
       pixel, if the temporary grid pixel is non-white AND the corresponding 
       intermediate canvas pixel is white, update the intermediate canvas pixel 
       to the temporary grid pixel's color.
6.  After processing all white rectangles, crop the intermediate canvas grid by 
    removing any all-white rows or columns from the outside edges inwards.
7.  Return the final cropped grid.
"""

def find_maximal_white_rectangles(grid):
    """
    Finds all maximal contiguous rectangular areas of white (0) pixels,
    ignoring the 1-pixel border.
    Returns a list of tuples: (row, col, height, width).
    """
    h, w = grid.shape
    if h <= 2 or w <= 2: # Cannot have content inside a border
        return []

    # Search area is inside the border
    inner_grid = grid[1:-1, 1:-1] 
    inner_h, inner_w = inner_grid.shape
    visited = np.zeros_like(inner_grid, dtype=bool)
    rectangles = []

    for r in range(inner_h):
        for c in range(inner_w):
            if inner_grid[r, c] == 0 and not visited[r, c]:
                # Found potential top-left corner of a white rectangle
                # Determine max width from this point
                max_c = c
                while max_c + 1 < inner_w and inner_grid[r, max_c + 1] == 0 and not visited[r, max_c + 1]:
                    max_c += 1
                current_w = max_c - c + 1

                # Determine max height for this initial width
                max_r = r
                possible = True
                while possible and max_r + 1 < inner_h:
                    # Check if the next row maintains the rectangle shape and color
                    for col_check in range(c, c + current_w):
                        if inner_grid[max_r + 1, col_check] != 0 or visited[max_r + 1, col_check]:
                            possible = False
                            break
                    if possible:
                        max_r += 1
                current_h = max_r - r + 1

                # Check if we can expand width further down
                for r_check in range(r + 1, r + current_h):
                    max_c_row = c + current_w - 1
                    while max_c_row + 1 < inner_w and inner_grid[r_check, max_c_row + 1] == 0 and not visited[r_check, max_c_row + 1]:
                        # Check if all cells above in this new column are also white and unvisited
                        valid_col_expansion = True
                        for r_above in range(r, r_check + 1):
                           if inner_grid[r_above, max_c_row + 1] != 0 or visited[r_above, max_c_row+1]:
                               valid_col_expansion = False
                               break
                        if valid_col_expansion:
                           max_c_row += 1
                        else:
                           break
                           
                    new_w = max_c_row - c + 1
                    if new_w < current_w: # Shrink width if necessary to maintain rectangular shape
                        current_w = new_w

                # Mark visited and store rectangle (adjusting coords for original grid)
                for row_idx in range(r, r + current_h):
                    for col_idx in range(c, c + current_w):
                        visited[row_idx, col_idx] = True
                
                # Store coordinates relative to the original grid (add 1 for border offset)
                rectangles.append({'r': r + 1, 'c': c + 1, 'h': current_h, 'w': current_w})

    # Filter for maximality (crude way: remove rectangles contained within others)
    # A better way is integrated into the search, the above attempts this.
    # Let's refine the check: only start a search if grid[r-1, c] or grid[r, c-1] was non-white
    
    # --- Re-implementing search focusing on top-left corners ---
    visited = np.zeros_like(inner_grid, dtype=bool)
    rectangles = []
    for r in range(inner_h):
        for c in range(inner_w):
            is_top = (r == 0 or inner_grid[r-1, c] != 0)
            is_left = (c == 0 or inner_grid[r, c-1] != 0)
            
            if inner_grid[r, c] == 0 and not visited[r,c]: #and is_top and is_left: #<-- this check makes it miss some cases if shapes touch
                 # Found a white cell, potentially part of a new maximal rectangle. Determine its extent.
                
                # Find width
                rect_w = 0
                while c + rect_w < inner_w and inner_grid[r, c + rect_w] == 0:
                     rect_w += 1

                # Find height
                rect_h = 0
                while r + rect_h < inner_h:
                    valid_row = True
                    for k in range(rect_w):
                        if c + k >= inner_w or inner_grid[r + rect_h, c + k] != 0:
                            valid_row = False
                            break
                    if valid_row:
                        rect_h += 1
                    else:
                        break
                
                # Now, we have a rectangle of size rect_h x rect_w starting at (r, c)
                # Mark cells as visited for this specific rectangle to avoid recounting sub-parts
                # However, we need *maximal* rectangles. The first one found might not be.
                # A better flood-fill or region growing approach is complex.

                # Let's try a simpler scan and record all possible white rectangles
                # Then filter based on maximality later? Or just assume the first pass gets it?
                # The logic above tries to find height first, then adjusts width. Let's stick with that
                # Mark cells visited only after finding the full HxW rectangle from a top-left candidate
                
                # --- Reverting to a modified version of the first attempt, seems more robust ---
                if inner_grid[r, c] == 0 and not visited[r, c]:
                    # Max width at current row r
                    start_c = c
                    while c + 1 < inner_w and inner_grid[r, c + 1] == 0 and not visited[r, c + 1]:
                        c += 1
                    current_w = c - start_c + 1
                    
                    # Max height for this width starting at start_c
                    start_r = r
                    possible_h = True
                    while possible_h and r + 1 < inner_h:
                        for col_idx in range(start_c, start_c + current_w):
                            if inner_grid[r + 1, col_idx] != 0 or visited[r + 1, col_idx]:
                                possible_h = False
                                break
                        if possible_h:
                            r += 1
                    current_h = r - start_r + 1

                    # Mark visited
                    is_maximal = True # Assume maximal until proven otherwise
                    for row_idx in range(start_r, start_r + current_h):
                       for col_idx in range(start_c, start_c + current_w):
                           if visited[row_idx, col_idx]:
                               is_maximal = False # Part of this rectangle was already claimed by another
                           visited[row_idx, col_idx] = True

                    # Store if it wasn't part of an already found larger one
                    # (This check might still not be perfect for complex overlaps)
                    if is_maximal:
                         rectangles.append({'r': start_r + 1, 'c': start_c + 1, 'h': current_h, 'w': current_w})
                    
                    c = start_c + current_w -1 # Continue scan after the found rect width
                    r = start_r # Reset row scanning for next column checks

    return rectangles


def crop_grid(grid):
    """Removes all-zero rows and columns from the border of the grid."""
    if grid.size == 0:
        return grid
    if np.all(grid == 0):
        return np.array([[0]]) # Return 1x1 white if grid is all white

    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    
    if not np.any(rows) or not np.any(cols):
         return np.array([[0]]) # Should not happen if check above works, but safety

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    return grid[rmin:rmax+1, cmin:cmax+1]

def transform(input_grid):
    """
    Finds white rectangles, calculates mode size, overlays content, crops result.
    """
    input_grid = np.array(input_grid, dtype=int)
    h, w = input_grid.shape

    # 1. Identify white rectangles inside the border
    white_rectangles = find_maximal_white_rectangles(input_grid)

    if not white_rectangles:
        # No white rectangles found, perhaps return empty or input?
        # Based on examples, this shouldn't happen. Let's return empty grid.
        return [[]]

    # 2. Record heights and widths
    heights = [rect['h'] for rect in white_rectangles]
    widths = [rect['w'] for rect in white_rectangles]

    # 3. Calculate Mode Height and Mode Width
    # Handle empty lists case although checked above
    if not heights or not widths:
       return [[]]
       
    height_counts = Counter(heights)
    width_counts = Counter(widths)
    
    # Find the mode (most frequent value). If ties, Counter().most_common(1) picks one.
    mode_height = height_counts.most_common(1)[0][0]
    mode_width = width_counts.most_common(1)[0][0]

    # 4. Prepare intermediate canvas
    intermediate_canvas = np.zeros((mode_height, mode_width), dtype=int)

    # 5. Iterate, extract, resize/align, and overlay
    for rect in white_rectangles:
        r, c, h_rect, w_rect = rect['r'], rect['c'], rect['h'], rect['w']
        
        # 5a. Extract content
        content = input_grid[r : r + h_rect, c : c + w_rect]
        
        # 5b/5c. Create temporary grid and place content (crop/pad)
        temp_grid = np.zeros((mode_height, mode_width), dtype=int)
        
        # Determine copy dimensions
        copy_h = min(h_rect, mode_height)
        copy_w = min(w_rect, mode_width)
        
        temp_grid[0:copy_h, 0:copy_w] = content[0:copy_h, 0:copy_w]
        
        # 5d. Overlay onto intermediate canvas (non-white onto white)
        # Create masks for where temp is non-zero and canvas is zero
        temp_non_white_mask = (temp_grid != 0)
        canvas_is_white_mask = (intermediate_canvas == 0)
        
        # Update canvas only where temp is non-white AND canvas is white
        update_mask = temp_non_white_mask & canvas_is_white_mask
        intermediate_canvas[update_mask] = temp_grid[update_mask]

    # 6. Crop final whitespace
    final_grid = crop_grid(intermediate_canvas)

    # 7. Return as list of lists
    return final_grid.tolist()
```