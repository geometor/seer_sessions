```python
import numpy as np

"""
Transformation Rule:

1. Identify the 'separator row' which is the last row in the input grid 
   consisting entirely of gray (5) pixels.
2. Divide the input grid:
   - The 'key panel' consists of the rows between the top row (row 0, assumed 
     to be a gray border) and the separator row (exclusive).
   - The 'main grid' consists of all rows below the separator row.
3. Extract 'explicit key colors' from the key panel: Find all unique colors 
   that are not white (0) and not gray (5), and are adjacent (4-connectivity) 
   to at least one white (0) pixel within the key panel.
4. Determine the 'background color' of the main grid: Find the most frequent 
   color in the main grid. If azure (8) is present, exclude it when 
   determining the most frequent color, unless the grid *only* contains azure 
   or is empty.
5. Create the 'protected colors set' by combining the 'explicit key colors' 
   and the 'background color'. Add azure (8) to this set as well, as the 
   stamp color itself should not be overwritten.
6. Create a new grid (the output grid) that is initially an exact copy of 
   the input's main grid.
7. Iterate through every possible 2x2 block of pixels in the *input's* main 
   grid, defined by its top-left corner (r, c).
8. For each 2x2 block in the input's main grid, check if *any* of its four 
   pixels have a color that is present in the 'protected colors set'.
9. If *none* of the four pixels in the input 2x2 block match any of the 
   protected colors, then change the corresponding 2x2 block of pixels in 
   the *output* grid to be entirely azure (8).
10. If *at least one* pixel in the input 2x2 block *does* match a protected 
    color, make no changes to the corresponding 2x2 block in the output grid.
11. Return the final output grid.
"""

def _find_separator_row(grid):
    """
    Finds the row index of the last solid horizontal gray (5) line.
    Returns -1 if no such line exists.
    """
    separator_row = -1
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 5):
            separator_row = r # Keep track of the latest one found
    return separator_row

def _extract_explicit_keys(key_panel):
    """
    Extracts explicitly protected colors from the key panel.
    A color is protected if it's non-white(0)/non-gray(5) and adjacent to white(0).
    """
    protected_colors = set()
    rows, cols = key_panel.shape
    if rows == 0 or cols == 0: 
        return protected_colors # Handle empty key panel

    for r in range(rows):
        for c in range(cols):
            color = key_panel[r, c]
            # Ignore background (white 0) and borders (gray 5)
            if color != 0 and color != 5:
                # Check neighbors (4-connectivity) for white pixels
                has_white_neighbor = False
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check bounds before accessing neighbor
                    if 0 <= nr < rows and 0 <= nc < cols and key_panel[nr, nc] == 0:
                        has_white_neighbor = True
                        break # Found a white neighbor, no need to check others
                if has_white_neighbor:
                    protected_colors.add(color)
    return protected_colors

def _determine_background_color(grid, stamp_color=8):
    """
    Determines the most frequent color in the grid, excluding the stamp_color
    unless it's the only color present or the grid is mostly stamp_color.
    Returns -1 if grid is empty.
    """
    if grid.size == 0:
        return -1 # No background color for an empty grid

    colors, counts = np.unique(grid, return_counts=True)
    
    if len(colors) == 1:
        return colors[0] # Only one color exists, it's the background

    # Create a mask to exclude the stamp color
    non_stamp_mask = (colors != stamp_color)
    
    # Check if there are any colors other than the stamp color
    if np.any(non_stamp_mask):
        # Find the index of the max count among non-stamp colors
        idx_max_non_stamp = np.argmax(counts[non_stamp_mask])
        # Get the color corresponding to that index
        background_color = colors[non_stamp_mask][idx_max_non_stamp]
    else:
        # Only the stamp color exists in the grid
        background_color = stamp_color
        
    return background_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    stamp_color = 8 # Azure
    
    # 1. Identify Separator
    separator_row = _find_separator_row(input_np)
    
    # 2. Split Grid
    # Handle edge cases: no separator, or separator is the first row
    if separator_row <= 0: 
         # Treat row 0 as border if it's gray, otherwise whole grid is main
         if separator_row == 0 and np.all(input_np[0,:] == 5):
              key_panel = np.array([[]], dtype=int) # No functional key panel
              main_grid = input_np[1:, :]          # Main grid is below row 0 border
         else: # No separator found or it's negative
              key_panel = np.array([[]], dtype=int) 
              main_grid = input_np                 # Assume whole grid is main grid
    else:
        # Key panel is between row 0 (exclusive) and separator row (exclusive)
        key_panel = input_np[1:separator_row, :] 
        # Main grid is below separator row (inclusive)
        main_grid = input_np[separator_row + 1:, :]

    # Check if main_grid is empty after splitting
    if main_grid.size == 0:
        return [] # Return empty list if main grid is empty

    # 3. Extract Explicit Keys
    explicit_keys = _extract_explicit_keys(key_panel)
    
    # 4. Determine Background Color
    background_color = _determine_background_color(main_grid, stamp_color)
    
    # 5. Define Protected Colors Set
    protected_colors_set = set(explicit_keys)
    if background_color != -1: # Add background if found
        protected_colors_set.add(background_color)
    # Also protect the stamp color itself, ensuring areas originally azure
    # aren't stamped over if they happen to be in an unprotected block
    # Although, stamping azure with azure has no effect, this clarifies intent.
    # protected_colors_set.add(stamp_color) # Decided against adding stamp color explicitly
                                            # as stamping azure with azure has no visible effect.
                                            # The background rule should handle azure backgrounds.


    # 6. Initialize Output Grid
    output_grid = main_grid.copy()
    rows, cols = main_grid.shape

    # 7. Iterate through main_grid with a 2x2 window
    # Loop bounds ensure the 2x2 window fits within the grid
    for r in range(rows - 1):
        for c in range(cols - 1):
            
            # 8. Get the 2x2 window from the *input* main_grid
            window = main_grid[r:r+2, c:c+2] 
            
            # Check if any pixel color in the window is in the protected set
            is_protected = False
            for pixel_color in window.flat: 
                if pixel_color in protected_colors_set:
                    is_protected = True
                    break # Found a protected color, stop checking this window
            
            # 9. If the block is NOT protected, stamp it with azure
            if not is_protected:
                output_grid[r:r+2, c:c+2] = stamp_color # Modify the output_grid
                
            # 10. If protected, the output_grid retains the initially copied values

    # 11. Finalize and Return
    return output_grid.tolist() # Convert back to list of lists
```