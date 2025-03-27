"""
The transformation rule is as follows:
1. Reverse each Row: Reverse the order of elements within each row of the input grid.
2. Reverse Row Order: Reverse the order of the rows in the result of step 1.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)

    # 1. Reverse each row.
    reversed_rows = np.fliplr(grid)

    # 2. Reverse the order of the rows.
    output_grid = np.flipud(reversed_rows)

    return output_grid.tolist()