import copy

def transform(input_grid):
    """
    Transforms the input grid by applying specific color substitutions:
    - Gray (5) pixels become Yellow (4).
    - Orange (7) pixels become Gray (5).
    - All other colors (White (0), Yellow (4)) remain unchanged.
    The transformation is applied pixel by pixel, preserving the grid dimensions.
    """

    # Get the dimensions of the input grid
    height = len(input_grid)
    width = len(input_grid[0])

    # Create a deep copy of the input grid to modify, 
    # ensuring other colors are preserved by default.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_grid[r][c]

            # Apply the color transformation rules
            if pixel_color == 5:  # If pixel is Gray
                output_grid[r][c] = 4  # Change it to Yellow
            elif pixel_color == 7:  # If pixel is Orange
                output_grid[r][c] = 5  # Change it to Gray
            # No need for an 'else' clause because we started with a copy,
            # so pixels that don't match these conditions already have the correct color.

    # Return the transformed grid
    return output_grid