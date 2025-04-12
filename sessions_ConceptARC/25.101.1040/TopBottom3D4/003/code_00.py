import copy

"""
Identifies the two unique non-white colors in the input grid. Let C_low be the
color with the lower numeric index and C_high be the color with the higher
index. The transformation involves shifting the C_low object one column to the
left. The original positions occupied by the C_low object are cleared (set to
white/0). If a pixel of the C_high object was originally immediately to the
right of a pixel belonging to the C_low object, the C_high color 'fills' the
vacated C_low position in the output grid. Otherwise, the vacated position
remains white. The shifted C_low pixels overwrite any existing pixel colors at
their new locations, unless that location is subsequently filled by C_high as
described above.
"""

def find_colors(grid: list[list[int]]) -> tuple[int | None, int | None]:
    """Finds the two unique non-background colors in the grid.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing the lower and higher color index (c_low, c_high),
        or (None, None) if exactly two non-white colors are not found.
    """
    colors = set()
    height = len(grid)
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                colors.add(grid[r][c])
    # Ensure exactly two colors are found
    if len(colors) != 2:
        return None, None
    color_list = sorted(list(colors))
    # Returns the color with the lower index first (c_low), then higher (c_high)
    return color_list[0], color_list[1]

def find_object_pixels(grid: list[list[int]], color: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with the specified color.

    Args:
        grid: The input grid.
        color: The color value to find.

    Returns:
        A list of (row, col) tuples for pixels matching the color.
    """
    pixels = []
    height = len(grid)
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] == color:
                pixels.append((r, c))
    return pixels

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on shifting the lower-indexed color object left
    and handling interaction with the higher-indexed color object.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)

    # Identify the two unique non-white colors and determine low/high index
    c_low, c_high = find_colors(input_grid)

    # If colors are not as expected, return the original grid copy
    if c_low is None:
        # print("Warning: Expected exactly two non-white colors, found different.")
        return output_grid

    # Find original pixel locations for both objects
    low_orig_coords = find_object_pixels(input_grid, c_low)
    high_orig_coords = find_object_pixels(input_grid, c_high)

    # Use a set for efficient lookup of original C_low positions
    low_orig_coords_set = set(low_orig_coords)

    # Perform transformations

    # 1. Process C_low object shift
    for r, c in low_orig_coords:
        # a. Clear the original location in the output grid
        output_grid[r][c] = 0

        # b. Calculate the potential new location (shifted left)
        nc = c - 1

        # c/d. Check if the new column is valid and paint the new location if so
        if 0 <= nc < width:
            output_grid[r][nc] = c_low # Paint C_low at the new location

    # 2. Process C_high object interaction (filling vacated C_low spots)
    for r, c in high_orig_coords:
        # a. Calculate the potential 'target' location (where C_high would shift into)
        nc = c - 1

        # b/c. Check if target column is valid AND if the target location was originally C_low
        if 0 <= nc < width and (r, nc) in low_orig_coords_set:
             # d. If both conditions met, paint C_high at the target location
             #    This overwrites the background (0) or C_low placed in step 1d
             output_grid[r][nc] = c_high

    return output_grid