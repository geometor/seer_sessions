import numpy as np

"""
Rearranges the pixels in a 5-element input column according to a fixed positional permutation:
- The first element moves to the second position.
- The second element moves to the first position.
- The third element stays in the third position.
- The fourth element moves to the fifth position.
- The fifth element moves to the fourth position.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a fixed positional rearrangement to a 5x1 input grid.

    Args:
        input_grid: A list of lists representing the 5x1 input grid.

    Returns:
        A list of lists representing the 5x1 output grid with rearranged pixels.
    """

    # Ensure input is treated as a numpy array for easier indexing if needed,
    # though direct list indexing works fine here.
    input_array = np.array(input_grid, dtype=int)

    # Get the height and width (should be 5x1 based on examples)
    height = input_array.shape[0]
    # width = input_array.shape[1] # Expected width is 1

    # Basic check for expected height (though problem description implies fixed height)
    if height != 5:
        # Depending on the expected behavior for other heights,
        # we could return the input, raise an error, or attempt a different logic.
        # Based on the analysis, we assume height is always 5.
        # For robustness, let's return the input unchanged if height is not 5.
        # print(f"Warning: Expected input height 5, got {height}. Returning input unchanged.")
        # return input_grid # Or handle as an error depending on requirements
        raise ValueError(f"Input grid height must be 5, but got {height}")


    # Initialize the output grid with the same dimensions and type, filled with zeros initially
    output_grid = [[0] for _ in range(height)] # Creates a 5x1 list of lists

    # Apply the rearrangement logic based on the natural language program:
    # 1. Place input[1][0] into output[0][0]
    output_grid[0][0] = input_grid[1][0]
    # 2. Place input[0][0] into output[1][0]
    output_grid[1][0] = input_grid[0][0]
    # 3. Place input[2][0] into output[2][0]
    output_grid[2][0] = input_grid[2][0]
    # 4. Place input[4][0] into output[3][0]
    output_grid[3][0] = input_grid[4][0]
    # 5. Place input[3][0] into output[4][0]
    output_grid[4][0] = input_grid[3][0]

    return output_grid