"""
The transformation rule is a 90-degree clockwise rotation of the input grid. The input grid is rotated such that:

*   The last column of the input becomes the first row of the output.
*   The second-to-last column of the input becomes the second row of the output.
* The third-to-last coloumn of the input becomes the third row of the output.
* This continues until all columns have become rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise using NumPy's rot90 function.
    # The 'k=-1' argument specifies a single 90-degree clockwise rotation.
    output_array = np.rot90(input_array, k=-1)

    # Convert the rotated NumPy array back to a list.
    output_grid = output_array.tolist()
    return output_grid