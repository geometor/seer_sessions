"""
The task involves extracting a specific sub-grid from the input grid. The output grid
is the largest square section from the top-left of the input grid that forms a block with uniform color (other than 0), before color changes along either rows or columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid by extracting the top-left
    square subgrid of uniform, non-zero color.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Get the top-left cell's color.
    top_left_color = input_grid[0, 0]

    # Handle the edge case where the top-left color is 0.
    if top_left_color == 0:
        for r in range(rows):
            for c in range(cols):
                if input_grid[r,c] != 0:
                    top_left_color = input_grid[r,c]
                    input_grid = input_grid[r:, c:]
                    rows, cols = input_grid.shape
                    break
            if top_left_color !=0:
                break
    if top_left_color == 0:
        return []

    # Find the size of the square subgrid.
    size = 0
    for i in range(min(rows, cols)):
        # Check if the row and column at the current size have uniform colors (excluding 0).
        row_uniform = all(input_grid[i, j] == top_left_color or input_grid[i,j] == 0 for j in range(i + 1))
        col_uniform = all(input_grid[j, i] == top_left_color or input_grid[j,i] == 0 for j in range(i + 1))

        
        if row_uniform and col_uniform:
             size = i + 1
        else:

            break

    # Extract the subgrid.
    output_grid = input_grid[:size, :size]
    
    new_output = []
    for i in range(size):
        all_0 = True
        for j in range(size):
            if output_grid[i,j] != 0:
                all_0 = False
        if not all_0:
            new_output.append(output_grid[i].tolist())
    if not new_output:
        return []
    output_grid = np.array(new_output)
    
    size = output_grid.shape[0]
    top_left_color = output_grid[0,0]
    if top_left_color == 0:
            for r in range(size):
                for c in range(size):
                    if output_grid[r,c] != 0:
                        top_left_color = output_grid[r,c]
                        break
                if top_left_color !=0:
                    break

    for i in range(min(output_grid.shape[0], output_grid.shape[1])):
        # Check if the row and column at the current size have uniform colors (excluding 0).
        row_uniform = all(output_grid[i, j] == top_left_color or output_grid[i,j] == 0 for j in range(i + 1))
        col_uniform = all(output_grid[j, i] == top_left_color or output_grid[j,i] == 0 for j in range(i + 1))
        if not (row_uniform and col_uniform):
            break
        size = i+1

    output_grid = output_grid[:size, :size]

    return output_grid.tolist()