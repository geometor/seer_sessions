import numpy as np

"""
Transforms a 1x12 grid based on the position of the first non-zero block in the row.

The input is assumed to be a 2D NumPy array with dimensions 1x12.
The single row contains primarily zeros and a single contiguous horizontal block 
of identical non-zero digits.

Transformation Rule:
1. Find the column index of the first non-zero digit in the first (only) row (`first_nz_col_index`).
2. If `first_nz_col_index` is 0 (the block starts at the first column) or -1 (no non-zero digits found), 
   the grid remains unchanged.
3. If `first_nz_col_index` is greater than 0:
   a. Convert the row to a list.
   b. Remove the zero digit immediately preceding the block (at index `first_nz_col_index - 1`).
   c. Append this removed zero to the end of the list.
   d. Convert the modified list back into a 1x12 NumPy array (within a 2D array structure).
4. Return the potentially modified grid.
"""

def find_first_nonzero_col_index(row):
  """
  Finds the column index of the first non-zero element in a 1D sequence (row).

  Args:
      row: A 1D iterable (list, NumPy array) of numbers.

  Returns:
      The index of the first non-zero element, or -1 if none is found.
  """
  for i, digit in enumerate(row):
    if digit != 0:
      return i
  return -1 # Indicate no non-zero element found

def transform(input_grid):
    """
    Applies the described transformation to the input 1x12 grid.

    Args:
        input_grid: A 1x12 NumPy array.

    Returns:
        A 1x12 NumPy array representing the transformed grid.
    """
    
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if the input grid has the expected shape (optional but good practice)
    if input_grid.shape != (1, 12):
        # Handle error or unexpected shape if necessary
        # For this problem, we assume the shape is always 1x12
        pass 

    # Extract the first (and only) row as a 1D NumPy array
    row = input_grid[0]

    # Find the starting column index of the non-zero block
    first_nz_col_index = find_first_nonzero_col_index(row)

    # Check the condition for transformation: block exists and doesn't start at index 0
    if first_nz_col_index > 0:
        # Convert the 1D NumPy row array to a Python list for easier manipulation
        row_list = row.tolist()
        
        # Identify and remove the zero element immediately preceding the non-zero block
        zero_to_move = row_list.pop(first_nz_col_index - 1)
        
        # Append the removed zero to the end of the list
        row_list.append(zero_to_move)
        
        # Convert the modified list back into a 1x12 NumPy array, 
        # ensuring it's wrapped in another list to create the 2D (1x12) structure
        output_grid = np.array([row_list])
    
    else:
        # If first_nz_col_index is 0 or -1, the grid remains unchanged.
        # Return a copy to avoid modifying the original input object unintentionally.
        output_grid = np.copy(input_grid)

    return output_grid