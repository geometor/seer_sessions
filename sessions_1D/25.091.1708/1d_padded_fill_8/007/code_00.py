"""
Processes each row of an input grid (assumed to be 3x23 based on examples) independently. 
If a row contains exactly two non-white pixels (pixels with color > 0) of the same color, it fills the horizontal segment between these two pixels (inclusive) with that color. 
Otherwise, the row remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a row-wise segment filling transformation to the input grid.

    For each row, it identifies non-white pixels. If exactly two such pixels
    exist and share the same color, the horizontal span between them (inclusive)
    in the output grid row is filled with that color. Otherwise, the row
    is copied unchanged from the input to the output.

    Args:
        input_grid (list of lists): A 2D list representing the input grid where
                                     each inner list is a row and values are integers 0-9.
                                     It's assumed the input dimensions match the examples (e.g., 3x23).

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    
    # Convert input list of lists to a NumPy array for efficient processing
    # This handles the 2D structure correctly if input_grid is a list of lists.
    input_array = np.array(input_grid, dtype=int)
    
    # Create a copy of the input array to store the output. This ensures that
    # rows not meeting the transformation criteria remain unchanged initially.
    output_array = np.copy(input_array)
    
    # Get the number of rows in the grid
    num_rows = input_array.shape[0]

    # Iterate through each row index
    for r in range(num_rows):
        # Extract the current row from the input array
        row = input_array[r, :]
        
        # Find the column indices of all non-white pixels (color != 0) in the current row
        # np.where returns a tuple of arrays; we need the first element which contains the column indices.
        non_white_indices = np.where(row != 0)[0]
        
        # Check if the number of non-white pixels in this row is exactly two
        if len(non_white_indices) == 2:
            # Get the column indices of the two non-white pixels
            col1_idx = non_white_indices[0]
            col2_idx = non_white_indices[1]
            
            # Get the colors of these two pixels from the original input row
            color1 = row[col1_idx]
            color2 = row[col2_idx]
            
            # Check if the colors of the two identified pixels are the same
            if color1 == color2:
                # Determine the starting and ending column indices for the segment to be filled.
                # Use min and max to handle cases where the pixels might appear in any order in the indices array.
                col_start = min(col1_idx, col2_idx)
                col_end = max(col1_idx, col2_idx)
                
                # Fill the segment in the corresponding row of the output grid.
                # NumPy slicing `start:end+1` includes the element at index `end`.
                # The color used for filling is the common color identified (color1 or color2).
                output_array[r, col_start : col_end + 1] = color1 
                
        # If the conditions (exactly two non-white pixels AND they are the same color) 
        # are not met for the current row, the corresponding row in `output_array` 
        # already retains its original values because we initialized output_array as a copy. 
        # No explicit 'else' action is needed for unchanged rows.

    # Convert the final NumPy array back to a list of lists format before returning
    return output_array.tolist()