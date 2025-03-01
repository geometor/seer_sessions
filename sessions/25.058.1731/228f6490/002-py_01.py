"""
The transformation rule involves identifying pairs of colors within the input grid and swapping their occurrences. The specific color pairs to be swapped are consistent across the examples: (8, 6), (3, 9), and (2, 8). Other colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by swapping specific color pairs.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.
        
    Returns:
        list of lists: The transformed grid.
    """
    # initialize output_grid
    output_grid = [row[:] for row in input_grid]  # Create a deep copy
    output_grid = np.array(output_grid)
    input_grid = np.array(input_grid)

    # change output pixels
    # Define the color swap pairs
    swap_pairs = [(8, 6), (3, 9), (2, 8)]

    for pair in swap_pairs:
        color1, color2 = pair
        
        # Find the locations (indices) of color1 and color2
        indices1 = np.where(input_grid == color1)
        indices2 = np.where(input_grid == color2)

        # Swap the colors in the output grid
        output_grid[indices1] = color2
        output_grid[indices2] = color1

    return output_grid.tolist()