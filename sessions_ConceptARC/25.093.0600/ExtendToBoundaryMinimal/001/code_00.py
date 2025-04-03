"""
Transforms an input grid based on the position of a single non-zero element.

1. Identify the row index `R`, column index `C`, and value `V` of the single non-zero cell in the input grid.
2. Create a new output grid with the same dimensions as the input grid, initially filled with zeros.
3. If the column index `C` of the non-zero cell is 0, fill the entire row `R` of the output grid with the value `V`.
4. Otherwise (if the column index `C` is not 0), fill the entire column `C` of the output grid with the value `V`.
5. Return the modified output grid.
"""

import numpy as np

def find_non_zero(grid):
  """Finds the first non-zero element's value and coordinates."""
  for r_idx, row in enumerate(grid):
    for c_idx, val in enumerate(row):
      if val != 0:
        return r_idx, c_idx, val
  return None, None, None # Should not happen based on task description


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output_grid with zeros, same shape as input
    output_grid = np.zeros_like(input_np)

    # Find the non-zero element's row, column, and value
    r, c, v = find_non_zero(input_np)

    # Check if a non-zero element was found (as expected)
    if v is not None:
        # If the non-zero element is in the first column (index 0)
        if c == 0:
            # Fill the corresponding row in the output grid with the value
            output_grid[r, :] = v
        # Otherwise (if the non-zero element is not in the first column)
        else:
            # Fill the corresponding column in the output grid with the value
            output_grid[:, c] = v

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
