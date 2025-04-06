"""
Takes a 3x3 input grid and generates a 6x6 output grid.
The output grid is composed of four 3x3 quadrants:
- Top-left: The original input grid (0 degrees rotation).
- Top-right: The input grid rotated 90 degrees clockwise.
- Bottom-left: The input grid rotated 270 degrees clockwise (90 degrees counter-clockwise).
- Bottom-right: The input grid rotated 180 degrees.
"""

import numpy as np

def rotate_grid(grid: np.ndarray, degrees: int) -> np.ndarray:
    """Rotates a numpy array grid clockwise by the specified degrees (must be multiple of 90)."""
    if degrees == 0:
        return grid
    elif degrees == 90:
        k = -1 # numpy rot90 rotates counter-clockwise by default, k=-1 is one 90 deg clockwise rotation
    elif degrees == 180:
        k = -2
    elif degrees == 270:
        k = -3
    else:
        raise ValueError("Rotation degrees must be 0, 90, 180, or 270")
    return np.rot90(grid, k=k)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 3x3 input grid into a 6x6 output grid by placing
    rotated versions of the input into four quadrants.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    n = input_array.shape[0] # Size of the input grid (assumed square)
    output_size = 2 * n

    # Initialize output_grid as a NumPy array filled with zeros (or any placeholder)
    output_array = np.zeros((output_size, output_size), dtype=int)

    # --- Perform transformations and place into quadrants ---

    # Top-left quadrant: 0 degrees rotation (original input)
    rot0 = rotate_grid(input_array, 0)
    output_array[0:n, 0:n] = rot0

    # Top-right quadrant: 90 degrees clockwise rotation
    rot90 = rotate_grid(input_array, 90)
    output_array[0:n, n:output_size] = rot90

    # Bottom-left quadrant: 270 degrees clockwise rotation (or 90 counter-clockwise)
    rot270 = rotate_grid(input_array, 270)
    output_array[n:output_size, 0:n] = rot270

    # Bottom-right quadrant: 180 degrees rotation
    rot180 = rotate_grid(input_array, 180)
    output_array[n:output_size, n:output_size] = rot180

    # Convert the final NumPy array back to a list of lists for the return value
    output_grid = output_array.tolist()

    return output_grid
