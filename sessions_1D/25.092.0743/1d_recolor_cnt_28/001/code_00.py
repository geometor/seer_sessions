import numpy as np

"""
Identify contiguous horizontal sequences of blue (1) pixels in the input grid (which is effectively a 1D array).
Replace each blue sequence with a sequence of the same length, using a new color determined by the length of the original blue sequence:
- Length 1 blue sequence becomes maroon (9).
- Length 2 blue sequence becomes azure (8).
- Length 3 blue sequence becomes yellow (4).
White (0) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the length of contiguous blue (1) sequences.

    Args:
        input_grid (list of lists): A 2D list representing the input grid,
                                     expected to be 1xN.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Create a copy to modify, preserving original white pixels
    output_array = input_array.copy()
    
    # Get dimensions (assuming it's effectively 1D, so shape[0] is 1)
    rows, cols = input_array.shape
    if rows != 1:
        # This specific logic assumes a 1xN grid based on examples
        # Handle potential other cases or raise an error if necessary
        print(f"Warning: Expected a 1xN grid, got {rows}x{cols}. Processing only the first row.")

    # Define the mapping from sequence length to replacement color
    length_to_color = {
        1: 9,  # maroon
        2: 8,  # azure
        3: 4   # yellow
    }

    # --- Process the first (and assumed only) row ---
    row_index = 0 
    current_sequence_start = -1
    current_sequence_length = 0

    # Iterate through columns to find sequences
    for col_index in range(cols):
        pixel_value = input_array[row_index, col_index]

        if pixel_value == 1:  # Found a blue pixel
            if current_sequence_start == -1:
                # Start of a new blue sequence
                current_sequence_start = col_index
                current_sequence_length = 1
            else:
                # Continue the existing blue sequence
                current_sequence_length += 1
        else:  # Found a white pixel (or any non-blue pixel)
            if current_sequence_start != -1:
                # End of a blue sequence detected, process it
                if current_sequence_length in length_to_color:
                    replacement_color = length_to_color[current_sequence_length]
                    # Replace the sequence in the output array
                    output_array[row_index, current_sequence_start:col_index] = replacement_color
                # else: If length is not in the map, the original blue pixels remain (though based on examples, this shouldn't happen)
                
                # Reset sequence tracking
                current_sequence_start = -1
                current_sequence_length = 0
            # If it was a white pixel and not ending a sequence, do nothing (already copied)

    # After the loop, check if a sequence was ongoing until the end of the grid
    if current_sequence_start != -1:
        if current_sequence_length in length_to_color:
            replacement_color = length_to_color[current_sequence_length]
            # Replace the sequence in the output array up to the end
            output_array[row_index, current_sequence_start:cols] = replacement_color
        # Reset sequence tracking (optional here, as loop is done)
        # current_sequence_start = -1
        # current_sequence_length = 0
            
    # Convert the final NumPy array back to a list of lists for the standard ARC format
    return output_array.tolist()