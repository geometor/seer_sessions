import copy

"""
Creates a copy of the input grid. Iterates through each pixel of the input grid, 
excluding the first and last columns. For each pixel, checks if it is non-white (not 0) 
and if its immediate left and right neighbors are both white (0). If these conditions 
are met, it modifies the corresponding pixels in the output grid: the pixel itself, 
its left neighbor, and its right neighbor are all set to the color of the original 
non-white pixel. Finally, returns the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rule:
    Expand isolated non-white pixels into horizontal lines of three, centered on the original pixel.
    Existing horizontal lines of three or more non-white pixels remain unchanged.
    """
    # Since the input is a single row (a list), create a shallow copy.
    # If it were a 2D grid (list of lists), a deepcopy would be safer.
    output_grid = list(input_grid) 
    
    # Get the width of the grid (length of the list)
    width = len(input_grid)

    # Iterate through the pixels, skipping the first and last columns
    # as they cannot be the center of a 3-pixel expansion.
    for i in range(1, width - 1):
        # Get the color of the current pixel and its neighbors
        center_color = input_grid[i]
        left_color = input_grid[i-1]
        right_color = input_grid[i+1]

        # Check if the current pixel is non-white (not 0)
        # and its immediate horizontal neighbors are white (0)
        if center_color != 0 and left_color == 0 and right_color == 0:
            # If it's an isolated pixel, expand it horizontally in the output grid
            output_grid[i-1] = center_color
            output_grid[i] = center_color
            output_grid[i+1] = center_color
            
    # Return the modified grid
    return output_grid
