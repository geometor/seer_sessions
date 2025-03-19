"""
The transformation rule involves a color mapping:
- Yellow (4) in the input becomes gray (5) in the output.
- Red (2) in the input becomes white (0) in the output.
- Green (3) in the input becomes white (0) in the output.
The spatial arrangement of the pixels is preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the defined color mapping.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Define the color mapping.
    color_map = {
        4: 5,  # Yellow to gray
        2: 0,  # Red to white
        3: 0   # Green to white
    }

    # Iterate through the input grid and apply the color mapping.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            input_color = input_grid[i, j]
            # change output pixels
            if input_color in color_map:
                output_grid[i, j] = color_map[input_color]

    return output_grid