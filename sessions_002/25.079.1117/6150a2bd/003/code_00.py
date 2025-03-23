"""
1. Transpose: The input grid is transposed (rows become columns and vice-versa).
2. Row-wise Reordering: Each row of the *transposed* grid is then processed individually. Within each row:
    *   Zero-valued elements are moved to the beginning (leftmost positions) of the row.
    *   Non-zero elements are reordered such that they are in the reverse order of the transposed row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing and then reordering each row based on element value.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Transpose the array.
    transposed_array = input_array.T

    # Reorder each row.
    output_array = []
    for row in transposed_array:
        zeros = [x for x in row if x == 0]
        non_zeros = [x for x in row if x != 0]
        reordered_row = zeros + non_zeros[::-1]  # Zeros first, then reversed non-zeros
        output_array.append(reordered_row)
    
    # Convert the NumPy array back to a list of lists.
    output_grid = np.array(output_array).tolist()

    return output_grid