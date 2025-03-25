"""
Rotate the input grid 90 degrees counter-clockwise.
Then, reorder the columns such that the original row index i becomes the new column index n-1-i, where n is the number of rows/columns.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the input array counter-clockwise by 90 degrees.
    rotated_array = np.rot90(input_array, k=1)

    # Reorder columns: The original row i becomes the new column n-1-i.
    n = rotated_array.shape[1]
    output_array = np.empty_like(rotated_array)
    for i in range(n):
        new_column_index = n - 1 - i
        output_array[:, new_column_index] = rotated_array[:, i]
    
    # Convert output_array to list format
    output_grid = output_array.tolist()

    return output_grid