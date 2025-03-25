"""
The transformation rule is a 90-degree clockwise rotation of a 3x3 grid.
Swap the first and last columns of the given grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid (list of lists): The 3x3 input grid.

    Returns:
        list of lists: The rotated 3x3 output grid.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid)

    # Swap first and last columns
    input_np[:, [0, 2]] = input_np[:, [2, 0]]  # Corrected indexing

    # Convert back to list of lists
    output_grid = input_np.tolist()
    
    return output_grid