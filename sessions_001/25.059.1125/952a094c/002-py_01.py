"""
1.  **Identify the Enclosed Shape:** Find the contiguous block of pixels forming a closed shape, defined by its uniform border color.

2.  **Extract Inner Colors:** Identify all unique colors *inside* this enclosed shape.

3.  **Extract Border Color:** Identify the color of the border.

4.  **Mirror Border:** Transfer the border color to the output, in the same position as in the input

5.  **Populate Output Grid:**
    *   Create an output grid of the same dimensions as the input grid.
    *   Place the inner colors in a specific order in the output: Top-left corner, bottom-left corner, bottom-right corner, top-right corner. Order of placement should match order within the input grid, going clockwise.
    *   All other cells in the output grid, except for the enclosed shape's border, remain '0' (white).
"""

import numpy as np

def find_enclosed_shape(grid):
    # Find the contiguous block of pixels forming a closed shape
    rows, cols = grid.shape
    border_color = None
    inner_pixels = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_color):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != current_color:
            return

        visited.add((r, c))

        # Check neighbors
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        is_border = False
        for nr, nc in neighbors:
            if is_valid(nr, nc):
                if grid[nr, nc] != current_color:
                    is_border = True
            else: #edge of grid is also a border
                is_border = True
        
        if is_border:
            nonlocal border_color
            border_color = current_color
            return

        #If it is not border, add to inner pixels, and continue searching
        inner_pixels.append((r,c, current_color))
        for nr, nc in neighbors:
            dfs(nr, nc, current_color)
    
    # Iterate through all the grid
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != 0:
                dfs(r,c, grid[r,c])
            if border_color is not None:
                break
        if border_color is not None:
            break
                
    return border_color, inner_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find the enclosed shape and extract border and inner colors
    border_color, inner_pixels = find_enclosed_shape(input_grid)

    # Extract inner colors and their positions relative to shape's top-left
    if inner_pixels:
        inner_colors = []
        min_row = min(r for r, c, _ in inner_pixels)
        min_col = min(c for r, c, _ in inner_pixels)
        
        # Extract unique colors from inner_pixels and calculate positions
        unique_inner_pixels_map = {} # use map for dedup
        for r,c,color in inner_pixels:
            if color not in unique_inner_pixels_map:
                unique_inner_pixels_map[color] = (r,c) # keep first occurrence

        # now sort by position going clock wise
        for color, pos in unique_inner_pixels_map.items():
          inner_colors.append( (pos[0], pos[1], color) )
        inner_colors.sort(key=lambda x: (x[0], x[1])) # sort first by row, then by col

    # Mirror the border
    if border_color is not None:
        for r in range(rows):
            for c in range(cols):
                if input_grid[r, c] == border_color:
                    output_grid[r, c] = border_color

    # Populate corners of the output grid with inner colors
    if inner_colors:

        num_inner_colors = len(inner_colors)

        # Map inner colors to corners.
        if num_inner_colors >= 1:
            output_grid[0, 0] = inner_colors[0][2]  # Top-left
        if num_inner_colors >= 2:
            output_grid[rows - 1, 0] = inner_colors[1][2]  # Bottom-left
        if num_inner_colors >= 3:
            output_grid[rows - 1, cols - 1] = inner_colors[2][2]  # Bottom-right
        if num_inner_colors >= 4:
            output_grid[0, cols - 1] = inner_colors[3][2]  # Top-right

    return output_grid