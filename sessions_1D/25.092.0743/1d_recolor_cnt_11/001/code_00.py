import numpy as np

"""
Processes a 1D sequence of pixels (represented as a list of integers).
Identifies contiguous blocks of maroon (9) pixels.
Replaces each maroon block with a block of the same length but with a different color based on the length of the block:
- Length 1: replaced with orange (7)
- Length 2: replaced with magenta (6)
- Length 3: replaced with gray (5)
White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input 1D grid based on the lengths of contiguous maroon blocks.

    Args:
        input_grid (list): A list of integers representing the input 1D grid.

    Returns:
        list: A list of integers representing the transformed 1D grid.
    """
    
    # Convert input to a NumPy array for easier manipulation if needed,
    # though list operations are sufficient here.
    # For consistency with potential future ARC tasks using grids, let's keep it list-based for 1D.
    input_list = list(input_grid) # Ensure it's a mutable list
    n = len(input_list)
    output_list = list(input_list) # Initialize output as a copy of input

    i = 0
    while i < n:
        # Check if the current pixel is maroon (9)
        if input_list[i] == 9:
            # Found the start of a potential maroon block, determine its length
            length = 0
            j = i
            while j < n and input_list[j] == 9:
                length += 1
                j += 1
            
            # Determine the replacement color based on the length
            replacement_color = -1 # Default or error value
            if length == 1:
                replacement_color = 7 # orange
            elif length == 2:
                replacement_color = 6 # magenta
            elif length == 3:
                replacement_color = 5 # gray
            # Add handling for unexpected lengths if necessary, though examples only show 1, 2, 3
            # else:
            #    # Keep original color or handle error? Keeping original for now if unexpected.
            #    replacement_color = 9 

            # Replace the block in the output list if a valid length was found
            if replacement_color != -1:
                 for k in range(i, i + length):
                    output_list[k] = replacement_color
            
            # Move the main index past the processed block
            i += length
        else:
            # If the pixel is not maroon (it must be white based on examples),
            # it's already correctly copied in the initialization. Move to the next pixel.
            i += 1
            
    return output_list
