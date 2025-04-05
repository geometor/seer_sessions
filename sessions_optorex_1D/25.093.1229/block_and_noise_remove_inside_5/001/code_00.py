"""
Transforms an input sequence of integers based on the following rules:
1. Identify all non-zero numbers in the input sequence.
2. Find the non-zero number that appears most frequently (the dominant_non_zero_number).
3. Create an output sequence of the same length as the input.
4. Iterate through the input sequence:
    a. If an element is 0, place 0 in the corresponding position in the output.
    b. If an element is non-zero, place the dominant_non_zero_number in the corresponding position in the output.
5. Return the output sequence.
"""

from collections import Counter
import numpy as np # Although not strictly necessary for list operations, might be useful for array handling if input format changes.

def find_dominant_non_zero(sequence):
    """
    Finds the most frequent non-zero number in a sequence.
    Returns None if no non-zero numbers are present.
    """
    # Filter out zero elements
    non_zeros = [num for num in sequence if num != 0]

    # If no non-zero numbers, return None
    if not non_zeros:
        return None

    # Count occurrences of each non-zero number
    counts = Counter(non_zeros)

    # Find the number with the highest frequency
    # most_common(1) returns a list like [(element, count)]
    dominant_non_zero_number = counts.most_common(1)[0][0]
    return dominant_non_zero_number

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.
    Replaces non-zero elements with the most frequent non-zero element,
    keeping zero elements as they are.
    """
    # Convert space-separated string input to list of integers
    # Assuming input might be string like examples, otherwise adjust if it's already a list
    if isinstance(input_sequence, str):
        input_list = [int(x) for x in input_sequence.split()]
    else:
        # Assume input is already a list-like structure of numbers
        input_list = list(input_sequence) 
        
    # Find the dominant non-zero number in the input list
    dominant_num = find_dominant_non_zero(input_list)

    # Initialize the output list with the same length
    output_list = [0] * len(input_list) # Pre-fill with 0, though it will be overwritten

    # Iterate through the input list and build the output list
    for i, element in enumerate(input_list):
        # If the element is 0, keep it as 0 in the output
        if element == 0:
            output_list[i] = 0
        # If the element is non-zero, replace it with the dominant non-zero number
        # Handle the case where there might be no non-zero numbers (dominant_num is None)
        elif dominant_num is not None:
             output_list[i] = dominant_num
        else:
             # This case implies the element is non-zero, but dominant_num is None.
             # This should not happen if there's at least one non-zero element.
             # If the input was all zeros, dominant_num is None, and this branch isn't reached.
             # If the input had non-zeros, dominant_num is not None.
             # As a fallback, maybe keep the original non-zero? Or raise error?
             # Based on logic, if element != 0, dominant_num must exist.
             # Let's stick to the rule: if non-zero, replace with dominant.
             # If dominant_num was None (all zeros input), this branch is never hit.
             pass # Should already be handled by the elif dominant_num is not None condition.

    # Convert back to space-separated string if needed to match output format, otherwise return list
    # Assuming the desired output format is like the examples (string)
    output_string = " ".join(map(str, output_list))
    return output_string

    # If a list output is desired instead:
    # return output_list
