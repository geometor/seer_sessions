import copy

"""
Transforms a 3x3 grid by shifting each row down by one position, with the bottom row wrapping around to the top.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a circular downward shift to the rows of the input grid.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A new 3x3 list of lists representing the transformed grid.
    """

    # Ensure the input is a 3x3 grid (optional, based on problem constraints)
    if not input_grid or len(input_grid) != 3 or not all(len(row) == 3 for row in input_grid):
        # Handle invalid input if necessary, though examples suggest fixed size
        # For this task, we assume valid 3x3 input based on examples.
        pass 

    # Get the number of rows (which is 3 for this task)
    num_rows = len(input_grid)

    # Create a new grid to store the result, avoiding modification of the input
    # Initialize with the same structure/dimensions
    output_grid = [[0 for _ in range(len(input_grid[0]))] for _ in range(num_rows)]

    # Perform the circular downward shift
    # The row at index i in the input moves to index (i + 1) % num_rows in the output.

    # Alternative, simpler logic: Extract rows and reassemble
    
    # Get the last row from the input grid
    last_row = input_grid[num_rows - 1]

    # Get all rows except the last one from the input grid
    first_rows = input_grid[0 : num_rows - 1]

    # Construct the output grid: place the last row at the top (index 0)
    output_grid[0] = last_row
    
    # Place the remaining rows below the first row
    for i in range(len(first_rows)):
        output_grid[i + 1] = first_rows[i]
        
    # --- Original Modulo Logic (kept for reference/alternative) ---
    # for i in range(num_rows):
    #   # Calculate the target row index in the output grid
    #   target_row_index = (i + 1) % num_rows
    #   # Assign the row from the input grid to the new position in the output grid
    #   output_grid[target_row_index] = input_grid[i]
    # --- End Modulo Logic ---

    return output_grid