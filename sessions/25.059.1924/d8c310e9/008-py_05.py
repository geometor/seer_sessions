"""
1.  **Identify Pattern:** Search for a repeating pattern within the input grid. The pattern can be of any height (not just two rows), starting from any row. The pattern is defined as a sequence of rows that repeats at least once within the input grid.
2.  **Replicate Pattern:** If a repeating pattern is found, replicate the full sequence of repeating rows.
3. **Preserve blank area:** If a pattern is not found, or after replicating the found pattern, do not modify the grid.
"""

import numpy as np

def find_repeating_pattern(grid):
    """Finds a repeating pattern of rows in the grid."""
    height, width = grid.shape
    for pattern_height in range(1, height + 1):
        for start_row in range(0, height - pattern_height + 1):
            pattern = grid[start_row:start_row + pattern_height]
            # Check if this pattern repeats
            next_occurrence = start_row + pattern_height
            if next_occurrence + pattern_height <= height:
                if np.array_equal(grid[next_occurrence:next_occurrence + pattern_height], pattern):
                    return pattern, start_row
    return None, -1

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_grid = np.array(input_grid)
    grid_height, grid_width = input_grid.shape

    # Find the repeating pattern and its starting position
    pattern, start_row = find_repeating_pattern(input_grid)

    # Initialize the output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)

    if pattern is not None:
        # Replicate the pattern
        pattern_height = pattern.shape[0]
        output_grid[:pattern_height] = pattern
        next_occurrence = start_row + pattern_height
        if next_occurrence < grid_height:  # only fill area of pattern
            output_grid[pattern_height:pattern_height+pattern_height] = pattern

    else: # no change
        output_grid = input_grid
    
    # Ensure that blank area is preserved
    if start_row > 0:
        for r in range(0, start_row):
          output_grid[r] = input_grid[r]

    return output_grid.tolist()