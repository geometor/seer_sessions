import numpy as np

"""
Identify the two non-white pixels in the input row. Determine their color and 
their start and end indices. Fill the segment between these two indices 
(inclusive) in the output row with that color. Keep other pixels white.
"""

def transform(input_grid):
    """
    Transforms a 1D grid by filling the segment between two non-white pixels.

    Args:
        input_grid (list[list[int]]): A list containing a single list representing the input row.

    Returns:
        list[list[int]]: A list containing a single list representing the transformed row.
    """
    # Convert input grid (list of lists) to a NumPy array for easier manipulation
    # Since the input is described as 1D, we expect a shape like (1, width)
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure it's effectively 1D by taking the first row if shape is (1, width)
    if input_array.shape[0] == 1:
        row_array = input_array[0]
    else:
        # Handle cases where input might be truly 1D array already, though ARC standard is 2D
        # This case might need adjustment based on how inputs are precisely formatted
        # Assuming for now it adheres to the [[...]] structure.
        # If not, might raise an error or adapt based on expected input variations.
        # For now, let's stick to the assumption of shape (1, width) based on examples.
        raise ValueError("Input grid is not a single row as expected.")

    # Find the indices (column positions) of non-white (non-zero) pixels
    non_white_indices = np.where(row_array != 0)[0]

    # Check if we found exactly two non-white pixels, as expected by the pattern
    if len(non_white_indices) != 2:
        # If not exactly two, the pattern doesn't match.
        # Depending on requirements, could return input unchanged, raise error, or handle differently.
        # Based on the examples, we assume exactly two exist. Let's return the input copy for robustness.
        # print(f"Warning: Expected 2 non-white pixels, found {len(non_white_indices)}. Returning copy.")
        return input_grid # Return original if assumption fails

    # Get the color of the non-white pixels (they should be the same color)
    pixel_color = row_array[non_white_indices[0]]
    
    # Verify the two pixels have the same color (as per perceived pattern)
    if row_array[non_white_indices[1]] != pixel_color:
        # print(f"Warning: Non-white pixels have different colors. Returning copy.")
        return input_grid # Return original if assumption fails

    # Determine the start and end indices of the segment to fill
    start_index = np.min(non_white_indices)
    end_index = np.max(non_white_indices)

    # Create the output array as a copy of the input row array
    output_row_array = row_array.copy()

    # Fill the segment between start_index and end_index (inclusive) with the pixel_color
    output_row_array[start_index : end_index + 1] = pixel_color

    # Convert the modified row array back into the required list of lists format
    # Reshape back to (1, width) before converting to list
    output_grid = output_row_array.reshape(1, -1).tolist()

    return output_grid