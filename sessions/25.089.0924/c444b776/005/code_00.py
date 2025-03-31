import numpy as np

"""
Identifies a unique horizontal or vertical line composed entirely of yellow 
pixels (4) that acts as a separator. This separator line is uniquely characterized 
by being adjacent to a region composed entirely of white pixels (0). 
The task is to reflect the content of the other adjacent region (the pattern 
region) across this separator line into the white region, overwriting its 
initial content. The separator line itself and the original pattern region 
remain unchanged.
"""

def _find_yellow_lines(grid):
    """Finds complete horizontal and vertical lines of yellow pixels."""
    rows, cols = grid.shape
    yellow = 4
    h_lines = [r for r in range(rows) if np.all(grid[r, :] == yellow)]
    v_lines = [c for c in range(cols) if np.all(grid[:, c] == yellow)]
    return h_lines, v_lines

def _is_region_all_white(grid, orientation, index, side):
    """Checks if a specified region is entirely white (0)."""
    rows, cols = grid.shape
    white = 0
    region = None

    if orientation == 'horizontal':
        if side == 'above':
            if index == 0: return True # Region above row 0 is considered empty/white
            region = grid[:index, :]
        elif side == 'below':
            if index == rows - 1: return True # Region below last row is considered empty/white
            region = grid[index+1:, :]
    elif orientation == 'vertical':
        if side == 'left':
            if index == 0: return True # Region left of col 0 is considered empty/white
            region = grid[:, :index]
        elif side == 'right':
            if index == cols - 1: return True # Region right of last col is considered empty/white
            region = grid[:, index+1:]

    if region is None or region.size == 0:
        return True # Empty regions are considered all white

    return np.all(region == white)

def transform(input_grid):
    """
    Transforms the input grid by reflecting a pattern across a unique yellow 
    separator line identified by its adjacency to an all-white region.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    rows, cols = grid.shape
    white = 0

    # 1. Find potential separator lines
    h_lines, v_lines = _find_yellow_lines(grid)

    separator_info = None # Stores ('horizontal'/'vertical', index, 'pattern_side')

    # 2. Identify the unique separator by checking for adjacent all-white regions
    # Check horizontal candidates first
    for r in h_lines:
        is_below_white = _is_region_all_white(grid, 'horizontal', r, 'below')
        is_above_white = _is_region_all_white(grid, 'horizontal', r, 'above')

        if is_below_white and not is_above_white:
            separator_info = ('horizontal', r, 'above') # Pattern is above
            break
        if is_above_white and not is_below_white:
            separator_info = ('horizontal', r, 'below') # Pattern is below
            break
    
    # If no horizontal separator found, check vertical candidates
    if separator_info is None:
        for c in v_lines:
            is_right_white = _is_region_all_white(grid, 'vertical', c, 'right')
            is_left_white = _is_region_all_white(grid, 'vertical', c, 'left')

            if is_right_white and not is_left_white:
                separator_info = ('vertical', c, 'left') # Pattern is left
                break
            if is_left_white and not is_right_white:
                 separator_info = ('vertical', c, 'right') # Pattern is right
                 break

    # 3. Perform reflection if a valid separator was found
    if separator_info:
        orientation, index, pattern_side = separator_info

        if orientation == 'horizontal':
            R = index
            if pattern_side == 'above':
                # Reflect region above (0 to R-1) into region below (R+1 onwards)
                for r_src in range(R):
                    for c_src in range(cols):
                        r_tgt = 2 * R - r_src
                        if 0 <= r_tgt < rows:
                            # Copy pixel from original grid to output grid
                            output_grid[r_tgt, c_src] = grid[r_src, c_src] 
            else: # pattern_side == 'below'
                # Reflect region below (R+1 to end) into region above (0 to R-1)
                 for r_src in range(R + 1, rows):
                    for c_src in range(cols):
                        r_tgt = 2 * R - r_src
                        if 0 <= r_tgt < rows:
                             # Copy pixel from original grid to output grid
                             output_grid[r_tgt, c_src] = grid[r_src, c_src]

        elif orientation == 'vertical':
            C = index
            if pattern_side == 'left':
                 # Reflect region left (0 to C-1) into region right (C+1 onwards)
                 for r_src in range(rows):
                    for c_src in range(C):
                        c_tgt = 2 * C - c_src
                        if 0 <= c_tgt < cols:
                            # Copy pixel from original grid to output grid
                            output_grid[r_src, c_tgt] = grid[r_src, c_src]
            else: # pattern_side == 'right'
                 # Reflect region right (C+1 to end) into region left (0 to C-1)
                for r_src in range(rows):
                     for c_src in range(C + 1, cols):
                         c_tgt = 2 * C - c_src
                         if 0 <= c_tgt < cols:
                             # Copy pixel from original grid to output grid
                             output_grid[r_src, c_tgt] = grid[r_src, c_src]

    # 4. Return the result as a list of lists
    return output_grid.tolist()