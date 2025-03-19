"""
1.  Identify Blue Objects: Find all distinct, contiguous regions of blue (1) pixels.  A contiguous region is defined as a group of blue pixels connected horizontally or vertically.

2.  Sort by Vertical Position: Order the identified blue objects from top to bottom based on the row index of their topmost pixel.

3.  Topmost Object Outline: For the topmost blue object, change the color of any pixels that are directly adjacent (horizontally or vertically) to the blue object but are *not* blue (1) or the background color (0) to red (2).

4.  Bottommost Object Outline: For the bottommost blue object, change the color of any pixels that are directly adjacent (horizontally or vertically) to the blue object but are *not* blue (1) or the background color (0) to green (3).

5. if a pixel is part of the outline of *both* the top and bottom object, do not modify it.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))

        return region

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                objects.append(dfs(row, col))
    return objects

def get_outline(grid, object_pixels):
    """
    Find the outline pixels of an object.
    """
    outline = set()
    for row, col in object_pixels:
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for n_row, n_col in neighbors:
            if 0 <= n_row < grid.shape[0] and 0 <= n_col < grid.shape[1] and grid[n_row, n_col] != 1:
                outline.add((n_row, n_col))
    return list(outline)

def transform(input_grid):
    # Initialize output grid with the same dimensions and background color
    output_grid = np.copy(input_grid)

    # Find blue objects
    blue_objects = get_objects(input_grid, 1)

    # Sort blue objects by topmost row coordinate
    blue_objects.sort(key=lambda obj: min(pixel[0] for pixel in obj))
    
    # Get outlines
    outlines = []
    for obj in blue_objects:
        outlines.append(get_outline(input_grid,obj))


    if len(blue_objects) >= 1:
        # Topmost blue object: replace outline with red (2) if original is not blue (1) or background (0)
        top_outline = outlines[0]
        for row, col in top_outline:
             if  input_grid[row, col] !=0 :
                output_grid[row,col] = 2

    if len(blue_objects) >= 2:
        # Bottommost blue object, replace outline with Green (3)
        bottom_outline = outlines[-1]
        for row, col in bottom_outline:
             if input_grid[row, col] !=0 :
                # check for overlap
                skip = False
                for top_row, top_col in top_outline:
                    if (row,col) == (top_row, top_col):
                        skip = True
                if not skip: 
                    output_grid[row, col] = 3


    return output_grid