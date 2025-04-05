import math
import numpy as np
import re # Using re for potentially parsing complex string inputs if needed, although simple split is fine here.

"""
Transformation Rule Natural Language Description:

1. Initialize the output sequence as a copy of the input sequence.
2. Identify the 'key digit' by taking the value of the first element in the input sequence.
3. Iterate through the input sequence from the 4th element (index 3) to the 12th element (index 11).
4. For each element at index `i` in the *original input sequence*:
   a. Check if the element is equal to the 'key digit'.
   b. If it is equal, modify the *output sequence* by setting the elements at indices `i-1`, `i`, and `i+1` to the 'key digit'.
5. Return the modified output sequence, formatted as a space-separated string.
"""

# No external library imports seem necessary beyond standard types and potentially numpy if array operations were more complex.

def parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.strip().split()]

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Finds the key digit (first digit) and replaces triplets in the sequence
    centered around occurrences of the key digit (after the initial three positions)
    with the key digit itself.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)
    
    # Initialize the output_list as a copy of the input list
    # Modifications will be made to this list
    output_list = list(input_list) 
    
    # Check if the input list is long enough (at least 3 elements for key digit)
    if len(input_list) < 3:
        # Or handle error appropriately, returning input for now if too short
        return format_output(output_list) 
        
    # Identify the 'key digit' from the first element
    key_digit = input_list[0]
    
    # Iterate through the *original* input_list from index 3 up to index 11 (inclusive)
    # We need to check indices i-1 and i+1, so the loop should technically go up to len-2
    # But the rule specifies checking input[i], so let's iterate i from 3 to len(input_list) - 1
    # The replacement affects i-1, i, i+1. We must ensure these indices are valid.
    # Given the examples, the key_digit seems to appear such that i-1 >= 0 and i+1 < len(input_list).
    # The rule description says "from the 4th element (index 3) to the 12th element (index 11)".
    # If i=11, i+1=12 is out of bounds for a 12-element list (indices 0-11).
    # Let's strictly follow the examples and assume the key digit won't appear at index 11.
    # The loop range should be from index 3 up to index 10 to allow i+1 to be valid (index 11).
    # However, the description says "up to 12th element (index 11)". Let's re-read the examples carefully.
    # Example 4: 9 at index 9. Modifies 8, 9, 10.
    # Example 6: 2 at index 9. Modifies 8, 9, 10.
    # It seems the latest index where the key digit is found is 9.
    # Let's iterate i from 3 up to len(input_list) - 1 = 11.
    
    list_len = len(input_list)
    indices_to_modify = [] # Store indices 'i' where key_digit is found in original input

    for i in range(3, list_len):
        # Check if the element in the *original* input list matches the key digit
        if input_list[i] == key_digit:
             # Check if the replacement indices are valid. 
             # We need i-1, i, and i+1 to be valid indices (0 to list_len-1)
             if i - 1 >= 0 and i + 1 < list_len:
                 indices_to_modify.append(i) # Record the index i where the trigger occurred

    # Apply the modifications to the output_list based on the found indices
    # This ensures modifications don't interfere with finding other triggers in the original input
    for i in indices_to_modify:
        # Modify the *output* sequence at indices i-1, i, and i+1
        output_list[i - 1] = key_digit
        output_list[i] = key_digit
        output_list[i + 1] = key_digit
            
    # Format the final output list back into a string
    return format_output(output_list)
