import numpy as np

"""
Finds all rectangular blocks composed entirely of white (0) pixels in the input grid.
Selects the block based on the following criteria in order:
1. Maximum height.
2. Maximum area (width * height). If heights are equal, this means maximum width.
3. Minimum row index of the top-left corner (top-most).
4. Minimum column index of the top-left corner (left-most).
Copies the input grid to the output grid and then fills the selected white rectangular block with magenta (6).
"""

def find_white_rectangles(grid):
    """
    Identifies all maximal rectangular blocks of white (0) pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple represents a rectangle
              (row, col, height, width).
    """
    rows, cols = grid.shape
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool) # To avoid redundant checks

    for r in range(rows):
        for c in range(cols):
            # If the cell is white and hasn't been part of a found maximal rectangle starting at an earlier point
            if grid[r, c] == 0 and not visited[r, c]:
                max_w = cols - c
                # Find the maximum possible height for a rectangle starting at (r, c) with width 1
                h = 0
                while r + h < rows and grid[r + h, c] == 0:
                    h += 1
                
                # Now expand width, reducing height if necessary
                for current_h in range(1, h + 1):
                    current_w = 1
                    # Check how far right we can go for this height
                    while c + current_w < cols:
                        is_white_column = True
                        # Check the column at c + current_w from row r to r + current_h - 1
                        for row_idx in range(r, r + current_h):
                           if grid[row_idx, c + current_w] != 0:
                               is_white_column = False
                               break
                        if not is_white_column:
                           break # Cannot extend width further for this height
                        current_w += 1
                    
                    # Record this rectangle
                    rectangles.append((r, c, current_h, current_w))
                    # Mark visited cells within this rectangle to avoid redundant checks? 
                    # No, finding *all* rectangles, not just maximal ones for now.
                    # Let's reconsider: the prompt says "all possible rectangular blocks".
                    # Does this mean *maximal* blocks or *any* sub-block?
                    # Example 1: input[0, 2:7] is 0 0 0 0 0. This contains 1x1, 1x2, ..., 1x5 blocks.
                    # The output fills the whole 2x5 block. This suggests we look for maximal blocks.
                    # However, the description says "all possible". Let's try finding *all* first.
                    # If we find *all*, the criteria (max height, max area) should still pick the largest one.

    # The above loop finds many overlapping rectangles. We need a better approach
    # to find just the potential *maximal* rectangles efficiently, or filter later.
    # Let's try finding *all* rectangles first, as it's simpler to implement.
    
    all_rects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 0:
                # Try expanding from (r,c) as top-left
                max_h = 0
                while r + max_h < rows and grid[r + max_h, c] == 0:
                    max_w = 0
                    while c + max_w < cols:
                        is_solid = True
                        # Check the rectangle from (r,c) to (r+max_h, c+max_w)
                        for i in range(r, r + max_h + 1):
                           for j in range(c, c + max_w + 1):
                               if grid[i,j] != 0:
                                   is_solid = False
                                   break
                           if not is_solid:
                               break
                        
                        if is_solid:
                           # This rectangle (r, c, max_h+1, max_w+1) is valid white block
                           all_rects.append((r, c, max_h + 1, max_w + 1))
                           max_w += 1
                        else:
                           break # Cannot expand width further for this height
                    max_h += 1 # Try next potential height

    if not all_rects:
        return []

    # Filter based on criteria
    # 1. Max height
    max_height = 0
    for _, _, h, _ in all_rects:
        if h > max_height:
            max_height = h
    
    height_filtered_rects = [(r, c, h, w) for r, c, h, w in all_rects if h == max_height]

    # 2. Max area (equivalent to max width since height is fixed now)
    max_width = 0 # Area = max_height * width
    for _, _, _, w in height_filtered_rects:
         if w > max_width:
             max_width = w

    area_filtered_rects = [(r, c, h, w) for r, c, h, w in height_filtered_rects if w == max_width]

    # 3. Top-most (min row)
    min_row = rows # Initialize with a value larger than any possible row index
    for r, _, _, _ in area_filtered_rects:
        if r < min_row:
            min_row = r
            
    row_filtered_rects = [(r, c, h, w) for r, c, h, w in area_filtered_rects if r == min_row]

    # 4. Left-most (min col)
    min_col = cols # Initialize with a value larger than any possible col index
    for _, c, _, _ in row_filtered_rects:
         if c < min_col:
             min_col = c

    # There should be exactly one rectangle left matching all criteria
    final_rect = [(r, c, h, w) for r, c, h, w in row_filtered_rects if c == min_col]

    # Return just the single best rectangle if found
    return final_rect # Should be a list containing zero or one rectangle tuple

def transform(input_grid):
    """
    Finds the largest white (0) rectangle based on height, then area, then position,
    and fills it with magenta (6).

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all potential white rectangles and select the best one based on criteria
    selected_rects = find_white_rectangles(output_grid)

    # If a rectangle was selected
    if selected_rects:
        # There should be only one rectangle in the list after filtering
        r, c, h, w = selected_rects[0]
        
        # Fill the selected rectangle in the output grid with magenta (6)
        output_grid[r:r+h, c:c+w] = 6

    return output_grid