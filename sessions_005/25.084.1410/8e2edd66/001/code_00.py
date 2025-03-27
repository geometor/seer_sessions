import numpy as np

"""
The transformation rule expands the input grid by a factor of 3 in both height and width.
The output grid can be thought of as a grid of 3x3 blocks, where each block corresponds to a cell in the original input grid.
If a cell in the input grid at position (r, c) has a non-zero color value, the corresponding 3x3 block in the output grid (starting at position (r*3, c*3)) is a copy of the *entire* original input grid.
If a cell in the input grid at position (r, c) has a zero color value (white), the corresponding 3x3 block in the output grid is filled entirely with zeros (white).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the described rule.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Get dimensions of the input grid
    input_height, input_width = input_grid.shape

    # Calculate output dimensions (3x scaling)
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize the output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=input_grid.dtype)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Check if the input cell value is non-zero
            if input_grid[r, c] != 0:
                # Calculate the top-left corner of the target 3x3 block in the output grid
                start_row = r * 3
                start_col = c * 3
                # Calculate the bottom-right corner (exclusive) of the target block
                # Since the block size is the same as the input grid size
                end_row = start_row + input_height
                end_col = start_col + input_width

                # Copy the entire original input grid into the target block
                output_grid[start_row:end_row, start_col:end_col] = input_grid
            # else: the block remains filled with zeros, as initialized

    return output_grid
