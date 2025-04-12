import collections

"""
Iterate through each row of the input grid. If the row index is even, 
copy the row unchanged to the output. If the row index is odd, perform 
a right circular shift on the elements of the row (last element becomes 
the first, others shift right) and place the shifted row in the output.
"""

def right_circular_shift(row: list[int]) -> list[int]:
    """
    Performs a right circular shift on the elements of a list.
    The last element moves to the first position.
    """
    if not row:
        return []
    # Use deque for efficient rotation
    deque_row = collections.deque(row)
    deque_row.rotate(1) # Rotate right by 1 position
    return list(deque_row)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on row index parity.
    Even rows are copied, odd rows are right-circularly shifted.
    """
    # Initialize output_grid as an empty list
    output_grid = []

    # Iterate through each row with its index
    for i, row in enumerate(input_grid):
        # Check if the current row index is odd
        if i % 2 != 0:
            # If odd, perform a right circular shift on the row
            shifted_row = right_circular_shift(row)
            # Append the shifted row to the output grid
            output_grid.append(shifted_row)
        else:
            # If even, copy the row directly to the output grid
            # Create a copy to avoid modifying the input if it were mutable elsewhere
            output_grid.append(list(row)) 

    # Return the completed output grid
    return output_grid