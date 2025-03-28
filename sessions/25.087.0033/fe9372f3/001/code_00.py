import numpy as np

def find_center(grid):
    """
    Finds the center pixel (intersection) of the red '+' object.
    The center is the red pixel with four adjacent red neighbors.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: Coordinates (row, col) of the center pixel, or None if not found.
    """
    height, width = grid.shape
    # Find all red pixels (color code 2)
    red_pixels = np.argwhere(grid == 2)

    if len(red_pixels) == 0:
        return None # No red pixels found

    # Iterate through red pixels to find the one with 4 red neighbors
    for r, c in red_pixels:
        neighbor_count = 0
        # Define relative coordinates for N, S, E, W neighbors
        neighbors_delta = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in neighbors_delta:
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is also red
                if grid[nr, nc] == 2:
                    neighbor_count += 1

        # The center of the '+' shape is the unique red pixel with 4 red neighbors
        if neighbor_count == 4:
            return (r, c)

    # This part should ideally not be reached if the input always contains a valid '+'
    return None

def transform(input_grid):
    """
    Identifies a red '+' shape in the input grid. Creates an output grid
    by copying the input, then fills background (white, 0) pixels based on their
    position relative to the center of the '+'.
    - Background pixels on diagonal lines radiating from the center become blue (1).
    - Background pixels on the horizontal or vertical line passing through the center
      become azure (8), unless their Manhattan distance 'd' from the center along
      that axis satisfies d % 3 == 1, in which case they become yellow (4).
    - The original red '+' shape remains unchanged.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Find the center of the red '+' object
    center = find_center(input_array)
    if center is None:
        # Return input unchanged or raise error if center finding fails
        # Based on examples, center should always be found.
        # raise ValueError("Center of the red '+' object not found.")
        # For robustness in case of unexpected input, return copy of input
         return input_grid

    center_r, center_c = center

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_array)

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the cell was originally background (white, 0)
            # We only modify background cells
            if input_array[r, c] == 0:
                # Calculate row and column differences from the center
                d_row = abs(r - center_r)
                d_col = abs(c - center_c)

                # Check if the current cell is the center pixel itself (d_row=0 and d_col=0)
                # If so, skip (it's part of the original object or should remain 0 if background)
                if d_row == 0 and d_col == 0:
                    continue

                # Rule 1: Check for diagonal lines (d_row == d_col)
                if d_row == d_col:
                    output_grid[r, c] = 1  # Blue

                # Rule 2: Check for horizontal (d_row == 0) or vertical (d_col == 0) lines
                elif d_row == 0 or d_col == 0:
                    # Calculate distance along the axis (Manhattan distance)
                    d_axis = d_row + d_col # Equivalent to max(d_row, d_col) since one is 0

                    # Sub-rule: Check periodicity for yellow color
                    if d_axis % 3 == 1:
                        output_grid[r, c] = 4  # Yellow
                    else:
                        output_grid[r, c] = 8  # Azure

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()