"""
The transformation identifies pairs of colors (4, 6) and (5, 9) in the input grid, swaps their positions, and arranges them into a condensed output grid, preserving their original relative order.
"""

import numpy as np

def find_pairs(grid):
    # Find coordinates of paired colors (4, 6) and (5, 9)
    pairs = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 4:
                # Check neighbors for 6
                neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1), (r-1,c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
                for nr, nc in neighbors:
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 6:
                        pairs.append( ((r,c), (nr, nc)) )
            elif grid[r, c] == 5:
                # Check neighbors for 9
                neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1), (r-1,c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
                for nr, nc in neighbors:
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 9:
                        pairs.append( ((r, c), (nr, nc)) )
    return pairs

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find pairs
    pairs = find_pairs(grid)

    # Determine output grid size
    num_pairs = len(pairs)
    if num_pairs == 0:
        return []
    
    # find height
    output_height = 0
    curr_row = -1
    for pair in pairs:
        first = pair[0]
        if first[0] > curr_row:
            curr_row = first[0]
            output_height += 1
    
    # find width
    output_width = 0
    curr_col = -1
    for pair in pairs:
        first = pair[0]
        if first[1] > curr_col:
            curr_col = first[1]
            output_width += 1
    
    width = 0
    for pair in pairs:
        width = max(width, abs(pair[0][1]-pair[1][1])+1)
            
    output_width = max(output_width, width)

    output_height = int(num_pairs * 2 / output_width)
    if num_pairs*2 % output_width != 0:
        output_height +=1
        

    # Initialize output grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Populate output grid with swapped pairs
    row, col = 0, 0
    for pair in pairs:
        first, second = pair
        output_grid[row, col] = grid[second]
        if col + 1 < output_width:
            output_grid[row,col+1] = grid[first]
        
        col += 2 # increment by two since we handle the neighbor in one go
        if col >= output_width:
            col = 0
            row += 1

    return output_grid.tolist()