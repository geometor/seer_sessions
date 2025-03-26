import numpy as np

"""
Transforms the input grid by first changing all blue (1) pixels to red (2) pixels, 
leaving white (0) pixels unchanged. Then, it appends the top half of this modified grid 
to its bottom, effectively increasing the grid's height by 50%.
"""

def transform(input_grid):
    """
    Applies a color change and vertical extension transformation to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid containing pixels 
                                                   represented by integers (0-9).

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input grid to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # --- Step 1: Color Transformation ---
    # Create a copy to store the color-transformed grid
    intermediate_grid = grid.copy()
    
    # Replace all blue (1) pixels with red (2) pixels
    # This uses boolean indexing for efficiency
    intermediate_grid[intermediate_grid == 1] = 2
    
    # --- Step 2: Structural Transformation ---
    # Get the height (number of rows) of the input grid
    input_height = intermediate_grid.shape[0]
    
    # Calculate the number of rows to append (top half)
    # Ensure integer division
    rows_to_append_count = input_height // 2
    
    # Extract the top portion (first 'rows_to_append_count' rows)
    top_portion = intermediate_grid[:rows_to_append_count, :]
    
    # --- Step 3: Concatenation ---
    # Vertically stack the intermediate grid and the extracted top portion
    output_grid = np.vstack((intermediate_grid, top_portion))

    return output_grid
