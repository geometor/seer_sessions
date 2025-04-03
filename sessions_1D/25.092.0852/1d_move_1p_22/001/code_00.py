"""
Transforms a single-row input grid by shifting all elements one position to the right, 
inserting a white pixel (0) at the beginning (index 0), and discarding the 
original last element. The dimensions of the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Shifts the elements of a single-row grid one step to the right, 
    inserting 0 at the start.

    Args:
        input_grid (list of lists): A grid represented as a list containing one list (the row).

    Returns:
        list of lists: The transformed grid with elements shifted right and 0 prepended.
    """
    # Convert the input grid (list of lists) to a numpy array
    input_array = np.array(input_grid, dtype=int)

    # Extract the single row from the input array
    # Since the input is guaranteed by the examples to be 1xN
    input_row = input_array[0]

    # Get the width of the row
    width = len(input_row)

    # Create the output row, initialized with the same size (or can be constructed directly)
    # Step 1: Take all elements from the input row *except* the last one.
    # input_row[:-1] selects elements from index 0 up to (but not including) the last index.
    elements_to_keep = input_row[:-1]

    # Step 2: Prepend a white pixel (0) to these elements.
    # np.insert inserts a value into an array at a specified index.
    # Here, we insert 0 at index 0 of the 'elements_to_keep' array.
    output_row = np.insert(elements_to_keep, 0, 0)

    # Reshape the resulting 1D numpy array back into a 2D array (1 row, width columns)
    # The -1 tells numpy to automatically calculate the number of columns.
    output_grid_np = output_row.reshape(1, width)

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid
