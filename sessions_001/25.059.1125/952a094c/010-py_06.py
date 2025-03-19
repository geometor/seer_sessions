"""
The transformation identifies a hollow orange frame within the grid. It then extracts the colors of the pixels inside the frame, which are not white or orange. Finally, it swaps the colors of the pixels from the inner corners of the frame, with a predefined mapping.
"""

import numpy as np

def find_frame(grid, frame_color=7):
    rows, cols = grid.shape
    top_left = None
    bottom_right = None

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == frame_color:
                if top_left is None:
                    top_left = (r, c)
                bottom_right = (r, c)
    return top_left, bottom_right

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the orange frame
    top_left, bottom_right = find_frame(input_grid)
    if top_left is None:
        return output_grid # early exit if no frame found

    # Extract inner colors
    inner_colors = []
    inner_positions = []

    # only works if the frame is only 1 pixel thick, check the diagonals
    if (input_grid[top_left[0]+1, top_left[1]+1] != 7):

      inner_positions = [(top_left[0], top_left[1]), (top_left[0], bottom_right[1]),
                        (bottom_right[0], top_left[1]),(bottom_right[0], bottom_right[1])]
      inner_colors = [input_grid[pos] for pos in inner_positions if input_grid[pos] != 7 and input_grid[pos] != 0]

      # Define swap positions
      # mapping based on observation in the example
      swap_positions = [(top_left[0]-2, bottom_right[1]-1), (top_left[0]-2, top_left[1]+1),
                      (bottom_right[0]-1, bottom_right[1]-1), (bottom_right[0]-1,top_left[1]+1 )]

      # swap the color values at the inner positions
      for i in range(len(swap_positions)):
        if (i < len(inner_colors)):
          output_grid[swap_positions[i]] = inner_colors[i]
        else:
          # set to white if no pixel to swap
          output_grid[swap_positions[i]] = 0
    return output_grid