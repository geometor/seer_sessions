"""
The transformation rule is a direct copy of the input grid to the output grid.
The output grid has the same dimensions (height and width) and the same pixel
values at each corresponding position as the input grid. No pixels are added,
removed, or altered in any way.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a direct copy of the input grid.
    output_grid = np.copy(input_grid)

    # No further operations are needed as the transformation is a direct copy.
    return output_grid