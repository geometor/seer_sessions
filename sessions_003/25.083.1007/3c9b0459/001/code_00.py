"""
The transformation rule involves two steps:
1. Reverse the order of elements in each row of the input grid.
2. Transpose the modified grid (swap rows and columns).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing each row and then transposing the result.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Reverse each row of the array.
    reversed_rows = np.fliplr(input_array)
    
    # Transpose the array (swap rows and columns).
    transposed_array = reversed_rows.T
    
    # Convert the NumPy array back to a list of lists.
    output_grid = transposed_array.tolist()
    
    return output_grid