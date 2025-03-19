"""
1.  **Identify**: Find all pixels with the color azure (8) in the input grid.
2.  **Count**: Count the number of azure pixels.
3. **Construct**: Create a new 1 x N grid, where N is the number of azure colored pixels in the input grid.
4. **Populate**: Fill all cells of the new grid with the value 8 (azure).
"""

import numpy as np

def transform(input_grid):
    # Count the number of azure pixels.
    azure_count = np.sum(input_grid == 8)

    # Create a new 1 x N grid, where N is the number of azure pixels.
    output_grid = np.full((1, azure_count), 8)

    return output_grid