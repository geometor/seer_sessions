"""
Transformation Rule:
1. Identify isolated non-white pixels in the input grid. An isolated pixel is defined as a non-white pixel whose immediate left and right neighbors are both white (0).
2. For each identified isolated pixel:
    a. Determine its color.
    b. Expand this pixel horizontally into a 1x3 block of the same color, centered at the original pixel's position. This means the pixel itself and its immediate left and right neighbors in the output grid will take on the color of the isolated pixel.
3. Pixels that are not identified as isolated non-white pixels, or pixels that are not overwritten by the expansion process, retain their original color from the input grid.
"""

import copy

def transform(input_grid):
    """
    Transforms the input grid by expanding isolated non-white pixels into 1x3 blocks.

    Args:
        input_grid (list): A 1D list representing a row of pixels (integers 0-9).

    Returns:
        list: The transformed 1D list representing the output row.
    """
    
    # Initialize output_grid as a copy of the input grid to preserve original values
    output_grid = copy.deepcopy(input_grid)
    grid_length = len(input_grid)

    # Iterate through the input grid, checking for isolated pixels
    # We need to check neighbors, so iterate from index 1 up to (but not including) length-1
    for i in range(1, grid_length - 1):
        
        # Get the current pixel and its immediate neighbors from the *input* grid
        current_pixel = input_grid[i]
        left_neighbor = input_grid[i - 1]
        right_neighbor = input_grid[i + 1]

        # Check if the current pixel is non-white (not 0)
        is_non_white = current_pixel != 0
        # Check if both neighbors are white (0), indicating it's isolated
        is_isolated = left_neighbor == 0 and right_neighbor == 0

        # If it's an isolated non-white pixel, apply the transformation
        if is_non_white and is_isolated:
            # Get the color of the isolated pixel
            color_to_expand = current_pixel
            
            # Expand the pixel in the *output* grid: update the pixel itself and its neighbors
            # This overwrites the original pixel and its white neighbors
            output_grid[i - 1] = color_to_expand
            output_grid[i] = color_to_expand
            output_grid[i + 1] = color_to_expand

    # Return the modified grid
    return output_grid
