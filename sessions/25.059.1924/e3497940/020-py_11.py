"""
The transformation extracts columns from the input grid that contain any pixel value other than 0 (white) and 5 (gray).
"""

import numpy as np

def get_columns_to_keep(input_grid):
    """
    Helper function to identify the indices of columns that contain values other than 0 or 5.
    """
    cols_to_keep = []
    for j in range(input_grid.shape[1]):
        if np.any((input_grid[:, j] != 0) & (input_grid[:, j] != 5)):
            cols_to_keep.append(j)
    return cols_to_keep

def transform(input_grid):
    """
    Transforms the input grid by keeping only columns that contain values other than 0 or 5.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Identify columns to keep (those with at least one element that's not 0 or 5)
    cols_to_keep = get_columns_to_keep(input_grid)
    
    # initialize output_grid with zeros based on selected column length
    output_grid = np.zeros((input_grid.shape[0], len(cols_to_keep)), dtype=int)


    # Extract the relevant columns and build output
    col_index = 0
    for j in cols_to_keep:
        output_grid[:, col_index] = input_grid[:,j]
        col_index += 1

    return output_grid.tolist()