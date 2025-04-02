import numpy as np

def find_first_of(arr, values):
    """Finds the index and value of the first element in arr that is present in the values set."""
    for i, x in enumerate(arr):
        if x in values:
            return i, x
    return -1, -1 # Not found

def find_first_not_of(arr, values_to_exclude, start_index=0):
    """Finds the index and value of the first element in arr starting from start_index
       that is NOT present in the values_to_exclude set."""
    for i in range(start_index, len(arr)):
        if arr[i] not in values_to_exclude:
            return i, arr[i]
    return -1, -1 # Not found

def find_last_contiguous(arr, value, start_index):
    """Finds the last index of a contiguous block of 'value' starting from start_index."""
    last_index = start_index
    for i in range(start_index + 1, len(arr)):
        if arr[i] == value:
            last_index = i
        else:
            break
    return last_index

def transform(input_grid):
    """
    Transforms the input 1D grid (represented as a list) by extending a colored
    block to the right until it reaches an orange boundary pixel.

    1. Identifies a contiguous block of a single color (not white '0' or orange '7').
    2. Identifies the orange ('7') boundary pixel to the right of the block.
    3. Fills the white ('0') pixels between the end of the block and the boundary
       pixel with the block's color.
    """
    # The input is expected to be a 1D list (single row)
    input_row = input_grid

    # Create a copy to modify for the output
    output_row = list(input_row)

    # Define colors to ignore when looking for the source block start
    ignore_colors = {0, 7} # white and orange

    # 1. Find the start of the source color block
    source_start_index, source_color = find_first_not_of(output_row, ignore_colors)

    # Check if a source block was found
    if source_start_index == -1:
        # No source block found, return the original row (or handle as error)
        return output_row # Or potentially raise an error depending on requirements

    # 2. Find the end of the source color block
    source_end_index = find_last_contiguous(output_row, source_color, source_start_index)

    # 3. Find the boundary pixel (orange '7') starting search after the source block
    boundary_index = -1
    try:
        # Use list.index() for simplicity, specifying the start search position
        boundary_index = output_row.index(7, source_end_index + 1)
    except ValueError:
        # No boundary pixel found after the source block, return unchanged row
        # This case might indicate an unexpected input format based on examples
        return output_row

    # 4. Fill the gap between the source block end and the boundary pixel
    # Iterate from the pixel *after* the source block end up to *before* the boundary
    for i in range(source_end_index + 1, boundary_index):
        # Only fill if the pixel is currently white (optional, but matches description)
        # Based on examples, the space *is* white, but this makes it robust.
        # if output_row[i] == 0:
        output_row[i] = source_color

    # 5. Return the modified row
    return output_row