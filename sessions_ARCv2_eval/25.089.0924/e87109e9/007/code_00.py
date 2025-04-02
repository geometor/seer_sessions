import numpy as np

"""
Transformation Rule:

1. Identify the 'separator row' which is the last row in the input grid 
   consisting entirely of gray (5) pixels.
2. Divide the input grid:
   - The 'key panel' consists of the rows between the top row (row 0, assumed 
     to be a gray border) and the separator row (exclusive).
   - The 'main grid' consists of all rows below the separator row.
3. Extract the 'protected colors set' from the key panel: Find all unique 
   colors that are not white (0) and not gray (5), and are adjacent 
   (4-connectivity) to at least one white (0) pixel within the key panel.
4. Create a new grid (the output grid) that is initially an exact copy of 
   the input's main grid.
5. Iterate through every possible 2x2 block of pixels in the *input's* main 
   grid, defined by its top-left corner (r, c).
6. For each 2x2 block in the input's main grid, check if *any* of its four 
   pixels have a color that is present in the 'protected colors set'.
7. If *none* of the four pixels in the input 2x2 block match any of the 
   protected colors, then change the corresponding 2x2 block of pixels in 
   the *output* grid to be entirely azure (8).
8. If *at least one* pixel in the input 2x2 block *does* match a protected 
   color, make no changes to the corresponding 2x2 block in the output grid.
9. Return the final output grid.
"""


def _find_separator_row(grid):
    """
    Finds the row index of the last solid horizontal gray (5) line.
    Returns -1 if no such line exists.
    """
    separator_row = -1
    for r in range(grid.shape[0]):
        # Check if all elements in the row are equal to 5
        if np.all(grid[r, :] == 5):
            separator_row = r # Keep track of the latest one found
    return separator_row

def _extract_protected_colors(key_panel):
    """
    Extracts explicitly protected colors from the key panel.
    A color is protected if it's non-white(0)/non-gray(5) and adjacent to white(0).
    """
    protected_colors = set()
    rows, cols = key_panel.shape
    # Return empty set if key panel is empty or invalid
    if rows == 0 or cols == 0: 
        return protected_colors

    for r in range(rows):
        for c in range(cols):
            color = key_panel[r, c]
            # Check if the color is a potential key (not white or gray)
            if color != 0 and color != 5:
                # Check neighbors (4-connectivity) for white pixels
                has_white_neighbor = False
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check bounds before accessing neighbor's color
                    if 0 <= nr < rows and 0 <= nc < cols and key_panel[nr, nc] == 0:
                        has_white_neighbor = True
                        break # Found a white neighbor, no need to check others for this pixel
                # If a white neighbor was found, add the color to the protected set
                if has_white_neighbor:
                    protected_colors.add(color)
    return protected_colors


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    stamp_color = 8 # Azure color for stamping
    
    # 1. Identify Separator Row
    separator_row = _find_separator_row(input_np)
    
    # 2. Split Grid into Key Panel and Main Grid
    # Handle edge cases: no separator found, or separator is the first row (row 0)
    if separator_row <= 0: 
         # If separator is row 0 and it's gray, treat it as a border
         if separator_row == 0 and np.all(input_np[0,:] == 5):
              key_panel = np.array([[]], dtype=int) # No functional key panel below border
              main_grid = input_np[1:, :]          # Main grid is everything below the border row
         else: # No separator found or it's negative (shouldn't happen based on examples)
              key_panel = np.array([[]], dtype=int) # Assume no key panel
              main_grid = input_np                 # Assume whole grid is main grid
    else:
        # Normal case: key panel is between row 0 (exclusive) and separator row (exclusive)
        key_panel = input_np[1:separator_row, :] 
        # Main grid starts from the row after the separator row
        main_grid = input_np[separator_row + 1:, :]

    # Handle case where splitting results in an empty main grid
    if main_grid.size == 0:
        return [] # Return empty list if main grid is empty

    # 3. Extract Protected Colors Set from Key Panel
    protected_colors_set = _extract_protected_colors(key_panel)
    
    # 4. Initialize Output Grid as a copy of the main grid
    output_grid = main_grid.copy()
    rows, cols = main_grid.shape

    # 5. Iterate through main_grid with a 2x2 window
    # Loop bounds ensure the 2x2 window (r:r+2, c:c+2) fits within the grid dimensions
    for r in range(rows - 1):
        for c in range(cols - 1):
            
            # 6. Get the 2x2 window from the *input* main_grid
            window = main_grid[r:r+2, c:c+2] 
            
            # Check if any pixel color within the window is in the protected set
            is_protected = False
            for pixel_color in window.flat: # Iterate through the 4 pixels in the window
                if pixel_color in protected_colors_set:
                    is_protected = True
                    break # Found a protected color, stop checking this window
            
            # 7. If the block is NOT protected, stamp it with azure in the output grid
            if not is_protected:
                output_grid[r:r+2, c:c+2] = stamp_color 
                
            # 8. If protected, do nothing (output_grid retains the initially copied values)

    # 9. Finalize and Return the transformed grid as a list of lists
    return output_grid.tolist() 