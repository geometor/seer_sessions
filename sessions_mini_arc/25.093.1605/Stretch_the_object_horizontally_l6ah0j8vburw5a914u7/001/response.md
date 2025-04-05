```python
import numpy as np

"""
Processes a 2D grid of integers (0s and 3s) row by row.
For each row:
1. If the row contains only 0s, it remains unchanged.
2. If the row contains one or more 3s:
   a. Find the index of the first (leftmost) '3' (first_idx).
   b. Find the index of the last (rightmost) '3' (last_idx).
   c. Determine the effective start index for the output: start_idx = max(0, first_idx - 1).
   d. Determine the effective end index for the output: end_idx = min(grid_width - 1, last_idx + 1).
   e. Initialize the output row with all 0s.
   f. Check if the segment of the input row from first_idx to last_idx (inclusive) consists entirely of 3s (contiguous).
      i. If first_idx == last_idx (only a single '3' in the input row): Set the output element at start_idx to 3.
      ii. If contiguous and first_idx != last_idx: Fill the output row with 3s from start_idx to end_idx (inclusive).
      iii. If not contiguous: Set the output element at start_idx to 3 and the output element at end_idx to 3.
"""

def find_indices(row, value):
    """Finds all indices of a specific value in a list or 1D numpy array."""
    return [i for i, x in enumerate(row) if x == value]

def is_contiguous(row, start, end, value):
    """Checks if all elements between start and end indices (inclusive) equal the given value."""
    if start > end: # Handles the case of a single element
        return True
    return all(x == value for x in row[start:end+1])

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    n_rows, n_cols = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize output grid with zeros

    # Process each row
    for r in range(n_rows):
        input_row = input_np[r]
        indices_of_3 = find_indices(input_row, 3)

        # If no 3s are found, the row remains all 0s (already initialized)
        if not indices_of_3:
            continue # Skip to the next row

        # Find first and last index of 3
        first_idx = indices_of_3[0]
        last_idx = indices_of_3[-1]

        # Calculate effective start and end indices for the output modification
        start_fill_idx = max(0, first_idx - 1)
        end_fill_idx = min(n_cols - 1, last_idx + 1)

        # Check for single '3' case
        if first_idx == last_idx:
             output_grid[r, start_fill_idx] = 3
        # Check for contiguity between first and last '3' in the input row
        elif is_contiguous(input_row, first_idx, last_idx, 3):
            # Fill the output row from start_fill_idx to end_fill_idx
            output_grid[r, start_fill_idx : end_fill_idx + 1] = 3
        else: # Not contiguous
            # Set the start and end fill indices in the output row
            output_grid[r, start_fill_idx] = 3
            output_grid[r, end_fill_idx] = 3

    # Convert back to list of lists if necessary, or return numpy array
    return output_grid.tolist()
```