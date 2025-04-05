import re

"""
Takes an input sequence of digits (represented as a space-separated string), 
removes the first digit, and appends it to the end of the remaining sequence.
"""

# No external libraries needed for this transformation

def transform(input_str: str) -> str:
    """
    Performs a cyclic left shift on a sequence of space-separated digits.

    Args:
        input_str: A string containing space-separated digits.

    Returns:
        A string representing the transformed sequence with the first digit
        moved to the end.
    """

    # Split the input string into a list of digit strings
    # Example: "1 7 8" -> ["1", "7", "8"]
    digits = input_str.split()

    # Check if the list is empty or has only one element, return as is if so
    if len(digits) <= 1:
        return input_str

    # Get the first element
    first_element = digits[0]

    # Get the remaining elements (from the second element onwards)
    remaining_elements = digits[1:]

    # Append the first element to the end of the remaining elements
    # Example: ["7", "8"] + ["1"] -> ["7", "8", "1"]
    output_digits = remaining_elements + [first_element]

    # Join the elements of the new list back into a space-separated string
    # Example: ["7", "8", "1"] -> "7 8 1"
    output_str = " ".join(output_digits)

    return output_str
