"""
Take the input grid and reverse the order of its rows. 
The first row becomes the last, the second row becomes the second-to-last, 
and so on, until the last row becomes the first. 
The resulting grid with the reordered rows is the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Reverses the order of rows in the input grid (vertical flip).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the output grid with rows reversed.
    """
    # Convert the input list of lists to a NumPy array for efficient slicing
    input_array = np.array(input_grid, dtype=int)

    # Reverse the order of the rows using slicing.
    # [::-1] creates a reversed view/copy of the array along the first axis (rows).
    output_array = input_array[::-1] 
    
    # Alternatively, np.flipud could be used:
    # output_array = np.flipud(input_array)

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid