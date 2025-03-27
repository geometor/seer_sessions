```python
import numpy as np

def transform(input_grid):
    """
    Identifies columns with red markers (2) in the last row. 
    Determines a target column based on the presence of gray (5) pixels above the marker:
    - If gray is present in the marker column (above the marker), the target column is shifted one position to the right.
    - Otherwise, the target column is the same as the marker column.
    Fills the target column with red (2), replacing only white (0) pixels and preserving existing non-white pixels (like gray).
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input grid
    # This preserves existing pixels, including gray ones, unless overwritten
    output_array = np.copy(input_array)
    
    # Identify the indices of columns containing red (2) in the last row
    last_row_index = height - 1
    # np.where returns a tuple of arrays, we need the first element for column indices
    marker_cols = np.where(input_array[last_row_index, :] == 2)[0] 
    
    # Iterate through each identified marker column index
    for marker_col in marker_cols:
        
        # --- Determine if there's a gray pixel above the marker in the same column ---
        has_gray_above = False
        # Check rows from 0 up to (but not including) the last row
        if marker_col < width: # Basic bounds check (though marker_col comes from existing indices)
            # Extract the column segment above the marker
            column_above_marker = input_array[0:last_row_index, marker_col] 
            # Check if any pixel in this segment is gray (5)
            if np.any(column_above_marker == 5):
                has_gray_above = True
        
        # --- Determine the target column to fill based on the presence of gray ---
        if has_gray_above:
            # If gray was found above, shift the target column one to the right
            fill_col = marker_col + 1
        else:
            # Otherwise, the target column is the same as the marker column
            fill_col = marker_col
            
        # --- Fill the target column ---
        # Ensure the calculated fill column is within the grid's width boundaries
        if 0 <= fill_col < width:
            # Iterate through all rows (0 to height-1) for the target fill column
            for row_idx in range(height):
                # Check if the pixel in the *original* input grid at this fill position is white (0)
                if input_array[row_idx, fill_col] == 0:
                    # If it's white, change the corresponding pixel in the *output* grid to red (2)
                    output_array[row_idx, fill_col] = 2
                    # If the original pixel was not white (e.g., gray 5), it remains unchanged 
                    # because output_array started as a copy of input_array.
                    
    # Convert the modified numpy array back to a list of lists for the final output format
    output_grid = output_array.tolist()
    
    return output_grid
```