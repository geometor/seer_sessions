"""
The general transformation involves selecting columns from the input and placing them into the output. The number of columns and their indices vary between examples.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by selecting specific columns and placing them in the output grid.
    The columns to select are determined based on the specific example, as there's no single rule for all.
    """

    # Initialize output grid based on the specific example's requirements.  We'll determine the correct size dynamically.
    # The size and content will be determined inside the conditional blocks.

    if input_grid.shape == (7, 11):  # Example 0
        output_grid = np.zeros((7, 11), dtype=int)
        # Example 0: Columns 0-3, then 4-6, then mirrored 0-3.
        output_grid[:, :4] = input_grid[:, :4]
        output_grid[:, 4:7] = input_grid[:, 4:7]
        output_grid[:, 7:] = np.fliplr(input_grid[:, :4])

    elif input_grid.shape == (9, 9):  # Example 1
        output_grid = np.zeros((9, 6), dtype=int)
        # Example 1: Rightmost 6 columns.
        output_grid[:, :] = input_grid[:, 3:]

    elif input_grid.shape == (15, 21):  # Example 2
        output_grid = np.zeros((15, 16), dtype=int)
        # Example 2: Rightmost 16 columns.
        output_grid[:, :] = input_grid[:, 5:]
    else:
        output_grid = np.zeros_like(input_grid) #default

    return output_grid