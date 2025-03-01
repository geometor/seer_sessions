"""
1.  **Identify Objects:** Locate all contiguous blocks of non-black (non-zero) colored pixels in the input grid. Consider each of these blocks as a separate object.

2.  **Discard Background:** Ignore all black (0) pixels.

3. **Rearrange and pack:** Arrange the colored objects into a 2x2 grid and pack each color into its own quadrant. Maintain original colors and shapes. There is a consistent placement:
    - The top-left quadrant contains any blue (1) objects.
    - The top-right quadrant contains any azure (8) objects.
    - The bottom-left quadrant contains any yellow (4) objects
    - The bottom-right quadrant contains any red (2) objects.

4. If two blocks of the same color exist, pack them together in their specific quadrant.

5. If there are no objects for a particular color, fill the quadrant for that color with white(0).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                if obj_pixels:
                    objects.append({'color': grid[row, col], 'pixels': obj_pixels})
    return objects

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Find objects
    objects = find_objects(input_grid)

    # Place objects in quadrants
    for obj in objects:
        color = obj['color']
        pixels = obj['pixels']

        # Determine quadrant and placement within quadrant
        if color == 1:  # Blue
            quadrant_row, quadrant_col = 0, 0
        elif color == 8:  # Azure
            quadrant_row, quadrant_col = 0, 2
        elif color == 4:  # Yellow
            quadrant_row, quadrant_col = 2, 0
        elif color == 2:  # Red
            quadrant_row, quadrant_col = 2, 2
        else:
            continue # skip if we do not know where to put

        # find top left of object in its own coordinates
        min_row = min(p[0] for p in pixels)
        min_col = min(p[1] for p in pixels)
        
        # Place pixels in quadrant, adjusting for relative position
        for r, c in pixels:
            # use delta from min row, col
            dr = r - min_row
            dc = c - min_col
            
            row_in_quadrant = quadrant_row + dr
            col_in_quadrant = quadrant_col + dc
          
            if 0 <= row_in_quadrant < 4 and 0<= col_in_quadrant < 4:
                output_grid[row_in_quadrant,col_in_quadrant] = color
            

    return output_grid