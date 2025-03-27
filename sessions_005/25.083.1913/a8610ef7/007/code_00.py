"""
1.  **Initialization:** Create an output grid identical in dimensions to the input grid.
2.  **Pixel Traversal:** Examine each pixel in the input grid, proceeding row by row, and within each row, from left to right.
3.  **Color Preservation:** If the current pixel is white (0), its value remains unchanged in the corresponding position of the output grid.
4.  **Azure Transformation:** If the current pixel is azure (8):
    *   Maintain a *global* counter (across all rows) to track the occurrences of azure pixels encountered so far.
    *   If the counter is even, replace the azure pixel with red (2) in the output grid.
    *   If the counter is odd, replace the azure pixel with gray (5) in the output grid.
    *   Increment the global azure counter.
5.  **Output:** Return the resulting output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    eight_count = 0  # Global counter for '8's

    # Iterate through each row and column
    for i in range(rows):
        for j in range(cols):
            # Preserve '0'
            if input_grid[i, j] == 0:
                continue  # Do nothing, keep '0' as is
            # Conditional Substitution for '8'
            elif input_grid[i, j] == 8:
                # Determine color based on eight_count
                if eight_count % 2 == 0:
                    output_grid[i, j] = 2  # Red
                else:
                    output_grid[i, j] = 5  # Gray
                eight_count += 1  # Increment the global '8' counter

    return output_grid