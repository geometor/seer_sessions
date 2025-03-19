"""
1.  **Replicate:** Copy the entire input row to create a new, identical row directly below the original.
2.  **Reflect/Mirror with Shift:** Create a third row by reflecting/mirroring the input row. During the reflection, shift the color values of each pixel one position to the *right*, within the row. If a color would shift "off the end" of the row, wrap it around to the beginning of that same row.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with tripled height.
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height * 3, input_width), dtype=int)

    # Replicate the input row.
    output_grid[0] = input_grid[0]
    output_grid[1] = input_grid[0]

    # Reflect/Mirror with shift.
    reflected_row = input_grid[0].copy()
    shifted_row = np.roll(reflected_row, 1)  # Use NumPy's roll for circular shift.
    output_grid[2] = shifted_row

    return output_grid