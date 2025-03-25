"""
Iterates through the input grid, identifies horizontally adjacent '1' (blue) pixels,
and inserts a '2' (red) pixel between them. The row length is maintained by truncating.
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
            
            # Check bounds after insertions
            if original_c + 1 >= len(modified_row):
                break

            if modified_row[original_c] == 1 and modified_row[original_c + 1] == 1:
                # Insert '2' and shift elements, only if space remains.
                if len(modified_row) < cols:
                  modified_row.insert(original_c + 1, 2)
                  insertions += 1
                else: # we are out of room
                  break


        # Update the output grid with the modified row, truncating to original size.
        output_grid[r] = modified_row[:cols]

    return output_grid.tolist()