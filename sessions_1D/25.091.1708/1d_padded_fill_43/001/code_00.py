import copy

"""
Identifies the unique non-white color C in the input sequence. Finds the index of the first occurrence (start_index) and the last occurrence (end_index) of C. Creates an output sequence by copying the input, then filling the segment from start_index to end_index (inclusive) with color C.
"""

def find_non_white_span(sequence):
    """
    Finds the non-white color, its first index, and its last index.

    Args:
        sequence (list): The input sequence of color values.

    Returns:
        tuple: (non_white_color, start_index, end_index)
               Returns (None, -1, -1) if no non-white color is found.
    """
    non_white_color = None
    start_index = -1
    end_index = -1

    for i, val in enumerate(sequence):
        if val != 0:  # Found a non-white pixel
            if non_white_color is None:
                non_white_color = val  # Store the first non-white color found
            # Ensure we only deal with one non-white color as per assumption
            # In a more robust version, we might handle multiple colors differently
            if val == non_white_color:
                if start_index == -1:
                    start_index = i  # Record the first occurrence index
                end_index = i  # Update the last occurrence index

    return non_white_color, start_index, end_index

def transform(input_sequence):
    """
    Transforms the input sequence by finding the first and last non-white pixel
    of a specific color and filling the space between them (inclusive) with that color.

    Args:
        input_sequence (list): A list of integers representing colors.

    Returns:
        list: The transformed sequence.
    """
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence) # Use list() for a shallow copy

    # Find the non-white color and its span
    non_white_color, start_index, end_index = find_non_white_span(input_sequence)

    # If a non-white color and its span were found
    if non_white_color is not None and start_index != -1:
        # Iterate through the indices from start_index to end_index (inclusive)
        for i in range(start_index, end_index + 1):
            # Set the color of the pixel at index i in the output sequence to the non-white color
            output_sequence[i] = non_white_color

    # Return the modified output sequence
    return output_sequence