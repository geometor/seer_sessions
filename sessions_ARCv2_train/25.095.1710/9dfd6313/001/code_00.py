import math
import numpy as np # Using numpy for convenient array handling, especially transposition

"""
Transposes the input 2D grid (matrix). 
The value at input[row][col] is moved to output[col][row].
The dimensions of the output grid are the swapped dimensions of the input grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transposes a 2D grid represented as a list of lists.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of lists of integers representing the transposed grid.
    """

    # Convert the input list of lists to a NumPy array for easier transposition
    # Handle empty input case gracefully
    if not input_grid or not input_grid[0]:
        return [] # Or handle as appropriate for the task context

    input_array = np.array(input_grid)

    # Determine the dimensions of the input grid
    num_rows, num_cols = input_array.shape

    # Perform the transpose operation using NumPy's transpose method (`.T`)
    output_array = input_array.T

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
