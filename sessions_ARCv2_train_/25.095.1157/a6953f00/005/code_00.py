"""
Extracts a 2x2 subgrid from the input grid and returns it as a formatted string.
The extraction always uses the first two rows (index 0 and 1).
The starting column depends on the width (number of columns) of the input grid:
- If the width is even, the subgrid is taken from the last two columns (columns N-2 and N-1).
- If the width is odd, the subgrid is taken from the first two columns (columns 0 and 1).
The output is a string with two lines, each containing two space-separated integers,
separated by a newline character.
"""

import numpy as np
from typing import List, Union

def transform(input_grid: Union[List[List[int]], np.ndarray]) -> str:
    """
    Transforms the input grid according to the specified rules.

    Args:
        input_grid: A list of lists or NumPy array representing the 2D integer grid.

    Returns:
        A string representing the 2x2 extracted subgrid, formatted with spaces and newlines.
        Returns an empty string if extraction is not possible (e.g., < 2 rows/cols).
    """
    # Convert input to a NumPy array for easier processing and slicing
    # This handles both list of lists and NumPy array inputs seamlessly.
    grid = np.array(input_grid)

    # Check if the grid has the minimum required dimensions (at least 2 rows and 2 columns)
    # If not, return an empty string as per potential implicit requirements or error handling.
    if grid.shape[0] < 2 or grid.shape[1] < 2:
        # Handle edge case: Cannot extract a 2x2 grid
        return "" # Or raise ValueError("Input grid must be at least 2x2.")

    # Determine the number of columns (width) of the input grid
    num_cols = grid.shape[1]

    # Calculate the starting column index based on the parity (even/odd) of the width
    if num_cols % 2 == 0:
        # If the width is even, the starting column is the second to last column (index N-2)
        start_col = num_cols - 2
    else:
        # If the width is odd, the starting column is the first column (index 0)
        start_col = 0

    # Extract the four relevant integer values from the first two rows (0 and 1)
    # and the calculated starting columns (start_col and start_col + 1).
    val_00 = grid[0, start_col]      # Top-left of the 2x2 subgrid
    val_01 = grid[0, start_col + 1]  # Top-right of the 2x2 subgrid
    val_10 = grid[1, start_col]      # Bottom-left of the 2x2 subgrid
    val_11 = grid[1, start_col + 1]  # Bottom-right of the 2x2 subgrid

    # Format the extracted values into the specified output string format:
    # Two lines, each with two space-separated numbers, separated by a newline.
    output_string = f"{val_00} {val_01}\n{val_10} {val_11}"

    # Return the final formatted string
    return output_string