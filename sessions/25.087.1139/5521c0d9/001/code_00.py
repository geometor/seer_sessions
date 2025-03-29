import numpy as np

"""
Identify each distinct non-background colored object in the input grid.
For each object, calculate its height (the number of rows it spans).
Create an output grid initialized with the background color (white, 0).
Move each object vertically upwards by a number of rows equal to its calculated height.
Draw the moved objects onto the output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by moving each colored object upwards.
    
    The amount each object moves upwards is equal to its height (number of rows it spans).
    
    Args:
        input_grid (list of list of int): The input grid representing colors.
        
    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    
    # Initialize output grid with background color (0)
    # Using the same dimensions and data type as the input
    output_array = np.zeros_like(input_array)
    
    # Find unique non-background colors present in the input grid
    # Exclude 0 (background) from the unique values
    unique_colors = np.unique(input_array[input_array != 0])
    
    # Process each unique color found
    for color in unique_colors:
        # Find all coordinates (pixels) where the input grid has the current color
        coords = np.argwhere(input_array == color)
        
        # Proceed only if coordinates were found for this color
        if coords.size > 0:
            # Extract the row indices from the coordinates
            current_rows = coords[:, 0]
            # Extract the column indices from the coordinates
            current_cols = coords[:, 1]
            
            # Determine the vertical span (height) of the object
            min_row = np.min(current_rows)
            max_row = np.max(current_rows)
            height = max_row - min_row + 1
            
            # The vertical shift amount is equal to the object's height
            # Positive shift means moving upwards (decreasing row index)
            shift = height
            
            # Calculate the new row indices after applying the upward shift
            new_rows = current_rows - shift
            
            # --- Boundary Check (Optional based on ARC constraints, but safer) ---
            # Identify indices where the new row position is still within the grid (>= 0)
            # Assumes objects do not wrap around or go out of bounds based on examples
            # valid_indices = new_rows >= 0
            # Filter coordinates to keep only those that remain within grid bounds
            # valid_new_rows = new_rows[valid_indices]
            # valid_cols = current_cols[valid_indices]
            # ---------------------------------------------------------------------
            
            # Place the pixels of the moved object onto the output grid
            # Uses advanced indexing: output_array[row_indices, col_indices] = value
            # Directly use new_rows and current_cols, assuming they stay within bounds as per examples
            # If boundary checks were enabled, use valid_new_rows and valid_cols instead.
            output_array[new_rows, current_cols] = color

    # Convert the resulting numpy array back to a list of lists format
    output_grid = output_array.tolist()
    
    return output_grid