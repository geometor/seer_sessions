"""
The transformation rule is as follows:
1. Identify a repeating 7x7 pattern in the input grid.
2. Locate all pixels with the value 0.
3. Replace each 0 with the value from the corresponding position in the repeating 7x7 pattern, determined by the (x, y) coordinates of the 0 within the entire grid.
4. Leave other non-zero pixels unchanged.
"""

import numpy as np

def get_repeating_pattern(grid, pattern_size=7):
    """Extracts the repeating pattern from the grid."""
    pattern = grid[:pattern_size, :pattern_size]
    return pattern

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = input_grid.copy()
    pattern_size = 7
    pattern = get_repeating_pattern(input_grid, pattern_size)

    rows, cols = input_grid.shape

    # Iterate through the entire grid
    for r in range(rows):
        for c in range(cols):
            # Replace 0s based on repeating pattern
            if input_grid[r, c] == 0:
                output_grid[r, c] = pattern[r % pattern_size, c % pattern_size]

    return output_grid.tolist()