"""
1.  **Identify the target pattern:** Find the bounding box of the repeating subgrid within the input that matches this configuration:
    * It contains rows like "0 1 3 8 0".
    *   Surrounded on all sides by a solid-color background, it appears that a 6 border surrounds the area to output.

2.  **Extract the subgrid:** Copy the pixels within the bounding box.
3.  **Perform color substitution:** if the bounding box area includes a 5, replace 5 with 6 everywhere in output.
4.  **Create the output grid:** form the smaller output grid using the copied and potentially color-modified pixel data. Surrounding border included in the input is not included in the output.
"""

import numpy as np

def find_pattern(grid):
    # Find the pattern "0 1 3 8 0" in the grid
    rows, cols = grid.shape
    target_row = [0, 1, 3, 8, 0]
    target_len = len(target_row)

    for r in range(rows):
        for c in range(cols - target_len + 1):
            if np.array_equal(grid[r, c:c + target_len], target_row):
                return (r,c)
    return None

def find_bounding_box(grid, start_row, start_col):
    # find smallest rectangle around start_row, start_col, extending to the border that has all the same color.

    rows, cols = grid.shape
    
    #check above
    border_color = grid[start_row - 1, start_col]
    top = start_row
    while top >0 and np.all(grid[top-1,start_col:start_col +5] == border_color):
        top-=1
        
    #check below
    bottom = start_row
    while bottom < rows-1 and np.all(grid[bottom+1, start_col:start_col+5] == border_color):
        bottom+=1
    
    #check left
    left = start_col
    while left > 0 and grid[start_row,left-1] == border_color:
        left-=1

    #check right
    right = start_col + 5 #because of length of first found pattern.
    while right < cols -1 and grid[start_row, right] == border_color:
           right += 1
    return top, left, bottom, right
        
def transform(input_grid):
    # Convert input grid to a NumPy array
    grid = np.array(input_grid)

    # 1. Find the starting position of the target pattern ("0 1 3 8 0")
    pattern_start = find_pattern(grid)
    if pattern_start is None:
        return None  # Pattern not found

    start_row, start_col = pattern_start

    #2. find the boundaries
    top, left, bottom, right = find_bounding_box(grid, start_row, start_col)
    
    # 3. Extract the subgrid within the bounding box, not the bounding box itself.
    extracted_subgrid = grid[top+1:bottom, left+1:right]

    # 4. Perform color substitution (5 to 6)
    output_grid = np.where(extracted_subgrid == 5, 6, extracted_subgrid)

    
    return output_grid.tolist()