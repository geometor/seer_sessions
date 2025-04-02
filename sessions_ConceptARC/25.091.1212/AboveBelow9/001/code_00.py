import numpy as np

def find_divider_row(grid):
    """Finds the row index of the solid horizontal yellow line."""
    yellow_color = 4
    num_rows, num_cols = grid.shape
    for r in range(num_rows):
        if np.all(grid[r, :] == yellow_color):
            return r
    return -1 # Should not happen based on examples, but good practice

def transform(input_grid):
    """
    Identifies a horizontal yellow line (color 4) in the input grid. 
    Creates an output grid of the same dimensions.
    Copies all pixels from the input grid to the output grid for rows at or above the yellow line's row index.
    Fills all rows below the yellow line's row index with the background color (white 0).
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_np.shape
    
    # Initialize output_grid with the background color (white 0)
    output_grid = np.zeros_like(input_np) 
    
    # Find the row index of the yellow divider line (color 4)
    divider_row = find_divider_row(input_np)
    
    # If no divider is found (edge case), return the empty grid - though problem implies it always exists
    if divider_row == -1:
        print("Warning: No divider row found.") # Or handle error as appropriate
        return output_grid.tolist() 
        
    # Copy rows from the input grid up to and including the divider row
    # Slicing includes the start index but excludes the end index, so use divider_row + 1
    output_grid[0:divider_row + 1, :] = input_np[0:divider_row + 1, :]
    
    # The rest of the output_grid is already initialized to 0 (white)
    
    # Convert back to list of lists for the required output format
    return output_grid.tolist()
