import numpy as np

"""
Identify the bounding box of all blue (1) pixels in the input grid.
If the height of the bounding box is strictly greater than its width, 
fill the rightmost column of the output grid with green (3).
Otherwise (if height is less than or equal to width), fill the topmost 
row of the output grid with green (3). The rest of the output grid 
retains the corresponding pixels from the input grid. If there are no 
blue pixels, the output grid is identical to the input grid.
"""

def find_pixel_coordinates(grid, color_value):
    """Finds the row and column indices of all pixels with a specific color."""
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def calculate_bounding_box(coordinates):
    """Calculates the bounding box dimensions from a list of coordinates."""
    if not coordinates:
        return None, None, None, None # Or handle as 0 height/width later

    rows = [r for r, c in coordinates]
    cols = [c for r, c in coordinates]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    return height, width, min_r, max_r, min_c, max_c


def transform(input_grid):
    """
    Applies the transformation rule based on the bounding box of blue pixels.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = grid_np.copy()
    
    # Find coordinates of all blue pixels (value 1)
    blue_coordinates = find_pixel_coordinates(grid_np, 1)
    
    # If no blue pixels are found, return the original grid copy
    if not blue_coordinates:
        return output_grid.tolist() # Return as list of lists

    # Calculate the bounding box dimensions
    height, width, _, _, _, _ = calculate_bounding_box(blue_coordinates)
    
    # Get grid dimensions
    grid_height, grid_width = output_grid.shape

    # Apply the transformation rule based on height vs width
    if height > width:
        # Fill the rightmost column (index grid_width - 1) with green (3)
        output_grid[:, grid_width - 1] = 3
    else: # height <= width
        # Fill the topmost row (index 0) with green (3)
        output_grid[0, :] = 3
        
    # Convert back to list of lists for the standard ARC format
    return output_grid.tolist()