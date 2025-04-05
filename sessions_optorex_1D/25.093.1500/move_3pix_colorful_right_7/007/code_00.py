"""
Transforms an input sequence (NumPy array) of 12 integers by taking the first 9 elements,
prepending them with 3 zeros, and returning the result as a space-separated string.
The last 3 elements of the original input are discarded.
"""

import numpy as np

# Constants derived from observations
SEQUENCE_LENGTH = 12
SHIFT_AMOUNT = 3
PADDING_VALUE = 0
ELEMENTS_TO_KEEP = SEQUENCE_LENGTH - SHIFT_AMOUNT # 9

def format_output_list(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_sequence: np.ndarray) -> str:
    """
    Applies the right-shift transformation to the input NumPy array.

    Args:
        input_sequence: A NumPy array containing 12 integers.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """

    # 1. Convert the input NumPy array to a standard Python list.
    #    This facilitates standard list slicing and concatenation.
    input_list = input_sequence.tolist()

    # Optional: Validate input length for robustness, although examples suggest it's always 12.
    if len(input_list) != SEQUENCE_LENGTH:
        # Log a warning or raise an error if the length is unexpected.
        # Based on prior error analysis, we expect length 12.
        # Raising an error might be appropriate if deviation indicates a problem.
        raise ValueError(f"Input sequence length is {len(input_list)}, expected {SEQUENCE_LENGTH}")

    # 2. Select the first 'ELEMENTS_TO_KEEP' elements from the input list.
    #    These are the elements that will be shifted right.
    truncated_input_sequence = input_list[:ELEMENTS_TO_KEEP] # Gets elements 0 through 8

    # 3. Create a padding list consisting of 'SHIFT_AMOUNT' zeros.
    #    This list will be placed at the beginning of the output.
    padding_sequence = [PADDING_VALUE] * SHIFT_AMOUNT # Creates [0, 0, 0]

    # 4. Construct the final output list by concatenating the padding sequence
    #    followed by the truncated input sequence.
    output_sequence = padding_sequence + truncated_input_sequence

    # 5. Format the resulting list of integers into a single string
    #    with elements separated by spaces.
    output_str = format_output_list(output_sequence)

    # 6. Return the formatted output string.
    return output_str