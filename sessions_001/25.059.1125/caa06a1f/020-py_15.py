"""
1.  **Identify Colors:** The relevant colors are blue (1) and azure (8).
2.  **Count Pixels:** Count the occurrences of blue and azure pixels in the input grid.
3.  **Equal Count Transformation:** If the counts of blue and azure are equal:
    *   Remove the last row of the grid.
4.  **Unequal Count Transformation:**
     * If the count of azure is greater than the count of blue, change one azure to blue.
     * If the count of blue is greater than the count of azure, change one blue to azure.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Count pixels
    blue_count = 0
    azure_count = 0
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if input_grid[row, col] == 1:
                blue_count += 1
            elif input_grid[row, col] == 8:
                azure_count += 1

    # Equal Count Transformation
    if blue_count == azure_count:
        # Remove last row and adjust the counts
        output_grid = output_grid[:-1]

    # Unequal Count Transformation (performed on input grid, or updated grid if counts were equal)
    blue_count = 0
    azure_count = 0

    for row in range(output_grid.shape[0]):
        for col in range(output_grid.shape[1]):
            if output_grid[row, col] == 1:
                blue_count += 1
            elif output_grid[row, col] == 8:
                azure_count += 1

    if azure_count > blue_count:
        # change one azure to blue.
        changed = False
        for row in range(output_grid.shape[0]):
            for col in range(output_grid.shape[1]):
                if output_grid[row, col] == 8 and not changed:
                    output_grid[row, col] = 1
                    changed = True

    elif blue_count > azure_count:
        # change one blue to azure
        changed = False
        for row in range(output_grid.shape[0]):
            for col in range(output_grid.shape[1]):
                if output_grid[row, col] == 1 and not changed:
                    output_grid[row, col] = 8
                    changed = True

    return output_grid