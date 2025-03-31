import numpy as np

"""
Transformation rule:
1. Find all red (2) pixels in the input grid.
2. For each red pixel at position (r, c):
   a. Extend lines horizontally (left/right) and vertically (up/down) from the red pixel's neighbors.
   b. The extension only modifies pixels that were originally white (0) in the input grid.
   c. The color used for extension in a specific direction is determined by the color of the neighbor of the red pixel in that direction in the *original* input grid:
      - If the neighbor is green (3), the extension color is green (3).
      - If the neighbor is white (0) or the red pixel is at the edge (neighbor is off-grid), the extension color is red (2).
   d. The extension in each direction continues until it hits a non-white pixel (from the original input grid) or the grid boundary.
3. Modifications from all red pixels are combined onto a copy of the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify for the output
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define color constants
    WHITE = 0
    RED = 2
    GREEN = 3

    # Find all red pixels
    red_pixels = np.argwhere(input_np == RED)

    # Helper function to safely get neighbor color
    def get_neighbor_color(grid, r, c):
        if 0 <= r < height and 0 <= c < width:
            return grid[r, c]
        else:
            return WHITE # Treat off-grid as white

    # Process each red pixel
    for r, c in red_pixels:

        # --- Horizontal Extensions ---

        # Left Extension
        left_neighbor_color = get_neighbor_color(input_np, r, c - 1)
        fill_color_left = GREEN if left_neighbor_color == GREEN else RED
        for cc in range(c - 1, -1, -1): # Iterate leftwards from neighbor
            if input_np[r, cc] == WHITE: # Check original grid pixel
                output_np[r, cc] = fill_color_left # Update output grid
            else:
                break # Stop extension if non-white pixel encountered

        # Right Extension
        right_neighbor_color = get_neighbor_color(input_np, r, c + 1)
        fill_color_right = GREEN if right_neighbor_color == GREEN else RED
        for cc in range(c + 1, width): # Iterate rightwards from neighbor
            if input_np[r, cc] == WHITE: # Check original grid pixel
                output_np[r, cc] = fill_color_right # Update output grid
            else:
                break # Stop extension

        # --- Vertical Extensions ---

        # Up Extension
        up_neighbor_color = get_neighbor_color(input_np, r - 1, c)
        fill_color_up = GREEN if up_neighbor_color == GREEN else RED
        for rr in range(r - 1, -1, -1): # Iterate upwards from neighbor
            if input_np[rr, c] == WHITE: # Check original grid pixel
                output_np[rr, c] = fill_color_up # Update output grid
            else:
                break # Stop extension

        # Down Extension
        down_neighbor_color = get_neighbor_color(input_np, r + 1, c)
        fill_color_down = GREEN if down_neighbor_color == GREEN else RED
        for rr in range(r + 1, height): # Iterate downwards from neighbor
            if input_np[rr, c] == WHITE: # Check original grid pixel
                output_np[rr, c] = fill_color_down # Update output grid
            else:
                break # Stop extension

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid
