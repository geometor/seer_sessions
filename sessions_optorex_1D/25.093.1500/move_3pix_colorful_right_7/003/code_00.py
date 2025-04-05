"""
Transforms an input sequence (list or array) of 12 integers by taking the first 9 elements 
and prepending them with 3 zeros, resulting in a new sequence of 12 integers. 
The last 3 elements of the original input are discarded. The final output is 
formatted as a space-separated string.
"""

import numpy as np # Keep numpy import as the error indicated it might be used by the environment

# Constants derived from observations
SEQUENCE_LENGTH = 12
SHIFT_AMOUNT = 3
PADDING_VALUE = 0

def format_output(output_list: list[int]) -> str:
    """Formats the list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_sequence) -> str:
    """
    Applies the right-shift transformation to the input sequence.

    1. Convert input (potentially NumPy array) to a standard Python list.
    2. Calculate the number of elements to keep from the input.
    3. Select the first 'elements_to_keep_count' elements from the input list.
    4. Create a padding list consisting of 'SHIFT_AMOUNT' zeros.
    5. Concatenate the padding list and the selected elements list.
    6. Format the resulting list into a space-separated string for output.
    """
    
    # 1. Convert input to a standard Python list to handle potential NumPy arrays
    #    or standard lists consistently.
    if isinstance(input_sequence, np.ndarray):
        input_list = input_sequence.tolist()
    elif isinstance(input_sequence, list):
        input_list = input_sequence
    else:
        # Attempt to handle other iterable types, or raise an error if incompatible
        try:
            input_list = list(input_sequence)
        except TypeError:
            raise TypeError(f"Input type {type(input_sequence)} is not convertible to a list.")

    # Validate input length (optional but good practice)
    if len(input_list) != SEQUENCE_LENGTH:
        # If the environment guarantees length 12, this might be unnecessary.
        # Keeping it for robustness based on initial analysis.
        print(f"Warning: Input sequence length is {len(input_list)}, expected {SEQUENCE_LENGTH}. Proceeding anyway.")
        # Or raise ValueError: raise ValueError(f"Input sequence must have length {SEQUENCE_LENGTH}")

    # 2. Calculate the number of elements to keep from the original input.
    elements_to_keep_count = SEQUENCE_LENGTH - SHIFT_AMOUNT
    
    # Handle cases where input might be shorter than expected after the warning
    actual_keep_count = min(elements_to_keep_count, len(input_list))

    # 3. Select the elements from the input list.
    kept_elements = input_list[:actual_keep_count]

    # 4. Create a padding list consisting of SHIFT_AMOUNT zeros.
    padding_list = [PADDING_VALUE] * SHIFT_AMOUNT

    # 5. Concatenate the padding list and the selected elements list.
    #    Ensure the total length respects SEQUENCE_LENGTH if input was shorter.
    output_list = (padding_list + kept_elements)[:SEQUENCE_LENGTH]
    
    # If the concatenation result is shorter than SEQUENCE_LENGTH (due to very short input),
    # pad with extra zeros at the end - though this scenario shouldn't occur based on examples.
    while len(output_list) < SEQUENCE_LENGTH:
         output_list.append(PADDING_VALUE)


    # 6. Format the output list back into a space-separated string.
    output_str = format_output(output_list)

    return output_str