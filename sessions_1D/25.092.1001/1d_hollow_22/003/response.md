```python
"""
Transformation Rule:
Iterate through each row of the input grid. For each row, find the first and last non-white pixels, which define the span of a contiguous block (assuming only one block per row). Create an output grid of the same dimensions, initially filled with white (0). For each row in the output grid corresponding to a row with a block in the input:
1. Set the pixel at the starting column index of the block to the block's original color.
2. Set the pixel at the ending column index of the block to the block's original color.
3. All other pixels in that output row (between the start and end, and outside the start/end) remain white (0).
If a row in the input grid contains no non-white pixels, the corresponding row in the output grid remains all white (0).
"""

import numpy as np

def find_block_endpoints(row: np.ndarray) -> tuple[int | None, int | None, int | None]:
    """
    Finds the start index, end index, and color of the contiguous non-white block in a row.

    Args:
        row: A 1D NumPy array representing a row of the grid.

    Returns:
        A tuple (start_index, end_index, color). Returns (None, None, None)
        if no non-white block is found. Assumes at most one block per row.
    """
    # Find indices of all non-white pixels
    non_white_indices = np.where(row != 0)[0]

    # If no non-white pixels, return None
    if len(non_white_indices) == 0:
        return None, None, None

    # Determine start and end indices
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]

    # Get the color of the block (from the start pixel)
    block_color = row[start_index]

    # Basic check for contiguity/single color (optional based on strictness)
    # Expected: all pixels between start_index and end_index should be block_color
    # This isn't strictly necessary based on the simple rule derived,
    # but good for confirming assumptions if needed.
    # Example: if not np.all(row[start_index : end_index + 1] == block_color):
    #    print(f"Warning: Non-contiguous or multi-color block detected in row: {row}")

    return start_index, end_index, block_color


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid. For each row,
    keeps only the first and last pixels of the non-white block,
    turning the intermediate pixels white.

    Args:
        input_grid: A 2D NumPy array representing the input grid.

    Returns:
        A 2D NumPy array representing the transformed grid.
    """
    # Initialize output_grid with the same shape as input, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each row of the input grid
    for r in range(input_grid.shape[0]):
        # Get the current row
        input_row = input_grid[r, :]

        # Find the block endpoints and color for the current row
        start_index, end_index, block_color = find_block_endpoints(input_row)

        # If a block was found in this row
        if start_index is not None and end_index is not None and block_color is not None:
            # Place the block's color at the start index in the output row
            output_grid[r, start_index] = block_color

            # Place the block's color at the end index in the output row
            # This handles blocks of length 1 or 2 correctly (start/end might be same)
            output_grid[r, end_index] = block_color

        # Else: No block found, the output row remains all zeros (white) as initialized.

    return output_grid
```