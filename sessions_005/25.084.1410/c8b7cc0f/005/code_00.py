import numpy as np

"""
Transforms an input grid into a 3x3 output grid based on the count of a specific 'signal' color.
1. Identifies the 'signal color' in the input grid, which is the non-white (0) and non-blue (1) color.
2. Counts the total number of occurrences (N) of this signal color.
3. Calculates a value M based on the remainder of N divided by 3 (R = N % 3):
    - If R is 0, M = 1.
    - If R is 1, M = 0.
    - If R is 2, M = 2.
4. Constructs a 3x3 output grid where:
    - The first row is entirely filled with the signal color.
    - The third row is entirely filled with white (0).
    - The second row contains M signal-colored pixels starting from the left, and the rest are white (0).
"""

def _find_signal_color(grid):
    """Finds the color in the grid that is not white (0) or blue (1)."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0 and color != 1:
            return color
    # Handle cases where no such color is found (e.g., only white or white+blue)
    # Based on examples, assume a signal color always exists. If not, return 0 as default.
    print("Warning: No signal color (non-0, non-1) found. Defaulting to 0.")
    return 0

def transform(input_grid):
    """
    Transforms the input grid based on the identified signal color and its count,
    using a specific modulo-based rule for the second row.

    Args:
        input_grid (list or np.ndarray): A 2D grid represented as a list of lists or numpy array.

    Returns:
        np.ndarray: A 3x3 numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)

    # 1. Identify the Signal Color
    signal_color = _find_signal_color(grid)

    # Handle edge case: if no signal color was found, return an all-white grid
    if signal_color == 0:
        return np.zeros((3, 3), dtype=int)

    # 2. Count Signal Pixels
    signal_count_N = np.count_nonzero(grid == signal_color)

    # 3. Determine Second Row Pattern (M)
    remainder_R = signal_count_N % 3
    second_row_pixels_M = 0  # Default value if R=1
    if remainder_R == 0:
        second_row_pixels_M = 1
    elif remainder_R == 2:
        second_row_pixels_M = 2
    # If remainder_R is 1, second_row_pixels_M remains 0

    # 4. Construct the Output Grid
    # Initialize 3x3 grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the first row with the signal color
    output_grid[0, :] = signal_color

    # Fill the second row based on M
    # Note: Slicing with 0 (e.g., output_grid[1, 0:0]) correctly does nothing
    output_grid[1, 0:second_row_pixels_M] = signal_color

    # The third row remains white (0) as initialized

    return output_grid