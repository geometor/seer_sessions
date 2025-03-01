"""
The transformation rule identifies the longest contiguous sequence of non-black (non-zero) pixels in any row of the input grid and creates a 1-row output grid containing that sequence. If multiple rows have sequences of the same maximum length, the transformation uses one of them. If the input contains only black (value 0) pixels, the output is a 1x1 grid containing only black.
"""

import numpy as np

def _find_longest_contiguous_sequence(grid):
    """Finds the longest contiguous sequence of non-zero pixels in a grid."""
    max_length = 0
    current_sequence = []
    longest_sequence = []

    for row in grid:
        for pixel in row:
            if pixel != 0:
                current_sequence.append(pixel)
            else:
                if len(current_sequence) > max_length:
                    max_length = len(current_sequence)
                    longest_sequence = current_sequence
                current_sequence = []
        # Check for sequence at the end of the row
        if len(current_sequence) > max_length:
            max_length = len(current_sequence)
            longest_sequence = current_sequence
        current_sequence = []  # reset for next row

    return longest_sequence

def transform(input_grid):
    """Transforms the input grid based on longest contiguous sequence."""
    
    longest_sequence = _find_longest_contiguous_sequence(input_grid)

    if len(longest_sequence) > 0:
        output_grid = np.array([longest_sequence])  # output is the list as a single row
    else:
        output_grid = np.array([[0]])

    return output_grid