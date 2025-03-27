import numpy as np

def check_neighbors(grid, r, c, target_color):
    """
    Checks the adjacent (up, down, left, right) neighbors of a cell (r, c)
    in the grid to see if any match the target_color.

    Args:
        grid (np.array): The input grid.
        r (int): The row index of the cell.
        c (int): The column index of the cell.
        target_color (int): The color value to look for in neighbors.

    Returns:
        bool: True if any adjacent neighbor has the target_color, False otherwise.
    """
    height, width = grid.shape
    # Define offsets for adjacent neighbors (up, down, left, right)
    neighbor_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in neighbor_offsets:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are within the grid bounds
        if 0 <= nr < height and 0 <= nc < width:
            # Check if the neighbor's color matches the target color
            if grid[nr, nc] == target_color:
                return True
    return False

def transform(input_grid):
    """
    Transforms the input grid based on adjacency rules between green (3) and red (2) pixels.
    - If a green (3) pixel is adjacent (up, down, left, right) to a red (2) pixel in the *input* grid, it becomes azure (8) in the output grid.
    - If a red (2) pixel is adjacent (up, down, left, right) to a green (3) pixel in the *input* grid, it becomes white (0) in the output grid.
    - All other pixels retain their original color in the output grid.
    The transformation considers only the adjacencies present in the original input grid.
    """
    # Convert input list of lists to a numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Initialize output_grid as a deep copy of the input grid
    # This ensures pixels not meeting the conditions retain their original color
    output_array = np.copy(input_array)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            current_color = input_array[r, c]

            # Check if the current pixel is green (3)
            if current_color == 3:
                # Check if any adjacent neighbor in the *input* grid is red (2)
                if check_neighbors(input_array, r, c, 2):
                    # If yes, change the corresponding pixel in the output grid to azure (8)
                    output_array[r, c] = 8

            # Check if the current pixel is red (2)
            elif current_color == 2:
                # Check if any adjacent neighbor in the *input* grid is green (3)
                if check_neighbors(input_array, r, c, 3):
                    # If yes, change the corresponding pixel in the output grid to white (0)
                    output_array[r, c] = 0

    # Convert the resulting numpy array back to a list of lists for the standard output format
    output_grid = output_array.tolist()
    return output_grid