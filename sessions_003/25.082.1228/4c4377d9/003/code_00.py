"""
The input grid is reflected vertically (flipped upside down), and then this
reflected grid is stacked on top of itself to create a new grid.
"""

import numpy as np

def reflect_vertical(grid):
    """Reflects the grid vertically."""
    return np.flipud(grid)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Create a vertically mirrored copy of the input grid
    vertical_reflection = reflect_vertical(input_grid)

    # stack the reflected grid with itself
    output_grid = np.concatenate((vertical_reflection, vertical_reflection), axis=0)


    return output_grid.tolist()