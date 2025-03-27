import numpy as np

"""
The transformation takes a 5-row input grid, typically 17 columns wide, which 
often contains vertical magenta lines (color 6) at columns 5 and 11 acting as visual
delimiters dividing the grid into three main sections.

The transformation produces a 5x5 output grid by selecting specific, fixed columns
from the input grid and arranging them sequentially in the output. The height 
remains unchanged.

The selection rule is as follows:
1. Output column 0 is a copy of input column 0.
2. Output column 1 is a copy of input column 1.
3. Output column 2 is a copy of input column 8. (This column is centrally 
   located in the section between the typical magenta delimiters).
4. Output column 3 is a copy of input column 15. (This is the second-to-last 
   column of the typical 17-column input).
5. Output column 4 is a copy of input column 16. (This is the last column of 
   the typical 17-column input).
"""

def transform(input_grid):
    """
    Selects specific columns (0, 1, 8, 15, 16) from the input grid 
    to form a new 5-column output grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the 5x5 output grid.
    """
    # Convert input list of lists to a NumPy array for efficient column slicing
    input_np = np.array(input_grid, dtype=int)

    # Get the height of the input grid
    height = input_np.shape[0]
    
    # Define the specific column indices to select from the input grid
    # Based on the observed pattern: 0, 1, 8, 15, 16
    selected_input_col_indices = [0, 1, 8, 15, 16]

    # Check if the input grid has enough columns
    if input_np.shape[1] <= max(selected_input_col_indices):
        # This case shouldn't happen based on examples, but good practice to check
        raise ValueError(f"Input grid width {input_np.shape[1]} is too small to select column index {max(selected_input_col_indices)}")

    # Initialize the output grid with the correct dimensions (height x 5)
    # Use the same data type as the input
    output_grid_np = np.zeros((height, 5), dtype=int)

    # Iterate through the desired output columns and copy the corresponding
    # input column data
    for output_col_index, input_col_index in enumerate(selected_input_col_indices):
        # Select the entire input column using slicing
        input_column = input_np[:, input_col_index]
        # Assign it to the corresponding output column
        output_grid_np[:, output_col_index] = input_column

    # Convert the resulting NumPy array back to a list of lists format
    output_grid = output_grid_np.tolist()

    return output_grid
