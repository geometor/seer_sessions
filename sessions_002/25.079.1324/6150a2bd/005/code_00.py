"""
1. **Reflect:** Horizontally reflect the input grid across its vertical center.
2. **Redistribute:** Redistribute the pixel values within the reflected grid such that the largest values are placed in the bottom rows, and smaller values are placed at the top. The exact order within rows is not fully determined yet, nor how the 'sorting' is achieved.
"""

import numpy as np

def reflect_horizontal(grid):
    """Reflects a grid horizontally."""
    return np.fliplr(grid)

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # 1. Reflect the grid horizontally
    reflected_array = reflect_horizontal(input_array)

    # 2. Redistribute values: largest at the bottom, smallest at the top
    sorted_values = np.sort(reflected_array.flatten())
    output_array = sorted_values.reshape(reflected_array.shape)
    # flip to get the largest values at the bottom
    output_array = np.flipud(output_array)


    return output_array.tolist()