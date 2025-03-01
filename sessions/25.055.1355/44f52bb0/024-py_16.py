"""
1. Identify the largest contiguous block of red pixels in the input grid. This block forms a rectangle.
2. Change all pixels within this red rectangle to blue.
3. Create output with dimensions equal to the identified rectangle.
4. Place the new blue rectangle in the top-left corner of the output grid.
"""

import numpy as np

def find_largest_red_rectangle(grid):
    """Finds the largest contiguous block of red pixels (value 2)."""
    rows, cols = grid.shape
    max_area = 0
    top_left = (0, 0)
    bottom_right = (0, 0)

    visited = np.zeros((rows, cols), dtype=bool)

    def dfs(row, col, current_top_left, current_area):
        nonlocal max_area, top_left, bottom_right
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != 2):
            return current_area, current_top_left, (row -1 if row > 0 else row, col -1 if col > 0 else col)

        visited[row, col] = True
        current_area += 1

        # Expand the rectangle in all four directions
        area1, top_left1, bottom_right1 = dfs(row + 1, col, current_top_left, current_area)  # Down
        area2, top_left2, bottom_right2 = dfs(row - 1, col, current_top_left, area1)        # Up
        area3, top_left3, bottom_right3 = dfs(row, col + 1, top_left2, area2)        # Right
        area4, top_left4, bottom_right4 = dfs(row, col - 1, top_left3, area3)     # Left
        
        current_bottom_right = bottom_right4
            
        if area4 > max_area:
            max_area = area4
            top_left = top_left4
            bottom_right = current_bottom_right

        return area4, top_left, bottom_right


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2 and not visited[r, c]:
                dfs(r, c, (r, c), 0)

    return top_left, bottom_right


def transform(input_grid):
    # Find the largest red rectangle
    input_grid = np.array(input_grid)
    top_left, bottom_right = find_largest_red_rectangle(input_grid)

    # If no red pixels are found, return an empty grid (or handle as needed)
    if top_left == (0, 0) and bottom_right == (0, 0) and input_grid[0,0] != 2:
        return np.array([])

    # Calculate dimensions of the rectangle
    height = bottom_right[0] - top_left[0] + 1
    width = bottom_right[1] - top_left[1] + 1
    
    # if no rectangle was found, return empty grid.
    if height <=0 or width <= 0:
        return np.array([])

    # Initialize output_grid as a blue rectangle of the calculated dimensions
    output_grid = np.ones((height, width), dtype=int)

    return output_grid