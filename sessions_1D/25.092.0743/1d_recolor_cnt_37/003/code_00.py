import numpy as np

"""
Transforms a 1xN input grid by replacing contiguous blocks of yellow (4) pixels 
based on their length, while keeping white (0) pixels unchanged.
- A block of 1 yellow pixel becomes 1 orange (7) pixel.
- A block of 2 yellow pixels becomes 2 maroon (9) pixels.
- A block of 3 yellow pixels becomes 3 red (2) pixels.
Input is assumed to be a 2D NumPy array with one row. Output is a 1D list.
"""

def find_yellow_block_length(row_data, start_index, width):
    """
    Finds the length of a contiguous block of yellow (4) pixels in a 1D array 
    starting at a given index.
    
    Args:
        row_data (np.array): The 1D array representing the grid row.
        start_index (int): The index where the yellow block starts.
        width (int): The total width of the row.
        
    Returns:
        int: The length of the contiguous yellow block. Returns 0 if the pixel
             at start_index is not yellow or if start_index is out of bounds.
    """
    # Check if the starting pixel is yellow and index is valid
    if start_index >= width or row_data[start_index] != 4:
        return 0
        
    length = 0
    # Iterate from the start index as long as we are within bounds and the pixel is yellow
    for i in range(start_index, width):
        if row_data[i] == 4:
            length += 1
        else:
            # Stop counting when a non-yellow pixel is encountered
            break
    return length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D NumPy array (expected shape 1xN) 
                               representing the input pixel row.

    Returns:
        list: A 1D list of integers representing the transformed output pixel row.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Validate input shape (should be 1xN)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle potential error case, maybe return input or raise error
        # For now, let's try to proceed if it looks like a 1D list/array
        if input_grid.ndim == 1:
           input_grid = input_grid.reshape(1, -1) # Reshape to 1xN
        else:
             raise ValueError("Input grid must be a 2D array with one row.")
             
    # Extract the row data and grid width
    row_data = input_grid[0]
    width = input_grid.shape[1]
    
    # Initialize output_grid as a list copy of the input row data
    output_grid = list(row_data)
    
    # Initialize processing index
    i = 0
    # Iterate through the grid row
    while i < width:
        # Get the current pixel value
        pixel_value = row_data[i]
        
        # Check if the current pixel is yellow
        if pixel_value == 4:
            # Find the length of the contiguous block of yellow pixels
            block_length = find_yellow_block_length(row_data, i, width)
            
            # Determine the replacement color based on the block length
            output_color = -1 # Default/error value
            if block_length == 1:
                output_color = 7 # Orange
            elif block_length == 2:
                output_color = 9 # Maroon
            elif block_length == 3:
                output_color = 2 # Red
            # Assume only lengths 1, 2, 3 occur based on examples.
            # If other lengths could occur, need rules for them.
            
            # Fill the corresponding section in the output grid with the new color
            if output_color != -1:
                for j in range(i, i + block_length):
                    # Check bounds (redundant due to while loop condition and block_length logic, but safe)
                    if j < width: 
                        output_grid[j] = output_color
            
            # Advance the index past the processed block
            # If block_length was 0 (e.g., unexpected non-4 pixel starting block), increment by 1
            i += max(1, block_length) 
        else:
            # If the pixel is not yellow (i.e., it's white or other), 
            # keep the original value (already in output_grid copy) 
            # and move to the next pixel.
            i += 1
            
    return output_grid