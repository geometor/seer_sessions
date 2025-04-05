```python
"""
Transforms an input sequence of 12 digits, provided as a space-separated string,
by shifting the first 9 digits 3 positions to the right and prepending three '0' digits.
The last 3 digits of the original input are discarded. The output is returned as a
space-separated string.
"""

import numpy as np # numpy is often available and might be useful for array ops if needed later

# Constants derived from observations
SEQUENCE_LENGTH = 12
SHIFT_AMOUNT = 3
PADDING_VALUE = 0

def parse_input_string(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    try:
        return [int(x) for x in input_str.strip().split()]
    except ValueError as e:
        # Provide more context if parsing fails
        raise ValueError(f"Failed to parse input string: '{input_str}'. Error: {e}") from e

def format_output_list(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the right-shift transformation to the input sequence string.
    
    Args:
        input_str: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """

    # 1. Parse the input string into a list of 12 integers (the `input_sequence`).
    input_sequence = parse_input_string(input_str)

    # Optional: Validate input length, though examples suggest it's always 12.
    if len(input_sequence) != SEQUENCE_LENGTH:
        # This case might indicate an unexpected input format based on the problem description.
        # Depending on requirements, could raise an error or attempt to handle gracefully.
        # For now, let's raise an error as it deviates from the observed pattern.
        raise ValueError(f"Input sequence length is {len(input_sequence)}, expected {SEQUENCE_LENGTH}")

    # 2. Determine the number of elements to keep from the start of the `input_sequence`.
    #    This is sequence_length - shift_amount.
    elements_to_keep_count = SEQUENCE_LENGTH - SHIFT_AMOUNT # 12 - 3 = 9

    # 3. Select the first 'elements_to_keep_count' elements from the `input_sequence`.
    truncated_input_sequence = input_sequence[:elements_to_keep_count]

    # 4. Create a `padding_sequence` consisting of 'SHIFT_AMOUNT' zeros.
    padding_sequence = [PADDING_VALUE] * SHIFT_AMOUNT # [0, 0, 0]

    # 5. Construct the `output_sequence` by concatenating the `padding_sequence`
    #    followed by the `truncated_input_sequence`.
    output_sequence = padding_sequence + truncated_input_sequence

    # Ensure the final output has the correct length (should already be correct if input was valid)
    # This check is mostly for robustness against potential logic errors above.
    if len(output_sequence) != SEQUENCE_LENGTH:
         # This indicates an internal logic error, as concatenation should yield the correct length.
         raise RuntimeError(f"Internal error: Output sequence length is {len(output_sequence)}, expected {SEQUENCE_LENGTH}")
         
    # 6. Format the `output_sequence` back into a single string with elements separated by spaces.
    output_str = format_output_list(output_sequence)

    # 7. Return the formatted output string.
    return output_str

```