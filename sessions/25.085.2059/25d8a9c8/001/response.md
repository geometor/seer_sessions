```python
"""
Transform an input grid to an output grid of the same dimensions.
For each row in the input grid:
- If all pixels in the row have the same color, the corresponding output row is filled entirely with Gray (5).
- If the pixels in the row have different colors, the corresponding output row is filled entirely with White (0).
"""

import numpy as np

def check_row_uniformity(row):
  """
  Checks if all elements in a list (row) are the same.

  Args:
    row: A list of pixel values representing a grid row.

  Returns:
    True if all elements are the same, False otherwise.
  """
  if not row: # Handle empty row case, though not expected in ARC
    return True
  first_element = row[0]
  for element in row:
    if element != first_element:
      return False
  return True

# Alternative using sets, potentially more concise but maybe less explicit for simple cases
# def check_row_uniformity_set(row):
#   """Checks if all elements in a list (row) are the same using sets."""
#   return len(set(row)) <= 1 # <= 1 handles empty rows gracefully

def transform(input_grid):
    """
    Transforms the input grid based on row uniformity.

    Args:
      input_grid: A list of lists representing the input grid.

    Returns:
      A numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize output grid with the same dimensions, default to White (0)
    output_grid = np.zeros((num_rows, num_cols), dtype=int)

    # Iterate through each row of the input grid
    for r in range(num_rows):
        current_row = input_array[r, :]

        # Check if all pixels in the current row have the same color
        is_uniform = check_row_uniformity(current_row.tolist()) # Use helper function

        # If the row is uniform (all same color)
        if is_uniform:
            # Fill the corresponding row in the output grid with Gray (5)
            output_grid[r, :] = 5
        # Else (row has different colors)
        else:
            # Fill the corresponding row in the output grid with White (0)
            # (Already initialized to 0, so no explicit action needed unless initialization changes)
            output_grid[r, :] = 0 # Explicitly set to 0 for clarity

    return output_grid.tolist() # Return as list of lists per ARC standard
```