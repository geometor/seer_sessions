"""
Transforms an input 1D sequence (list or NumPy array) of 12 integers by 
shifting all non-zero elements (objects) 4 positions to the right 
(increasing index). The relative order of the objects is preserved. 
Objects shifted beyond the end of the list (index 11) are discarded. 
Original positions of shifted objects, and any positions not filled by a 
shifted object, become zero in the output list. The input might be 
provided as a nested list or 2D NumPy array representing a single row, 
so it should be flattened or the first row selected. The output is returned
as a standard Python list of integers.
"""

import numpy as np

def find_objects(sequence_1d):
    """
    Finds the indices and values of non-zero elements in a 1D sequence.

    Args:
        sequence_1d: A 1D NumPy array or list.

    Returns:
        A tuple containing:
          - indices: A list of indices where elements are non-zero.
          - values: A list of the non-zero values corresponding to the indices.
    """
    arr = np.array(sequence_1d) # Ensure it's a NumPy array
    indices = np.where(arr != 0)[0]
    values = arr[indices]
    return indices.tolist(), values.tolist()

def shift_objects(indices, values, shift_amount, sequence_length):
    """
    Calculates the new positions for objects after shifting and filters invalid ones.

    Args:
        indices: List of original indices of the objects.
        values: List of values of the objects.
        shift_amount: The amount to shift indices (positive for right).
        sequence_length: The total length of the sequence.

    Returns:
        A tuple containing:
         - valid_new_indices: List of new indices within bounds.
         - valid_values: List of values corresponding to the valid new indices.
    """
    valid_new_indices = []
    valid_values = []
    for i, index in enumerate(indices):
        new_index = index + shift_amount
        if 0 <= new_index < sequence_length:
            valid_new_indices.append(new_index)
            valid_values.append(values[i])
    return valid_new_indices, valid_values

def transform(input_grid):
    """
    Applies the right shift transformation to the input grid.

    Args:
        input_grid: A list or NumPy array representing the 1D sequence, 
                    potentially nested (e.g., [[0, 0, 8, ...]]).

    Returns:
        A list of integers representing the transformed sequence.
    """
    # Ensure input is a 1D NumPy array
    # Flatten handles lists, 1D arrays, and [[...]] style 2D arrays correctly
    input_1d = np.array(input_grid).flatten()
    
    # Get the length of the sequence
    grid_length = len(input_1d)

    # Initialize the output grid as a list of zeros
    # Using a list directly as the final output format is list[int]
    output_grid = [0] * grid_length

    # Find the non-zero objects (values and their original positions)
    original_indices, object_values = find_objects(input_1d)

    # Define the shift amount
    shift_amount = 4

    # Calculate the new positions for the objects, filtering those shifted out of bounds
    new_indices, valid_object_values = shift_objects(original_indices, object_values, shift_amount, grid_length)

    # Place the valid objects into their new positions in the output grid
    for i, new_index in enumerate(new_indices):
        output_grid[new_index] = valid_object_values[i]

    # Return the transformed grid as a list
    return output_grid