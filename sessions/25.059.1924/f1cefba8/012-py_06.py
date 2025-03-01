"""
1.  **Identify the Blue Region:** Find the contiguous block of blue (1) pixels. This is the primary object.

2.  **Inner Yellow Transformation:** The yellow (4) pixels inside the blue object are modified based on their position relative to the boundaries of the blue object.
    *   Yellow pixels at even rows are changed to blue.
    *   The outer border of the blue object is removed.

3.  **Create Outer Yellow Border:** A new, one-pixel-wide, yellow border is created around the *outermost* boundary of the modified blue object.

4. **Preserve Orange Object(s):** If present, orange objects are not changed.
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
        blue_region = get_contiguous_block(input_grid, blue_pixels[0][0], blue_pixels[0][1], 1)


        # Inner Yellow Transformation
        yellow_pixels = find_objects(input_grid, 4)
        for r, c in yellow_pixels:
            if (r,c) in blue_region:
                if r % 2 == 0:  # Even row index
                    output_grid[r, c] = 1  # Change to blue

        # Remove existing outer border
        blue_border = get_outer_border(blue_region)
        for r,c in blue_border:
            output_grid[r,c] = 0

        # get modified blue region for next step
        modified_blue_pixels = find_objects(output_grid, 1)
        modified_blue_region = get_contiguous_block(output_grid, modified_blue_pixels[0][0], modified_blue_pixels[0][1], 1)
        
        # Create Outer Yellow Border
        modified_blue_border = get_outer_border(modified_blue_region)
        
        for r, c in modified_blue_border:
            output_grid[r,c] = 4

    # Preserve Orange object - find and preserve all other objects
    orange_pixels = find_objects(input_grid, 7)
    for r,c in orange_pixels:
        output_grid[r,c] = 7
        
    return output_grid