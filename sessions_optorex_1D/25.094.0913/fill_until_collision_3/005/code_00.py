import numpy as np
import math # Although math isn't used here, it's available if needed

"""
Transforms an input sequence (represented as a row in a grid) of integers.
The transformation fills sequences of zeros located strictly between non-zero numbers.
The fill value depends on the first element of the sequence:
- If the first element is 5, zeros are replaced by the value of the nearest non-zero number to their right (Backward Fill).
- Otherwise (if the first element is not 5), zeros are replaced by the value of the nearest non-zero number to their left (Forward Fill).
Zeros before the first non-zero number and zeros after the last non-zero number remain unchanged.
"""

def find_non_zero_indices(data_array):
  """
  Helper function: Finds the indices of all non-zero elements in a 1D numpy array.
  Returns a 1D numpy array of indices.
  """
  # np.where returns a tuple of arrays (one for each dimension), 
  # so we take the first element for a 1D array.
  return np.where(data_array != 0)[0]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A numpy array, expected to have one row.

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    # Ensure input is a numpy array and extract the first row
    # Assuming the input is always structured like the examples (e.g., np.array([[5, 0, ...]]))
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid) # Convert if not already numpy array

    # Handle cases where input might be empty or have unexpected dimensions
    if input_grid.size == 0:
        return [[]] # Return grid with an empty row if input is empty
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
         # Or raise an error, or try to handle differently.
         # For now, assume valid input means one row.
         # Let's try taking the first row if ndim==1, otherwise assume error/unexpected
         if input_grid.ndim == 1:
             input_row = input_grid
         else:
              # Returning original or empty might be safer than guessing
              # For this problem, the structure seems fixed, so proceed with first row.
               input_row = input_grid[0]
    else:
         input_row = input_grid[0]


    # Create a copy of the input row to modify. Work with numpy array for efficiency.
    output_row = input_row.copy()

    # Find indices of all non-zero elements in the original input row
    non_zero_indices = find_non_zero_indices(input_row)

    # If there are 0 or 1 non-zero numbers, no filling *between* non-zeros can occur.
    # Leading/trailing zeros are already preserved in the copy.
    if non_zero_indices.size < 2:
        # Return the unmodified row, converted to list format within a list
        return [output_row.tolist()]

    # Determine the fill rule based on the value of the first element of the original row
    # Need to check if input_row is not empty before accessing input_row[0]
    # This is covered by the input_grid.size == 0 check earlier.
    use_backward_fill = (input_row[0] == 5)

    # Iterate through consecutive pairs of non-zero indices
    # e.g., if indices are [2, 5, 8], pairs will be (2, 5) and (5, 8)
    for i in range(non_zero_indices.size - 1):
        idx_left = non_zero_indices[i]      # Index of the left non-zero number in the pair
        idx_right = non_zero_indices[i+1]   # Index of the right non-zero number in the pair

        # Check if there is at least one element (originally zero) between the two non-zero numbers
        if idx_right > idx_left + 1:
            # Determine the value to use for filling based on the rule
            if use_backward_fill:
                # Backward Fill: use the value of the right non-zero neighbor from the original row
                fill_value = input_row[idx_right]
            else:
                # Forward Fill: use the value of the left non-zero neighbor from the original row
                fill_value = input_row[idx_left]

            # Fill the elements in the output_row located strictly between the non-zero neighbors.
            # Use numpy slicing for efficient assignment.
            output_row[idx_left + 1 : idx_right] = fill_value

    # Convert the final numpy row to a list and wrap it in another list
    # to match the expected output format (list of lists, even for a single row)
    output_grid = [output_row.tolist()]

    return output_grid