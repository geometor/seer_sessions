import numpy as np

"""
1. Scan the input grid to find the horizontal line composed entirely of magenta (6) pixels.
2. Identify the 2x2 square object located in the region of the grid *above* the magenta line.
3. Create a new 2x2 grid.
4. Fill the new 2x2 grid with the color of the square identified in step 2. This new grid is the output.
"""

def find_magenta_line_row(grid):
    """Finds the row index of the horizontal magenta line."""
    num_rows, num_cols = grid.shape
    for r in range(num_rows):
        if np.all(grid[r, :] == 6):
            return r
    return -1 # Indicate not found

def find_colored_square_above(grid, magenta_row_index):
    """Finds the 2x2 square above the magenta line."""
    num_rows, num_cols = grid.shape
    # Search only in the region above the magenta line
    for r in range(magenta_row_index - 1): # Stop before the line itself, need space for 2x2
        for c in range(num_cols - 1): # Stop before the last column, need space for 2x2
            # Check if top-left pixel is non-white and non-magenta
            color = grid[r, c]
            if color != 0 and color != 6:
                # Check if it forms a 2x2 square of the same color
                if (grid[r+1, c] == color and
                    grid[r, c+1] == color and
                    grid[r+1, c+1] == color):
                    return color # Return the color of the square
    return None # Indicate not found


def transform(input_grid):
    """
    Transforms the input grid by finding a magenta horizontal separator line,
    locating a 2x2 colored square above the line, and returning a 2x2 grid
    filled with the color of that square.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)
    
    # Find the row index of the magenta line
    magenta_row = find_magenta_line_row(input_array)
    if magenta_row == -1:
        # Handle error: magenta line not found (though not expected based on examples)
        print("Error: Magenta line not found.")
        return None 

    # Find the color of the 2x2 square above the magenta line
    square_color = find_colored_square_above(input_array, magenta_row)
    
    if square_color is None:
         # Handle error: square not found (though not expected based on examples)
        print("Error: Square above magenta line not found.")
        return None

    # Initialize the output grid as a 2x2 array
    output_grid = np.full((2, 2), square_color, dtype=int)

    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
