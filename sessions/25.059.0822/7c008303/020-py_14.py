"""
1.  **Dimension Reduction:** The output grid is always 6x6, while the input is 9x9.

2.  **Consistent First Column and Last Column Mapping:**
    *   The first two rows of the output's first column consistently contain color `2` (red) if the input contains color `8` (azure).
    *   The first two rows of the output's last column consistently contain color `4` (yellow) if the input contains color `8` (azure).
    * It appears that color `8` (azure) is always present in the input, and is related to the presence of colors `2` and `4` in the first and last column of the output.

3.  **Green (3) to Gray (5) and Magenta (6) Mapping (Conditional):**
    *   If green (3) exists, map it to gray (5) or magenta (6).  The mapping to `5` appears more common and takes precedence.
    * The column index is preserved during this transformation if the input column index is < 6
    * The row index is preserved during this transformation if the input row index < 6.

4.  **Other Colors:**
    * Colors, other than `3` and `8` are not consistently preserved in the output. Colors `1`, `2`, `4`, `5`, `6`, and `7` seem to disappear or are not directly mapped using a simple rule.

5. **Object-Based Logic:**  The transformation seems to prioritize preserving the *existence* of certain objects, rather than strictly preserving their positions:
    * The vertical line of azure gets "summarized" by the red and yellow pixels.
    * The existence of green seems to create gray or magenta in output.
"""

import numpy as np

def get_positions(grid, color):
    """
    Returns a list of (row, col) tuples representing the positions of a given color in the grid.
    """
    return [(row, col) for row in range(grid.shape[0]) for col in range(grid.shape[1]) if grid[row, col] == color]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((6, 6), dtype=int)

    # Check for the presence of azure (8)
    azure_positions = get_positions(input_grid, 8)
    if azure_positions:
        output_grid[0, 0] = 2  # First column, first row: Red (2)
        output_grid[0, 5] = 4  # Last column, first row: Yellow (4)

    # Handle Green (3) to Gray (5) or Magenta (6) mapping
    green_positions = get_positions(input_grid, 3)
    for row, col in green_positions:
        if row < 6 and col < 6:
            output_grid[row, col] = 5  # Default to Gray (5)

    return output_grid