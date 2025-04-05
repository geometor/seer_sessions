import math # Not strictly needed, but good practice to include if math ops might arise
import numpy as np # Also not strictly needed for this list-based solution

"""
Transforms an input sequence (list) of 12 integers by performing the following steps:
1. Identifies a single contiguous block of identical non-zero integers within the input sequence.
2. Determines the value (V), length (L), and starting index (S_in) of this block.
3. Calculates a new starting index (S_out) by shifting the block left by its length: S_out = S_in - L.
4. Creates an output sequence of 12 zeros.
5. Places the block (value V repeated L times) into the output sequence starting at index S_out.
6. Returns the resulting output sequence.
"""

def find_non_zero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        sequence: A list of numbers.

    Returns:
        A tuple (value, length, start_index) if a block is found,
        otherwise None. Returns None if no non-zero element is found or
        if the input is empty/invalid.
    """
    start_index = -1
    block_value = 0
    block_length = 0
    found_start = False

    if not sequence: # Handle empty sequence case
        return None

    for i, val in enumerate(sequence):
        if not found_start and val != 0:
            # Found the start of the block
            start_index = i
            block_value = val
            block_length = 1
            found_start = True
        elif found_start:
            # Already found the start, now check if the block continues or ends
            if val == block_value:
                block_length += 1
            else:
                # Block ended because the value changed (or hit a zero)
                break # Exit loop once the block is fully identified

    if found_start:
        return block_value, block_length, start_index
    else:
        # No non-zero element was found in the sequence
        return None

def transform(input_grid):
    """
    Applies the block-shifting transformation to the input list.

    Args:
        input_grid: A list of 12 integers representing the input state.

    Returns:
        A list of 12 integers representing the transformed state.
    """
    # Ensure input is treated as a flat list if it comes in another format (e.g., numpy array)
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.flatten().tolist()
    else:
        # Assume it's already a list or compatible sequence
        input_list = list(input_grid) 
        
    grid_size = len(input_list)
    # Initialize the output grid (list) with zeros, matching input size
    output_grid = [0] * grid_size

    # Step 1 & 2: Find the non-zero block details
    block_info = find_non_zero_block(input_list)

    # Check if a block was found
    if block_info:
        block_value, block_length, start_index = block_info

        # Step 3: Calculate the new starting index for the block
        # Shift left by block_length positions
        new_start_index = start_index - block_length

        # Ensure the new start index is not negative (though examples suggest it won't be)
        # This also handles the case where new_start_index might become < 0
        # new_start_index = max(0, new_start_index) # Redundant if placement checks bounds

        # Step 5: Place the block into the output grid at the new position
        for i in range(block_length):
            # Calculate the target index in the output grid
            output_index = new_start_index + i
            
            # Check bounds to prevent errors if shift goes out of range
            # (though examples fit within the 0-11 range)
            if 0 <= output_index < grid_size:
                 output_grid[output_index] = block_value
            # else:
                 # If the shift could potentially go out of bounds left or right,
                 # handle it here (e.g., wrap around, clip, or raise error).
                 # Based on examples, clipping (doing nothing) is sufficient.
                 # pass

    # Step 6: Return the modified output grid
    # If no block was found, the initialized list of zeros is returned.
    return output_grid