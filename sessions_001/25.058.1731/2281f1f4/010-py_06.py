"""
The transformation identifies horizontal ranges defined by gray pixels in each row. Within these horizontal ranges, excluding grey pixels, white pixels are replaced with red pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        # Find gray pixel indices in the current row
        gray_indices = np.where(input_grid[r] == 5)[0]

        if len(gray_indices) > 0 :
            #get the start of range
            start = gray_indices[0]
            #get the end of range
            end = gray_indices[-1]
            # Replace white pixels with red within the range (exclusive of gray pixels)
            for c in range(start+1,end):
                if output_grid[r,c] == 0:
                    output_grid[r, c] = 2

    return output_grid