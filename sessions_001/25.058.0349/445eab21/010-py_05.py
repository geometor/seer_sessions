"""
1. Check if the input grid contains the color orange (7).
2. If the input grid contains orange, create an output grid consisting of a single orange pixel.
3. If the input grid does not contain orange, return an empty output (or potentially raise an error, but for now, return a 1x1 grid with a default color of 0).
"""

import numpy as np

def transform(input_grid):
    # Check if the input grid contains orange (7)
    if np.any(input_grid == 7):
        # Create a 1x1 output grid with an orange pixel.
        output_grid = np.array([[7]])
    else:
        # Create a 1x1 output grid with a default color (0).
        output_grid = np.array([[0]])  
    return output_grid