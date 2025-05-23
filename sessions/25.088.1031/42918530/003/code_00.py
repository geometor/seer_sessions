import numpy as np

"""
The transformation identifies white pixels (0) enclosed within shapes made of a single other color. 
If a white pixel has exactly two orthogonal neighbors of the *enclosing* color, it is changed to that enclosing color. 
Otherwise, it remains white (0). Non-white pixels are unchanged.
"""

def find_neighbors(r, c, height, width):
    """Yields coordinates of 4 orthogonal neighbors within grid bounds."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def transform(input_grid):
    """
    Transforms the input grid based on the neighbor rule.

    For each white pixel (0) in the input grid:
    1. Check its four orthogonal neighbors.
    2. Count the number of non-white neighbors and identify their unique colors.
    3. If there are exactly two non-white neighbors AND they both have the SAME color,
       change the white pixel to that color in the output grid.
    4. Otherwise, the pixel remains white (or its original color if not white).
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = np.copy(input_grid_np)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0)
            if input_grid_np[r, c] == 0:
                
                non_white_neighbor_colors = []
                # Check orthogonal neighbors
                for nr, nc in find_neighbors(r, c, height, width):
                    neighbor_color = input_grid_np[nr, nc]
                    # If neighbor is not white, record its color
                    if neighbor_color != 0:
                        non_white_neighbor_colors.append(neighbor_color)
                
                # Check the conditions for changing the color
                # Condition 1: Exactly two non-white neighbors
                if len(non_white_neighbor_colors) == 2:
                    # Condition 2: Both non-white neighbors have the same color
                    fill_color = non_white_neighbor_colors[0]
                    if non_white_neighbor_colors[1] == fill_color:
                         # If both conditions met, change the pixel in the output grid
                        output_grid[r, c] = fill_color
            
            # If the pixel is not white, or if the conditions are not met for a white pixel,
            # it remains unchanged (already copied to output_grid).

    # Return the transformed grid as a list of lists
    return output_grid.tolist()