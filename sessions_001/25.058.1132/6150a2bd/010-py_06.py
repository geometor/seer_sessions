"""
The input grid is mirrored vertically (top-to-bottom).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Flip the rows vertically
    output_grid = np.flipud(output_grid)

    return output_grid