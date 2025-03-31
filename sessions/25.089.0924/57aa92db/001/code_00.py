import numpy as np

"""
Identifies pairs of adjacent, non-white pixels where one color's index is greater than the other. 
For each such pair, the pixel with the lower color index ('target') triggers an expansion. 
The expansion fills any white (0) pixels within the 3x3 neighborhood centered on the 'target' pixel with the color of the adjacent pixel having the higher index ('expander'). 
This process is applied based on the state of the original input grid, modifying a copy which becomes the output. 
Pixels that are not white in the input grid retain their original color.
"""

def transform(input_grid):
    """
    Applies the expansion transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each cell (r, c) of the input grid
    for r in range(height):
        for c in range(width):
            color_b = input_grid[r, c]

            # Skip if the current cell is white (background)
            if color_b == 0:
                continue

            # Check cardinal neighbors (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # Check if the neighbor is within grid boundaries
                if 0 <= nr < height and 0 <= nc < width:
                    color_a = input_grid[nr, nc]

                    # Check if neighbor is non-white, different from current cell, and has a higher index
                    if color_a != 0 and color_a != color_b and color_a > color_b:
                        # color_b at (r, c) is the 'target', color_a is the 'expander'
                        
                        # Iterate through the 3x3 neighborhood centered at the target (r, c)
                        for tr_offset in range(-1, 2):
                            for tc_offset in range(-1, 2):
                                tr, tc = r + tr_offset, c + tc_offset

                                # Check if the neighborhood cell is within grid boundaries
                                if 0 <= tr < height and 0 <= tc < width:
                                    # Check if the cell in the original input grid is white
                                    if input_grid[tr, tc] == 0:
                                        # Update the corresponding cell in the output grid with the expander color
                                        output_grid[tr, tc] = color_a
                                        
    return output_grid
