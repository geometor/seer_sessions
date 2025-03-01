"""
The transformation rule involves expanding a colored square region from the input grid into a larger rectangular region in the output grid. The corners of the original color region in the input are marked with the color '2' (red) in the corresponding locations of the expanded region within the output grid. The bottom-right corner of the input grid is also copied to the bottom-right corner of the output grid. The rest of the output image is filled with white '0'.
"""

import numpy as np

def find_object(grid):
    # Find the bounding box of the non-zero, non-background object.
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None, None, None, None  # Handle empty object case

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    
    # check the top left and bottom right part
    top_left_color = -1
    bottom_right_color = -1
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col + 1):
            if grid[r,c]!=0:
                if top_left_color == -1:
                    top_left_color = grid[r,c]
                if r > (max_row + min_row)//2 and c > (max_col + min_col) //2:
                    bottom_right_color = grid[r,c]
    if bottom_right_color == -1:
        return (min_row, min_col, max_row, max_col), None, None, None, None
    else:
        # find the bottom right region
        rows, cols = np.where(grid == bottom_right_color)
        br_min_row, br_max_row = np.min(rows), np.max(rows)
        br_min_col, br_max_col = np.min(cols), np.max(cols)
        return (min_row, min_col, max_row, max_col), top_left_color, (br_min_row, br_min_col, br_max_row, br_max_col),bottom_right_color, grid.shape

def transform(input_grid):
    input_grid = np.array(input_grid)
    (min_row, min_col, max_row, max_col), top_left_color, (br_min_row, br_min_col, br_max_row, br_max_col),bottom_right_color, in_shape = find_object(input_grid)
    
    if top_left_color is None:  # Handle cases where no object is found
       return input_grid
        
    
    # calculate output grid
    output_grid_height = (max_row - min_row + 1) * 4 + in_shape[0]
    output_grid_width = (max_col - min_col + 1) * 4 + in_shape[1]
    output_grid = np.zeros((output_grid_height, output_grid_width), dtype=int)
    
    # expand object
    expanded_height = (max_row - min_row + 1) * 4
    expanded_width = (max_col - min_col + 1) * 4
    for i in range(expanded_height):
        for j in range(expanded_width):
            output_grid[i,j] = top_left_color

    # mark corner
    output_grid[min_row*4, min_col*4] = 2
    output_grid[min_row*4, max_col*4] = 2
    output_grid[max_row*4, min_col*4] = 2
    output_grid[max_row*4, max_col*4] = 2

    #copy bottom right object
    if bottom_right_color is not None:
        for i in range(br_max_row - br_min_row+1):
            for j in range(br_max_col - br_min_col + 1):
                output_grid[output_grid_height - in_shape[0] + br_min_row + i, output_grid_width - in_shape[1] + br_min_col + j] = input_grid[br_min_row + i, br_min_col+j]
    

    return output_grid