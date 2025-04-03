import numpy as np
import sys # adding sys to allow helper function imports

# Add helper functions directory to Python path if needed (adjust path as necessary)
# sys.path.append('/path/to/your/helper_functions') 
# from helper_functions import find_foreground_color, find_longest_block # Example import

# Define helper functions directly within the module for simplicity in this case

def find_foreground_color(row):
    """
    Finds the first non-zero color in the row.
    Assumes 0 is the background color.

    Args:
        row (list): A list of integers representing a row of pixels.

    Returns:
        int or None: The first non-zero color found, or None if only
                     background color (0) exists.
    """
    for pixel in row:
        if pixel != 0:
            return pixel
    return None # Return None if only background color exists

def find_longest_block(row, foreground_color):
    """
    Finds the start index and length of the longest contiguous block 
    of the specified foreground_color in the row.

    Args:
        row (list): A list of integers representing a row of pixels.
        foreground_color (int): The color value to search for blocks of.

    Returns:
        tuple (int, int): A tuple containing:
            - The start index of the longest block found (-1 if no block found).
            - The length of the longest block found (0 if no block found).
    """
    n = len(row)
    max_len = 0
    longest_block_start = -1
    current_start = -1
    current_len = 0

    for i in range(n):
        if row[i] == foreground_color:
            # If this is the start of a new block
            if current_len == 0:  
                current_start = i
            # Increment length of current block
            current_len += 1
        else:  
            # Reached the end of a potential block (or still in background)
            # Check if the block just ended was the longest found so far
            if current_len > 0:  # Only check if we were actually tracking a block
                if current_len > max_len:
                    max_len = current_len
                    longest_block_start = current_start
            # Reset current block tracking
            current_len = 0  

    # After the loop, check if the last sequence was a block and potentially the longest
    # This handles cases where the longest block extends to the end of the row
    if current_len > max_len:
        max_len = current_len
        longest_block_start = current_start

    return longest_block_start, max_len


def transform(input_grid):
    """
    Transforms the input single-row grid by identifying the longest
    contiguous block of the foreground color and preserving only that
    block in the output row. All other pixels in the output row are 
    set to the background color (0).

    Args:
        input_grid (list of lists): A grid represented as a list containing a single list (row) of integers.

    Returns:
        list of lists: A new grid containing the transformed single row.
                       Returns an empty list if the input is invalid.
    """
    # --- Input Validation and Setup ---
    # Check for empty or invalid input format
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Consider logging a warning or raising an error for invalid input
        return [] 

    # Extract the single row from the input grid structure
    input_row = input_grid[0]
    n = len(input_row) # Get the length of the row

    # --- Identify Foreground Color ---
    # Determine the color used for foreground objects (assumes only one non-background color)
    foreground_color = find_foreground_color(input_row)

    # Handle the case where the input row contains only the background color
    if foreground_color is None:
        # Return a new grid of the same size filled with background color
        return [[0] * n] 

    # --- Find the Longest Block ---
    # Locate the starting position and length of the longest continuous sequence 
    # of the foreground color.
    start_index, length = find_longest_block(input_row, foreground_color)

    # --- Create Output Grid ---
    # Initialize a new output row filled entirely with the background color (0)
    output_row = [0] * n

    # If a longest block was actually found (i.e., length > 0)
    if start_index != -1 and length > 0:
        # Copy the pixels corresponding to the longest block from the input 
        # into the output row at the same position.
        for i in range(length):
            # Calculate the index in the output row
            output_index = start_index + i
            # Check bounds just in case, though logic should prevent out-of-bounds
            if 0 <= output_index < n: 
                output_row[output_index] = foreground_color

    # Return the transformed row, wrapped in a list to match the grid format
    return [output_row]