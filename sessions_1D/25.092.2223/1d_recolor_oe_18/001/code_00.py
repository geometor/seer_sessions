import numpy as np
from collections import deque

"""
Identify contiguous horizontal segments (objects) of orange (7) pixels in the input grid (which is always 1 row).
Recolor these segments based on their length (number of pixels).
If a segment's length is odd, recolor it magenta (6).
If a segment's length is even, recolor it azure (8).
Leave all other pixels (background white/0) unchanged.
"""

def find_1d_objects(row, target_color):
    """
    Finds contiguous horizontal segments of a target color in a 1D list or array.

    Args:
        row (list or np.array): The 1D input grid row.
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of objects, where each object is a list of column indices
              belonging to that segment.
              e.g., [[3, 4, 5], [8, 9], [13, 14, 15, 16, 17, 18], [22, 23, 24]]
    """
    objects = []
    current_object_indices = []
    in_object = False
    
    # Iterate through the row with index
    for col_idx, pixel_color in enumerate(row):
        if pixel_color == target_color:
            # If we find the target color, start or continue the current object
            current_object_indices.append(col_idx)
            in_object = True
        else:
            # If we encounter a different color and were previously in an object
            if in_object:
                # Finalize the current object segment and add it to the list
                objects.append(current_object_indices)
                # Reset for the next potential object
                current_object_indices = []
                in_object = False
                
    # After the loop, check if we were in an object when the row ended
    if in_object:
        objects.append(current_object_indices)
        
    return objects

def transform(input_grid):
    """
    Transforms the input grid by recoloring orange segments based on length parity.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.
                                     For this task, it's expected to be 1xN.

    Returns:
        list of lists: The transformed grid.
    """
    # Ensure input is treated as numpy array for easier handling
    # Given the task structure, the grid is 1xN
    input_row = np.array(input_grid[0])
    
    # Initialize the output grid as a copy of the input row
    output_row = input_row.copy()

    # Define the color constants used in this task
    ORANGE = 7
    MAGENTA = 6
    AZURE = 8

    # Find all contiguous segments (objects) of orange color in the input row
    orange_objects = find_1d_objects(input_row, ORANGE)

    # Iterate through each identified orange object (segment)
    for object_indices in orange_objects:
        # Calculate the size (length) of the current object
        size = len(object_indices)
        
        # Determine the new color based on whether the size is odd or even
        if size % 2 != 0:  # Odd size
            new_color = MAGENTA
        else:  # Even size
            new_color = AZURE
            
        # Update the pixels in the output row corresponding to the current object
        for index in object_indices:
            output_row[index] = new_color

    # Return the transformed row wrapped in a list to match the grid format
    return [output_row.tolist()]