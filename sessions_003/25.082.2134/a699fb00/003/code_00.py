"""
Iterates through the input grid, identifies horizontally adjacent '1' (blue) pixels,
and inserts a '2' (red) pixel between them, shifting subsequent pixels on the row to the right.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Initialize with a copy
    rows, cols = input_grid.shape

    for r in range(rows):
        # Create a list to store the modified row
        modified_row = list(input_grid[r])

        insertions = 0  # Track insertions to adjust indices
        for c in range(cols - 1):  # Iterate up to the second-to-last element
            original_c = c + insertions
            
            if modified_row[original_c] == 1 and modified_row[original_c + 1] == 1:
                # Insert '2' and shift elements
                modified_row.insert(original_c + 1, 2)
                insertions += 1

        # Update the output grid with the modified row, padding with zeros if necessary
        output_grid[r] = np.pad(modified_row, (0, cols - len(modified_row)), 'constant')

    return output_grid.tolist()