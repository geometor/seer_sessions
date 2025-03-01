"""
Change to green all white pixels in a region formed by the left, the top, and a line that would connect the azure pixels.
"""

import numpy as np

def find_red_rectangle(grid):
    # Find the coordinates of the red (2) rectangle.
    rows, cols = np.where(grid == 2)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def find_azure_pixels(grid):
    # Find the coordinates of the azure (8) pixels.
    rows, cols = np.where(grid == 8)
    return list(zip(rows, cols))

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the red rectangle.
    red_rect = find_red_rectangle(input_grid)
    if red_rect is None:
        return output_grid  # Return original if no red rectangle
    min_row_red, max_row_red, min_col_red, max_col_red = red_rect
    
    # Find azure pixels.
    azure_pixels = find_azure_pixels(input_grid)
    if not azure_pixels:
        return output_grid # Return original if no azure pixels
        
    # Find top right coordinate
    height, width = input_grid.shape
    top_right = (0, width-1)


    # Determine the bounding line.  We'll use the lowest azure pixel
    # as the starting point for our diagonal.
    azure_pixels.sort() # sort by row, ascending
    lowest_azure = azure_pixels[-1]
    
    # define filling function
    def fill_region(grid, start_row, start_col, end_row, end_col):
        # start filling from top right using flood fill approach
        rows, cols = grid.shape
        visited = np.zeros_like(grid, dtype=bool)
        stack = [(start_row, start_col)]

        while stack:
            row, col = stack.pop()

            if row < 0 or row >= rows or col < 0 or col >= cols or visited[row, col] or grid[row,col] != 0:
                continue

            visited[row, col] = True
            grid[row,col] = 3

            stack.append((row - 1, col)) #up
            stack.append((row , col+1)) #right
            
            if (row - lowest_azure[0]) >= (col - lowest_azure[1]) :
               #stop when below the diagonal line defined by the azure pixels
                stack.append((row + 1, col))  # Down
            if (row - lowest_azure[0]) > (col - lowest_azure[1]) :
               #stop when below the diagonal line defined by the azure pixels
                stack.append((row, col - 1))  # Left
                
    
    # fill
    fill_region(output_grid, 0, max_col_red +1, lowest_azure[0], lowest_azure[1]  )

    return output_grid