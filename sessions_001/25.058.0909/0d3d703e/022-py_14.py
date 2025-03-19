"""
The transformation rule is a direct color substitution.  The following mapping is applied consistently across all input pixels:

1.  Maroon (9) is replaced with Azure (8).
2.  Yellow (4) is replaced with Green (3).
3.  Red (2) is replaced with Magenta (6).
4.  All other colors remain unchanged.

The size and shape of the grid do not change. The transformation operates on each pixel independently, based solely on its initial color value.
"""

def transform(input_grid):
    """
    Applies a color substitution to the input grid based on a predefined mapping.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = [row[:] for row in input_grid]

    # Define the color mapping.
    color_map = {
        9: 8,
        4: 3,
        2: 6,
    }

    # Iterate through each cell of the grid.
    for i in range(len(output_grid)):
        for j in range(len(output_grid[0])):
            # Check if the current color is in the mapping.
            if output_grid[i][j] in color_map:
                # Apply the color substitution.
                output_grid[i][j] = color_map[output_grid[i][j]]

    return output_grid