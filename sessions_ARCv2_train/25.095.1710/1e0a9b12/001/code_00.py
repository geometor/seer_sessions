import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a vertical "gravity" effect to each column of the input grid independently.
    Non-zero numbers fall downwards, preserving their relative order within the column,
    and stack at the bottom or on top of other non-zero numbers. Zeros are treated as
    empty space.

    Steps:
    1. Initialize an output grid of the same dimensions as the input, filled with zeros.
    2. Get the number of rows and columns.
    3. Iterate through each column of the input grid.
    4. For each column:
        a. Extract all non-zero numbers, maintaining their top-to-bottom order.
        b. Place these extracted numbers into the corresponding column of the output grid,
           starting from the bottom row and moving upwards, preserving their order.
    5. Return the completed output grid.
    """

    # Handle empty input grid case
    if not input_grid or not input_grid[0]:
        return []

    # Get dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid with zeros using list comprehensions for clarity
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # Iterate through each column index
    for c in range(num_cols):
        # Extract non-zero numbers from the current column, preserving order
        column_numbers = []
        for r in range(num_rows):
            if input_grid[r][c] != 0:
                column_numbers.append(input_grid[r][c])

        # Place the extracted numbers into the output grid column from bottom up
        num_non_zero = len(column_numbers)
        for i in range(num_non_zero):
            # The i-th number (0-indexed) from the top goes into the i-th available slot from the bottom
            target_row = num_rows - num_non_zero + i
            output_grid[target_row][c] = column_numbers[i]

    return output_grid