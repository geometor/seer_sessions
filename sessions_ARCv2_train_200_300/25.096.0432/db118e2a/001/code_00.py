"""
Creates a 15x15 output grid initialized with the value 7. 
Then, it places two copies of the input grid onto this output grid.
The first copy is placed starting at row 2, column 3 (0-based index).
The second copy is placed starting at row 8, column 9 (0-based index).
If the placement areas overlap, the values from the second copy overwrite 
the values from the first copy. The copying process respects the 15x15
boundary of the output grid; parts of the input grid that would fall outside 
this boundary are clipped.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by placing two copies onto a 15x15 background grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the 15x15 transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape
    
    # Define output grid dimensions and background color
    output_height = 15
    output_width = 15
    background_color = 7

    # Initialize the 15x15 output grid with the background color
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # Define offsets for the two copies
    offset1_row, offset1_col = 2, 3
    offset2_row, offset2_col = 8, 9

    # --- Place the first copy ---
    # Calculate the boundaries for placing the first copy
    # Ensure we don't write outside the output grid bounds
    end_row1 = min(offset1_row + input_height, output_height)
    end_col1 = min(offset1_col + input_width, output_width)
    
    # Determine the slice of the input grid to use (in case it needs clipping)
    input_slice_height1 = end_row1 - offset1_row
    input_slice_width1 = end_col1 - offset1_col

    # Copy the relevant part of the input grid to the output grid
    if input_slice_height1 > 0 and input_slice_width1 > 0:
        output_grid[offset1_row:end_row1, offset1_col:end_col1] = input_np[:input_slice_height1, :input_slice_width1]

    # --- Place the second copy ---
    # Calculate the boundaries for placing the second copy
    # Ensure we don't write outside the output grid bounds
    end_row2 = min(offset2_row + input_height, output_height)
    end_col2 = min(offset2_col + input_width, output_width)

    # Determine the slice of the input grid to use (in case it needs clipping)
    input_slice_height2 = end_row2 - offset2_row
    input_slice_width2 = end_col2 - offset2_col

    # Copy the relevant part of the input grid to the output grid
    # This will overwrite parts of the first copy if they overlap
    if input_slice_height2 > 0 and input_slice_width2 > 0:
        output_grid[offset2_row:end_row2, offset2_col:end_col2] = input_np[:input_slice_height2, :input_slice_width2]

    # Convert the final numpy array back to a list of lists for the return value
    return output_grid.tolist()