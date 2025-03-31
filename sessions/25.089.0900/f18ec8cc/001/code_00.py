import numpy as np
from typing import List, Tuple

"""
Identifies vertical stripes in the input grid based on contiguous blocks of color
in the top row. Swaps the first identified vertical stripe block with the last
identified vertical stripe block. Any stripes between the first and last retain
their relative order and are positioned between the swapped end stripes.
"""

def find_stripes_from_top_row(grid: np.ndarray) -> List[Tuple[int, int]]:
    """
    Identifies vertical stripe boundaries based on color changes in the top row.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A list of tuples, where each tuple represents a stripe
        as (start_column_index, end_column_index).
    """
    if grid.shape[1] == 0:
        return []

    top_row = grid[0, :]
    width = len(top_row)
    stripes = []
    start_col = 0
    current_color = top_row[0]

    for col in range(1, width):
        if top_row[col] != current_color:
            # End of a stripe detected
            stripes.append((start_col, col))
            # Start of a new stripe
            start_col = col
            current_color = top_row[col]

    # Add the last stripe
    stripes.append((start_col, width))

    return stripes


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by swapping the first and last vertical stripes.

    The vertical stripes are identified based on contiguous blocks of the same
    color in the top row of the input grid. The first stripe and the last
    stripe are swapped, while any intermediate stripes maintain their relative
    order between the swapped stripes.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to NumPy array for easier slicing
    np_grid = np.array(input_grid, dtype=int)
    height, width = np_grid.shape

    # If the grid is empty or has no width, return it as is
    if height == 0 or width == 0:
        return input_grid

    # 1. Identify the distinct vertical stripes based on the top row.
    stripes = find_stripes_from_top_row(np_grid)
    num_stripes = len(stripes)

    # If there's only one stripe or fewer (e.g., empty grid handled earlier),
    # no swap is needed.
    if num_stripes <= 1:
        return input_grid

    # 2. Extract the block of columns corresponding to the first stripe.
    first_stripe_cols = stripes[0]
    first_block = np_grid[:, first_stripe_cols[0]:first_stripe_cols[1]]

    # 3. Extract the block of columns corresponding to the last stripe.
    last_stripe_cols = stripes[-1]
    last_block = np_grid[:, last_stripe_cols[0]:last_stripe_cols[1]]

    # 4. Extract the block of columns for middle stripes (if any).
    middle_block = None
    if num_stripes > 2:
        # The middle block starts at the beginning of the second stripe
        middle_start_col = stripes[1][0]
        # and ends at the beginning of the last stripe.
        middle_end_col = stripes[-1][0]
        middle_block = np_grid[:, middle_start_col:middle_end_col]

    # 5. Construct the output grid by concatenating the blocks in the new order.
    blocks_to_concat = []
    blocks_to_concat.append(last_block) # Last block comes first
    if middle_block is not None:
        blocks_to_concat.append(middle_block) # Middle block(s) in the middle
    blocks_to_concat.append(first_block) # First block comes last

    output_np = np.concatenate(blocks_to_concat, axis=1)

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()

    return output_grid