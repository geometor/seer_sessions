"""
Generates an output grid based on coordinate parity (odd row or odd column -> azure)
and masks it using the azure pixels from the input grid.
Specifically:
1. If the input pixel at (r, c) is azure (8), the output pixel at (r, c) is white (0).
2. If the input pixel at (r, c) is white (0), the output pixel at (r, c) is:
   - azure (8) if the row index r is odd OR the column index c is odd.
   - white (0) if both the row index r is even AND the column index c is even.
"""

import numpy as np

def transform(input_grid_list):
    """
    Transforms the input grid based on coordinate parity and input masking.

    Args:
        input_grid_list (list[list[int]]): A 2D list of integers representing the input grid.

    Returns:
        list[list[int]]: A 2D list of integers representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, default to white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each cell of the grid using its row and column index
    for r in range(height):
        for c in range(width):
            # Get the value of the corresponding input cell
            input_value = input_grid[r, c]

            # Apply the masking rule: if input is azure (8), output is white (0)
            if input_value == 8:
                output_grid[r, c] = 0
            # Apply the coordinate pattern rule: if input is white (0)
            else:
                # Check if row index r is odd OR column index c is odd
                if r % 2 != 0 or c % 2 != 0:
                    # If either index is odd, set output to azure (8)
                    output_grid[r, c] = 8
                else:
                    # If both indices are even, set output to white (0)
                    # Note: This case is covered by the initialization, but explicitly setting it adds clarity.
                    output_grid[r, c] = 0 

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()