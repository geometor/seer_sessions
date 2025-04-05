import numpy as np

"""
Takes an input sequence (list) of 12 digits and shifts the first 8 digits
4 positions to the right, placing them starting at index 4 in the output sequence.
The first 4 positions of the output sequence are filled with zeros. The last 4
digits of the input sequence are effectively discarded.
"""

# No external libraries are strictly needed for this list manipulation,
# but numpy can be useful for array operations if the input/output were grids.
# For this specific task, standard list operations are sufficient.

def transform(input_sequence: list) -> list:
    """
    Shifts the first 8 elements of the input sequence 4 positions to the right.

    Args:
        input_sequence: A list of 12 integers.

    Returns:
        A new list of 12 integers representing the transformed sequence.
    """
    # Define the length of the sequence and the shift amount
    sequence_length = 12
    shift_amount = 4
    elements_to_copy = sequence_length - shift_amount # We copy the first 8 elements

    # Initialize the output sequence with zeros
    output_sequence = [0] * sequence_length

    # Copy the relevant elements from the input to the output sequence with the shift
    # Iterate through the indices of the elements to be copied from the input
    for i in range(elements_to_copy):
        # Check if the input index is within the bounds of the input sequence
        # (This is guaranteed by the loop range based on elements_to_copy)
        # Calculate the corresponding output index by adding the shift amount
        output_index = i + shift_amount
        # Assign the input element to the calculated output position
        output_sequence[output_index] = input_sequence[i]

    # Return the newly created and populated output sequence
    return output_sequence
