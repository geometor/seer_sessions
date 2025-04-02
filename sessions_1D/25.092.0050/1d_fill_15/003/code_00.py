"""
Transforms a single-row input grid by filling the horizontal gap between two 
identical non-white pixels with their color.

1.  Verify the input grid has exactly one row.
2.  Extract the single row.
3.  Find the column indices and color of the two non-white pixels in the row.
4.  Verify exactly two non-white pixels of the same color exist.
5.  Determine the start and end column indices of the segment defined by these two pixels.
6.  Create a copy of the row.
7.  Fill the pixels in the copied row from the start to the end index (inclusive) with the identified color.
8.  Return the modified row wrapped in a list to form the 2D output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Fills the horizontal gap between two identical non-white pixels in a single-row grid.

    Args:
        input_grid (list of lists or numpy array): A grid representing the input, 
                                                    expected to have shape (1, N).

    Returns:
        list of lists: The transformed grid with the gap filled, or the original 
                       grid if the input conditions are not met.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # --- Verification Steps ---
    # 1. Verify the input grid has exactly one row.
    if input_array.shape[0] != 1:
        # Return input unchanged if it's not a single row grid
        return input_grid 

    # 2. Extract the single row.
    row = input_array[0]

    # 3. Find the column indices of all non-white pixels.
    non_white_indices = np.where(row != 0)[0]

    # 4. Verify exactly two non-white pixels were found.
    if len(non_white_indices) != 2:
        # Return input unchanged if not exactly two non-white pixels
        return input_grid

    # 5. Determine the color C and verify they are identical.
    idx1, idx2 = non_white_indices[0], non_white_indices[1]
    color1 = row[idx1]
    color2 = row[idx2]

    if color1 != color2:
        # Return input unchanged if the two non-white pixels have different colors
        return input_grid
    
    fill_color = color1 # Use the determined color for filling

    # --- Transformation Steps ---
    # 6. Determine the start and end column indices.
    col_start = min(idx1, idx2)
    col_end = max(idx1, idx2)

    # 7. Create a copy of the extracted row to serve as the output row.
    output_row = np.copy(row)

    # 8. Iterate through the column indices from col_start to col_end (inclusive) 
    #    and fill with the color.
    #    Using NumPy slicing for efficiency:
    output_row[col_start : col_end + 1] = fill_color

    # 9. Construct the final 2D output grid.
    #    Reshape the 1D output_row back into a 2D array (1 row, N columns).
    output_grid = output_row.reshape(1, -1)

    # 10. Return the output grid (convert back to list of lists if necessary,
    #     assuming the standard ARC format prefers lists).
    return output_grid.tolist()