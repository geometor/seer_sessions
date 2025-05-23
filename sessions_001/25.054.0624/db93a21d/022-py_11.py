"""
This program transforms an input grid containing two or three maroon rectangles into an output grid where the rectangles
are partially recolored to blue and green, and surrounded by green and blue filling.
"""

import numpy as np

def find_objects(grid, color):
    """Finds all rectangular objects of a given color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                # Get bounding box
                min_row = min(cell[0] for cell in current_object)
                max_row = max(cell[0] for cell in current_object)
                min_col = min(cell[1] for cell in current_object)
                max_col = max(cell[1] for cell in current_object)
                objects.append(((min_row, min_col), (max_row, max_col)))

    return objects

def get_top_left_rectangle(rectangles):
    """Returns the top-leftmost rectangle."""
    if not rectangles:
        return None
    return min(rectangles, key=lambda rect: (rect[0][0], rect[0][1]))

def get_bottom_right_rectangle(rectangles):
    """Returns the bottom-rightmost rectangle."""
    if not rectangles:
        return None
    return max(rectangles, key=lambda rect: (rect[1][0], rect[1][1]))

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the maroon rectangles
    maroon_rectangles = find_objects(input_grid, 9)

    for rect in maroon_rectangles:
        top_left, bottom_right = rect
        height = bottom_right[0] - top_left[0] + 1
        width = bottom_right[1] - top_left[1] + 1
        
        #Inner recolor
        if height > 1 and width > 1:
            # Calculate quarter boundaries
            row_mid = top_left[0] + height // 2
            col_mid = top_left[1] + width // 2
            #green quadrant
            output_grid[top_left[0]:row_mid, top_left[1]:col_mid] = 3
            #blue otherwise
            output_grid[top_left[0]:bottom_right[0] + 1, top_left[1]:bottom_right[1] + 1] = 1
            output_grid[top_left[0]:row_mid, top_left[1]:col_mid] = 3

        #border recolor

        #top two rows green
        output_grid[top_left[0]:min(top_left[0] + 2, bottom_right[0] + 1), top_left[1]:bottom_right[1] + 1] = 3
        #bottom two rows green
        output_grid[max(bottom_right[0] - 1, top_left[0]):bottom_right[0] + 1, top_left[1]:bottom_right[1] + 1] = 3
        #left two columns green
        output_grid[top_left[0]:bottom_right[0] + 1, top_left[1]:min(top_left[1] + 2, bottom_right[1]+1)] = 3
        #right two columns green
        output_grid[top_left[0]:bottom_right[0] + 1, max(bottom_right[1] - 1, top_left[1]):bottom_right[1] + 1] = 3


    #Surround with color
    top_left_rect = get_top_left_rectangle(maroon_rectangles)
    if top_left_rect:
        # Fill right with green
        output_grid[top_left_rect[0][0]:top_left_rect[1][0]+1, top_left_rect[1][1] + 1:top_left_rect[1][1] + 3] = 3
        # Fill below with blue
        output_grid[top_left_rect[1][0] + 1:top_left_rect[1][0] + 3, top_left_rect[0][1]:top_left_rect[1][1]+1] = 1
        
    bottom_right_rect = get_bottom_right_rectangle(maroon_rectangles)
    
    if bottom_right_rect:
        # Fill left with blue
        output_grid[bottom_right_rect[0][0]:bottom_right_rect[1][0]+1, bottom_right_rect[0][1]-2:bottom_right_rect[0][1]] = 1
        #Fill above with green
        output_grid[bottom_right_rect[0][0]-2:bottom_right_rect[0][0], bottom_right_rect[0][1]:bottom_right_rect[1][1]+1] = 3



    return output_grid