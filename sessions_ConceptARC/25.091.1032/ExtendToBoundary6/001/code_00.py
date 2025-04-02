"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Identify the locations (row, column) of all blue pixels (color 1) in the input grid.
3. For each identified blue pixel location:
    a. Start tracing a path diagonally upwards and to the right (row decreases, column increases).
    b. The path consists of blue pixels. The starting blue pixel is the first pixel of the path.
    c. Continue tracing the path one step at a time.
    d. Before adding the next pixel to the path, check if the next position:
        i. Is outside the top grid boundary (row < 0).
        ii. Is outside the right grid boundary (column >= grid width).
        iii. Corresponds to a red pixel (color 2) in the original input grid.
    e. If any of these conditions are met, stop tracing the path for the current starting blue pixel.
    f. Otherwise, set the pixel at the current path position in the output grid to blue (color 1) and move to the next diagonal position.
4. Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the diagonal blue path tracing transformation to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the locations of all initial blue pixels (color 1)
    start_blue_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 1:
                start_blue_pixels.append((r, c))

    # Trace the path for each starting blue pixel
    for start_r, start_c in start_blue_pixels:
        current_r, current_c = start_r, start_c

        while True:
            # Set the current position in the output grid to blue
            # This ensures the starting pixel is blue and overwrites any white pixels along the path
            if 0 <= current_r < height and 0 <= current_c < width:
                 output_grid[current_r, current_c] = 1
            else:
                # Should not happen if starting pixel is within bounds, but safe check
                break 

            # Calculate the next potential position (up and right)
            next_r = current_r - 1
            next_c = current_c + 1

            # Check stopping conditions for the *next* position
            # 1. Check top boundary
            if next_r < 0:
                break
            # 2. Check right boundary
            if next_c >= width:
                break
            # 3. Check for red pixel (color 2) at the next position in the *input* grid
            if input_grid[next_r, next_c] == 2:
                break

            # If no stopping conditions met, update current position for the next iteration
            current_r = next_r
            current_c = next_c
            
            # Note: The pixel at the new (current_r, current_c) will be colored blue 
            # at the start of the *next* loop iteration.

    return output_grid