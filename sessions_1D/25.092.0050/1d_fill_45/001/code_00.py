import numpy as np
from typing import List, Tuple

"""
Identifies the two non-white pixels in a single-row input grid, determines their color, and fills the segment between (and including) these two pixels with that color in the output grid, maintaining the original grid dimensions. Pixels outside this segment remain white.
"""

def find_non_white_pixels(row: List[int]) -> Tuple[int, int, int]:
    """
    Finds the color and indices of the first and last non-white pixels in a row.

    Args:
        row: A list of integers representing a single row of the grid.

    Returns:
        A tuple containing:
        - color: The color of the non-white pixels.
        - min_col: The index of the leftmost non-white pixel.
        - max_col: The index of the rightmost non-white pixel.
        Returns (-1, -1, -1) if fewer than two non-white pixels are found.
    """
    non_white_indices = [i for i, pixel in enumerate(row) if pixel != 0]
    if len(non_white_indices) < 2:
        # Handle cases not represented in examples, though instructions imply exactly two
        print("Warning: Less than two non-white pixels found.") 
        # Based on examples, we expect exactly two. If not, the logic might fail.
        # For robustness, we could return default values or raise an error.
        # Given the examples, we proceed assuming exactly two exist.
        return -1, -1, -1 # Indicate failure or unexpected input

    min_col = min(non_white_indices)
    max_col = max(non_white_indices)
    color = row[min_col] # Color is assumed to be the same for both points

    # Optional check: Verify both points have the same color
    if row[max_col] != color:
        print(f"Warning: Non-white pixels have different colors ({row[min_col]} and {row[max_col]}). Using color {color}.")
        # Decide how to handle this inconsistency if it occurs. Sticking with the first color found.

    return color, min_col, max_col


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid according to the described rule:
    Fills the segment between the two non-white pixels in the single row
    with their color.

    Args:
        input_grid: A list of lists representing the input grid (expected 1xN).

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Ensure input is treated as a numpy array for easier indexing
    input_array = np.array(input_grid, dtype=int)

    # Assuming the grid is always 1xN based on examples
    if input_array.shape[0] != 1:
         raise ValueError("Input grid must have exactly one row.")

    input_row = input_array[0]

    # 1. Identify all non-white pixels in the input row.
    # 2. Determine the color of these non-white pixels.
    # 3. Find the column index of the leftmost non-white pixel (`min_col`).
    # 4. Find the column index of the rightmost non-white pixel (`max_col`).
    color, min_col, max_col = find_non_white_pixels(input_row.tolist())

    if color == -1: # Handle case where finding pixels failed
         print("Error processing input: Could not find two non-white pixels.")
         return input_grid # Return original grid or handle error appropriately

    # 5. Create an output row of the same length as the input row, initialized with white (0) pixels.
    # Alternatively, start with a copy of the input and modify it. Let's create a new one.
    output_row = np.zeros_like(input_row) # Initialize with background color (0)

    # 6. Fill the pixels in the output row from column index `min_col` to `max_col` (inclusive)
    #    with the color identified in step 2.
    output_row[min_col : max_col + 1] = color

    # Convert back to list of lists format for the ARC standard
    output_grid = [output_row.tolist()]

    return output_grid