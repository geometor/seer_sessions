import math # example import, not used in this specific code but available

"""
Transforms a sequence of integers based on contiguous blocks of '3's.

The input is a space-separated string of digits (0s and 3s).
The output is a space-separated string of digits of the same length.
Rule:
1. '0' in the input maps to '0' in the output.
2. Contiguous blocks of '3's (separated by '0's) are identified.
3. The first block of '3's encountered when scanning left-to-right is 
   transformed into a block of '1's of the same length.
4. The second block of '3's encountered is transformed into a block 
   of '2's of the same length.
5. This pattern continues if more blocks were present (though examples only 
   show two).
"""

def transform(input_str: str) -> str:
    """
    Applies the block transformation rule to the input string.

    Args:
        input_str: A space-separated string of digits (0s and 3s).

    Returns:
        A space-separated string representing the transformed sequence.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)
    output_list = [0] * n # Initialize output list, 0 is default

    # Initialize state variables
    block_counter = 0  # Counts the blocks of '3's encountered
    in_block = False   # Flag to track if currently inside a block of '3's
    
    # Iterate through the input list
    for i in range(n):
        current_val = input_list[i]

        if current_val == 0:
            # If current value is 0, output 0 and reset the in_block flag
            output_list[i] = 0
            in_block = False
        elif current_val == 3:
            # If current value is 3
            if not in_block:
                # If this is the start of a new block
                in_block = True      # Set the flag
                block_counter += 1   # Increment the block counter
            
            # Determine the output value based on the block counter
            if block_counter == 1:
                output_list[i] = 1
            elif block_counter == 2:
                output_list[i] = 2
            # else: # Handle potential future cases with more blocks if needed
            #     output_list[i] = block_counter # Or some other logic

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    
    return output_str
