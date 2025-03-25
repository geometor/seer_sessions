"""
The input grid is mirrored vertically, such that the order of the input rows are reversed and duplicated on the center.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically mirroring it and duplicating the original at the center.
    
    Args:
        input_grid (list of lists): The input 2D grid.
    
    Returns:
        list of lists: The transformed 2D grid.
    """
    input_grid = np.array(input_grid)
    # Reverse Rows
    reversed_rows = np.flipud(input_grid)

    # Duplicate the Input and reversed
    duplicated_input = np.copy(input_grid)
    
    reversed_duplicated_input = np.flipud(duplicated_input)

    # Concatenate the reversed rows and duplicated input.
    output_grid = np.concatenate((reversed_rows,reversed_duplicated_input), axis=0)

    return output_grid.tolist()