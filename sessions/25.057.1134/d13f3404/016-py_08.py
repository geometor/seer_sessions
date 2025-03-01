"""
The input grid is considered as the core. Examine the core to find repeated sequences by starting with the longest possible sequence and working backward to single pixels. When the input contains a repeated segments at each end, the segment is appended to the input to create the output. If there are no repeating segments, rotate 90 degrees and arrange as a 2x2 grid.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1)

def find_repeating_segment(grid):
    """Finds repeating segments at the beginning and end of the grid's first row."""
    grid = np.array(grid)
    first_row = grid[0, :]
    n = len(first_row)
    
    for length in range(n // 2, 0, -1):  # Iterate through possible segment lengths
        for start in range(n - 2 * length + 1):
            segment = first_row[start : start + length]
            if np.array_equal(first_row[:length], segment) and np.array_equal(first_row[n-length:], segment):
                return segment.tolist() # Return as list
    return None

def transform(input_grid):
    """Transforms the input grid based on repeating segments or rotation."""
    
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Check for repeating segments
    segment = find_repeating_segment(input_grid)

    if segment:
        # If segments are found, append to output
        # Extend only the first row of the input, as the transformation only changes the width
        new_row = np.concatenate([input_grid[0,:], segment]).tolist()
        
        # create the grid by coping new_row for each row in input
        output_grid = [new_row[:] for _ in range(input_grid.shape[0])]
        
    else:
       # No repeating segments, perform 2x2 rotation (as in original logic)
        core = np.array(input_grid)
        output_grid = np.zeros((core.shape[0] * 2, core.shape[1] * 2), dtype=int)
        output_grid[:core.shape[0], :core.shape[1]] = core
        rotated_core = rotate_grid(core)
        output_grid[:core.shape[0], core.shape[1]:] = rotated_core
        rotated_core = rotate_grid(rotated_core)
        output_grid[core.shape[0]:, :core.shape[1]] = rotated_core
        rotated_core = rotate_grid(rotated_core)
        output_grid[core.shape[0]:, core.shape[1]:] = rotated_core
        output_grid = output_grid.tolist()

    return output_grid