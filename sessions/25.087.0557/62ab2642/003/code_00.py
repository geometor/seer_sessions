import copy

"""
Identify all gray (5) pixels in the input grid. Determine the minimum (leftmost) and maximum (rightmost) column indices occupied by these gray pixels. Find all gray pixels located at the minimum column index (leftmost_pixels) and all gray pixels located at the maximum column index (rightmost_pixels). Identify all white (0) pixels that are 8-way adjacent (including diagonals) to any pixel in leftmost_pixels. Change these white pixels to orange (7) in the output grid. Identify all white (0) pixels that are 8-way adjacent to any pixel in rightmost_pixels. Change these white pixels to azure (8) in the output grid. If a white pixel is adjacent to both leftmost_pixels and rightmost_pixels, it should be changed to azure (8) (azure takes precedence). If there are no gray pixels or if the minimum and maximum column indices are the same, return the input grid unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Initialize output grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # 1. Identify the locations (row, column) of all gray (5) pixels
    gray_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == 5:
                gray_pixels.append((r, c))

    # 2. If no gray pixels are found, return the copied grid without changes.
    if not gray_pixels:
        return output_grid

    # 3. Determine the minimum column index (min_col)
    min_col = width
    for r, c in gray_pixels:
        if c < min_col:
            min_col = c

    # 4. Determine the maximum column index (max_col)
    max_col = -1
    for r, c in gray_pixels:
        if c > max_col:
            max_col = c

    # 5. If min_col is equal to max_col, return the copied grid without changes.
    if min_col == max_col:
        return output_grid

    # 6. Create a set of "leftmost gray pixels"
    leftmost_gray_pixels = set()
    for r, c in gray_pixels:
        if c == min_col:
            leftmost_gray_pixels.add((r, c))

    # 7. Create a set of "rightmost gray pixels"
    rightmost_gray_pixels = set()
    for r, c in gray_pixels:
        if c == max_col:
            rightmost_gray_pixels.add((r, c))

    # 8. Initialize two empty sets for neighbors
    orange_neighbors = set()
    azure_neighbors = set()

    # Define 8-way neighbor offsets
    neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1), (1, 0), (1, 1)]

    # 9. Find white neighbors of leftmost gray pixels
    for r_gray, c_gray in leftmost_gray_pixels:
        for dr, dc in neighbor_offsets:
            nr, nc = r_gray + dr, c_gray + dc
            # Check grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white in the *input* grid
                if input_grid[nr][nc] == 0:
                    orange_neighbors.add((nr, nc))

    # 10. Find white neighbors of rightmost gray pixels
    for r_gray, c_gray in rightmost_gray_pixels:
        for dr, dc in neighbor_offsets:
            nr, nc = r_gray + dr, c_gray + dc
            # Check grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white in the *input* grid
                if input_grid[nr][nc] == 0:
                    azure_neighbors.add((nr, nc))

    # 11. Color orange neighbors in the output grid
    for r, c in orange_neighbors:
        output_grid[r][c] = 7

    # 12. Color azure neighbors in the output grid (overwrites orange if necessary)
    for r, c in azure_neighbors:
        output_grid[r][c] = 8

    # 13. Return the modified output grid
    return output_grid