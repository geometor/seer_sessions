"""
1.  **Identify the Primary Object:** Find the largest contiguous block of blue (1) pixels. This is the primary object. If there are multiple blue blocks of the same size, the program is undefined, and existing behavior can remain as is.

2.  **Inner Yellow Transformation:** Within the blue object, locate any yellow (4) pixels. Yellow pixels on rows with even indices (0-based) within the original input grid are changed to blue (1).

3.  **Border Transformation:**
    *   The original outer border of the blue object is removed (changed to black (0)).
    *   A new, one-pixel-wide, yellow (4) border is created around the *outermost* boundary of the *modified* blue object.

4.  **Preserve Other Colors:** Pixels that are not part of the blue object or the transformed yellow pixels within it remain unchanged. This explicitly includes any orange (7) objects, as observed in some examples.
"""

import numpy as np

def find_objects(grid, color):
    # returns a list of coordinates of the target color
    objects = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
          if grid[r,c] == color:
            objects.append((r,c))
    return objects

def get_contiguous_block(grid, start_row, start_col, color):
    # returns a set of the coordinates in a continguous block
    rows, cols = grid.shape
    visited = set()
    queue = [(start_row, start_col)]

    while queue:
        r, c = queue.pop(0)
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if grid[r, c] == color:
            neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
            for nr, nc in neighbors:
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    queue.append((nr, nc))
    return visited

def get_outer_border(block_coords):
    # identify the outermost border pixels of a contiguous block

    border = set()
    for r, c in block_coords:
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if (nr, nc) not in block_coords:
                border.add((r,c))
                break # once a coord is identified as border, stop checking neighbors
    return border
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify the Blue Region
    blue_pixels = find_objects(input_grid, 1)
    if blue_pixels:  # Check if blue_pixels is not empty
        # find largest blue region
        largest_blue_region = set()
        max_size = 0
        for r,c in blue_pixels:
            blue_region = get_contiguous_block(input_grid, r, c, 1)
            if len(blue_region) > max_size:
                largest_blue_region = blue_region
                max_size = len(blue_region)

        # Inner Yellow Transformation
        yellow_pixels = find_objects(input_grid, 4)
        for r, c in yellow_pixels:
            if (r,c) in largest_blue_region:
                if r % 2 == 0:  # Even row index
                    output_grid[r, c] = 1  # Change to blue

        # Remove existing outer border
        blue_border = get_outer_border(largest_blue_region)
        for r,c in blue_border:
            output_grid[r,c] = 0

        # get modified blue region for next step
        modified_blue_pixels = find_objects(output_grid, 1)
        
        if modified_blue_pixels: # handles edge case when no blue left
            modified_blue_region = get_contiguous_block(output_grid, modified_blue_pixels[0][0], modified_blue_pixels[0][1], 1)        
            # Create Outer Yellow Border
            modified_blue_border = get_outer_border(modified_blue_region)

            for r, c in modified_blue_border:
                output_grid[r,c] = 4

    # Preserve Other Colors - iterate all other colors
    for color in range(2,10): # skip black and blue
      if color != 4: # skip yellow - already processed
        other_pixels = find_objects(input_grid, color)
        for r,c in other_pixels:
            output_grid[r,c] = color
        
    return output_grid