"""
The input is a grid. The output is the total number of red (2) pixels minus the total number of azure (8) pixels. The absolute value of the result.
"""

import numpy as np

def transform(input_grid):
    # Count the number of red (2) pixels.
    red_count = np.sum(input_grid == 2)
    
    # Count the number of azure (8) pixels.
    azure_count = np.sum(input_grid == 8)
    
    # Subtract the count of azure pixels from the count of red pixels.
    result = abs(red_count - azure_count)
    
    # Create a 1x1 output grid.
    output_grid = np.array([[result]])
    
    return output_grid