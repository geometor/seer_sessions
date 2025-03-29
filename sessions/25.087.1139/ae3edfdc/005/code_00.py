import numpy as np

"""
Transformation rule:
1. Initialize an output grid of the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify the locations of all blue pixels (1) and red pixels (2) in the input grid. These are the 'center' pixels.
3. Count the total number of orange pixels (7) in the input grid (`N_orange`).
4. Count the total number of green pixels (3) in the input grid (`N_green`).
5. Define a mapping from the count `N` (where `N` is `N_orange` or `N_green`, assumed to be between 1 and 4) to a specific set of relative neighbor positions (offsets):
    - N=1: `[Up (-1, 0)]`
    - N=2: `[Left (0, -1), Down (1, 0)]`
    - N=3: `[Up (-1, 0), Right (0, 1), Down (1, 0)]`
    - N=4: `[Up (-1, 0), Left (0, -1), Right (0, 1), Down (1, 0)]`
    - If N=0, the list is empty. If N > 4, use the N=4 pattern.
6. Determine the list of relative offsets to use for orange partners based on `N_orange` using the mapping from step 5.
7. For each blue center pixel location `(r, c)` identified in step 2:
    a. Place a blue pixel (1) at `(r, c)` in the output grid.
    b. For each relative offset `(dr, dc)` determined in step 6:
        i. Calculate the target coordinate `(tr, tc) = (r + dr, c + dc)`.
        ii. If `(tr, tc)` is within the boundaries of the grid, place an orange pixel (7) at `(tr, tc)` in the output grid.
8. Determine the list of relative offsets to use for green partners based on `N_green` using the mapping from step 5.
9. For each red center pixel location `(r, c)` identified in step 2:
    a. Place a red pixel (2) at `(r, c)` in the output grid.
    b. For each relative offset `(dr, dc)` determined in step 8:
        i. Calculate the target coordinate `(tr, tc) = (r + dr, c + dc)`.
        ii. If `(tr, tc)` is within the boundaries of the grid, place a green pixel (3) at `(tr, tc)` in the output grid.
10. Return the final output grid.
"""

def find_pixels(grid, color):
    """Finds all pixels of a specific color in the grid."""
    return list(map(tuple, np.argwhere(grid == color)))

def count_pixels(grid, color):
    """Counts the number of pixels of a specific color."""
    return np.count_nonzero(grid == color)

def get_relative_offsets(count):
    """Determines the relative offsets based on the count N."""
    offset_map = {
        1: [(-1, 0)],                            # Up
        2: [(0, -1), (1, 0)],                    # Left, Down
        3: [(-1, 0), (0, 1), (1, 0)],            # Up, Right, Down
        4: [(-1, 0), (0, -1), (0, 1), (1, 0)]    # Up, Left, Right, Down
    }
    if count <= 0:
        return []
    # Use N=4 pattern for counts >= 4
    key = min(count, 4)
    return offset_map.get(key, []) # Return empty list if key somehow invalid

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np)

    # Find center pixel locations
    blue_centers = find_pixels(input_np, 1)
    red_centers = find_pixels(input_np, 2)

    # Count partner pixels in the input grid
    n_orange = count_pixels(input_np, 7)
    n_green = count_pixels(input_np, 3)

    # Determine the relative offsets based on counts
    orange_offsets = get_relative_offsets(n_orange)
    green_offsets = get_relative_offsets(n_green)

    # Process Blue Centers (1) and Orange Partners (7)
    for center_r, center_c in blue_centers:
        # Place the blue center pixel in the output (check bounds just in case)
        if 0 <= center_r < height and 0 <= center_c < width:
            output_grid[center_r, center_c] = 1

        # Place orange pixels based on calculated offsets
        for dr, dc in orange_offsets:
            target_r, target_c = center_r + dr, center_c + dc

            # Check bounds before placing partner pixel
            if 0 <= target_r < height and 0 <= target_c < width:
                output_grid[target_r, target_c] = 7

    # Process Red Centers (2) and Green Partners (3)
    for center_r, center_c in red_centers:
        # Place the red center pixel in the output (check bounds just in case)
        if 0 <= center_r < height and 0 <= center_c < width:
            output_grid[center_r, center_c] = 2

        # Place green pixels based on calculated offsets
        for dr, dc in green_offsets:
            target_r, target_c = center_r + dr, center_c + dc

            # Check bounds before placing partner pixel
            if 0 <= target_r < height and 0 <= target_c < width:
                output_grid[target_r, target_c] = 3

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()