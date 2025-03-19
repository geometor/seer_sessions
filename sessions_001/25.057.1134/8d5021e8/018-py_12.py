"""
Expands a grid based on gray pixels, with adjacency rules. Output grid dimensions are determined by a rule.
Height: 3x input height, unless input height is 1, then output height is 4.
Width: 2x input width, unless input width is 1, then output width is 4.

Gray pixels attempt to expand to 2x2, but are reduced by adjacent gray pixels.
Remaining cells are filled with white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions based on input
    input_rows, input_cols = input_grid.shape
    output_rows = 3 * input_rows if input_rows > 1 else 4
    output_cols = 2 * input_cols if input_cols > 1 else 4
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    for i in range(input_rows):
        for j in range(input_cols):
            if input_grid[i, j] == 5:
                # Calculate the starting position for the expanded block
                start_row = i * 3 if input_rows > 1 else i*2 + (i//2)*2 # adjust for single-row
                start_col = j * 2

                # default is 2x2 cell, may be reduced
                row_end = min(start_row + 2, output_rows) # limit
                col_end = min(start_col + 2, output_cols)

                # corners
                top_left = i > 0 and j > 0 and input_grid[i-1,j-1] == 5
                top_right = i > 0 and j < input_cols - 1 and input_grid[i-1,j+1] == 5
                bottom_left = i < input_rows - 1 and j > 0 and input_grid[i+1,j-1] == 5
                bottom_right = i < input_rows - 1 and j < input_cols-1 and input_grid[i+1,j+1] == 5

                if top_left:
                    output_grid[start_row,start_col] = 5
                if top_right:
                    output_grid[start_row,start_col+1] = 5
                if bottom_left:
                    output_grid[start_row+1,start_col] = 5
                if bottom_right:
                    output_grid[start_row + 1, start_col + 1] = 5
                
                # sides, do after corners so they will reduce corner if necessary
                top = i > 0 and input_grid[i-1,j] == 5
                left = j > 0 and input_grid[i, j-1] == 5
                bottom = i < input_rows - 1 and input_grid[i+1,j] == 5
                right = j < input_cols - 1 and input_grid[i, j+1] == 5

                if top:
                    col_end = min(start_col + 2, output_cols)
                    row_end = min(start_row + 1, output_rows)
                if bottom:
                    col_end = min(start_col + 2, output_cols)
                    row_end = min(start_row + 1, output_rows)      
                if left:
                    col_end = min(start_col + 1, output_cols)
                    row_end = min(start_row + 2, output_rows)
                if right:
                    col_end = min(start_col + 1, output_cols)
                    row_end = min(start_row + 2, output_rows)


                # Fill the block, which will be 2x2, or less due to neighbors
                for row in range(start_row,row_end):
                    for col in range(start_col, col_end):
                         output_grid[row,col] = 5

    return output_grid