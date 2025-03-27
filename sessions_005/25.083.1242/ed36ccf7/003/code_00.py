"""
The transformation rule is a 90-degree clockwise rotation of the 3x3 input grid. The output grid is the result of rotating each element (pixel) in the input grid 90 degrees to the right, relative to the grid's center. The colors of the pixels remain unchanged during the rotation.
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

    # Rotate 90 degrees clockwise using numpy's rot90 function
    # k=-1 signifies a 90-degree clockwise rotation
    output_np = np.rot90(input_np, k=-1)

    # Convert back to list of lists
    output_grid = output_np.tolist()
    
    return output_grid