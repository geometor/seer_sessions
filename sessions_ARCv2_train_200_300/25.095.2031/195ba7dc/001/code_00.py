import math

"""
Combines information from the left and right halves of an input grid, separated by a column of '2's, to produce a smaller output grid.

The output grid's value at position (r, c) is 1 if either the corresponding element in the left half (input_grid[r][c]) or the right half (input_grid[r][separator_index + 1 + c]) is 7. Otherwise, the output value is 0.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the presence of '7' in corresponding
    positions in the left and right halves separated by a '2' column.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """

    # Get dimensions of the input grid
    num_rows = len(input_grid)
    if num_rows == 0:
        return []
    num_cols_input = len(input_grid[0])
    if num_cols_input == 0:
        return [[] for _ in range(num_rows)]

    # Find the separator column index (assuming it's consistent and exists)
    # Based on examples, the separator is always at index 6
    separator_index = 6 
    
    # --- Simple approach assuming fixed separator index ---
    # try:
    #     separator_index = -1
    #     # Check first row for the separator column index
    #     for c_idx, val in enumerate(input_grid[0]):
    #          # A simple check if the column consists only of 2s might be needed for robustness
    #          # but for now, finding the first 2 in the first row is assumed sufficient
    #          if val == 2: 
    #              separator_index = c_idx
    #              break
    #     if separator_index == -1:
    #         raise ValueError("Separator column with value 2 not found.")
    # except (IndexError, ValueError) as e:
    #      print(f"Error determining separator index: {e}")
    #      # Handle error appropriately, maybe return empty or raise exception
    #      return [] 
    # --------------------------------------------------------


    # Calculate the number of columns for the output grid
    num_cols_output = (num_cols_input - 1) // 2

    # Initialize the output grid with zeros
    output_grid = [[0 for _ in range(num_cols_output)] for _ in range(num_rows)]

    # Iterate through each cell position of the output grid
    for r in range(num_rows):
        for c in range(num_cols_output):
            # Get the corresponding value from the left half of the input grid
            left_value = input_grid[r][c]

            # Calculate the corresponding column index in the right half
            right_col_index = separator_index + 1 + c

            # Get the corresponding value from the right half of the input grid
            # Add boundary check just in case
            if right_col_index < num_cols_input:
                right_value = input_grid[r][right_col_index]
            else:
                # Handle potential malformed input where right half is too short
                # Based on problem description, this shouldn't happen
                right_value = 0 # Or raise an error

            # Apply the transformation rule: output is 1 if either input is 7
            if left_value == 7 or right_value == 7:
                output_grid[r][c] = 1
            # No need for an else statement, as the grid is initialized with 0s

    return output_grid