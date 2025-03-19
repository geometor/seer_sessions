"""
The transformation identifies the object count of specific colors (blue and white), and displays them sequentially in the output.
"""

import numpy as np

def count_contiguous_blocks(grid, color):
    """
    Counts the number of contiguous blocks of a specific color in a grid.
    Uses a depth-first search approach.
    """
    visited = set()
    count = 0

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
        dfs(row + 1, col + 1)
        dfs(row + 1, col-1)
        dfs(row -1, col + 1)
        dfs(row -1, col -1)


    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                dfs(row, col)
                count += 1
    return count

def transform(input_grid):
    # Count contiguous blocks of blue (1)
    blue_count = count_contiguous_blocks(np.array(input_grid), 1)

    # Count contiguous blocks of white (0)
    white_count = count_contiguous_blocks(np.array(input_grid), 0)
    
    #find number of instances where a non-white is surrounded by white
    non_white = 0
    grid = np.array(input_grid)
    rows, cols = grid.shape
    for r in range(rows):
       for c in range(cols):
           if grid[r,c] != 0:
               #check neighbors - diagonals too
               is_surrounded = True
               for i in range(-1,2):
                   for j in range(-1, 2):
                       if (i != 0 or j != 0) and 0<= r+i < rows and 0<= c+j < cols:
                            if grid[r+i,c+j] != 0:
                                is_surrounded = False
               if is_surrounded == True:
                 non_white+=1


    # Construct the output grid (1x5)

    output_grid = np.array([[blue_count, white_count, 0 ,0, 0]]) #added an extra 0 per output size

    return output_grid.tolist()