import copy

"""
Iterate through each row of the input grid based on its 0-based index. 
If the row index is odd, perform a right circular shift on the elements of that row by one position. 
The last element becomes the first, and all other elements shift one position to the right. 
If the row index is even, the row remains unchanged. 
Construct the output grid from these processed rows.
"""

def _rotate_row_right(row: list[int]) -> list[int]:
    """
    Performs a right circular shift on the elements of a list by one position.
    
    Args:
        row: The list of integers representing a row.
        
    Returns:
        A new list with elements shifted one position to the right.
    """
    if not row:  # Handle empty rows
        return []
    # Take the last element and prepend it to the list of elements excluding the last one.
    return [row[-1]] + row[:-1]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by applying a right circular shift 
    to rows with odd indices.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of lists of integers representing the transformed output grid.
    """
    # Initialize an empty list to store the rows of the output grid
    output_grid = []

    # Iterate through each row along with its index (0-based)
    for i, row in enumerate(input_grid):
        # Check if the current row index is odd
        if i % 2 != 0:
            # If the index is odd, apply the right circular shift
            modified_row = _rotate_row_right(row)
            output_grid.append(modified_row)
        else:
            # If the index is even, keep the row as is
            # Appending a copy ensures the original input_grid isn't modified 
            # if the row object were mutable in a more complex scenario, 
            # though here list slicing in _rotate_row_right already creates copies.
            # Using the original row directly is also fine here.
            output_grid.append(row[:]) # Appending a shallow copy

    # Return the constructed output grid
    return output_grid
