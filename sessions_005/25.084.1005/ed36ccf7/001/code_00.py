import copy

"""
The transformation rule rotates the input grid 270 degrees clockwise (or 90 degrees counter-clockwise).
The value of the pixel at input grid coordinates (row `r`, column `c`) is moved 
to the output grid coordinates (row `c`, column `W-1-r`), where `W` is the width 
of the input grid.
"""

def transform(input_grid):
    """
    Rotates the input grid 270 degrees clockwise.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the rotated output grid.
    """
    # Get the dimensions of the input grid
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)] # Return empty rows if width is 0

    # Initialize the output grid with the dimensions swapped (width x height)
    # but since it's a rotation of a square grid in this task, 
    # the output dimensions will be the same (height x width)
    # The new grid will have 'width' rows and 'height' columns after rotation.
    # However, the formula output[c][W-1-r] implies the output grid should have
    # dimensions W x H (width rows, height columns). Let's stick to H x W 
    # for standard representation and adjust the formula access if needed.
    # Wait, the formula output[c][W-1-r] means the new row index is 'c' (0 to W-1)
    # and the new column index is 'W-1-r' (0 to H-1).
    # So the output grid has dimensions W x H.
    
    output_grid_height = width
    output_grid_width = height
    
    # Initialize output grid with placeholder value (e.g., 0)
    output_grid = [[0 for _ in range(output_grid_width)] for _ in range(output_grid_height)]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the value from the input grid
            value = input_grid[r][c]
            
            # Calculate the corresponding coordinates in the output grid
            # for a 270-degree clockwise rotation
            output_r = c
            output_c = height - 1 - r # Use height here as it relates to the 'r' index range

            # Place the value into the output grid
            output_grid[output_r][output_c] = value

    return output_grid
