"""
1. **Identify the Core:** Locate the contiguous non-zero cluster of pixels in the input grid. In this example it is pixels with values 8,3,2 near the top left.
2. **Horizontal Expansion:** Identify row 5 of the input grid. Replicate the non-zero pixel sequence ('8 3 2') across the entire width of the output grid on the corresponding row (row 5).
3. **Vertical mirroring**. Take the column of pixels in the core (column 3). Mirror these below the core downwards.
4. **Preserve and fill**: The original core is kept in the output. Fill every other value with 0.
"""

import numpy as np

def find_cluster(grid):
    # Find the bounding box of the non-zero elements
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:  # Handle the case of an all-zero grid
        return (0, 0, 0, 0)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find cluster bounding box.
    min_row, max_row, min_col, max_col = find_cluster(input_grid)

    # 1. Preserve original cluster.
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            output_grid[r,c] = input_grid[r,c]
            
    # 2. Horizontal Expansion on row 5 (index 4).
    row_to_expand = 4
    cluster_values = []
    for c in range(min_col,max_col+1):
        cluster_values.append(input_grid[row_to_expand,c])

    
    num_repeats = output_grid.shape[1] // len(cluster_values)
    remainder = output_grid.shape[1] % len(cluster_values)
    
    expanded_row = (cluster_values * num_repeats)
    
    for i in range(remainder):
        expanded_row.append(cluster_values[i])
    
    output_grid[row_to_expand,:] = expanded_row

    # 3. vertical mirroring.
    
    vertical_values = []
    for r in range(min_row,max_row+1):
        vertical_values.append(input_grid[r,min_col+2]) # column 2
    
    for i in range(len(vertical_values)):
      if (max_row+1+i) < output_grid.shape[0]:
        output_grid[max_row+1+i,min_col+2] = vertical_values[i]


    return output_grid