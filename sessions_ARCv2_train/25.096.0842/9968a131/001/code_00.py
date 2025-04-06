import collections

"""
Iterate through each row of the input grid based on its index (0-based).
If the row index is even, keep the row unchanged.
If the row index is odd, perform a right circular shift on the elements of the row:
  - Move the last element to the first position.
  - Shift all other elements one position to the right.
Construct the output grid using these processed rows.
"""

def _rotate_row_right(row: list[int]) -> list[int]:
    """
    Performs a right circular shift on the elements of a list.
    Moves the last element to the first position.
    """
    if not row:  # Handle empty row
        return []
    if len(row) == 1: # Handle single element row
        return row[:] # Return a copy
        
    # Take the last element and prepend it to the list of the remaining elements
    return [row[-1]] + row[:-1]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by applying a right circular shift to odd-indexed rows.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    # Initialize the output grid
    output_grid = []

    # Iterate through each row and its index in the input grid
    for i, row in enumerate(input_grid):
        # Check if the row index is even or odd
        if i % 2 == 0:
            # If the index is even, copy the row directly
            # Use row[:] to ensure a copy is appended, not a reference
            output_grid.append(row[:]) 
        else:
            # If the index is odd, perform a right circular shift
            shifted_row = _rotate_row_right(row)
            output_grid.append(shifted_row)

    # Return the fully transformed grid
    return output_grid