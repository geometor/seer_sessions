import numpy as np

"""
Transforms a sequence of 0s and 1s based on the '1 1' pattern.

Specifically, iterates through the input sequence. If a consecutive '1 1' pattern 
is found starting at index i, it checks the elements immediately before (index i-1) 
and immediately after (index i+2) the pattern in the original input sequence. 
If the element before the pattern is '0', it's changed to '3' in the output. 
If the element after the pattern is '0', it's changed to '3' in the output. 
All other elements ('1's and '0's not adjacent to a '1 1' pattern) 
remain unchanged. Changes are based on the original input to prevent cascading effects.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A string containing space-separated 0s and 1s.

    Returns:
        A string containing the transformed sequence with space-separated digits.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize the output list as a copy of the input list
    # We modify this list based on conditions found in the input_list
    output_list = list(input_list)

    # Iterate through the input sequence to find '1 1' patterns
    # The loop goes up to n-2 because we need to check indices i and i+1
    for i in range(n - 1):
        # Check if the elements at index i and i+1 form the sequence '1 1'
        if input_list[i] == 1 and input_list[i+1] == 1:
            # Check the element *before* the '1 1' sequence (at index i-1)
            # Ensure the index i-1 is valid (i > 0)
            # Check the value in the *original* input_list
            if i > 0 and input_list[i-1] == 0:
                # Modify the element in the *output* list
                output_list[i-1] = 3

            # Check the element *after* the '1 1' sequence (at index i+2)
            # Ensure the index i+2 is valid (i+2 < n)
            # Check the value in the *original* input_list
            if i + 2 < n and input_list[i+2] == 0:
                # Modify the element in the *output* list
                output_list[i+2] = 3

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
