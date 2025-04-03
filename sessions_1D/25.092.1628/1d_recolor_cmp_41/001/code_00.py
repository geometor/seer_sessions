import copy

"""
Identifies all contiguous sequences of green pixels (value 3) in the input 1D array. 
Determines the maximum length among these sequences. 
Selects the first sequence encountered that has this maximum length. 
Changes the color of all pixels within this selected sequence from green (3) to red (2) in the output array.
All other pixels retain their original color.
"""

def find_sequences(data, target_value):
    """
    Finds all contiguous sequences of a target value in a 1D list.

    Args:
        data (list): The input 1D list of values.
        target_value: The value to search for sequences of.

    Returns:
        list: A list of tuples, where each tuple is (start_index, length)
              representing a sequence found. Returns an empty list if no
              sequences are found.
    """
    sequences = []
    in_sequence = False
    start_index = -1
    current_length = 0

    for i, value in enumerate(data):
        if value == target_value:
            if not in_sequence:
                # Start of a new sequence
                in_sequence = True
                start_index = i
                current_length = 1
            else:
                # Continue existing sequence
                current_length += 1
        else:
            if in_sequence:
                # End of the current sequence
                sequences.append((start_index, current_length))
                in_sequence = False
                start_index = -1
                current_length = 0

    # Check if the list ends with a sequence
    if in_sequence:
        sequences.append((start_index, current_length))

    return sequences

def transform(input_grid):
    """
    Transforms the input grid by finding the longest contiguous sequence of 
    green pixels (3) and changing them to red pixels (2). If multiple 
    sequences have the same maximum length, the first one encountered is chosen.

    Args:
        input_grid (list): A 1D list representing the input grid pixels.

    Returns:
        list: A 1D list representing the transformed output grid pixels.
    """
    
    # Find all sequences of green (3) pixels
    green_sequences = find_sequences(input_grid, 3)

    # If no green sequences are found, return the input grid unchanged
    if not green_sequences:
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original

    # Find the maximum length among the found sequences
    max_length = 0
    for _, length in green_sequences:
        if length > max_length:
            max_length = length

    # Find the first sequence that has the maximum length
    longest_sequence_info = None
    for start, length in green_sequences:
        if length == max_length:
            longest_sequence_info = (start, length)
            break # Stop after finding the first one

    # Create a copy of the input grid to modify
    output_grid = copy.deepcopy(input_grid)

    # If a longest sequence was identified (should always be true if green_sequences wasn't empty)
    if longest_sequence_info:
        start_index, length = longest_sequence_info
        # Change the pixels in the identified sequence to red (2)
        for i in range(start_index, start_index + length):
            output_grid[i] = 2

    return output_grid
