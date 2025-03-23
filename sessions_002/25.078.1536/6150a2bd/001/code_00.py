"""
The input grid is transposed (reflected across the main diagonal) and then the rows of the transposed grid are reversed.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing it and then reversing the order of its rows.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.
        
    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Transpose the array (reflect across the main diagonal).
    transposed_array = np.transpose(input_array)

    # Reverse the order of the rows.
    output_array = np.flipud(transposed_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid