"""
The transformation identifies the unique non-zero digits in the input grid, orders them numerically, and then uses this ordered sequence to fill the output grid, creating a repeating pattern.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Extract Sequence: Find unique non-zero digits and sort them.
    unique_non_zero = np.unique(input_grid[input_grid != 0])
    sequence = sorted(unique_non_zero)

    # Create Output Grid: Initialize an output grid of the same size.
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Populate Output: Fill the output grid with the repeating sequence.
    seq_len = len(sequence)
    if seq_len > 0:  # Handle cases where the input grid might be all zeros
        for i in range(rows):
            for j in range(cols):
                output_grid[i, j] = sequence[(i * cols + j) % seq_len]
    
    return output_grid