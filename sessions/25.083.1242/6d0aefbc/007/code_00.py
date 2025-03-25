"""
The transformation rule is as follows: The output grid is created by first duplicating the input grid. Then, the *order of the columns* in the duplicated portion is reversed. Finally, the original input grid and the column-reversed duplicate are joined together, side-by-side. The output grid's width is twice the input grid's width, and the height remains the same. The transformation can be described as a horizontal mirror or reflection along the Y axis.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by appending a horizontally mirrored copy of itself to the right.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid)
    # Duplicate the input grid
    duplicated_grid = np.copy(input_grid)
    # Reverse the order of columns in the duplicated grid
    mirrored_grid = np.fliplr(duplicated_grid)
    # Concatenate the original grid with the mirrored grid along the horizontal axis
    output_grid = np.concatenate((input_grid, mirrored_grid), axis=1)

    return output_grid.tolist()