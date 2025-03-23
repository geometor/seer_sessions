"""
Swaps the second and third columns of the input 3x3 grid to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by swapping its second and third columns.

    Args:
        input_grid (list of lists): A 3x3 grid represented as a list of lists.

    Returns:
        list of lists: The transformed 3x3 grid.
    """
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Create a copy to avoid modifying the original input
    output_array = np.copy(input_array)

    # Swap the second and third columns.  numpy uses 0-indexing
    output_array[:, [1, 2]] = output_array[:, [2, 1]]

    # convert back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid