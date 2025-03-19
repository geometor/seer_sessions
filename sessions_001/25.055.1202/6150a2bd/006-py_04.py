"""
The input grid is *transposed* to create the output grid. Transposing swaps rows and columns. The number of rows in the input grid becomes the number of columns in the output grid, and the number of columns in the input grid becomes the number of rows in the output grid. The color of each cell is preserved during the transposition.
"""

import numpy as np

def transform(input_grid):
    # Transpose the input grid using numpy
    output_grid = np.transpose(np.array(input_grid)).tolist()
    return output_grid