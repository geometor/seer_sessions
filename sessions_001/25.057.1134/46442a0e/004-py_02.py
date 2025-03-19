"""
The transformation rule involves tiling the input grid to create an output grid that is twice the size in both dimensions. The input grid is directly tiled without any mirroring.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid into an output grid by tiling. The output
    grid's dimensions are double the input grid's dimensions.
    """
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Tile the input array to double its size in both dimensions.
    output_array = np.tile(input_array, (2, 2))

    return output_array.tolist()