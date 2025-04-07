import numpy as np

"""
Transforms an input 5x5 binary grid into an output 5x5 binary grid.
The output grid contains a single diagonal sequence of 1s starting from the
position of the first '1' encountered in the input grid when scanning
top-to-bottom, then left-to-right. All other cells in the output grid are 0.
If the input grid contains only 0s, the output grid also contains only 0s.
"""

def find_first_one(grid):
    """
    Finds the coordinates (row, col) of the first '1' in the grid.
    Scans row by row, then column by column.
    Returns (None, None) if no '1' is found.
    """
    rows = len(grid)
    if rows == 0:
        return None, None
    cols = len(grid[0])
    if cols == 0:
        return None, None
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                return r, c  # Return coordinates of the first '1' found
    return None, None # Return None if no '1' is found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Assuming input_grid is a list of lists
    rows = len(input_grid)
    if rows == 0:
        return [] # Handle empty input
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle rows with empty columns

    # Initialize output_grid with zeros using numpy for convenience
    output_grid_np = np.zeros((rows, cols), dtype=int)

    # Find the starting coordinates (r_start, c_start) of the first '1'
    r_start, c_start = find_first_one(input_grid)

    # If a '1' was found in the input grid
    if r_start is not None and c_start is not None:
        # Iterate diagonally from the start cell
        i = 0
        while True:
            # Calculate current diagonal cell coordinates
            r_diag, c_diag = r_start + i, c_start + i
            
            # Check if the coordinates are within the grid bounds
            if 0 <= r_diag < rows and 0 <= c_diag < cols:
                # Set the corresponding cell in the output grid to 1
                output_grid_np[r_diag, c_diag] = 1
                # Move to the next diagonal cell
                i += 1
            else:
                # Stop if coordinates go out of bounds
                break
                
    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid
