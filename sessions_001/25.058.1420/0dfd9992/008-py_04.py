"""
The transformation rule identifies and removes all white pixels (color value 0) from the input grid. After removing the white pixels, the remaining non-white pixels are compacted downwards. All non-white pixels shift downwards until they encounter another non-white pixel or the edge of the grid. The output grid will have different dimensions compared to the input grid if the compaction alters the number of rows.
"""

import numpy as np

def transform(input_grid):
    # Create a list to store non-white rows.
    non_white_rows = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Check if the row contains any non-white pixels.
        if np.any(row != 0):
            # Add the row to the list of non-white rows.
            non_white_rows.append(row[row != 0])

    # If there are no non-white pixels, return an empty grid.
    if not non_white_rows:
        return np.array([[]])
    
    # Concatenate the non-white pixel rows
    compacted_rows = []
    for row in input_grid:
        non_white_pixels = row[row != 0]
        if non_white_pixels.size > 0:
            compacted_rows.append(non_white_pixels)
    
    # Find the maximum length among all compacted rows
    max_length = max(len(row) for row in compacted_rows)
    
    # Pad shorter rows with 0s (white) to make them equal length
    padded_rows = [np.pad(row, (0, max_length - len(row)), constant_values=0) for row in compacted_rows]
    
    # Stack compacted rows vertically to form the output grid.
    output_grid = np.array(padded_rows)

    return output_grid