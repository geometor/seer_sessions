"""
Transforms a 1xN input grid by finding the single contiguous block of 
non-white pixels within the row and shifting this block 2 positions 
(columns) to the right. The output grid has the same dimensions as the 
input, with the shifted block placed at its new position and all other 
pixels set to white (0).
"""

import numpy as np

def find_contiguous_block_in_row(row_sequence):
    """
    Finds the start index, end index (exclusive), color, and length 
    of the first contiguous block of non-white pixels in a 1D sequence.
    
    Args:
        row_sequence (np.array): The 1D input sequence (a row from the grid).

    Returns:
        tuple: (start_index, end_index, color, length) or None if no block found.
    """
    start_index = -1
    color = 0
    length = 0
    block_found = False # Flag to track if we are inside a potential block

    for i, pixel in enumerate(row_sequence):
        # If we haven't started a block yet and find a non-white pixel
        if start_index == -1 and pixel != 0:
            start_index = i
            color = pixel
            length = 1
            block_found = True
        # If we are inside a block (block_found is True)
        elif block_found:
            # Check if the current pixel continues the block
            if pixel == color:
                length += 1
            # If the pixel is different (or white), the block has ended
            else:
                end_index = start_index + length
                return start_index, end_index, color, length
                
    # Handle case where the block extends to the very end of the sequence
    if block_found:
        end_index = start_index + length
        return start_index, end_index, color, length
        
    # No non-white block found
    return None

def transform(input_grid):
    """
    Applies the block shifting transformation to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid (expected 1xN).

    Returns:
        list: A list of lists representing the transformed grid.
    """
    # Convert input grid (list of lists) to a numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure it's a 2D array even if input is just a flat list sometimes
    if input_array.ndim == 1:
         # This case handles if input_grid was accidentally flattened e.g., [3,3,3,...]
         # We reshape it back to the expected 1xN format
         input_array = input_array.reshape(1, -1) 
         
    # Verify shape is 1xN (or handle other cases if needed, though not expected)
    if input_array.shape[0] != 1:
        # Handle error or unexpected input format if necessary
        # For this specific task, assume it's always 1xN
        print(f"Warning: Expected input grid shape (1, N), but got {input_array.shape}. Processing the first row only.")
        # Or raise ValueError("Input grid must have exactly one row.")

    # Extract the single row as a 1D sequence
    row_sequence = input_array[0, :]
    sequence_length = len(row_sequence)
    
    # Initialize the output grid with the same shape as input, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Find the non-white block in the row sequence
    block_info = find_contiguous_block_in_row(row_sequence)

    # If a block was found
    if block_info:
        start_index, end_index, color, length = block_info
        
        # Calculate the new start index by shifting right by 2 positions
        shift_amount = 2
        new_start_index = start_index + shift_amount
        new_end_index = new_start_index + length # Calculate new end index (exclusive)
        
        # Check if the new block position fits within the sequence boundaries
        if new_end_index <= sequence_length:
            # Place the block (with its original color and length) 
            # into the first row of the output array at the new position
            output_array[0, new_start_index:new_end_index] = color
        else:
            # Handle potential out-of-bounds scenario if required by task rules.
            # Based on examples, the shift seems safe, so we assume it fits.
            # If it could go out of bounds, we might need to clip or wrap, 
            # but for now, just place it assuming it fits.
            # Example clipping:
            # placeable_length = sequence_length - new_start_index
            # if placeable_length > 0:
            #    output_array[0, new_start_index : new_start_index + placeable_length] = color
            print(f"Warning: Shifted block from {start_index}-{end_index} to {new_start_index}-{new_end_index} might exceed bounds {sequence_length}.")
            # For safety, let's implement clipping just in case.
            actual_end_index = min(new_end_index, sequence_length)
            if new_start_index < sequence_length: # Ensure start is within bounds
                 output_array[0, new_start_index:actual_end_index] = color


    # Convert the resulting numpy array back to a list of lists for the expected output format
    output_grid = output_array.tolist()
    
    return output_grid