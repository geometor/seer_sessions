import math
import collections

"""
Identifies contiguous blocks of zeros within the sequence that are immediately preceded and succeeded by non-zero numbers (pattern: X 0...0 Y). 
If such a block is found, all zeros in that block are replaced.
The replacement value is determined by the succeeding non-zero number (Y):
- If Y is 2, the zeros are replaced by the value of the preceding non-zero number (X).
- Otherwise (if Y is not 2), the zeros are replaced by the value of Y itself.
Sequences of zeros at the beginning or end of the sequence, or zeros not adjacent to non-zero numbers on both sides, are left unchanged.
"""

def transform(input_sequence):
    """
    Transforms the input sequence based on the described rules.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Create a mutable copy of the input sequence to modify
    output_sequence = list(input_sequence)
    n = len(output_sequence)
    
    # Iterate through the sequence to find potential zero blocks
    i = 1 # Start checking from the second element (index 1)
    while i < n - 1: # Need at least one element before (X) and one after (Y) the potential zero block
        
        # Check if we are at the beginning of a potential zero block bounded by non-zeros
        # output_sequence[i] must be 0
        # output_sequence[i-1] must be non-zero (X)
        if output_sequence[i] == 0 and output_sequence[i-1] != 0:
            start_zero_index = i
            
            # Find the end of the contiguous block of zeros
            k = i
            # Move k forward as long as we are within bounds and find zeros
            while k + 1 < n and output_sequence[k+1] == 0:
                k += 1
            # Now, k is the index of the last zero in this contiguous block
            end_zero_index = k
            
            # Check if this block of zeros is followed by a non-zero number (Y)
            # We need to ensure there's an element at end_zero_index + 1
            # and that element is not zero
            if end_zero_index + 1 < n and output_sequence[end_zero_index + 1] != 0:
                # Found a valid X 0...0 Y pattern
                x_value = output_sequence[start_zero_index - 1]
                y_value = output_sequence[end_zero_index + 1]
                
                # Determine the value to fill the zeros with
                fill_value = 0 # Default shouldn't be used, initialize defensively
                if y_value == 2:
                    fill_value = x_value
                else:
                    fill_value = y_value
                    
                # Replace the zeros in the block with the determined fill_value
                for j in range(start_zero_index, end_zero_index + 1):
                    output_sequence[j] = fill_value
                    
                # Move the main loop index past the block we just processed
                # The next potential start could be at end_zero_index + 2 
                # (since end_zero_index + 1 is Y, a non-zero)
                # Set i to end_zero_index + 1; the loop increment will move it to +2
                i = end_zero_index + 1 
            else:
                # The block of zeros either extends to the end of the sequence
                # or is followed by the end, so it doesn't fit the X 0...0 Y pattern.
                # Move the index past this block of zeros to continue searching.
                # Next potential start is after the last zero found.
                i = end_zero_index + 1
        else:
            # The current element output_sequence[i] is not the start of a 
            # qualifying zero block (either it's non-zero, or the preceding element is zero).
            # Move to the next element.
            i += 1
            
    return output_sequence
