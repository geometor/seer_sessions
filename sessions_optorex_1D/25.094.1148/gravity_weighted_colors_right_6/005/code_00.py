import math
import numpy as np
# from skimage import measure # example - can uncomment if needed

"""
Transforms an input string, which represents a sequence of digits (0, 1, 2) potentially enclosed in brackets and separated by spaces (e.g., "[0 0 2 ... 1]"), by sorting these digits in descending numerical order (2 > 1 > 0) and formatting the result as a space-separated string.
"""

def transform(input_str: str) -> str:
    """
    Parses an input string representing a sequence of digits, sorts these digits
    in descending order, and returns them as a space-separated string.

    Args:
        input_str: A string potentially like "[0 0 2 ... 1]" containing
                   space-separated digits 0, 1, or 2.

    Returns:
        A string containing the same digits sorted in descending order,
        separated by spaces.
    """

    # 1. Preprocess the input string: Remove leading/trailing whitespace
    #    and the enclosing square brackets (`[` and `]`) if present.
    cleaned_str = input_str.strip(' []')

    # 2. Split the processed string by spaces to obtain a list of strings.
    #    Filter out empty strings resulting from multiple spaces.
    digit_strings = [s for s in cleaned_str.split(' ') if s]

    # 3. Convert this list of digit strings into a list of actual integers.
    try:
        digits = [int(d) for d in digit_strings]
    except ValueError as e:
        # Handle cases where conversion might fail unexpectedly
        print(f"Error converting digits from string: '{input_str}' -> '{cleaned_str}' -> {digit_strings}")
        raise e # Re-raise the error after printing context

    # 4. Sort the list of integers in descending numerical order.
    digits.sort(reverse=True)

    # 5. Convert the sorted integers back into a list of strings.
    sorted_digit_strings = [str(d) for d in digits]

    # 6. Join the elements of the sorted list of strings using a single space
    #    as a separator.
    output_str = ' '.join(sorted_digit_strings)

    # 7. Output the resulting space-separated string.
    return output_str
