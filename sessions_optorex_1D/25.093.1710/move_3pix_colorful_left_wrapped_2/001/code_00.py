import collections

"""
Takes an input sequence of 12 integers, splits it into the first 3 elements and the remaining 9 elements, and constructs the output sequence by concatenating the 9-element part followed by the 3-element part. This effectively performs a left rotation of the sequence by 3 positions.
"""

def transform(input_str: str) -> str:
    """
    Performs a left rotation by 3 positions on a sequence of 12 integers.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing the transformed sequence of 12 space-separated integers.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(x) for x in input_str.split()]

    # Check if the input sequence has the expected length (optional but good practice)
    if len(input_sequence) != 12:
        raise ValueError("Input sequence must contain exactly 12 integers.")

    # Identify the first 3 elements
    first_part = input_sequence[:3]

    # Identify the remaining 9 elements (from index 3 onwards)
    second_part = input_sequence[3:]

    # Construct the output sequence by concatenating the second part followed by the first part
    output_sequence = second_part + first_part

    # Convert the elements of the output sequence back to strings
    output_str_list = [str(x) for x in output_sequence]

    # Join the string elements with spaces to form the final output string
    output_str = " ".join(output_str_list)

    return output_str
