import numpy as np

"""
Transposes the input grid. For each cell at position (row, col) in the input grid, 
its value is placed at position (col, row) in the output grid. 
The dimensions of the grid remain unchanged.
"""

def transform(input_grid):
    """
    Applies a matrix transpose operation to the input grid.

    Args:
        input_grid (list of lists of int): The input 2D grid.

    Returns:
        list of lists of int: The transposed 2D grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # Initialize the output grid with zeros, maintaining the original dimensions
    # Note: While the prompt description focuses on non-zero elements,
    # transposing the entire grid correctly handles both zero and non-zero elements.
    # A simpler approach is to directly use numpy's transpose function.
    
    # Perform the transpose operation
    output_array = input_array.T # .T is the shorthand for transpose()

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
