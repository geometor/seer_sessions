"""
Transforms the input grid based on the following rule:
1. Initialize the output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2. Find the coordinates (seed_row, seed_col) of the top-most, left-most pixel with the seed color (orange, 7) in the input grid. If no such pixel exists, return the initialized white grid.
3. Determine the parameter H by measuring the height of the continuous vertical line of the seed color (orange, 7) starting downwards from the seed pixel.
4. For each pixel at position (row, col) in the grid:
    a. Calculate the Manhattan distance `d` between (row, col) and (seed_row, seed_col).
    b. Calculate the absolute row difference `dr` between `row` and `seed_row`.
    c. If `d` is less than H:
        i.  Determine the target color based on the parity of `dr` and `d`:
            *   If `dr` is even: use pattern color 1 (orange, 7) if `d` is even, and pattern color 2 (azure, 8) if `d` is odd.
            *   If `dr` is odd: use pattern color 2 (azure, 8) if `d` is even, and pattern color 1 (orange, 7) if `d` is odd.
        ii. Set the output pixel at (row, col) to the determined target color.
    d. If `d` is not less than H, the output pixel at (row, col) remains the background color (white, 0).
5. Return the final output grid.
"""

import numpy as np

def find_top_left_pixel(grid, color):
    """
    Finds the row and column of the top-most, then left-most pixel of a given color.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        tuple or None: A tuple (row, col) of the first occurrence, or None if not found.
    """
    locations = np.argwhere(grid == color)
    if len(locations) == 0:
        return None  # Color not found
    # np.argwhere returns coordinates sorted by row, then column.
    # The first element is the top-most, left-most.
    top_left = locations[0]
    return tuple(top_left)

def get_vertical_line_height(grid, start_row, col, color):
    """
    Calculates the height of a vertical line of a specific color starting from a point downwards.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index.
        col (int): The column index.
        color (int): The color of the line pixels.

    Returns:
        int: The height of the vertical line.
    """
    height = 0
    num_rows = grid.shape[0]
    for r in range(start_row, num_rows):
        if grid[r, col] == color:
            height += 1
        else:
            break # Stop counting when the color changes or grid ends
    return height

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Define colors used in the transformation
    seed_color = 7      # orange
    pattern_color_1 = 7 # orange
    pattern_color_2 = 8 # azure
    background_color = 0 # white

    # 1. Initialize output_grid with background color (white)
    output_grid = np.full_like(input_grid_np, background_color)

    # 2. Find the seed pixel (top-leftmost orange)
    seed_pixel = find_top_left_pixel(input_grid_np, seed_color)

    # If no seed color pixel is found, return the empty white grid
    if seed_pixel is None:
        return output_grid.tolist()

    seed_r, seed_c = seed_pixel

    # 3. Determine the height H of the vertical orange line starting from the seed
    line_height_H = get_vertical_line_height(input_grid_np, seed_r, seed_c, seed_color)

    # 4. Iterate through each pixel, calculate distances, and fill the output grid
    for r in range(height):
        for c in range(width):
            # 4a. Calculate Manhattan distance from the seed pixel
            distance_d = abs(r - seed_r) + abs(c - seed_c)
            # 4b. Calculate absolute row difference
            row_diff_dr = abs(r - seed_r)

            # 4c. Check if distance is less than the measured line height H
            if distance_d < line_height_H:
                # 4ci. Determine the target color based on parity of dr and d
                target_color = background_color # Default should not be used if logic is correct
                if row_diff_dr % 2 == 0: # dr is even
                    if distance_d % 2 == 0: # d is even
                        target_color = pattern_color_1 # orange
                    else: # d is odd
                        target_color = pattern_color_2 # azure
                else: # dr is odd
                    if distance_d % 2 == 0: # d is even
                        target_color = pattern_color_2 # azure
                    else: # d is odd
                        target_color = pattern_color_1 # orange
                
                # 4cii. Set the output pixel color
                output_grid[r, c] = target_color
            # 4d. Else (distance_d >= line_height_H): Pixel remains background_color (white) as initialized

    # 5. Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()