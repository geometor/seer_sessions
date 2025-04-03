"""
Identifies all contiguous sequences of azure (8) pixels in the input list.
Determines the sequence with the maximum length. If multiple sequences share the maximum length, selects the one that appears latest (rightmost).
Changes the color of the pixels in this selected longest sequence from azure (8) to blue (1).
All other pixels remain unchanged.
"""

import numpy as np # Although not strictly necessary for lists, it's common in ARC tasks

def find_azure_sequences(data):
    """
    Finds all contiguous sequences of azure (8) in a 1D list.

    Args:
        data (list): The input list of pixel values.

    Returns:
        list: A list of dictionaries, each representing a sequence with
              'start', 'end', and 'length' keys. Returns an empty list
              if no azure sequences are found.
    """
    sequences = []
    in_sequence = False
    start_index = -1
    current_length = 0
    azure_color = 8

    for i, pixel in enumerate(data):
        if pixel == azure_color:
            if not in_sequence:
                # Start of a new sequence
                in_sequence = True
                start_index = i
                current_length = 1
            else:
                # Continue the current sequence
                current_length += 1
        else:
            if in_sequence:
                # End of the current sequence
                sequences.append({
                    'start': start_index,
                    'end': i - 1, # End index is inclusive
                    'length': current_length
                })
                in_sequence = False
                start_index = -1
                current_length = 0

    # Check if the list ended while in a sequence
    if in_sequence:
        sequences.append({
            'start': start_index,
            'end': len(data) - 1, # End index is inclusive
            'length': current_length
        })

    return sequences

def transform(input_grid):
    """
    Transforms the input list by changing the longest contiguous sequence
    of azure (8) pixels to blue (1). If there's a tie in length, the
    rightmost (latest occurring) sequence is chosen.

    Args:
        input_grid (list): A 1D list representing the input pixels.

    Returns:
        list: The transformed list.
    """
    # Find all contiguous sequences of azure (8)
    azure_sequences = find_azure_sequences(input_grid)

    # Initialize output_grid as a copy of the input
    # Using list() ensures it's a shallow copy, suitable for 1D lists of primitives
    output_grid = list(input_grid)

    # If no azure sequences were found, return the copy directly
    if not azure_sequences:
        return output_grid

    # Find the sequence with the maximum length
    # Handle ties by selecting the latest occurring one (which naturally happens
    # if we iterate and update whenever we find an equal or greater length)
    max_length = 0
    longest_sequence = None
    for seq in azure_sequences:
        # We choose the latest sequence in case of a tie
        if seq['length'] >= max_length:
            max_length = seq['length']
            longest_sequence = seq

    # If a longest sequence was determined (should always happen if azure_sequences is not empty)
    if longest_sequence:
        # Change the pixels in the selected sequence to blue (1) in the output grid
        start = longest_sequence['start']
        end = longest_sequence['end']
        blue_color = 1
        for i in range(start, end + 1):
            output_grid[i] = blue_color

    return output_grid
