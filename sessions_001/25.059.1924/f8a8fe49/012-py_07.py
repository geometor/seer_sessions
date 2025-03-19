"""
Transformation Rule:

1.  **Identify Red Structures:** Locate contiguous areas of red pixels. These form the reference structures.
2.  **Identify Gray Pixels and their Relation to Red Structures:** Find all gray pixels. Determine if these gray pixels are located *between* two "mostly vertical" sections of the red structure.
3. **Reposition Gray Pixels:**
    *   Gray pixels that are found between nearly verticle red structure sections are moved.
    *   The gray pixels that are moved are repositioned one column to the left of the left red section and one column to the right of the right red section.
    * The moved gray pixels form vertical lines adjacent to and outside of the red structure's almost vertical bars. The height of these vertical lines is equal to the number of gray pixels that are between vertical bars in the original input.
"""

import numpy as np

def find_red_structures(grid):
    """Finds contiguous areas of red pixels."""
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) == 0:
        return []

    visited = set()
    structures = []

    def dfs(row, col, current_structure):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != 2:
            return
        visited.add((row, col))
        current_structure.append((row, col))
        dfs(row + 1, col, current_structure)
        dfs(row - 1, col, current_structure)
        dfs(row, col + 1, current_structure)
        dfs(row, col - 1, current_structure)

    for r, c in red_pixels:
        if (r, c) not in visited:
            current_structure = []
            dfs(r, c, current_structure)
            structures.append(current_structure)

    return structures

def find_mostly_vertical_sections(red_structure):
    """Identifies mostly vertical sections within a red structure."""
    if not red_structure:
      return [],[]
    
    #find leftmost and rightmost columns
    cols = [p[1] for p in red_structure]
    min_col = min(cols)
    max_col = max(cols)

    left_section = []
    right_section = []
    
    #simplification, take leftmost and rightmost columns of the structure
    for r,c in red_structure:
      if c == min_col:
        left_section.append((r,c))
      elif c == max_col:
        right_section.append((r,c))

    return left_section, right_section

def is_between(gray_pixel, left_section, right_section):
    """Checks if a gray pixel is between two vertical sections."""
    if not left_section or not right_section:
      return False
    
    gray_row, gray_col = gray_pixel
    
    left_col = left_section[0][1]
    right_col = right_section[0][1]

    if gray_col > left_col and gray_col < right_col:
      #check for mostly vertical by comparing row extents
      left_rows = [p[0] for p in left_section]
      right_rows = [p[0] for p in right_section]

      min_row = max(min(left_rows), min(right_rows))
      max_row = min(max(left_rows), max(right_rows))
      if gray_row >= min_row and gray_row <= max_row:
        return True

    return False

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find red structures.
    red_structures = find_red_structures(input_grid)

    # Find gray pixels.
    gray_pixels = np.argwhere(input_grid == 5)
    
    # Iterate through red structures and find mostly vertical sections
    for red_structure in red_structures:
      left_section, right_section = find_mostly_vertical_sections(red_structure)

      # Gray pixels to move
      gray_pixels_to_move = []      
      for gray_pixel in gray_pixels:
        if is_between(gray_pixel, left_section, right_section):
          gray_pixels_to_move.append(gray_pixel)

      # Reposition gray pixels that are between vertical bars of red structure
      num_to_move = len(gray_pixels_to_move)
      
      if num_to_move > 0:  # only move if there are any
        #clear pixels
        for r,c in gray_pixels_to_move:
          output_grid[r,c] = 0

        #find placement
        left_rows = [p[0] for p in left_section]
        right_rows = [p[0] for p in right_section]
        left_col = left_section[0][1]
        right_col = right_section[0][1]

        min_row = max(min(left_rows), min(right_rows))
        new_left_col = left_col - 1
        new_right_col = right_col + 1

        # place new columns
        for i in range(num_to_move):
          output_grid[min_row + i, new_left_col] = 5
          output_grid[min_row + i, new_right_col] = 5
    
    return output_grid