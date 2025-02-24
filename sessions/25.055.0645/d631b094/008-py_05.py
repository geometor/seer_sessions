"""
Extracts all red cells (value 2) from the input grid and forms a single-row grid containing only the red cells.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting all red cells (value 2) and 
    creating a 1xN output grid where N is the number of red cells.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find all cells with the value 2 (red cells).
    red_cells = input_array[input_array == 2]

    # Create a new 1xN array where N is the number of red cells.
    output_grid = red_cells.reshape(1, -1)

    return output_grid.tolist()