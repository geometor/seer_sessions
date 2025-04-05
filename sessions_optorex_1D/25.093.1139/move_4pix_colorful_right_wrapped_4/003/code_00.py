"""
Rearrange a sequence of 12 numerical elements from a NumPy array by moving the last 4 elements to the beginning, preserving relative order, and return the result as a space-separated string.
"""

import numpy as np

def format_output(output_array: np.ndarray) -> str:
    """Formats a numpy array of numbers into a space-separated string."""
    # Convert each element to string and join with spaces
    return ' '.join(map(str, output_array))

def transform(input_grid: np.ndarray) -> str:
    """
    Transforms a 1D NumPy array of 12 elements by moving the last 4 elements
    to the front.

    Args:
        input_grid: A 1D NumPy array containing 12 numerical elements.

    Returns:
        A string representing the transformed sequence of elements, 
        separated by spaces.
    """
    # Define sequence and block parameters based on observations
    sequence_length = 12
    block_size_to_move = 4
    
    # Ensure input is treated as a 1D array if it comes in other shapes (e.g., (1, 12))
    # This handles potential variations in how the environment might pass the array
    if input_grid.ndim > 1:
        input_array = input_grid.flatten()
    else:
        input_array = input_grid
        
    # Validate input length (optional, but good practice)
    # if len(input_array) != sequence_length:
    #     raise ValueError(f"Input array must have exactly {sequence_length} elements.")

    # 1. Identify the last 4 elements (Part B)
    part_b_start_index = sequence_length - block_size_to_move
    part_b = input_array[part_b_start_index:] # Elements from index 8 to the end

    # 2. Identify the first 8 elements (Part A)
    part_a = input_array[:part_b_start_index] # Elements from index 0 to 7

    # 3. Construct the new NumPy array by concatenating Part B followed by Part A.
    output_array = np.concatenate((part_b, part_a))

    # 4. Convert the resulting array to a space-separated string format.
    output_str = format_output(output_array)

    return output_str