import numpy as np

"""
Identifies the location of the single red (2) pixel in the input grid.
Creates an output grid of the same size, filled with gray (6).
Places a 2x2 square of red (2) pixels in the output grid.
The top-left corner of the 2x2 red square is positioned at row 2 and column (c-1), 
where 'c' is the column index of the red pixel found in the input grid.
"""

def find_color_coordinates(grid, color):
    """
    Finds the coordinates of the first pixel with the specified color.
    Assumes exactly one such pixel exists.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        tuple: A tuple (row, col) of the pixel coordinates, or None if not found.
    """
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        return tuple(coords[0])
    return None

def transform(input_grid):
    """
    Transforms the input grid based on the location of the red pixel.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Define colors
    background_color = 6
    target_color = 2
    
    # Initialize output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Locate the single red (2) pixel in the input grid
    red_pixel_coords = find_color_coordinates(input_grid, target_color)

    if red_pixel_coords:
        # Extract the column index of the red pixel
        input_row, input_col = red_pixel_coords
        
        # Determine the top-left coordinate for the 2x2 square in the output grid
        # The rule derived from examples is: row = 2, col = input_col - 1
        output_square_row_start = 2
        output_square_col_start = input_col - 1
        
        # Define the boundaries of the 2x2 square
        row_end = output_square_row_start + 2
        col_end = output_square_col_start + 2

        # Check if the square fits within the grid boundaries (although examples suggest it always will)
        if 0 <= output_square_row_start < height and 0 <= output_square_col_start < width and \
           row_end <= height and col_end <= width:
            # Change the color of the 2x2 area in the output grid to red (2)
            output_grid[output_square_row_start:row_end, output_square_col_start:col_end] = target_color
        else:
            # Handle cases where the square might go out of bounds, though not expected based on examples
            # For robustness, we could clip or just skip drawing if it doesn't fit.
            # Based on the problem structure, it's likely guaranteed to fit.
            print(f"Warning: Calculated square position ({output_square_row_start},{output_square_col_start}) might be out of bounds.")


    return output_grid