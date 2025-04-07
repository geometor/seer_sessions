import numpy as np

"""
Applies a 'gravity' effect independently to each column of the input grid.
Non-zero numbers within each column fall downwards, maintaining their relative 
vertical order, until they stack up at the bottom of the column. 
Cells left empty by this movement are filled with zeros.

1. Initialize an output grid of the same dimensions as the input, filled with zeros.
2. Iterate through each column of the input grid.
3. For each column:
    a. Extract all non-zero numbers from top to bottom, preserving their order.
    b. Determine the starting row index in the output column where these non-zero numbers should be placed (bottom-justified).
    c. Place the extracted non-zero numbers into the output grid column starting from the calculated row index downwards.
4. Return the resulting output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by applying columnar gravity.

    Args:
        input_grid: A list of lists representing the 2D input grid of integers.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier handling, though list operations are also possible
    input_array = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_array.shape

    # Initialize the output grid with zeros, same dimensions as input
    output_array = np.zeros_like(input_array)

    # Iterate through each column index
    for c in range(num_cols):
        # Extract non-zero elements from the current column in the input grid
        # Maintain the original top-to-bottom order
        non_zeros_in_col = []
        for r in range(num_rows):
            if input_array[r, c] != 0:
                non_zeros_in_col.append(input_array[r, c])

        # Determine the number of non-zero elements found
        num_non_zeros = len(non_zeros_in_col)

        # Calculate the row index in the output grid where the stack of non-zeros should start
        # This ensures they are placed at the bottom of the column
        start_row = num_rows - num_non_zeros

        # Place the collected non-zero elements into the corresponding output column
        # Start placing from 'start_row' downwards
        for i in range(num_non_zeros):
            output_array[start_row + i, c] = non_zeros_in_col[i]

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_array.tolist()
    
    return output_grid
