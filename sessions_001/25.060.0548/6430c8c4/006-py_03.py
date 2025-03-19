"""
The output grid maintains the same dimensions as the input grid. Every instance of an orange (7) pixel in the input is replaced by a green (3) pixel in the output. All other pixels in the input grid remain unchanged in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for efficient operations
    input_np = np.array(input_grid)

    # Create a copy to serve as the output grid
    output_np = input_np.copy()

    # Use NumPy's boolean indexing to find all orange (7) pixels
    orange_pixels = output_np == 7

    # Replace all orange pixels with green (3) using boolean indexing
    output_np[orange_pixels] = 3

    # Convert the NumPy array back to a list
    output_grid = output_np.tolist()
    return output_grid