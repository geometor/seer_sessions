"""
Transforms the input grid based on the following rule:
1. Find the top-leftmost pixel of the orange color (7). This is the 'seed' pixel.
2. Determine the height (H) of the vertical orange line starting from the seed pixel.
3. Create an output grid of the same dimensions, initialized to white (0).
4. For each pixel (r, c) in the output grid:
   a. Calculate the Manhattan distance 'd' from the seed pixel: d = abs(r - seed_r) + abs(c - seed_c).
   b. If d < H:
      - If d is even, set the output pixel to azure (8).
      - If d is odd, set the output pixel to orange (7).
   c. Else (d >= H), leave the pixel as white (0).
"""

import numpy as np

def find_top_left_pixel(grid, color):
    """Finds the row and column of the top-most, then left-most pixel of a given color."""
    locations = np.argwhere(grid == color)
    if len(locations) == 0:
        return None  # Color not found
    # Sort by row, then by column to find the top-most, then left-most
    top_left = min(locations, key=lambda x: (x[0], x[1]))
    return tuple(top_left)

def get_vertical_line_height(grid, start_row, col, color):
    """Calculates the height of a vertical line of a specific color starting from a point."""
    height = 0
    num_rows = grid.shape[0]
    for r in range(start_row, num_rows):
        if grid[r, col] == color:
            height += 1
        else:
            break # Stop counting when the color changes or grid ends
    return height

def transform(input_grid):
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape

    # Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid_np) 

    # Define colors used in the transformation
    orange = 7
    azure = 8
    white = 0

    # 1. Find the seed pixel (top-leftmost orange)
    seed_pixel = find_top_left_pixel(input_grid_np, orange)

    # If no orange pixel is found, return the empty white grid
    if seed_pixel is None:
        return output_grid.tolist() 

    seed_r, seed_c = seed_pixel

    # 2. Determine the height H of the vertical orange line starting from the seed
    line_height = get_vertical_line_height(input_grid_np, seed_r, seed_c, orange)

    # 3 & 4. Iterate through each pixel, calculate distance, and fill the output grid
    for r in range(height):
        for c in range(width):
            # a. Calculate Manhattan distance from the seed pixel
            distance = abs(r - seed_r) + abs(c - seed_c)

            # b. Check if distance is less than the measured line height
            if distance < line_height:
                # Check the parity of the distance and assign color accordingly
                # **Correction**: Even distance -> azure (8), Odd distance -> orange (7)
                if distance % 2 == 0:
                    output_grid[r, c] = azure
                else:
                    output_grid[r, c] = orange
            # c. Else: Pixel remains white (0) as initialized

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist() 