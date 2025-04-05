import re
from typing import List

"""
Transforms a sequence of 0s and 1s based on adjacency rules.
Specifically, a 0 is changed to a 3 if it is immediately preceded
by '1 1' OR immediately succeeded by '1 1'. Otherwise, the
sequence remains unchanged. The input and output are space-separated
strings of digits.
"""

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.

    Args:
        input_str: A space-separated string of 0s and 1s.

    Returns:
        A space-separated string representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # Iterate through each element of the input sequence
    for i in range(n):
        # Check if the current element is 0
        if input_list[i] == 0:
            # Check the preceding pair condition
            precedes_11 = False
            if i >= 2 and input_list[i-2] == 1 and input_list[i-1] == 1:
                precedes_11 = True

            # Check the succeeding pair condition
            succeeds_11 = False
            if i <= n - 3 and input_list[i+1] == 1 and input_list[i+2] == 1:
                succeeds_11 = True

            # If either condition is met, change the corresponding output element to 3
            if precedes_11 or succeeds_11:
                output_list[i] = 3

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))
    return output_str
