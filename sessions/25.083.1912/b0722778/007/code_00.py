"""
The transformation extracts the two rightmost columns of the input grid and maps their values to create a new 2-column output grid. The mapping is specific to each of the two extracted columns and depends solely on the original pixel value in that column.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the two rightmost columns of the input, then remaps values
    based on the column and the original value.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid)
    height, width = input_array.shape
    last_two_cols = input_array[:, width-2:width]
    output_array = np.zeros_like(last_two_cols)

    # Combined mapping rules from both examples
    mapping_rules = [
        {8: 8, 0: 0, 5: 4, 4: 4, 3: 8, 2: 2, 9: 9, 7: 9},  # second-to-last column
        {6: 8, 8: 8, 0: 0, 5: 5, 4: 4, 3: 3, 7: 3, 2: 3, 9: 9}   # last column
    ]

    for row_index in range(height):
        for col_index in range(2):
            original_value = last_two_cols[row_index, col_index]
            # Apply mapping based on column and original value
            output_array[row_index, col_index] = mapping_rules[col_index].get(original_value, original_value) # Use get() to avoid key errors

    return output_array.tolist()