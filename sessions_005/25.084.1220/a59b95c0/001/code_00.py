"""
1. Calculate K: Determine the number of unique pixel values (colors) present in the input grid.
2. Determine Output Size: The output grid's dimensions will be K times the input grid's dimensions (height * K, width * K).
3. Tile the Input: Create the output grid by repeating (tiling) the input grid pattern K times horizontally and K times vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by tiling it based on the number of unique colors present.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # 1. Calculate K: Find the number of unique non-zero pixel values
    unique_colors = np.unique(input_array)
    k = len(unique_colors)

    # Handle edge case where k might be 0 if grid is empty (though constraints likely prevent this)
    if k == 0:
        # Or return an empty grid, depending on desired behavior for empty input
        return [] 
        
    # Get input dimensions
    input_height, input_width = input_array.shape

    # 2. Determine Output Size (redundant if using np.tile, but good for clarity)
    # output_height = input_height * k
    # output_width = input_width * k

    # 3. Tile the Input: Use numpy's tile function to repeat the input array
    # The second argument is a tuple specifying the number of repetitions along each axis (rows, columns)
    output_array = np.tile(input_array, (k, k))

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
