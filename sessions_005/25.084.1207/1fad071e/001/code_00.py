import numpy as np

"""
Identify all distinct 2x2 squares composed entirely of blue pixels (color 1) and count them (N_blue).
Identify all distinct 2x2 squares composed entirely of red pixels (color 2) and count them (N_red).
Compare N_blue and N_red.
If N_blue > N_red, the output is a 1x5 grid: [[1, 1, 1, 1, 0]].
If N_blue < N_red, the output is a 1x5 grid: [[1, 1, 0, 0, 0]].
The case N_blue == N_red is assumed not to occur based on the training examples.
"""

def find_2x2_squares(grid, color):
    """
    Finds and counts all non-overlapping 2x2 squares of a specific color in the grid.
    
    Args:
        grid (np.array): The input grid.
        color (int): The color of the square to search for.
        
    Returns:
        int: The number of 2x2 squares of the specified color found.
    """
    count = 0
    height, width = grid.shape
    # Iterate through possible top-left corners of a 2x2 square
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 block starting at (r, c) matches the target color
            if (grid[r, c] == color and
                grid[r+1, c] == color and
                grid[r, c+1] == color and
                grid[r+1, c+1] == color):
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid based on the relative counts of blue and red 2x2 squares.
    
    Args:
        input_grid (list of lists): The input grid containing pixel values.
        
    Returns:
        list of lists: The transformed 1x5 output grid.
    """
    # Convert input list of lists to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Count the number of blue (1) 2x2 squares
    n_blue = find_2x2_squares(grid_np, 1)
    
    # Count the number of red (2) 2x2 squares
    n_red = find_2x2_squares(grid_np, 2)
    
    # Determine the output pattern based on the comparison
    if n_blue > n_red:
        # Output pattern for more blue squares
        output_grid = np.array([[1, 1, 1, 1, 0]], dtype=int)
    elif n_blue < n_red:
        # Output pattern for more red squares (or fewer blue squares)
        output_grid = np.array([[1, 1, 0, 0, 0]], dtype=int)
    else:
        # Case where counts are equal (not expected based on examples)
        # Defaulting to one of the patterns or handle as an error
        # Based on instruction "Assume the case N_blue == N_red does not occur",
        # we can technically omit this else, but it's safer to include a fallback.
        # Let's default to the 'fewer blue' case as a placeholder.
        output_grid = np.array([[1, 1, 0, 0, 0]], dtype=int) 
        # Or raise ValueError("Equal number of blue and red squares found, case undefined.")

    # Convert the numpy array back to a list of lists for the standard output format
    return output_grid.tolist()