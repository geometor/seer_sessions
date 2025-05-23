import copy

"""
Transformation Rule Description:
The transformation takes a 2D input grid (list of lists) which, for this specific task, always has a height of 1 (a single row).
It identifies the first contiguous block of non-white (non-zero) pixels within this row.
This identified block is then shifted exactly 2 positions (columns) to the right.
The pixels in the new positions occupied by the shifted block take the color of the block. If the shift causes part of the block to extend beyond the right boundary of the grid, that part is truncated.
All other pixels in the output grid row (positions not occupied by the shifted block) are set to the background color, which is white (0).
The dimensions (height and width) of the grid remain unchanged.
"""

def find_first_object(row):
    """
    Finds the color, start index, and length of the first contiguous
    block of non-background (0) pixels in a 1D list (row).
    
    Args:
        row (list): A list of integers representing a row in the grid.
        
    Returns:
        tuple: (color, start_index, length) of the first object found,
               or None if no non-background object is found.
    """
    start_index = -1
    color = 0
    length = 0
    in_object = False
    
    for i, pixel in enumerate(row):
        # If we are not currently inside an object and we encounter a non-background pixel
        if not in_object and pixel != 0: 
            start_index = i  # Mark the start index
            color = pixel    # Record the color
            length = 1       # Start counting the length
            in_object = True # Set the flag indicating we are inside an object
        # If we are inside an object and the current pixel matches the object's color
        elif in_object and pixel == color: 
            length += 1      # Increment the length
        # If we are inside an object but the current pixel is different (either background or another color)
        elif in_object and pixel != color: 
            # We have found the end of the first contiguous object, so we can stop searching.
            break 
            
    # If no non-background pixel was ever found, start_index will remain -1
    if start_index == -1:
        return None
        
    # Return the found object's properties
    return color, start_index, length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.
                                      Expected to have height 1 for this task.
                                      
    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Validate input format - assuming ARC standard list[list[int]]
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         # Return a deep copy if input is invalid or empty to avoid errors
         # Or handle error appropriately depending on expected behavior
         return copy.deepcopy(input_grid) 

    # Extract the first (and only expected) row
    input_row = input_grid[0]
    grid_width = len(input_row)
    
    # Initialize the output row with the background color (0)
    output_row = [0] * grid_width

    # Find the object (contiguous block of non-zero pixels) in the input row
    object_info = find_first_object(input_row)

    # Proceed only if an object was found
    if object_info:
        color, start_index, length = object_info

        # Calculate the new starting position by shifting right by 2
        new_start_index = start_index + 2

        # Place the object into the output row at the new position
        # Iterate through the length of the object
        for i in range(length):
            # Calculate the target index in the output row
            current_output_index = new_start_index + i
            
            # Check if the target index is within the grid boundaries
            if 0 <= current_output_index < grid_width:
                # If within bounds, place the object's pixel color here
                output_row[current_output_index] = color
            # else: If the index is out of bounds (shifted off the right edge), 
            # the pixel is truncated (effectively ignored).

    # Wrap the single output row back into a 2D grid format
    output_grid = [output_row]
    
    return output_grid