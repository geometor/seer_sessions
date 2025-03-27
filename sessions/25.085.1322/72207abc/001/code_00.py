import numpy as np
import math

def find_pattern_and_initial_block(input_row):
    """
    Helper function to find the sequence of non-white pixels (pattern) 
    and the initial block from the input row.
    The initial block extends from the start up to and including the index 
    of the last occurrence of a pattern pixel.
    
    Args:
        input_row (list): The middle row of the input grid.
        
    Returns:
        tuple: (pattern_pixels, initial_block)
               pattern_pixels (list): List of non-zero pixel values in order.
               initial_block (list): The initial segment of the input row.
    """
    # Extract all non-white pixels, preserving order
    pattern_pixels = [pixel for pixel in input_row if pixel != 0]
    
    # If there are no non-white pixels in the row
    if not pattern_pixels:
        # The pattern is empty, and the initial block is the entire row
        # (as there's no 'last pattern pixel' index to define a shorter block)
        return [], list(input_row) 

    # Find the index of the last occurrence of any pattern pixel
    last_pattern_idx = -1
    # Iterate backwards to find the last index efficiently
    for i in range(len(input_row) - 1, -1, -1):
        # Check if the pixel at this index is part of our pattern
        if input_row[i] in pattern_pixels:
            last_pattern_idx = i
            break # Found the last one, no need to search further
            
    # Define the initial block: from the start up to and including the last pattern pixel
    # If last_pattern_idx remained -1 (shouldn't happen if pattern_pixels is not empty), 
    # this slice would be input_row[:0] which is [], but the check above prevents this.
    initial_block = list(input_row[:last_pattern_idx + 1]) 
    
    return pattern_pixels, initial_block

def transform(input_grid):
    """
    Transforms the input grid based on repeating a pattern with increasing spacing.

    The transformation works as follows:
    1. Identify the sequence of non-white pixels in the middle row (row 1) 
       as the 'pattern', preserving their order.
    2. Determine the 'initial block' of the middle row, which is the segment 
       starting from the first column up to and including the column where the 
       last pattern pixel appears.
    3. Initialize the output grid's middle row by copying this 'initial block'.
    4. Calculate the initial number of white spaces to insert: num_spaces = len(pattern) - 1.
    5. Repeatedly perform the following until the output middle row reaches the 
       input grid's width:
       a. Append 'num_spaces' white pixels (0). Stop if the row reaches the target width.
       b. If the row is not yet full, append the next pixel from the 'pattern' sequence 
          (cycling back to the start of the pattern if necessary). Stop if the row 
          reaches the target width.
       c. Increment 'num_spaces' by 1 for the next iteration.
    6. The top (row 0) and bottom (last row) rows of the grid remain unchanged 
       (assumed to be all white based on examples).
    """
    # Convert input to a numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Create the output grid, starting as a copy of the input
    output_np = np.copy(input_np) 

    # The transformation logic applies only to the middle row (index 1)
    # Assuming grid height is always 3 based on examples
    if height != 3:
        # If height is not 3, return the input unchanged as the logic is specific
        # print("Warning: Grid height is not 3. Returning input grid unchanged.")
        return input_np.tolist()

    input_row_1 = list(input_np[1, :])

    # Use the helper function to get the pattern and the initial block
    pattern_pixels, initial_block = find_pattern_and_initial_block(input_row_1)

    # Edge case: If there are no non-white pixels in the input row
    if not pattern_pixels:
        # The middle row remains unchanged, and output_np already holds the copy.
        return output_np.tolist() 

    # Initialize the output middle row (as a list for easy appending)
    # Start with a copy of the initial_block
    output_row_1_list = initial_block[:] 

    # Calculate the initial number of white spaces to insert between pattern elements
    # If pattern has length 1, num_spaces = 0, which is correct.
    num_spaces = len(pattern_pixels) - 1 
    # Ensure num_spaces is not negative (shouldn't happen if pattern_pixels is not empty)
    num_spaces = max(0, num_spaces) 

    # Initialize the index for cycling through the pattern_pixels
    pattern_index = 0
    
    # Fill the rest of the output middle row by appending spaces and pattern pixels
    while len(output_row_1_list) < width:
        
        # --- Step 1: Append spaces ---
        spaces_to_add_now = num_spaces
        for _ in range(spaces_to_add_now):
            # Check if there's still room in the row
            if len(output_row_1_list) < width:
                output_row_1_list.append(0) # Append a white pixel
            else:
                # If adding a space would exceed width, break this inner loop
                break 
        
        # Check if the row became full just by adding spaces
        if len(output_row_1_list) >= width:
            break # Exit the main while loop

        # --- Step 2: Append the next pattern pixel ---
        pixel_to_add = pattern_pixels[pattern_index]
        # Check again if there's room before appending the pattern pixel
        if len(output_row_1_list) < width:
             output_row_1_list.append(pixel_to_add)
        else:
             # If adding the pixel would exceed width, break the main loop
             break 

        # --- Step 3: Update pattern index for the next cycle ---
        pattern_index = (pattern_index + 1) % len(pattern_pixels)

        # --- Step 4: Increment the number of spaces for the next iteration ---
        num_spaces += 1

    # The loop ensures the list does not exceed width. 
    # If it's shorter (only possible if width was smaller than initial_block), 
    # truncate (though this case seems unlikely based on task structure).
    # If it's exactly width, this slice does nothing.
    final_output_row_1 = output_row_1_list[:width]

    # Place the generated row back into the numpy output grid
    output_np[1, :] = np.array(final_output_row_1, dtype=int)

    # Return the result as a list of lists
    return output_np.tolist()