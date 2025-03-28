import numpy as np

"""
Identifies blue (1) pixels in the input grid, determines the arithmetic sequence 
(step) defined by their coordinates, and extrapolates this sequence by adding 
red (2) pixels starting one step after the last blue pixel in the sequence, 
continuing until the grid boundary is reached. The rest of the grid remains unchanged.
"""

def transform(input_grid):
    """
    Applies the sequence extrapolation transformation to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with the extrapolated sequence marked in red.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the coordinates of all blue (1) pixels
    blue_pixels_coords = np.argwhere(input_grid == 1)

    # Convert coordinates to a list of tuples (row, col)
    blue_pixels_list = [tuple(coord) for coord in blue_pixels_coords]

    # Sort the coordinates, typically by row then column, to establish order
    blue_pixels_list.sort()

    # Need at least two points to determine a sequence and step
    if len(blue_pixels_list) < 2:
        # If fewer than 2 blue pixels, cannot determine sequence, return copy of input
        return output_grid

    # Calculate the step (delta_row, delta_col) from the first two points
    # Assuming the points form a consistent arithmetic sequence as per examples
    delta_row = blue_pixels_list[1][0] - blue_pixels_list[0][0]
    delta_col = blue_pixels_list[1][1] - blue_pixels_list[0][1]

    # Get the coordinates of the last blue pixel in the sequence
    last_row, last_col = blue_pixels_list[-1]

    # Calculate the starting position for the first red pixel
    next_row = last_row + delta_row
    next_col = last_col + delta_col

    # Extrapolate the sequence and add red (2) pixels
    while 0 <= next_row < height and 0 <= next_col < width:
        # Place a red pixel at the calculated position
        output_grid[next_row, next_col] = 2
        
        # Update the position for the next potential red pixel
        next_row += delta_row
        next_col += delta_col

    return output_grid