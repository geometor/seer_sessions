import copy

"""
Transforms an input grid by horizontally mirroring all non-white pixels 
across the grid's vertical centerline. The original pixels remain, and 
their mirrored copies are added to the grid.

1. Initialize the output grid as an exact copy of the input grid.
2. Determine the width of the grid.
3. Iterate through each pixel of the input grid at position (row, column).
4. If the pixel's color is not white (value is not 0):
    a. Calculate the mirrored column index: mirrored_column = grid_width - 1 - column.
    b. Update the pixel in the output grid at position (row, mirrored_column) 
       with the same color as the input pixel at (row, column).
5. Return the final output grid containing both original and mirrored non-white shapes.
"""

def transform(input_grid):
    """
    Mirrors non-white pixels horizontally across the vertical centerline.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A new 2D list representing the output grid with mirrored shapes.
    """
    # Determine the dimensions of the grid
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)] # Return grid of empty rows if width is 0

    # Initialize the output_grid as a deep copy of the input_grid
    # This ensures the original pixels are preserved and we don't modify the input directly
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            color = input_grid[r][c]

            # Check if the pixel is not white (color 0)
            if color != 0:
                # Calculate the mirrored column index
                mirrored_c = width - 1 - c

                # Update the pixel at the mirrored position in the output grid
                # with the color of the original pixel
                # Ensure the mirrored column is within bounds (it always should be by calculation)
                if 0 <= mirrored_c < width:
                     output_grid[r][mirrored_c] = color

    # Return the final grid with original and mirrored non-white pixels
    return output_grid