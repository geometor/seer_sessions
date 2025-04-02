import numpy as np

def find_first_of_color(grid_row, color):
    """Finds the index of the first occurrence of a specific color in a 1D array."""
    for i, pixel in enumerate(grid_row):
        if pixel == color:
            return i
    return -1 # Not found

def find_last_of_color(grid_row, color):
    """Finds the index of the last occurrence of a specific color in a 1D array."""
    last_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == color:
            last_index = i
    return last_index # Returns -1 if not found

def find_main_segment(grid_row):
    """Identifies the main color segment and its end index."""
    segment_color = -1
    segment_start_index = -1
    segment_end_index = -1

    for i, pixel in enumerate(grid_row):
        # Find the start of a potential segment (not white, not orange)
        if segment_color == -1 and pixel != 0 and pixel != 7:
            segment_color = pixel
            segment_start_index = i
            segment_end_index = i # Initialize end index
        # If we are inside a segment, check if it continues
        elif segment_color != -1 and pixel == segment_color:
            segment_end_index = i
        # If the segment ends (color changes or becomes white/orange)
        elif segment_color != -1 and pixel != segment_color:
            break # Found the end of the first main segment

    if segment_color == -1:
         raise ValueError("No main color segment found in the input grid.")

    return segment_color, segment_end_index


def transform(input_grid):
    """
    Identifies a contiguous horizontal segment of a single non-white, non-orange color
    and extends it to the right until it reaches the column immediately preceding
    a single orange pixel (color 7). The intervening white pixels are filled
    with the segment's color.
    """
    # Ensure input is a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle the 1D case explicitly
    if input_grid_np.ndim == 1:
        grid_row = input_grid_np
    elif input_grid_np.shape[0] == 1: # Check if it's a 2D array with one row
        grid_row = input_grid_np[0]
    else:
        # This function is designed for 1D grids as per the examples
        raise ValueError("Input grid must be 1-dimensional or a 2D array with a single row.")


    # Initialize output_grid as a copy of the input row
    output_grid_row = grid_row.copy()

    # 1. Identify the main color segment and its end index
    try:
        segment_color, segment_end_index = find_main_segment(grid_row)
    except ValueError as e:
        print(f"Error processing grid: {e}")
        # Depending on requirements, might return input grid or handle differently
        return input_grid # Return original if segment not found as per examples

    # 2. Identify the index of the orange pixel
    orange_index = find_first_of_color(grid_row, 7)

    # Check if the orange pixel exists and is to the right of the segment
    if orange_index == -1:
        print("Warning: Orange pixel (7) not found. Returning original grid.")
        return input_grid # Or raise error depending on spec
    if orange_index <= segment_end_index:
        print("Warning: Orange pixel is not to the right of the segment. Returning original grid.")
        return input_grid # Or raise error

    # 3. Iterate through the columns from segment_end_index + 1 up to orange_index
    # 4. Change the color of the pixels in this range to segment_color
    for i in range(segment_end_index + 1, orange_index):
         # Only change if it's currently white (as per examples, prevents overwriting other colors if logic changes)
        if output_grid_row[i] == 0:
            output_grid_row[i] = segment_color
        # If the task implies *always* filling, regardless of current color:
        # output_grid_row[i] = segment_color

    # Return the modified grid row (as a standard list if necessary, matching input type)
    # If original input was 2D, return 2D
    if input_grid_np.ndim == 2:
        return output_grid_row.reshape(1, -1) # Reshape back to 1xN
    else:
        return output_grid_row.tolist() # Return as list if input was 1D list