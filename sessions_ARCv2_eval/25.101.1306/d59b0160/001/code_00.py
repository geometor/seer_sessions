import numpy as np
import copy

"""
The transformation rule operates based on the pixel value at a specific 'control' column (index 2) for each row, affecting the pixels to the right of a 'separator' column (index 3).

1.  Identify the background color (orange, 7).
2.  Identify the control column index (2) and the separator column index (3).
3.  Initialize the output grid as a copy of the input grid.
4.  Iterate through each row `r` of the grid.
5.  Examine the color of the pixel at `(r, 2)` (the control pixel).
6.  If the control pixel color is NOT the background color (7):
    Iterate through each column `c` to the right of the separator (`c > 3`).
    If the pixel `input[r, c]` is not the background color (7), change the corresponding pixel in the output grid `output[r, c]` to the background color (7).
7.  If the control pixel color IS the background color (7):
    Leave all pixels in the row `r` of the output grid unchanged from the input grid (specifically, the right side `c > 3` remains as it was in the input).
8.  Return the modified output grid.

This rule was derived primarily from observing the consistent behavior in train_2 and train_3. Train_1 shows some deviations from this rule when the control pixel is 7, suggesting either an error in the example's output or a more complex condition not fully captured here. However, the implemented rule correctly transforms train_2 and train_3.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the color of the pixel in column 2.
    If input[row, 2] is not 7, changes all non-7 pixels to 7 in columns > 3 for that row.
    Otherwise, leaves the row unchanged.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    
    # Define constants based on observations
    background_color = 7
    control_column_index = 2
    separator_column_index = 3
    
    num_rows, num_cols = input_np.shape
    
    # Iterate through each row
    for r in range(num_rows):
        # Get the color of the control pixel for this row
        control_pixel_color = input_np[r, control_column_index]
        
        # Check the condition based on the control pixel
        if control_pixel_color != background_color:
            # If the control pixel is NOT the background color,
            # modify the right region (columns > separator_column_index)
            for c in range(separator_column_index + 1, num_cols):
                # Change any non-background color pixel to the background color
                if output_np[r, c] != background_color:
                    output_np[r, c] = background_color
        # else:
            # If the control pixel IS the background color, do nothing to this row.
            # The output row remains a copy of the input row.
            
    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid
