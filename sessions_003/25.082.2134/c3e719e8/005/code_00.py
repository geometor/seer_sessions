"""
The transformation involves creating an output grid that is three times the height and width of the input grid. The input grid is then replicated within this larger output grid. The positions of these replications vary depending on the specific example, and empty cells in the output grid are filled with zeros.

Here's a breakdown of the replication rules for each example:

*   **Example 1:** The input grid is replicated three times diagonally, starting at the top-left corner (0, 0), then (input_height, input_width), and finally (2*input_height, 2*input_width).

*   **Example 2:** The input grid is replicated four times: at the top-left corner (0, 0), top-right corner (0, 2*input_width), bottom-left corner (2*input_height, 0), and bottom-right corner (2*input_height, 2*input_width).

*   **Example 3:** The input grid is replicated three times: starting at (0, input_width), then (0, 2*input_width), and finally (2*input_height, 0).

The core concept is creating a 3x3 grid based on the input dimensions, but the placement logic is specific and distinct for each of the examples, with no simple general rule covering the different placement strategies.
"""

import numpy as np

def transform(input_grid, example_index):
    """Transforms the input grid according to the observed pattern, which is specific to each example.

    Args:
        input_grid (list of lists): The input grid.
        example_index: index to use when calculating padding style.

    Returns:
        list of lists: The transformed output grid.
    """
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    if example_index == 0:  # Example 1: Diagonal replication
        replications = [(0, 0), (input_height, input_width), (2 * input_height, 2 * input_width)]
    elif example_index == 1:  # Example 2: Corner replication
        replications = [(0, 0), (0, 2 * input_width), (2 * input_height, 0), (2 * input_height, 2 * input_width)]
    elif example_index == 2:  # Example 3: Specific replication
        replications = [(0, input_width), (0, 2 * input_width), (2 * input_height, 0)]
    else:
        replications = []

    for row_offset, col_offset in replications:
        output_grid[row_offset:row_offset + input_height, col_offset:col_offset + input_width] = input_grid
    
    return output_grid.tolist()