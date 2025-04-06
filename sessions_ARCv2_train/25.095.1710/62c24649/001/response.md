```python
"""
Takes an N x N input grid and constructs a 2N x 2N output grid.
The output grid is composed of four quadrants:
- Top-left: The original input grid.
- Top-right: The input grid flipped horizontally.
- Bottom-left: The input grid flipped vertically.
- Bottom-right: The input grid flipped both horizontally and vertically.
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described tiling and flipping transformation to the input grid.

    Args:
        input_grid: A square 2D list of integers.

    Returns:
        A 2D list of integers representing the transformed grid, with dimensions
        twice those of the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    n = input_array.shape[0] # Assuming square grid

    # Create the transformed versions of the input grid
    # Top-left: original
    top_left = input_array

    # Top-right: flipped horizontally (left-right)
    top_right = np.fliplr(input_array)

    # Bottom-left: flipped vertically (up-down)
    bottom_left = np.flipud(input_array)

    # Bottom-right: flipped both horizontally and vertically
    # Can flip the vertically flipped one horizontally, or the horizontally flipped one vertically
    bottom_right = np.fliplr(bottom_left)
    # Alternatively: bottom_right = np.flipud(top_right)
    # Alternatively: bottom_right = np.fliplr(np.flipud(input_array))


    # Assemble the output grid by combining the quadrants
    # Combine top row quadrants horizontally
    top_row = np.hstack((top_left, top_right))

    # Combine bottom row quadrants horizontally
    bottom_row = np.hstack((bottom_left, bottom_right))

    # Combine the top and bottom rows vertically
    output_array = np.vstack((top_row, bottom_row))

    # Convert the final NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid

```