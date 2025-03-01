"""
The transformation identifies grey (5) objects and changes the color of their "inner" pixels based on the object's quadrant location within the grid. The presence of other colored pixels doesn't prevent the transformation of the grey objects, but grey objects are only transformed if they are in either the top-left or bottom-right quadrants.

1.  **Identify Grey Objects:** Find all contiguous regions (objects) of grey pixels (color 5).
2.  **Determine Quadrant and Transform:** For each grey object:
    *   Determine if the object is in the top-left or bottom-right quadrant of the grid.  The quadrant is determined by calculating the average row and column of the object's pixels and comparing this to the *inclusive* center of the grid. The center is inclusive, that is, it belongs to both sides, top and bottom, left and right.
    *   Identify the "inner" pixels of the grey object. "Inner" pixels are grey pixels with at least three grey neighbors (including diagonals).
    *   If in the top-left quadrant, change inner pixels to green (3).
    *   If in the bottom-right quadrant, change inner pixels to maroon (9).
3.  **Other Colors:** Pixels of other colors remain unchanged.
"""

import numpy as np

def find_grey_objects(grid):
    """
    Finds contiguous objects of grey color (5) in a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != 5):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)
        dfs(row + 1, col - 1, current_object)
        dfs(row - 1, col + 1, current_object)
        dfs(row - 1, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == 5:
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    objects.append(current_object)
    return objects


def get_quadrant(grid, object_pixels):
    """Determine the quadrant of an object within the grid.

    Args:
        grid: The input numpy array.
        object_pixels: list of (row,col) pixels

    Returns: quadrant "top_left", "top_right", "bottom_left", "bottom_right"
    """
    center_row = grid.shape[0] / 2
    center_col = grid.shape[1] / 2
    
    # find the "average" or representative row,col for the object
    total_row = 0
    total_col = 0
    for r,c in object_pixels:
        total_row += r
        total_col += c
    avg_row = total_row / len(object_pixels)
    avg_col = total_col / len(object_pixels)    

    if avg_row < center_row and avg_col < center_col:
        return "top_left"
    elif avg_row < center_row and avg_col >= center_col:
        return "top_right"
    elif avg_row >= center_row and avg_col < center_col:
        return "bottom_left"
    elif avg_row >= center_row and avg_col >= center_col:
        return "bottom_right"
    
    return "unknown"  # Should not normally happen

def find_inner_pixels(object_pixels):
    """
    Finds the inner pixels of a grey object. Inner pixels have at least 3 grey neighbors.
    """
    inner_pixels = []
    for row, col in object_pixels:
        neighbor_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) == (row, col):
                    continue  # Skip the pixel itself
                if (r, c) in object_pixels:
                    neighbor_count += 1
        if neighbor_count >= 3:
            inner_pixels.append((row, col))
    return inner_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grey_objects = find_grey_objects(input_grid)

    # change output pixels 
    for pixels in grey_objects:
        quadrant = get_quadrant(input_grid, pixels)
        inner_pixels = find_inner_pixels(pixels)
        if quadrant == "top_left":
            for r, c in inner_pixels:
                 output_grid[r,c] = 3   # green
        elif quadrant == "bottom_right":
            for r,c in inner_pixels:
                output_grid[r, c] = 9  # maroon

    return output_grid