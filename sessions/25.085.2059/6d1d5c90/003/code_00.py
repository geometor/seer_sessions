import numpy as np

"""
Transformation Rule:
1. Examine the color of the pixel at the top-left corner (row 0, column 0) of the input grid.
2. Create an intermediate grid by removing the first column (column 0) from the input grid.
3. If the top-left pixel color was red (value 2), the output grid is the intermediate grid, preserving the original row order.
4. If the top-left pixel color was not red, the output grid is the intermediate grid with its rows sorted lexicographically.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the color of the top-left pixel.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Handle edge case: If the input grid has no columns, return an empty grid
    # with the correct number of rows but zero width.
    if width == 0:
        return [[] for _ in range(height)]

    # Step 1: Examine the color of the top-left pixel.
    # The grid must have at least one row and one column to check input_np[0, 0].
    # If height is 0, the width == 0 check already handled it.
    top_left_color = input_np[0, 0]

    # Determine if sorting is needed based on the top-left color.
    # Sort if the color is NOT red (2).
    should_sort = top_left_color != 2

    # Step 2: Create an intermediate grid by removing the first column.
    # Slicing input_np[:, 1:] works correctly even if width is 1,
    # resulting in a grid with shape (height, 0).
    intermediate_grid_np = input_np[:, 1:]

    # Convert the intermediate numpy grid back to a list of lists.
    intermediate_grid_list = intermediate_grid_np.tolist()

    # Step 3 & 4: Conditionally sort the rows of the intermediate grid.
    if should_sort:
        # Sort the list of lists (rows) lexicographically.
        # The `sorted()` function handles this correctly for lists of lists.
        output_grid_list = sorted(intermediate_grid_list)
    else:
        # If the top-left was red, keep the rows in their original order
        # (after the first column was removed).
        output_grid_list = intermediate_grid_list

    # Return the final transformed grid as a list of lists.
    return output_grid_list