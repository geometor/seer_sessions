import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Find all horizontal sequences of three consecutive orange (7) pixels.
    2. For each sequence found at columns c, c+1, c+2 in a given row r:
       - Change the pixel at (r, c) to gray (8).
       - Change the pixel at (r, c+1) to magenta (6).
       - Change the pixel at (r, c+2) to gray (8).
    3. All other pixels remain unchanged.
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Get the dimensions of the grid
    height, width = input_np.shape
    
    # Iterate through each row
    for r in range(height):
        # Iterate through columns, checking for the sequence '7 7 7'
        # Stop at width - 3 to avoid index out of bounds when checking c+1 and c+2
        for c in range(width - 2):
            # Check if the current pixel and the next two are orange (7)
            if input_np[r, c] == 7 and input_np[r, c+1] == 7 and input_np[r, c+2] == 7:
                # Apply the transformation to the output grid
                output_grid[r, c]   = 8  # Change first 7 to gray (8)
                output_grid[r, c+1] = 6  # Change middle 7 to magenta (6)
                output_grid[r, c+2] = 8  # Change last 7 to gray (8)
                
                # Optional: Skip the next two columns as they've been processed
                # This avoids potential overlapping modifications if sequences could overlap,
                # although in this specific rule (777 -> 868), overlaps like 7777 are not an issue.
                # c += 2 # No need here, the outer loop takes care of advancing c.

    # Return the modified grid as a list of lists
    return output_grid.tolist()
