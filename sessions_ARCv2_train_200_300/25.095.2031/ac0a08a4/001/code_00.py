"""
Upscales an input 2D integer grid. The scaling factor (S) is determined by the
count of non-zero elements in the input grid. Each cell (r, c) in the input
grid with value V is expanded into an S x S block in the output grid, starting
at row r*S and column c*S, where all cells within that block are assigned the
value V. If the scaling factor S is 0 (input grid contains only zeros), an
empty grid ([]) is returned.
"""

# No external imports needed for this implementation

def _calculate_scaling_factor(grid: list[list[int]]) -> int:
    """
    Helper function to count non-zero elements in the grid.
    Args:
        grid: The input 2D list of integers.
    Returns:
        The count of non-zero elements.
    """
    count = 0
    # Iterate through each row in the grid
    for row in grid:
        # Iterate through each cell value in the row
        for cell in row:
            # Increment count if the cell value is not zero
            if cell != 0:
                count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Performs the grid upscaling transformation based on the count of non-zero
    elements.

    Args:
        input_grid: A list of lists representing the input 2D integer grid.

    Returns:
        A list of lists representing the transformed (upscaled) 2D integer grid,
        or an empty list if the scaling factor is 0.
    """
    # --- Input Validation ---
    # Handle empty input grid case gracefully. If the grid is empty or rows are empty, return empty list.
    if not input_grid or not input_grid[0]:
        return []

    # --- Determine Scaling Factor ---
    # Count the number of non-zero cells in the input grid. This determines
    # the side length (S) of the square blocks in the output grid.
    scaling_factor = _calculate_scaling_factor(input_grid)

    # --- Handle Zero Scaling Factor ---
    # If scaling factor is 0 (meaning the input grid contains only zeros),
    # the conceptual output grid has dimensions (rows*0) x (cols*0) = 0x0.
    # We represent this as an empty list.
    if scaling_factor == 0:
        return []

    # --- Calculate Dimensions ---
    # Get the dimensions (number of rows and columns) of the input grid.
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])

    # Calculate the dimensions of the output grid by multiplying input dimensions
    # by the scaling factor.
    output_rows = input_rows * scaling_factor
    output_cols = input_cols * scaling_factor

    # --- Initialize Output Grid ---
    # Create the output grid structure with the calculated dimensions.
    # Initialize all cells to 0. This is a default value; cells will be
    # overwritten with values from the input grid during the transformation.
    # Using nested list comprehensions for efficient initialization.
    output_grid = [[0 for _ in range(output_cols)] for _ in range(output_rows)]

    # --- Perform Transformation ---
    # Iterate through each cell of the input grid using its row (r) and column (c) index.
    for r in range(input_rows):
        for c in range(input_cols):
            # Get the value V from the current input cell (r, c).
            value = input_grid[r][c]

            # Calculate the starting row and column index in the output grid
            # for the top-left corner of the block corresponding to input cell (r, c).
            start_row = r * scaling_factor
            start_col = c * scaling_factor

            # Fill the S x S block in the output grid with the value V.
            # Iterate through the rows of the target block in the output grid.
            for out_r in range(start_row, start_row + scaling_factor):
                # Iterate through the columns of the target block in the output grid.
                for out_c in range(start_col, start_col + scaling_factor):
                    # Assign the value V to the current cell (out_r, out_c) in the output block.
                    output_grid[out_r][out_c] = value

    # --- Return Result ---
    # Return the fully populated and transformed output grid.
    return output_grid