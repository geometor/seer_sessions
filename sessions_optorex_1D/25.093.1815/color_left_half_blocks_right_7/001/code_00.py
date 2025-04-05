import math

"""
Transforms a sequence of digits (0s and 2s) based on contiguous blocks of the digit 2.
For each contiguous block of k twos, the first floor(k / 2) twos are changed to 8,
while the remaining twos stay as 2. Zeros remain unchanged.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated digits (0s and 2s).

    Returns:
        A string containing the transformed space-separated digits.
    """
    # Parse the input string into a list of integers
    try:
        input_list = [int(digit) for digit in input_str.split()]
    except ValueError:
        # Handle cases where input might not be purely digits or space-separated
        print("Warning: Input string contains non-integer values or incorrect formatting.")
        # Attempt to filter, or return input as is, or raise an error depending on desired robustness
        input_list = [int(digit) for digit in input_str.split() if digit.isdigit()]
        if not input_list and len(input_str.split()) > 0 : # If filtering removed everything but there was content
             raise ValueError("Input string could not be parsed into a list of integers.")


    output_list = list(input_list)  # Create a mutable copy for the output
    n = len(input_list)
    i = 0

    # Iterate through the list to find blocks of 2s
    while i < n:
        if input_list[i] == 2:
            # Found the start of a potential block of 2s
            start_index = i
            # Find the end of the block
            while i < n and input_list[i] == 2:
                i += 1
            end_index = i  # end_index is the index *after* the last 2 in the block
            
            # Calculate block properties
            block_length = end_index - start_index
            num_to_change = block_length // 2  # Integer division equivalent to floor(k/2)

            # Apply the transformation to the output list for this block
            for j in range(start_index, start_index + num_to_change):
                output_list[j] = 8
            
            # The loop variable 'i' is already positioned at the end of the block or beyond
            # Continue the outer loop from the current 'i'
        else:
            # If the current element is not 2, just move to the next element
            i += 1

    # Format the output list back into a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
