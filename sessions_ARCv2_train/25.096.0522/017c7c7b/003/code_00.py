"""
Transforms an input grid of 0s and 1s into an output grid of 0s and 2s.
The transformation involves two main steps:
1. Value Replacement: All 1s in the input grid are replaced with 2s to create a modified grid.
2. Row Appending: A specific slice of rows from the modified grid is appended to its bottom. The number of rows to append is ceil(H/2), and they are selected as a contiguous block starting from row index floor(H/3) up to min(floor(H/3) + ceil(H/2), H), where H is the original height of the input grid.
"""

import math
import copy # Used for deep copying the grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """

    # Get input dimensions
    H = len(input_grid)

    # Handle empty input grid
    if H == 0:
        return [] 
    W = len(input_grid[0])

    # 1. Create the modified grid by replacing 1s with 2s
    modified_grid = []
    for r in range(H):
        new_row = []
        for c in range(W):
            # Replace 1 with 2, keep 0 as 0
            if input_grid[r][c] == 1:
                new_row.append(2)
            else:
                new_row.append(0)
        modified_grid.append(new_row)

    # 2. Calculate parameters for row appending slice
    num_appended_rows = math.ceil(H / 2)
    start_index = math.floor(H / 3)
    # Calculate the end index, ensuring it doesn't exceed the grid height
    end_index = min(start_index + num_appended_rows, H)

    # 3. Select the rows to append from the modified grid using slicing
    # Slicing handles cases where start_index >= H or end_index <= start_index correctly (returns empty list)
    appended_rows = modified_grid[start_index:end_index]

    # 4. Construct the final output grid by concatenating
    # Use deepcopy to ensure the original modified_grid part isn't aliased, especially relevant
    # if appended_rows were modified later (though they aren't here). Good practice.
    output_grid = copy.deepcopy(modified_grid)
    # Append the selected rows to the bottom
    output_grid.extend(appended_rows) 

    return output_grid
