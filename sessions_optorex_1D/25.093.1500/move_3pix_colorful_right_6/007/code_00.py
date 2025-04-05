import math
# No external libraries like numpy needed based on the core logic identified.

"""
Identifies a contiguous block of non-zero numbers within an input list, 
shifts this block 3 positions to the right, and places it into an 
output list of the same size, padded with zeros elsewhere. Handles cases 
where the shifted block might extend beyond the list boundaries by truncating 
the block. If the input list contains only zeros, the output list will also 
contain only zeros.
"""

def _find_non_zero_indices(data_list):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.
    
    Args:
        data_list: A list of numbers.

    Returns:
        A tuple (start_index, end_index). Returns (None, None) if no 
        non-zero numbers are found.
    """
    first_nz_index = None
    last_nz_index = None
    # Iterate through the list with index and value
    for i, val in enumerate(data_list):
        # Check if the value is not zero
        if val != 0:
            # If this is the first non-zero found, record its index
            if first_nz_index is None:
                first_nz_index = i
            # Always update the last non-zero index found
            last_nz_index = i
            
    # Return the found indices (or None if none were found)
    return first_nz_index, last_nz_index

def transform(input_list):
    """
    Transforms the input list by shifting the block of non-zero numbers 
    3 positions to the right.

    Args:
        input_list: A list of integers (represented as input_grid in template but is 1D).

    Returns:
        A new list of integers with the non-zero block shifted, or a list 
        of zeros if no non-zero block exists in the input.
    """
    # Ensure input is a standard list, in case it's passed as another iterable type
    # This also handles potential numpy arrays being passed, converting them to lists.
    if not isinstance(input_list, list):
        # Attempt conversion if possible (e.g., from tuple, numpy array)
        try:
            input_list = list(input_list)
        except TypeError:
            raise TypeError("Input must be a list or convertible to a list.")
            
    # Determine the length of the list
    list_length = len(input_list)

    # initialize output_list: Create a list of the same length, filled with zeros.
    output_list = [0] * list_length

    # Find the start and end indices of the non-zero block using the helper function
    first_nz_index, last_nz_index = _find_non_zero_indices(input_list)

    # Check if a non-zero block was actually found
    if first_nz_index is not None:
        # Extract the non-zero block using list slicing
        # Note: slicing is exclusive of the end index, so add 1 to last_nz_index
        non_zero_block = input_list[first_nz_index : last_nz_index + 1]

        # Calculate the new starting position for the block (shift right by 3)
        shift_amount = 3
        new_start_index = first_nz_index + shift_amount
        
        # Determine the length of the extracted block
        block_len = len(non_zero_block)
        
        # change output pixels: Calculate placement boundaries and handle truncation
        
        # Calculate the index where the placement *would* end if it fit entirely
        potential_end_placement_index = new_start_index + block_len

        # Determine how many elements from the block can actually be placed
        # without going out of bounds of the output list.
        elements_to_place = block_len
        if potential_end_placement_index > list_length:
            # If the block overflows, calculate how many elements fit
            elements_to_place = list_length - new_start_index
            # If the adjusted count is negative (meaning the start index is already out of bounds), set to 0
            if elements_to_place < 0:
                elements_to_place = 0
        
        # Place the block (or the portion that fits) into the output list
        # Ensure the new start index is within the list bounds AND there are elements to place
        if new_start_index < list_length and elements_to_place > 0:
            # Slice the output list and assign the appropriate slice of the non_zero_block
            # The slice of non_zero_block must have length equal to elements_to_place
            output_list[new_start_index : new_start_index + elements_to_place] = non_zero_block[:elements_to_place]

    # Return the constructed output list (either modified or still all zeros)
    return output_list