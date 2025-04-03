import math

def transform(input_grid):
    """
    Determines the length of a zero-filled output row based on the spatial 
    distribution of non-zero elements in an input grid. The length is the 
    minimum of the number of unique rows and the number of unique columns 
    that contain at least one non-zero element. The output row itself 
    contains only zeros.
    """

    # Initialize sets to store unique row and column indices with non-zero values
    non_zero_rows = set()
    non_zero_cols = set()

    # Get grid dimensions
    num_rows = len(input_grid)
    if num_rows == 0:
        return [] # Handle empty input grid
    num_cols = len(input_grid[0])
    if num_cols == 0:
         return [] # Handle grid with empty rows

    # Iterate through each cell of the input grid
    for r in range(num_rows):
        for c in range(num_cols):
            # If the cell value is not zero, record its row and column index
            if input_grid[r][c] != 0:
                non_zero_rows.add(r)
                non_zero_cols.add(c)

    # Calculate the number of unique rows and columns containing non-zero values
    num_active_rows = len(non_zero_rows)
    num_active_cols = len(non_zero_cols)

    # Determine the target length for the output row
    # It's the minimum of the count of active rows and active columns
    output_length = min(num_active_rows, num_active_cols)

    # Create the output row filled with zeros
    output_row = [0] * output_length

    # Return the resulting output row
    return output_row