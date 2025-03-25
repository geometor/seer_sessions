"""
1.  **Identify Gray Objects:** Find all contiguous blocks of gray (5) pixels in the input grid.

2.  **Replace Borders with Azure:** For each identified gray object, locate the border/edge of the grey object. Replace these gray pixels with azure (8) pixels.

3.  **Replace Vertical Middle with Red:** For each gray object, identify a vertical line of pixels splitting the grey object as close to the middle as possible. Replace those grey pixels with red (2) pixels. If a grey object is one pixel wide, it's considered its own middle.

4.  **Output:** Create a new grid with the replaced azure and red pixels, keeping all other pixels (white (0) in this case) the same as the input.
"""

import numpy as np

def find_objects(grid, color):
    """Find contiguous objects of a given color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_object_border(object_pixels, grid_shape):
    """Get the border pixels of an object."""
    border_pixels = []
    for r, c in object_pixels:
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        for nr, nc in neighbors:
            if (nr < 0 or nr >= grid_shape[0] or nc < 0 or nc >= grid_shape[1] or (nr, nc) not in object_pixels):
                border_pixels.append((r,c))
                break #pixel is a border if one neighbor isn't the right color
    return border_pixels

def get_vertical_middle(object_pixels):
    """Get the vertical middle pixels of an object"""
    #find range of columns in object
    cols = [c for r, c in object_pixels]
    min_col = min(cols)
    max_col = max(cols)

    #find middle column
    mid_col = (min_col + max_col) // 2

    #return all object pixels in that column
    middle_pixels = [(r,c) for r, c in object_pixels if c == mid_col]
    return middle_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape

    # find grey objects
    gray_objects = find_objects(input_grid, 5)

    # replace gray pixels at object borders with azure
    for obj in gray_objects:
        border = get_object_border(obj, grid_shape)
        for r, c in border:
            output_grid[r, c] = 8
    
    # replace gray pixels at vertical middle with red
    for obj in gray_objects:
        middle = get_vertical_middle(obj)
        for r, c in middle:
            output_grid[r,c] = 2
    
    return output_grid