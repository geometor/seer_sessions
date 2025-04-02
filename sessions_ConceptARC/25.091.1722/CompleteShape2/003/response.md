```python
import numpy as np
from typing import List, Dict, Set, Tuple

"""
Transforms the input grid by filling white pixels (0) in specific rows and columns.

The transformation rule identifies rows and columns in the *original* input grid
that meet two criteria:
1. They contain exactly one unique non-white color.
2. They contain at least two instances (pixels) of that single non-white color.

If a row meets these criteria, all white pixels (0) in that corresponding row
of a *working copy* grid are filled with the identified non-white color.
This process is done for all qualifying rows first.

Then, if a column meets the same criteria (based on the original input grid),
all white pixels (0) currently present in that corresponding column of the
*working copy* grid are filled with the identified non-white color. This process
is done for all qualifying columns after the row processing is complete.

The final state of the working copy grid is returned.
"""

def _get_non_white_info(line: np.ndarray) -> Tuple[Set[int], Dict[int, int]]:
    """
    Analyzes a 1D array (row or column) to find unique non-white colors
    and their counts.

    Args:
        line: A 1D numpy array representing a row or column.

    Returns:
        A tuple containing:
        - A set of unique non-white colors found in the line.
        - A dictionary mapping each non-white color to its count.
    """
    unique_colors = set()
    counts = {}
    for color in line:
        if color != 0:
            unique_colors.add(color)
            counts[color] = counts.get(color, 0) + 1
    return unique_colors, counts

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the row and column completion transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input; this grid will be modified
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # --- Row Processing ---
    # Iterate through each row of the *original* input grid
    for r in range(height):
        row = input_np[r, :]
        # Get unique non-white colors and their counts for this row
        unique_colors, counts = _get_non_white_info(row)

        # Check if the row meets the criteria: exactly one non-white color AND more than one instance
        if len(unique_colors) == 1:
            fill_color = list(unique_colors)[0] # Get the single non-white color
            if counts.get(fill_color, 0) > 1:
                # Iterate through the pixels of this row in the *output* grid
                for c in range(width):
                    # If the pixel in the output grid is currently white, fill it
                    if output_np[r, c] == 0:
                        output_np[r, c] = fill_color

    # --- Column Processing ---
    # Iterate through each column of the *original* input grid
    for c in range(width):
        col = input_np[:, c]
        # Get unique non-white colors and their counts for this column
        unique_colors, counts = _get_non_white_info(col)

        # Check if the column meets the criteria: exactly one non-white color AND more than one instance
        if len(unique_colors) == 1:
            fill_color = list(unique_colors)[0] # Get the single non-white color
            if counts.get(fill_color, 0) > 1:
                # Iterate through the pixels of this column in the *output* grid
                for r in range(height):
                    # If the pixel in the output grid is currently white, fill it
                    if output_np[r, c] == 0:
                        output_np[r, c] = fill_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()
```