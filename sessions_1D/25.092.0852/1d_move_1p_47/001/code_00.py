import numpy as np # although not strictly needed for lists, good practice for ARC

"""
Identify the contiguous block of non-white pixels in the input sequence. 
Locate the first white pixel (value 0) that immediately follows this non-white block.
Remove this white pixel from its current position.
Insert the removed white pixel into the sequence at the original start index of the non-white block.
"""

def find_non_white_block(sequence):
    """
    Finds the start and end indices of the first contiguous block of non-white pixels.
    Returns (start_index, end_index) or (None, None) if not found.
    """
    start_index = -1
    end_index = -1
    in_block = False
    for i, pixel in enumerate(sequence):
        if pixel != 0 and not in_block:
            start_index = i
            in_block = True
        elif pixel == 0 and in_block:
            end_index = i - 1
            break
        elif i == len(sequence) - 1 and in_block: # Handle block ending at the sequence end
             end_index = i

    if start_index != -1 and end_index == -1: # Block found but goes to the end
        end_index = len(sequence) - 1

    if start_index == -1: # No non-white pixel found at all
        return None, None

    return start_index, end_index


def transform(input_sequence: list[int]) -> list[int]:
    """
    Transforms the input sequence by moving the first white pixel after the 
    non-white block to the position just before the non-white block.

    Args:
        input_sequence: A list of integers representing pixel colors.

    Returns:
        A new list with the transformation applied.
    """

    # Find the contiguous block of non-white pixels
    start_index, end_index = find_non_white_block(input_sequence)

    # If no block is found, or the block spans the entire sequence, return the original
    if start_index is None:
        return list(input_sequence) # Return a copy

    # Identify the index of the white pixel to move
    # It's the one immediately after the block ends
    source_index = end_index + 1

    # Check if the source index is valid and points to a white pixel
    if source_index >= len(input_sequence) or input_sequence[source_index] != 0:
        # This case shouldn't happen based on examples, but handle defensively
        # It means there's no white pixel immediately after the block
        return list(input_sequence) # Return a copy

    # Identify the destination index (where the white pixel will be inserted)
    # This is the start index of the non-white block
    destination_index = start_index

    # Create a mutable copy of the input sequence
    output_sequence = list(input_sequence)

    # Remove the white pixel from its source position
    # We don't need the value, we know it's 0
    output_sequence.pop(source_index)

    # Insert the white pixel (value 0) at the destination position
    output_sequence.insert(destination_index, 0)

    # Return the modified sequence
    return output_sequence