import numpy as np

"""
Transforms an input grid by expanding each cell into a 2x2 block in the output grid.
Input cells with value 0 are replaced by a 2x2 block of 0s.
Input cells with value 5 are replaced by a 2x2 block with the pattern [[1, 2], [2, 1]].
The output grid dimensions are twice the height and twice the width of the input grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the cell expansion transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid (e.g., 3x3).

    Returns:
        A list of lists representing the transformed output grid (e.g., 6x6).
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    input_rows, input_cols = input_np.shape
    
    # Calculate the dimensions of the output grid
    output_rows = input_rows * 2
    output_cols = input_cols * 2
    
    # Initialize the output grid with zeros
    # Using numpy makes initialization and slicing easier
    output_np = np.zeros((output_rows, output_cols), dtype=int)
    
    # Define the 2x2 block pattern for input value 5
    pattern_5 = np.array([[1, 2], [2, 1]], dtype=int)

    # Iterate through each cell (r, c) of the input grid
    for r in range(input_rows):
        for c in range(input_cols):
            # Get the value of the current input cell
            input_value = input_np[r, c]
            
            # Calculate the top-left coordinates (out_r, out_c) for the 
            # corresponding 2x2 block in the output grid
            out_r = r * 2
            out_c = c * 2
            
            # If the input value is 5, place the pattern_5 block
            if input_value == 5:
                # Assign the 2x2 pattern to the corresponding slice in the output grid
                # output_np[start_row:end_row, start_col:end_col]
                output_np[out_r:out_r + 2, out_c:out_c + 2] = pattern_5
            # If the input value is 0, the corresponding 2x2 block 
            # in the output grid remains 0 (as initialized), so no explicit action is needed.

    # Convert the resulting numpy array back to a list of lists for the final output
    output_grid = output_np.tolist()

    return output_grid