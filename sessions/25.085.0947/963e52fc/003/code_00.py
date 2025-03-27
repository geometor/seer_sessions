"""
Transforms an input grid into an output grid by extending horizontal patterns within each row.

1. Initialize an output grid with the same height as the input grid and double the width.
2. Iterate through each row of the input grid.
3. If a row consists entirely of the background color (white, 0), fill the corresponding output row with the background color.
4. If a row contains non-background colors, find the shortest repeating horizontal pattern (P) starting from the first pixel that generates the entire input row.
5. Construct the corresponding output row by repeating pattern P until the row length is double the original input width.
6. Return the completed output grid.
"""

import numpy as np

def _find_shortest_repeating_pattern(row):
    """
    Finds the shortest repeating pattern P starting from index 0 in a given row.
    The pattern P must be such that repeating it generates the entire row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        np.array: The shortest repeating pattern found.
                  Returns the entire row if no shorter pattern is found.
    """
    n = len(row)
    # Iterate through possible pattern lengths p from 1 to n
    for p in range(1, n + 1):
        # Assume the pattern of length p works initially
        is_repeating = True
        # Check if the rest of the row matches the pattern P = row[0:p]
        for i in range(p, n):
            if row[i] != row[i % p]:
                # Mismatch found, this pattern length p does not work
                is_repeating = False
                break
        # If the inner loop completed without finding a mismatch,
        # then p is the length of the shortest repeating pattern
        if is_repeating:
            return row[0:p]
    # Should technically not be reached if the logic is sound for ARC tasks,
    # as the entire row itself is always a valid (though not necessarily shortest) pattern.
    # Return the full row as the pattern if no shorter repeat found (p=n case).
    return row


def transform(input_grid):
    """
    Transforms the input grid by extending horizontal patterns in each row to double the width.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get input dimensions
    height, input_width = input_grid.shape
    output_width = input_width * 2

    # Initialize the output grid (e.g., with zeros, matching dtype of input)
    output_grid = np.zeros((height, output_width), dtype=input_grid.dtype)

    # Process each row independently
    for r in range(height):
        input_row = input_grid[r]

        # Check if the row is entirely background (color 0)
        if np.all(input_row == 0):
            # Fill the corresponding output row with background color
            # Note: output_grid is already initialized with zeros, so this line is
            # technically redundant if the background is 0, but good for clarity
            # and if the background color were different.
            output_grid[r, :] = 0
        else:
            # Find the shortest repeating pattern in the non-background row
            pattern = _find_shortest_repeating_pattern(input_row)
            pattern_length = len(pattern)

            # Construct the output row by repeating the pattern
            output_row = np.zeros(output_width, dtype=input_grid.dtype)
            for c in range(output_width):
                output_row[c] = pattern[c % pattern_length]

            # Assign the constructed row to the output grid
            output_grid[r, :] = output_row

    return output_grid