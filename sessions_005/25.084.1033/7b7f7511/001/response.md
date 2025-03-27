```python
"""
Identifies if an input grid is composed of two identical halves, either horizontally or vertically.
If horizontal duplication (left half equals right half) exists, the output is the left half.
If vertical duplication (top half equals bottom half) exists, the output is the top half.
It is assumed that only one type of duplication exists for valid inputs.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting either the left or top half,
    depending on whether the grid is duplicated horizontally or vertically.

    Args:
        input_grid (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: The extracted half of the grid (left or top).
    """
    # Convert input list of lists to a NumPy array for easier slicing and comparison
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape # Get height and width

    # Initialize output_grid (although we'll directly return the slice)
    output_grid = None

    # 1. Check for horizontal duplication
    # Check if the width is even
    if W % 2 == 0:
        # Calculate the midpoint width
        mid_w = W // 2
        # Extract the left half (columns 0 to mid_w - 1)
        left_half = grid[:, :mid_w]
        # Extract the right half (columns mid_w to W - 1)
        right_half = grid[:, mid_w:]

        # Compare the left and right halves
        if np.array_equal(left_half, right_half):
            # If identical, the output is the left half
            output_grid = left_half
            # Convert back to list of lists before returning
            return output_grid.tolist()

    # 2. Check for vertical duplication (only if horizontal wasn't found or wasn't applicable)
    # Check if the height is even
    if H % 2 == 0:
        # Calculate the midpoint height
        mid_h = H // 2
        # Extract the top half (rows 0 to mid_h - 1)
        top_half = grid[:mid_h, :]
        # Extract the bottom half (rows mid_h to H - 1)
        bottom_half = grid[mid_h:, :]

        # Compare the top and bottom halves
        if np.array_equal(top_half, bottom_half):
            # If identical, the output is the top half
            output_grid = top_half
            # Convert back to list of lists before returning
            return output_grid.tolist()

    # According to the task description and examples, one of the above conditions
    # should always be met. If not, returning the original grid might be a fallback,
    # but based on the analysis, it's expected to find a duplication.
    # If output_grid is still None here, it indicates an unexpected input pattern.
    # For this task, we assume a valid duplication is always present.
    # However, adding a safeguard might be prudent in a general case.
    # If no duplication is found (which shouldn't happen based on examples):
    if output_grid is None:
         # This case should not occur based on the provided examples and description.
         # Depending on requirements, could raise an error or return input.
         # Let's return the input grid as a fallback, though unlikely needed.
         print("Warning: No horizontal or vertical duplication found. Returning original grid.")
         return input_grid # Or raise ValueError("No duplication found")

    # Should have returned within the if blocks
    return output_grid.tolist() # Should ideally not be reached if logic inside loops is correct

```