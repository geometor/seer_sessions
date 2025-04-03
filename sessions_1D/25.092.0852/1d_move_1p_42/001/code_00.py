import numpy as np

"""
Performs a circular shift of all pixels in the input grid row one position to the right.
The pixel value from the last position moves to the first position, and all other
pixel values shift one position to the right.
"""

def transform(input_grid):
    """
    Applies a one-position right circular shift to the input grid row.

    Args:
        input_grid (list): A list containing a single list representing the input row. 
                           Example: [[2, 2, 2, ..., 0, 0, 0]]

    Returns:
        list: A list containing a single list representing the shifted output row.
              Example: [[0, 2, 2, 2, ..., 2, 0, 0]]
    """
    # The input is expected as a list containing one row (list)
    # Extract the actual row data
    input_row = input_grid[0]

    # Get the number of columns (length of the row)
    num_cols = len(input_row)

    # Handle edge case: empty or single-element row (no shift needed)
    if num_cols <= 1:
        return [list(input_row)] # Return a copy wrapped in a list

    # Perform the circular right shift
    # Take the last element
    last_element = input_row[-1]
    
    # Take all elements except the last one
    remaining_elements = input_row[:-1]
    
    # Create the new row by placing the last element at the beginning
    output_row = [last_element] + remaining_elements

    # Wrap the output row in a list to match the expected output format
    output_grid = [output_row]
    
    return output_grid
