import numpy as np

def is_white_square(grid, r, c, size):
    """
    Checks if the square subgrid of given size starting at (r, c)
    is composed entirely of white (0) pixels.

    Args:
        grid (np.ndarray): The input grid.
        r (int): Top row index of the square.
        c (int): Left column index of the square.
        size (int): Side length of the square.

    Returns:
        bool: True if the square is all white, False otherwise.
    """
    if r + size > grid.shape[0] or c + size > grid.shape[1]:
        return False # Square goes out of bounds
    subgrid = grid[r:r+size, c:c+size]
    return np.all(subgrid == 0)

def transform(input_grid):
    """
    Identifies the largest square subgrid composed entirely of white (0) pixels
    in the input grid and fills this square with azure (8) pixels in the output grid.
    All other pixels remain unchanged. Assumes a unique largest white square exists
    or implicitly picks the top-most, left-most one in case of ties by search order.
    """
    # Convert input to numpy array for easier slicing and operations
    input_grid_np = np.array(input_grid)
    output_grid = input_grid_np.copy()
    rows, cols = input_grid_np.shape

    # Variables to store the best square found so far
    max_size = 0
    best_r = -1
    best_c = -1

    # Iterate through possible square sizes, from largest possible down to 1
    # The largest possible square is min(rows, cols)
    for size in range(min(rows, cols), 0, -1):
        # Iterate through all possible top-left corners (r, c) for this size
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                # Check if the current square is all white
                if is_white_square(input_grid_np, r, c, size):
                    # If it is white and its size is greater than the current max_size found,
                    # update the max_size and location.
                    # Since we iterate from largest size down, the first one we find
                    # for a given size *must* be the largest overall.
                    # We only need to find one.
                    if size > max_size:
                        max_size = size
                        best_r = r
                        best_c = c
                        # Optimization: Once the largest possible size is found,
                        # no need to check smaller sizes for this specific top-left corner approach.
                        # However, a larger square might exist elsewhere.
                        # We need to continue scanning all positions for the *current* size 'size'.
                        # But once *any* square of size 'size' is found, we can break
                        # the inner loops and stop searching for smaller sizes because
                        # we started with the largest possible 'size'.
                        goto fill_square # Jump out of loops once the first largest is found

    # Label to jump to after finding the largest square
    fill_square:

    # If a white square was found (max_size > 0)
    if max_size > 0:
        # Fill the identified largest white square area in the output grid with azure (8)
        output_grid[best_r:best_r + max_size, best_c:best_c + max_size] = 8

    # Convert back to list of lists if necessary, depending on expected output format
    return output_grid.tolist()