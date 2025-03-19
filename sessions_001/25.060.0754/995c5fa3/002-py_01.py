"""
The transformation rule identifies the arrangement of white (0) pixels within a grey (5) background input grid.
The arrangement of these white pixels determines a single color. A 3x3 output grid is then created and filled entirely with this determined color.
"""

import numpy as np

def get_white_pixel_positions(grid):
    """Finds the positions of white pixels (value 0) in the grid."""
    return np.argwhere(grid == 0)

def determine_color(white_pixel_positions, input_grid):
    """Determines the output color based on the white pixel pattern."""
    num_white_pixels = len(white_pixel_positions)
    rows, cols = input_grid.shape

    if num_white_pixels == 4:
        #check if 4 in a L shape
        if(white_pixel_positions[0][1] == white_pixel_positions[1][1] == white_pixel_positions[2][1] == white_pixel_positions[3][1]):
            return 4

        if (white_pixel_positions[0][0] + 1 == white_pixel_positions[1][0] and
            white_pixel_positions[0][1] == white_pixel_positions[1][1] and
            white_pixel_positions[2][0] + 1 == white_pixel_positions[3][0] and
            white_pixel_positions[2][1] == white_pixel_positions[3][1]):
               if (white_pixel_positions[1][1] + 1 == white_pixel_positions[2][1] ):
                return 8

    if num_white_pixels == 3:
        if(white_pixel_positions[0][1] == white_pixel_positions[1][1] and
            white_pixel_positions[0][0] + 1 == white_pixel_positions[1][0] and
            white_pixel_positions[1][1] < white_pixel_positions[2][1] and
            white_pixel_positions[1][0]  == white_pixel_positions[2][0]

           ):

            return 3

    if num_white_pixels > 0:

        if (white_pixel_positions[0][0] + 1 == white_pixel_positions[1][0] and
                white_pixel_positions[0][1] == white_pixel_positions[1][1] ):

            return 2



    return None  # Default case if no pattern is recognized.


def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find white pixel positions
    white_pixel_positions = get_white_pixel_positions(input_grid)

    # Determine output color
    output_color = determine_color(white_pixel_positions, input_grid)

   # Fill output grid with determined color.
    if output_color is not None:
      output_grid[:] = output_color

    return output_grid