"""
Iterates through each row of the input grid. If a row contains only zeros, it remains unchanged in the output grid, but is padded
with zeros to match the maximum output width. Otherwise, the row's width is doubled by duplicating each pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as an empty list to hold rows
    output_grid = []
    max_width = 0

    # First pass to calculate doubled width for non-zero rows and find the maximum width
    for row in input_grid:
        if np.any(row):  # Check if the row contains any non-zero values
            expanded_row = []
            for element in row:
                expanded_row.extend([element, element])  # Duplicate each element
            max_width = max(max_width, len(expanded_row))
        else:
            max_width = max(max_width, len(row))

    # Second pass to build output grid
    for row in input_grid:
        if np.any(row):
            expanded_row = []
            for element in row:
                expanded_row.extend([element, element])
            output_grid.append(expanded_row)
        else:
           padded_row = list(row) + [0] * (max_width - len(row))
           output_grid.append(padded_row)


    return output_grid