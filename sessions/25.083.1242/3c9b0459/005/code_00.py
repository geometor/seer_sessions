"""
The transformation rule is a reflection of the input grid across both its horizontal and vertical axes. This is equivalent to a 180-degree rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it across both its horizontal and vertical axes.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the reflected output grid.
    """
    # Convert the input list to a NumPy array
    input_array = np.array(input_grid)

    # Reflect across the horizontal axis (flip vertically)
    reflected_horizontal = np.flipud(input_array)

    # Reflect across the vertical axis (flip horizontally)
    reflected_both = np.fliplr(reflected_horizontal)
    
    # Convert the reflected array back to a list
    output_grid = reflected_both.tolist()

    return output_grid