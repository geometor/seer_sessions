"""
Accept an input sequence of integers (containing only 0s and 2s).
Initialize an empty output sequence.
Iterate through the input sequence using an index, processing each element exactly once.
If the current element is `0`, append `0` to the output sequence and advance the index by 1.
If the current element is `2`:
    a.  Check if this `2` starts a "qualifying block": it must be at index 0 OR the preceding element must be `0`.
    b.  If it *does not* start a qualifying block (i.e., it follows another `2`), append `2` to the output sequence and advance the index by 1.
    c.  If it *does* start a qualifying block:
        i.  Determine the `length` of this consecutive block of `2`s starting from the current index.
        ii. Process the elements within this block based on their position (0-indexed) within the block and the total block `length`:
            *   Append `8` for the first element (position 0).
            *   Append `8` for the second element (position 1) if `length` is 4 or greater; otherwise, append `2`.
            *   Append `8` for the third element (position 2) if `length` is 6 or greater; otherwise, append `2`.
            *   Append `2` for all subsequent elements (positions 3, 4, ...).
        iii. Advance the main iteration index by the `length` of the block just processed.
Continue until the entire input sequence has been processed.
Return the completed output sequence.
"""

# No external libraries needed

def _get_consecutive_twos_length(sequence, start_index):
    """Helper function to find the length of consecutive 2s from a start index."""
    count = 0
    # Iterate from the start index until the end of the sequence
    for i in range(start_index, len(sequence)):
        # If the element is 2, increment count
        if sequence[i] == 2:
            count += 1
        # If the element is not 2, the block ends, break the loop
        else:
            break
    return count

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence (list of integers).
    """
    # initialize output_sequence as an empty list
    output_sequence = []
    n = len(input_sequence)
    i = 0 # Initialize the main loop index

    # Iterate through the input sequence using the index i
    while i < n:
        # Get the value at the current index
        current_val = input_sequence[i]

        # Check if the current value is 0
        if current_val == 0:
            # Append 0 to the output and advance the index
            output_sequence.append(0)
            i += 1
            continue # Move to the next iteration of the while loop

        # Check if the current value is 2
        if current_val == 2:
            # Determine if this 2 starts a qualifying block
            # A block qualifies if it's at the beginning (i=0) or follows a 0
            is_start_of_qualifying_block = (i == 0 or input_sequence[i-1] == 0)

            # If it is the start of a qualifying block
            if is_start_of_qualifying_block:
                # Find the length of the consecutive block of 2s starting here
                block_length = _get_consecutive_twos_length(input_sequence, i)

                # Process each element within this identified block
                for block_pos in range(block_length):
                    # Determine the output value based on position within the block and block length
                    output_val = 2 # Default for positions >= 3 or unmet conditions

                    if block_pos == 0: # First element always transforms to 8
                        output_val = 8
                    elif block_pos == 1 and block_length >= 4: # Second element transforms if block length >= 4
                        output_val = 8
                    elif block_pos == 2 and block_length >= 6: # Third element transforms if block length >= 6
                        output_val = 8

                    # Append the determined value (8 or 2) to the output
                    output_sequence.append(output_val)

                # Advance the main loop index past the entire block that was just processed
                i += block_length

            # If it is a 2, but not the start of a qualifying block (it follows another 2)
            else:
                # Append 2 directly to the output
                output_sequence.append(2)
                # Advance the index by 1
                i += 1

        # Safety net for unexpected values, though problem statement implies only 0s and 2s
        # else:
        #     # Handle potential errors or unexpected input values if necessary
        #     # For now, just advance index to avoid infinite loop on bad input
        #     i += 1

    # Return the fully constructed output sequence
    return output_sequence
