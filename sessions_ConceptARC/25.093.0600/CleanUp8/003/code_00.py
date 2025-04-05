"""
Processes a 2D integer grid by iterating through pairs of consecutive rows (0&1, 2&3, etc.).
For each pair:
1. Counts the non-zero elements in both rows.
2. Selects a 'candidate' row: the one with fewer non-zero elements. If counts are equal, the first row (even index) is the candidate. The other row becomes the 'comparison' row.
3. Creates an 'output pattern' row. For each column index:
    - If the element in the candidate row AND the element in the comparison row are both non-zero, the output pattern row gets the value from the candidate row at that index.
    - Otherwise, the output pattern row gets 0 at that index.
4. Both rows in the output grid corresponding to the input pair are replaced with copies of this generated 'output pattern' row.
"""

import numpy as np

def count_non_zeros(row):
  """Counts the number of non-zero elements in a list or 1D numpy array."""
  # Using numpy count_nonzero is efficient
  return np.count_nonzero(np.array(row))

def transform(input_grid):
    """
    Applies the row-pair sparsity comparison and intersection filtering
    transformation to the input grid.

    Args:
        input_grid: A list of lists representing the 2D integer grid.

    Returns:
        A list of lists representing the transformed 2D integer grid.
    """
    # Convert input to numpy array for easier slicing and operations
    input_np = np.array(input_grid)
    num_rows, num_cols = input_np.shape

    # Initialize output grid with zeros, matching input dimensions and type
    output_np = np.zeros_like(input_np)

    # Iterate through the grid rows in steps of 2
    for i in range(0, num_rows, 2):
        # Ensure we have a pair of rows
        if i + 1 < num_rows:
            row_A = input_np[i]
            row_B = input_np[i + 1]

            # Count non-zero elements in each row of the pair
            count_A = count_non_zeros(row_A)
            count_B = count_non_zeros(row_B)

            # Determine candidate and comparison rows based on counts
            # Tie goes to the first row (row_A).
            if count_A <= count_B:
                candidate_row = row_A
                comparison_row = row_B
            else: # count_B < count_A
                candidate_row = row_B
                comparison_row = row_A

            # Generate the output pattern row based on intersection
            output_pattern_row = np.zeros(num_cols, dtype=input_np.dtype)
            for j in range(num_cols):
                # Keep value from candidate only if both candidate and comparison are non-zero
                if candidate_row[j] != 0 and comparison_row[j] != 0:
                    output_pattern_row[j] = candidate_row[j]
                # Otherwise, it remains 0 (due to initialization)

            # Assign the generated pattern row to both corresponding output rows
            output_np[i] = output_pattern_row
            output_np[i + 1] = output_pattern_row
        # Handle potential odd number of rows if the problem spec allowed it
        # elif i < num_rows:
        #    # If there's a single last row, maybe copy it? Or zero it out?
        #    # Based on examples, seems grids are always even height or last row ignored.
        #    # Let's assume for now we only process full pairs.
        #    pass

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()

    return output_grid