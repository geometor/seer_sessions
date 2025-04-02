import numpy as np

"""
Transforms a 1D input grid (represented as a single row) by finding a
contiguous block of a 'primary' color (not white=0, not gray=5) and a
single gray=5 pixel. It then fills any white=0 pixels located directly
between the primary color block and the gray pixel with the primary color.
The filling stops adjacent to the gray pixel.
"""

def find_primary_color_block(row):
    """
    Finds the primary color (first non-0, non-5) and the start and end
    indices of its first contiguous block in the row.

    Args:
        row (np.ndarray): The 1D array representing the grid row.

    Returns:
        tuple[int, int, int]: primary_color, start_index, end_index.
                              Returns (-1, -1, -1) if no block is found.
    """
    primary_color = -1
    start_index = -1
    end_index = -1

    # Find the first non-zero, non-gray color to identify the primary color
    for pixel in row:
        if pixel != 0 and pixel != 5:
            primary_color = pixel
            break

    if primary_color == -1:
        return -1, -1, -1 # No primary color found in the row

    # Find the start and end indices of the first contiguous block of the primary color
    try:
        current_index = 0
        while current_index < len(row):
             # Find the start of a block
             if row[current_index] == primary_color:
                 start_index = current_index
                 # Find the end of this contiguous block
                 end_index = start_index
                 while end_index + 1 < len(row) and row[end_index + 1] == primary_color:
                     end_index += 1
                 # Found the first complete block, assume only one matters per task description
                 break
             current_index += 1
    except IndexError: # Should not happen with a valid row length check
        return -1, -1, -1 # Indicate block finding failed unexpectedly

    # Check if a block was actually found (start_index should be non-negative)
    if start_index == -1:
        return -1, -1, -1

    return primary_color, start_index, end_index

def find_gray_pixel(row):
    """
    Finds the index of the first gray pixel (5) in the row.

    Args:
        row (np.ndarray): The 1D array representing the grid row.

    Returns:
        int: The index of the gray pixel, or -1 if not found.
    """
    try:
        # Find indices where the pixel value is 5
        indices = np.where(row == 5)[0]
        if len(indices) > 0:
            # Assume only one gray pixel is relevant per task constraints
            return indices[0]
        else:
            return -1 # Gray pixel not found
    except Exception:
         return -1 # Handle potential errors during search

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]] or np.ndarray): A grid, expected to be 1xN.

    Returns:
        list[list[int]]: The transformed grid in list of lists format.
    """
    # Validate input grid structure
    if not isinstance(input_grid, (list, np.ndarray)):
         raise TypeError("Input grid must be a list of lists or a numpy array")
    if isinstance(input_grid, list):
         if not input_grid or not input_grid[0]:
              return [] # Handle empty list input
         # Convert list of lists to numpy array for processing
         input_row = np.array(input_grid[0], dtype=int)
    elif isinstance(input_grid, np.ndarray):
         if input_grid.ndim != 2 or input_grid.shape[0] != 1 or input_grid.shape[1] == 0:
              # Handle empty or incorrectly shaped numpy array
              # Return format consistent with empty list input
              return []
         input_row = input_grid[0].astype(int) # Work with the first row as integer type

    # Create a modifiable copy of the input row
    output_row = input_row.copy()

    # --- Identify key components ---
    # Find the primary color block details
    primary_color, start_index, end_index = find_primary_color_block(output_row)

    # Find the gray pixel index
    gray_index = find_gray_pixel(output_row)

    # --- Apply transformation ---
    # Proceed only if both the primary block and gray pixel were successfully found
    if primary_color != -1 and start_index != -1 and gray_index != -1:

        # Determine if the gray pixel is to the right or left of the block
        if gray_index > end_index:
            # Case: Gray pixel is to the right of the block
            # Define the 'gap' range: from pixel after block end up to pixel before gray pixel
            fill_start = end_index + 1
            fill_end = gray_index
            # Iterate through the gap indices and fill white pixels
            for i in range(fill_start, fill_end):
                if output_row[i] == 0: # Check if the pixel is white
                    output_row[i] = primary_color # Change white pixel to primary color

        elif gray_index < start_index:
            # Case: Gray pixel is to the left of the block
            # Define the 'gap' range: from pixel before block start down to pixel after gray pixel
            # range() needs careful handling for reverse iteration: start, stop (exclusive), step
            fill_start = start_index - 1
            fill_end = gray_index # Stop index for range is exclusive, so gray_index works
            # Iterate through the gap indices (in reverse) and fill white pixels
            for i in range(fill_start, fill_end, -1):
                if output_row[i] == 0: # Check if the pixel is white
                    output_row[i] = primary_color # Change white pixel to primary color

    # --- Format output ---
    # Return the modified row, wrapped in a list to match ARC format
    return [output_row.tolist()]