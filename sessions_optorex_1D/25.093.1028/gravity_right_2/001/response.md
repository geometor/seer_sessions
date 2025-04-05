```python
import re # used for splitting the string and converting to int

"""
Transforms an input sequence of integers by moving all zero elements to the beginning 
while preserving the relative order of the non-zero elements. The input and output 
are space-separated strings of integers.
"""

def transform(input_str: str) -> str:
    """
    Moves all zeros in a sequence of space-separated integers to the front,
    preserving the relative order of non-zero elements.

    Args:
        input_str: A string containing space-separated integers.

    Returns:
        A string containing the transformed sequence, with zeros moved to the
        front and non-zeros following in their original relative order,
        also space-separated.
    """

    # Parse the input string into a list of integers
    # Use list comprehension for conciseness
    input_list = [int(num) for num in input_str.split()]

    # Initialize two lists to hold zeros and non-zeros
    zeros = []
    non_zeros = []

    # Iterate through the input list and partition elements
    for num in input_list:
        if num == 0:
            # If the number is 0, add it to the zeros list
            zeros.append(num)
        else:
            # If the number is not 0, add it to the non_zeros list
            non_zeros.append(num)

    # Concatenate the zeros list followed by the non_zeros list
    output_list = zeros + non_zeros

    # Convert the integers in the output list back to strings
    # Use list comprehension again
    output_str_list = [str(num) for num in output_list]

    # Join the string elements with spaces to form the final output string
    output_str = " ".join(output_str_list)

    # Return the transformed string
    return output_str

```