"""
The transformation extracts a 4x4 subgrid from the input grid. The subgrid is
formed by selecting four specific columns from the input and arranging them in a
fixed order.  The selected columns always correspond to the colors Maroon (9),
Yellow (4), White (0), and Yellow (4) respectively, regardless of the size of
the input or presence of other colors. The transformation identifies the
*first* instance of columns matching these colors. If a color does not exist
the transformation will select a column with all zeros (empty).

1.  **Identify Target Columns:** Locate the first column containing the color
    maroon (9). Locate the first column containing the color yellow (4). Locate
    the first column containing the color white (0). Locate the *second* column
    containing yellow (4).
2.  **Construct Output:** Create a 4x4 grid by using the identified columns, in
    the specified order (maroon, yellow, white, yellow).
"""

import numpy as np

def get_column(grid, col_index):
    return [row[col_index] for row in grid]

def find_first_column_with_color(grid, color):
    grid = np.array(grid)
    num_cols = grid.shape[1]
    for j in range(num_cols):
        if color in grid[:, j]:
            return grid[:, j].tolist()
    return [0] * grid.shape[0]  # Return a column of zeros if color not found

def find_second_column_with_color(grid, color):
    grid = np.array(grid)
    num_cols = grid.shape[1]
    first_found = False
    for j in range(num_cols):
        if color in grid[:, j]:
            if first_found:
                return grid[:, j].tolist()
            else:
                first_found = True
    return [0] * grid.shape[0]

def transform(input_grid):
    # 1. Identify Target Columns
    maroon_col = find_first_column_with_color(input_grid, 9)
    yellow_col_1 = find_first_column_with_color(input_grid, 4)
    white_col = find_first_column_with_color(input_grid, 0)
    yellow_col_2 = find_second_column_with_color(input_grid, 4)
    
    # Find first non-zero length
    col_lengths = [len(col) for col in [maroon_col, yellow_col_1, white_col, yellow_col_2] if len(col)>0]
   
    if not col_lengths: # if all are zero length
      output_length = 4
    else:
      output_length = col_lengths[0]

    # make all columns the same length by padding or truncating
    maroon_col = (maroon_col + [0] * output_length)[:output_length]
    yellow_col_1 = (yellow_col_1 + [0] * output_length)[:output_length]
    white_col = (white_col + [0] * output_length)[:output_length]
    yellow_col_2 = (yellow_col_2 + [0] * output_length)[:output_length]
    
    # 2. Construct Output
    output_grid = np.array([
        maroon_col,
        yellow_col_1,
        white_col,
        yellow_col_2,
    ]).T  # Transpose to arrange as columns

    return output_grid.tolist()