import math  # Although not strictly needed for this logic, included as per template instruction
import copy # Used for deep copying if needed, but direct assignment works here

# Potentially useful helper (though simple enough not to require it here)
# def get_grid_dimensions(grid):
#     rows = len(grid)
#     cols = len(grid[0]) if rows > 0 else 0
#     return rows, cols

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 10x9 input grid into a 10x4 output grid.
    The transformation uses the 5th column (index 4) of the input as a conceptual separator.
    For each cell in the output grid (r, c), its value is determined as follows:
    1. Look at the corresponding cell (r, c) in the left part (columns 0-3) of the input grid.
    2. If the value in input_grid[r][c] is non-zero, use this value for output_grid[r][c].
    3. If the value in input_grid[r][c] is zero, use the value from the mirrored cell in the right part
       (columns 5-8) of the input grid. The mirrored cell is at input_grid[r][8-c].
    """

    # Get input grid dimensions (assuming consistent format)
    input_rows = len(input_grid)
    # input_cols = len(input_grid[0]) # Expected to be 9

    # Define output grid dimensions
    output_rows = input_rows # Same number of rows
    output_cols = 4         # Fixed number of columns

    # Initialize the output grid with zeros (or any placeholder)
    # Creating a new grid is important to avoid modifying the input directly
    # if that's not desired.
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # Iterate through each cell position of the *output* grid
    for r in range(output_rows):
        for c in range(output_cols):
            # Get the value from the corresponding cell in the left part of the input grid
            left_value = input_grid[r][c]

            # Check the condition: if the left value is zero, use the mirrored right value
            if left_value == 0:
                # Calculate the mirrored column index in the right part of the input grid
                # Mirror axis is conceptually between col 4 and col 5.
                # Col 0 mirrors Col 8
                # Col 1 mirrors Col 7
                # Col 2 mirrors Col 6
                # Col 3 mirrors Col 5
                # Formula: mirrored_col = (input_cols - 1) - c = 8 - c
                mirrored_col_index = 8 - c

                # Get the value from the mirrored cell in the right part of the input grid
                right_mirrored_value = input_grid[r][mirrored_col_index]

                # Assign the mirrored value to the output grid cell
                output_grid[r][c] = right_mirrored_value
            else:
                # If the left value is non-zero, assign it directly to the output grid cell
                output_grid[r][c] = left_value

    # Return the completed output grid
    return output_grid
