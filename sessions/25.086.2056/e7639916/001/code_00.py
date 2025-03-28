import numpy as np

"""
Draws a blue (1) rectangular perimeter enclosing all azure (8) pixels found in the input grid. 
The perimeter is drawn only on white (0) background pixels. Original azure pixels are preserved, even if they fall on the perimeter.
"""

def find_color_coordinates(grid, color_value):
    """Finds all coordinates (row, col) of a given color in the grid."""
    rows, cols = np.where(grid == color_value)
    return list(zip(rows, cols))

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)
    
    # Define the colors
    azure_color = 8
    blue_color = 1
    white_color = 0

    # 1. Identify the coordinates of all azure (8) pixels
    azure_coords = find_color_coordinates(grid, azure_color)

    # If there are no azure pixels, return the original grid
    if not azure_coords:
        return output_grid.tolist()

    # 2. Determine the bounding box
    rows = [r for r, c in azure_coords]
    cols = [c for r, c in azure_coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # 3. & 4. Iterate through the cells along the perimeter of the bounding box
    # Draw top and bottom edges
    for col in range(min_col, max_col + 1):
        # 5. Check if the input cell is white (0)
        if grid[min_row, col] == white_color:
            # 6. Change its color to blue (1) in the output grid
            output_grid[min_row, col] = blue_color
        if grid[max_row, col] == white_color:
            output_grid[max_row, col] = blue_color
            
    # Draw left and right edges (excluding corners already drawn)
    for row in range(min_row + 1, max_row):
        # 5. Check if the input cell is white (0)
        if grid[row, min_col] == white_color:
            # 6. Change its color to blue (1) in the output grid
            output_grid[row, min_col] = blue_color
        if grid[row, max_col] == white_color:
            output_grid[row, max_col] = blue_color

    # 7. Original azure pixels and other pixels are already preserved due to copying initially.

    # Convert back to list of lists before returning
    return output_grid.tolist()
