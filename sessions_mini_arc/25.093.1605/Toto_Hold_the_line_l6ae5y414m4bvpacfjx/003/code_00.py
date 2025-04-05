"""
Transforms a 2D grid containing 0s and 8s. Finds pairs of 8s in the input grid that lie on the same row or column. If all cells strictly between such a pair along that line contain 0 in the input grid, those 0s are changed to 8s in the output grid. Original 8s and other 0s remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the segment filling transformation to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_array as a copy of the input_array. We will modify this copy.
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # --- Horizontal Filling ---
    # Iterate through each row
    for r in range(height):
        # Find the column indices where the value is 8 in the current row of the input grid
        eight_cols = np.where(input_array[r, :] == 8)[0]
        
        # We need at least two 8s in the row to potentially fill a segment
        if len(eight_cols) >= 2:
            # Iterate through consecutive pairs of 8s found in this row
            for i in range(len(eight_cols) - 1):
                c1 = eight_cols[i]
                c2 = eight_cols[i+1]
                
                # Check if there's a gap between the two 8s (c2 > c1 + 1)
                if c2 > c1 + 1:
                    # Extract the segment between the two 8s from the original input array
                    segment_to_check = input_array[r, c1 + 1 : c2]
                    
                    # Check if all values in this segment are 0
                    if np.all(segment_to_check == 0):
                        # If all are 0, fill the corresponding segment in the output array with 8s
                        output_array[r, c1 + 1 : c2] = 8

    # --- Vertical Filling ---
    # Iterate through each column
    for c in range(width):
        # Find the row indices where the value is 8 in the current column of the input grid
        eight_rows = np.where(input_array[:, c] == 8)[0]
        
        # We need at least two 8s in the column to potentially fill a segment
        if len(eight_rows) >= 2:
            # Iterate through consecutive pairs of 8s found in this column
            for i in range(len(eight_rows) - 1):
                r1 = eight_rows[i]
                r2 = eight_rows[i+1]
                
                # Check if there's a gap between the two 8s (r2 > r1 + 1)
                if r2 > r1 + 1:
                    # Extract the segment between the two 8s from the original input array
                    segment_to_check = input_array[r1 + 1 : r2, c]
                    
                    # Check if all values in this segment are 0
                    if np.all(segment_to_check == 0):
                        # If all are 0, fill the corresponding segment in the output array with 8s
                        output_array[r1 + 1 : r2, c] = 8

    # Convert the final NumPy array back to a list of lists format
    output_grid = output_array.tolist()
    
    return output_grid
