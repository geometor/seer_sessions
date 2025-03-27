"""
Transforms a 3x3 input grid by applying a specific number substitution rule.

The rule dictates a one-to-one mapping for each number in the input grid:
- 5 becomes 1
- 8 becomes 9
- 6 becomes 2
- 2 becomes 6
- 3 becomes 4
- 9 becomes 8
- 4 becomes 3
- 1 becomes 5

The function iterates through each cell of the input grid and applies this
substitution, returning a new 3x3 grid with the transformed values.
"""

def transform(input_grid):
    """
    Applies a number substitution to each cell of the input grid.
    """
    # Initialize the output grid with the same dimensions as the input.
    output_grid = [[0] * len(input_grid[0]) for _ in range(len(input_grid))]

    # Define the substitution mapping.
    substitution_map = {
        5: 1,
        8: 9,
        6: 2,
        2: 6,
        3: 4,
        9: 8,
        4: 3,
        1: 5,
    }

    # Iterate through each cell of the input grid.
    for row_index, row in enumerate(input_grid):
        for col_index, cell_value in enumerate(row):
            # Apply the substitution and update the output grid.
            output_grid[row_index][col_index] = substitution_map.get(cell_value, cell_value)  # Use .get() for safety

    return output_grid