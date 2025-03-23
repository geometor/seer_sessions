"""
The output grid is the same size as the input grid and filled entirely with the most frequent color in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array.
    input_grid = np.array(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Find the most frequent color in the input grid.
    values, counts = np.unique(input_grid, return_counts=True)
    most_frequent_color = values[np.argmax(counts)]

    # Create an output grid of the same dimensions, filled with the most frequent color.
    output_grid = np.full((rows, cols), most_frequent_color)

    return output_grid.tolist() # return as list