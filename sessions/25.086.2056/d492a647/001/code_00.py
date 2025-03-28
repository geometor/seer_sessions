import numpy as np

"""
Transforms the input grid by identifying a unique 'target' pixel (neither white=0 nor gray=5), 
determining the parity (even/odd) of its row and column coordinates, and then changing 
all white (0) pixels in the grid to the target pixel's color if and only if their 
row and column parities match those of the target pixel. All other pixels retain 
their original color.
"""

def find_target_pixel(grid):
    """
    Finds the unique pixel in the grid that is not white (0) or gray (5).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (target_color, target_row, target_col) if found, else (None, -1, -1).
    """
    target_color = None
    target_row, target_col = -1, -1
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != 5:
                # Assuming there's exactly one such pixel per the task description
                target_color = color
                target_row = r
                target_col = c
                return target_color, target_row, target_col
    return target_color, target_row, target_col # Should ideally not happen based on examples

def transform(input_grid):
    """
    Applies the parity-based color transformation to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Find the target pixel's color and coordinates
    target_color, target_row, target_col = find_target_pixel(input_np)
    
    # If no target pixel is found (edge case, shouldn't happen based on examples), return the copy
    if target_color is None:
        return output_grid.tolist()
        
    # Determine the required parity for rows and columns based on the target pixel
    required_row_parity = target_row % 2
    required_col_parity = target_col % 2
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if input_np[r, c] == 0:
                # Check if the current pixel's row and column parities match the required parities
                current_row_parity = r % 2
                current_col_parity = c % 2
                
                if current_row_parity == required_row_parity and current_col_parity == required_col_parity:
                    # If all conditions are met, change the color in the output grid
                    output_grid[r, c] = target_color
                    
    # Convert the result back to a list of lists before returning
    return output_grid.tolist()
