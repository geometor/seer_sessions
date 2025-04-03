"""
Transforms the input grid by finding the single longest contiguous sequence of 
green pixels (3) in the flattened representation of the grid (read row-by-row). 
Changes the pixels in this specific sequence to red (2). If multiple sequences 
share the same maximum length, the one that appears earliest (lowest starting 
index in the flattened sequence) is chosen. The output grid retains the original 
dimensions.
"""

import numpy as np

def find_sequences_1d(data_1d, target_value):
    """
    Finds all contiguous sequences of a target value in a 1D numpy array.

    Args:
        data_1d (np.ndarray): The input 1D numpy array.
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

    for i, value in enumerate(data_1d):
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
                # Reset sequence tracking
                # start_index = -1 # Not strictly necessary to reset here
                # current_length = 0 # Not strictly necessary to reset here
            # Reset state regardless if value != target_value
            in_sequence = False

    # Check if the array ends with a sequence
    if in_sequence:
        sequences.append((start_index, current_length))

    return sequences

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    
    # Record the original shape of the input grid
    original_shape = input_grid.shape
    
    # Flatten the 2D input grid into a 1D array (row-major order by default)
    input_flat = input_grid.flatten()
    
    # Define the target (green) and replacement (red) colors
    target_color = 3
    replacement_color = 2
    
    # Find all contiguous sequences of the target color (green) in the flattened array
    green_sequences = find_sequences_1d(input_flat, target_color)

    # If no green sequences are found, return the input grid unchanged
    if not green_sequences:
        # Return a copy to ensure the original input isn't modified if it's passed around elsewhere
        return np.copy(input_grid) 

    # Find the maximum length among the found green sequences
    max_length = 0
    for _, length in green_sequences:
        if length > max_length:
            max_length = length
            
    # It's possible no sequence was found if max_length remained 0, handle this edge case
    # (although already handled by the `if not green_sequences` check earlier)
    if max_length == 0:
         return np.copy(input_grid)

    # Find the first sequence (earliest start index) that has the maximum length
    longest_sequence_start = -1
    longest_sequence_length = -1
    for start, length in green_sequences:
        if length == max_length:
            longest_sequence_start = start
            longest_sequence_length = length
            break # Stop after finding the first one with max length

    # Create a copy of the flattened array to modify
    output_flat = np.copy(input_flat)

    # Modify the copied flattened array: change the selected sequence to the replacement color (red)
    # Check if a valid sequence was identified (start index should not be -1)
    if longest_sequence_start != -1:
        start_index = longest_sequence_start
        end_index = start_index + longest_sequence_length
        output_flat[start_index:end_index] = replacement_color

    # Reshape the modified 1D array back to the original 2D grid dimensions
    output_grid = output_flat.reshape(original_shape)

    return output_grid