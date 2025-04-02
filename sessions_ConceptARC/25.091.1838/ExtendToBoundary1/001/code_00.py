import numpy as np

def find_single_object_bbox(grid):
    """
    Finds the bounding box and color of the single non-background object in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (top_row, bottom_row, left_col, right_col, color) or None if no object found.
    """
    non_background_pixels = np.where(grid > 0)
    if not non_background_pixels[0].size:
        return None  # No object found

    rows, cols = non_background_pixels
    top_row = np.min(rows)
    bottom_row = np.max(rows)
    left_col = np.min(cols)
    right_col = np.max(cols)
    
    # Assume all object pixels have the same color, get it from the first found pixel
    color = grid[rows[0], cols[0]]
    
    return top_row, bottom_row, left_col, right_col, color

def transform(input_grid):
    """
    Transforms the input grid by adding a line extending from the central point 
    of a single rectangular object to a grid edge.
    
    The line is horizontal (extending right) if the object's width is >= height.
    The line is vertical (extending down) if the object's height > width.
    The line uses the same color as the object.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    grid_height, grid_width = output_grid.shape

    # Find the single non-white rectangular object and its properties
    bbox = find_single_object_bbox(input_np)
    
    if bbox is None:
        # No object found, return the original grid
        return input_grid 
        
    top_row, bottom_row, left_col, right_col, object_color = bbox
    
    # Calculate object dimensions
    height = bottom_row - top_row + 1
    width = right_col - left_col + 1

    # Compare width and height to determine line direction
    if width >= height:
        # Draw a horizontal line to the right edge
        # Calculate the middle row of the object
        target_row = top_row + height // 2
        
        # Iterate from the column just right of the object to the grid edge
        for col in range(right_col + 1, grid_width):
            # Check if target_row is within grid bounds (should always be if object is found)
            if 0 <= target_row < grid_height:
                 output_grid[target_row, col] = object_color
                 
    else: # height > width
        # Draw a vertical line to the bottom edge
        # Calculate the middle column of the object
        target_col = left_col + width // 2
        
        # Iterate from the row just below the object to the grid edge
        for row in range(bottom_row + 1, grid_height):
             # Check if target_col is within grid bounds (should always be if object is found)
            if 0 <= target_col < grid_width:
                output_grid[row, target_col] = object_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()