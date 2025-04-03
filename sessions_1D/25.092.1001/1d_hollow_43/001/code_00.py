import copy

"""
Identifies a single contiguous horizontal block of non-white pixels
in the input grid (assumed to be 1D). It keeps the first and last
pixels of this block and changes all pixels in between to white (0).
Surrounding white pixels are unchanged.
"""

def find_block_indices(row):
    """
    Finds the start and end indices of the first contiguous non-zero block in a list.

    Args:
        row: A list representing a row of the grid.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    # Iterate through the row to find the first non-white pixel
    for i, pixel in enumerate(row):
        if pixel != 0:
            if start_index == -1:
                start_index = i
            # Keep updating the end index as long as we find non-white pixels
            end_index = i
            
    # Check if the block continues immediately after the first found non-white pixel
    # This refined logic ensures we only capture the *first* contiguous block
    # if there were multiple separate blocks (though the problem description implies only one).
    if start_index != -1:
        current_end = start_index
        for i in range(start_index + 1, len(row)):
            if row[i] != 0:
                current_end = i
            else:
                # Stop searching once a white pixel is encountered after the block started
                break
        end_index = current_end

    return start_index, end_index


def transform(input_grid):
    """
    Applies the transformation rule: identify the non-white block, keep its
    endpoints, and set the interior pixels to white (0).

    Args:
        input_grid: A list of lists representing the 1D input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Ensure input is valid (basic check)
    if not input_grid or not input_grid[0]:
        # Return empty or handle error based on expected behavior for invalid input
        return [] 

    # Create a deep copy of the input grid to modify
    # Using list comprehension for a deep copy of a list of lists of primitives
    output_grid = [list(row) for row in input_grid]

    # As the task description implies 1D grids, we operate on the first row
    row_index = 0
    input_row = input_grid[row_index]
    output_row = output_grid[row_index] # Get a reference to the row in the output grid

    # Find the start and end column indices of the contiguous non-white block
    start_col, end_col = find_block_indices(input_row)

    # Check if a valid block was found and if it has interior points
    # A block needs at least 3 pixels to have an interior (start, middle, end)
    # So, end_col must be at least start_col + 2
    if start_col != -1 and end_col >= start_col + 2:
        # Iterate through the column indices *between* the start and end points
        for col in range(start_col + 1, end_col):
            # Set the interior pixels of the block to white (0) in the output grid
            output_row[col] = 0

    # Return the modified grid
    return output_grid