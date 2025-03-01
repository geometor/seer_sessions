"""
Expands each non-zero pixel in the input grid into a cross-shaped pattern in the output grid. The center of the cross retains the original pixel's color. The outline of the '+' uses color 4(yellow) if it's within the first 4 rows and columns of the input, and uses orange(7) otherwise.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            # Find non-zero pixels
            if input_grid[r, c] != 0:
                # Get the center color
                center_color = input_grid[r, c]

                # Determine outline color based on position
                outline_color = 4 if r < 4 and c < 4 else 7
                if r < 4 and c >= 5:
                    outline_color = 7
                if r >=5 and c < 4:
                    outline_color = 7
                if r >= 5 and c>=5:
                    outline_color=7


                # Create the cross pattern
                output_grid[r, c] = center_color  # Center

                if r > 0:
                   output_grid[r - 1, c] = outline_color if input_grid[r-1,c] == 0 else output_grid[r-1,c]  # Top
                if r < output_grid.shape[0] - 1:
                    output_grid[r + 1, c] = outline_color if input_grid[r+1, c] == 0 else output_grid[r + 1, c] # Bottom
                if c > 0:
                    output_grid[r, c - 1] = outline_color if input_grid[r,c-1] == 0 else output_grid[r, c - 1] # Left
                if c < output_grid.shape[1] - 1:
                    output_grid[r, c + 1] = outline_color if input_grid[r,c+1] == 0 else output_grid[r,c+1] # Right

    return output_grid