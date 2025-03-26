"""
Identify a repeating pattern within the input grid and extract a single instance.
If the pattern repeats horizontally (left half equals right half), return the left half.
If the pattern repeats vertically (top half equals bottom half), return the top half.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by identifying a horizontally or vertically repeated
    pattern and returning a single instance of that pattern.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid (one instance
                         of the repeated pattern).
    """
    # Convert the input list of lists to a numpy array for easier slicing and comparison
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape

    # Check for horizontal repetition
    # Condition: Width must be even and greater than 0
    if W > 0 and W % 2 == 0:
        # Calculate the midpoint width
        mid_w = W // 2
        # Slice the grid into left and right halves
        left_half = grid[:, :mid_w]
        right_half = grid[:, mid_w:]
        # Compare the two halves
        if np.array_equal(left_half, right_half):
            # If they are identical, return the left half as a list of lists
            return left_half.tolist()

    # Check for vertical repetition (only if horizontal repetition wasn't found or applicable)
    # Condition: Height must be even and greater than 0
    if H > 0 and H % 2 == 0:
        # Calculate the midpoint height
        mid_h = H // 2
        # Slice the grid into top and bottom halves
        top_half = grid[:mid_h, :]
        bottom_half = grid[mid_h:, :]
        # Compare the two halves
        if np.array_equal(top_half, bottom_half):
            # If they are identical, return the top half as a list of lists
            return top_half.tolist()

    # As per the analysis, one of the conditions should always be met.
    # If neither repetition is found (which shouldn't happen based on the examples),
    # we might return the original grid or raise an error. Let's return original for now.
    # Consider adding error handling if the problem statement guarantees repetition.
    print("Warning: No horizontal or vertical repetition found. Returning original grid.")
    return input_grid
