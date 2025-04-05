import numpy as np

"""
Transforms a 1x12 input grid by shifting all non-zero elements in its single 
row 4 positions to the right. Positions vacated by the shift and any new 
positions at the beginning of the row are filled with zeros. Elements shifted 
beyond the end of the row (index 11) are discarded. The output is a 1x12 
grid containing the transformed row.
"""

def transform(input_grid):
    """
    Applies a right shift transformation to the non-zero elements of the single 
    row within the input grid.

    Args:
        input_grid: A 1x12 grid-like structure (e.g., list of lists or 2D 
                    NumPy array) containing one row of 12 integers.

    Returns:
        A 1x12 NumPy array representing the transformed grid.
    """
    # --- Constants ---
    sequence_length = 12
    shift_amount = 4
    fill_value = 0

    # --- Input Processing ---
    # Ensure input is a NumPy array and extract the single row (1D array)
    # Handles both list of lists [[...]] and 2D NumPy array input.
    input_array_2d = np.array(input_grid)
    if input_array_2d.shape != (1, sequence_length):
        # Optional: Add more robust error handling or assumptions
        # For now, assume the input structure is correct if it can be converted
        # If conversion fails or shape is wrong, np.array might raise an error
        # or subsequent operations might fail.
        # Basic check:
        if input_array_2d.ndim == 1 and len(input_array_2d) == sequence_length:
             # If input was accidentally flattened [[1,2,3]] -> [1,2,3]
             input_array_2d = input_array_2d.reshape(1, sequence_length)
        elif input_array_2d.size == sequence_length:
             # If shape is different but total elements match (e.g., (12,1))
             input_array_2d = input_array_2d.reshape(1, sequence_length)
        else:
             raise ValueError(f"Input grid must be convertible to a 1x{sequence_length} array. Got shape {input_array_2d.shape}")


    data_row = input_array_2d[0] # Extract the first (and only) row

    # --- Transformation Logic ---
    # Initialize the output row with the fill value (zeros)
    # Ensure the dtype matches the input to handle different integer types if necessary
    output_row = np.full(sequence_length, fill_value, dtype=data_row.dtype)

    # Iterate through the elements of the extracted data_row
    for i in range(sequence_length):
        # Get the element at the current index
        element = data_row[i]

        # Check if the element is non-zero
        if element != fill_value:
            # Calculate the target index after shifting
            target_index = i + shift_amount

            # Check if the target index is within the bounds of the sequence (0 to 11)
            if 0 <= target_index < sequence_length:
                # Copy the non-zero element to the target position in the output row
                output_row[target_index] = element
            # Else (target_index is out of bounds): the element is discarded (do nothing)

    # --- Output Formatting ---
    # Reshape the 1D output_row back into a 1x12 grid format (2D NumPy array)
    output_grid = output_row.reshape(1, sequence_length)

    return output_grid