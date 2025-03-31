import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on row-specific rules triggered by the value
    of the second pixel in each row.

    1. Iterate through each row of the input grid.
    2. Check if the row has at least 3 pixels. If not, the row remains unchanged.
    3. If the row has 3 or more pixels, examine the value of the second pixel (index 1).
    4. If the second pixel is 8 (azure):
       - Keep the first pixel (index 0).
       - Set the second pixel (index 1) to the input's first pixel value.
       - Set the third pixel (index 2) to the input's second pixel value.
       - If the row has 4 or more pixels, set the fourth pixel (index 3) to the input's third pixel value.
       - Keep remaining pixels (index 4+) unchanged.
    5. Else if the second pixel is 0 (white):
       - Set the first pixel (index 0) to the input's third pixel value.
       - Set the second pixel (index 1) to the input's first pixel value.
       - Set the third pixel (index 2) to the input's second pixel value.
       - Keep remaining pixels (index 3+) unchanged.
    6. Else (second pixel is neither 8 nor 0): The row remains unchanged.
    7. Return the modified grid.
    """

    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the default case (no change) is handled
    output_grid = input_np.copy()
    
    num_rows, num_cols = input_np.shape

    # Iterate through each row
    for r in range(num_rows):
        row = input_np[r]
        row_len = len(row)

        # Check if the row is long enough for the rules to apply
        if row_len >= 3:
            second_pixel = row[1]

            # Rule for azure (8) at the second position
            if second_pixel == 8:
                # Apply the transformation for the first 3 pixels
                output_grid[r, 1] = row[0]  # Second output pixel = First input pixel
                output_grid[r, 2] = row[1]  # Third output pixel = Second input pixel
                # Apply the transformation for the fourth pixel if the row is long enough
                if row_len >= 4:
                     output_grid[r, 3] = row[2] # Fourth output pixel = Third input pixel
                # Pixels from index 4 onwards are already copied correctly

            # Rule for white (0) at the second position
            elif second_pixel == 0:
                 # Apply the transformation for the first 3 pixels
                 output_grid[r, 0] = row[2] # First output pixel = Third input pixel
                 output_grid[r, 1] = row[0] # Second output pixel = First input pixel
                 output_grid[r, 2] = row[1] # Third output pixel = Second input pixel
                 # Pixels from index 3 onwards are already copied correctly
            
            # Else (second pixel is neither 8 nor 0), do nothing as the row is already copied

        # Else (row_len < 3), do nothing as the row is already copied

    # Convert back to list of lists if necessary, or return numpy array
    # The standard ARC format expects list of lists
    return output_grid.tolist()
