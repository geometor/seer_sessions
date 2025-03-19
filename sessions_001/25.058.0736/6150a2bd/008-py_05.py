"""
Rotate the input grid 90 degrees clockwise. Reflect the rotated grid across the main diagonal (top-left to bottom-right).

Reflect the input grid across the vertical axis, y. This moves (x,y) -> (width-1-x, y)
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it across the vertical axis.
    """
    # Convert input_grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Get the dimensions of the input grid
    height, width = input_array.shape
    
    # Initialize the output grid with zeros
    output_array = np.zeros_like(input_array)
    
    # Reflect across the vertical axis
    for y in range(height):
        for x in range(width):
            output_array[y, x] = input_array[y, width - 1 - x]
            
    return output_array.tolist()