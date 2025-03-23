"""
1.  **Reverse the Input:** Take the rows of the input grid and reverse their order. The first row becomes the last, the second row becomes the second-to-last, and so on.
2.  **Transpose the Result:** Swap the rows and columns of the reversed grid. What were rows are now columns and vice-versa. This is mathematically equivalent to flipping the grid along its main diagonal (from the top-left to bottom-right corner).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of its rows and then transposing it.
    """
    # Reverse the order of the rows
    reversed_grid = input_grid[::-1]

    # Transpose the reversed grid
    output_grid = np.transpose(reversed_grid)

    return output_grid