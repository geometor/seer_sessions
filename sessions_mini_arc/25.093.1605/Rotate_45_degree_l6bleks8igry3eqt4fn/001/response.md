```python
import copy

"""
Transforms a 5x5 grid based on the value of its corner cells.

1. Initialize the output grid as a copy of the input 5x5 grid.
2. Check the value of the input corner cells (e.g., at location [0,0]).
3. If the corner value is 0:
    a. Get the value of an adjacent border cell (e.g., at [0,1]).
    b. Set all four corner cells and all four midpoint edge cells ([0,2], [2,0], [2,4], [4,2]) in the output grid to this adjacent value.
4. If the corner value is not 0:
    a. Set all four corner cells in the output grid to 0.
    b. For each midpoint edge cell ([0,2], [2,0], [2,4], [4,2]), find the value of its immediate inner neighbor cell in the input grid ([1,2], [2,1], [2,3], [3,2] respectively) and set the output midpoint cell to this value.
5. All other cells remain unchanged.
6. Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 5x5 list of lists representing the input grid.

    Returns:
        A 5x5 list of lists representing the transformed output grid.
    """
    # Ensure the input is a 5x5 grid (basic check)
    if not (len(input_grid) == 5 and all(len(row) == 5 for row in input_grid)):
        raise ValueError("Input grid must be 5x5")

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Define key locations
    corner_locs = [(0, 0), (0, 4), (4, 0), (4, 4)]
    midpoint_locs = [(0, 2), (2, 0), (2, 4), (4, 2)]
    # Map midpoints to their inner neighbors
    midpoint_to_inner = {
        (0, 2): (1, 2),
        (2, 0): (2, 1),
        (2, 4): (2, 3),
        (4, 2): (3, 2),
    }
    # Location of an adjacent border cell (used when corners are 0)
    adjacent_border_loc = (0, 1) # Could also be (1,0), (0,3) etc.

    # Get the value of the top-left corner cell from the input
    input_corner_value = input_grid[0][0]

    # Apply transformation based on the corner value
    if input_corner_value == 0:
        # Case 1: Input corners are 0
        # Get the value from an adjacent border cell in the input
        adjacent_value = input_grid[adjacent_border_loc[0]][adjacent_border_loc[1]]

        # Set output corners to the adjacent value
        for r, c in corner_locs:
            output_grid[r][c] = adjacent_value

        # Set output midpoints to the adjacent value
        for r, c in midpoint_locs:
            output_grid[r][c] = adjacent_value
    else:
        # Case 2: Input corners are non-zero
        # Set output corners to 0
        for r, c in corner_locs:
            output_grid[r][c] = 0

        # Set output midpoints to the value of their inner neighbor in the input
        for mid_r, mid_c in midpoint_locs:
            inner_r, inner_c = midpoint_to_inner[(mid_r, mid_c)]
            inner_neighbor_value = input_grid[inner_r][inner_c]
            output_grid[mid_r][mid_c] = inner_neighbor_value

    # Return the modified grid
    return output_grid

```