```python
import copy

"""
Transforms the input grid based on the pair of non-white colors present.
The transformation depends on the specific pair of non-white colors (C1, C2) found in the grid.
Let C_low be the color with the lower index and C_high be the color with the higher index.

1.  If the pair is {1 (Blue), 2 (Red)} or {4 (Yellow), 6 (Magenta)}:
    - The object composed of C_low pixels is identified.
    - This object is shifted one column to the left.
    - The original positions of the shifted object become background (white, 0).
    - The shifted object overwrites any pixels in its new path.

2.  If the pair is {3 (Green), 4 (Yellow)}:
    - Pixels of color C_high (Yellow) are changed to color C_low (Green) if they have a C_low (Green) neighbor directly to their right OR directly below them.

3.  If the pair is {1 (Blue), 5 (Gray)}:
    - Pixels of color C_high (Gray) are changed to color C_low (Blue) if they have a C_low (Blue) neighbor directly to their right.
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
    Applies the transformation rule based on the pair of non-white colors present.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # 1. Identify the two unique non-white colors and determine low/high index
    c_low, c_high = find_colors(input_grid)

    # If colors are not as expected (e.g., not exactly 2 non-white), return the original grid
    if c_low is None:
        print("Warning: Expected exactly two non-white colors, found different.")
        return output_grid

    color_pair = {c_low, c_high}

    # 2. Determine and execute the transformation based on the color pair

    # Case 1: Shift Left (pairs {1, 2} or {4, 6})
    if color_pair == {1, 2} or color_pair == {4, 6}:
        # Find original pixels of the object to be shifted (c_low)
        pixels_to_shift = find_object_pixels(input_grid, c_low)

        # Calculate new locations after shifting left
        new_pixel_locations = []
        for r, c in pixels_to_shift:
            new_c = c - 1
            # Check boundary conditions for the new column
            if 0 <= new_c < width:
                 new_pixel_locations.append((r, new_c))

        # Clear original locations in output grid
        # Note: This happens *before* painting new locations, correctly handling overlaps
        for r, c in pixels_to_shift:
            output_grid[r][c] = 0 # Set to white/background

        # Fill new locations in output grid with c_low
        for r, new_c in new_pixel_locations:
             output_grid[r][new_c] = c_low

    # Case 2: Color Bleed (pairs {1, 5} or {3, 4})
    elif color_pair == {1, 5} or color_pair == {3, 4}:
        # Find pixels of the higher color object (potential targets for change)
        pixels_high = find_object_pixels(input_grid, c_high)
        pixels_to_change = []

        # Iterate through the higher color pixels to check for required adjacency
        for r_high, c_high_px in pixels_high:
            change_pixel = False

            # Rule for {3, 4} (Green changes adjacent Yellow)
            if color_pair == {3, 4}:
                # Check if neighbor to the RIGHT (r_high, c_high_px + 1) is c_low (Green)
                has_green_right = (c_high_px + 1 < width and input_grid[r_high][c_high_px + 1] == c_low)
                # Check if neighbor BELOW (r_high + 1, c_high_px) is c_low (Green)
                has_green_below = (r_high + 1 < height and input_grid[r_high + 1][c_high_px] == c_low)
                # If either condition is true, mark for change
                if has_green_right or has_green_below:
                    change_pixel = True

            # Rule for {1, 5} (Blue changes adjacent Gray)
            elif color_pair == {1, 5}:
                 # Check if neighbor to the RIGHT (r_high, c_high_px + 1) is c_low (Blue)
                 # Rule: Gray pixel (r_high, c_high_px) changes if Blue pixel is at (r_high, c_high_px + 1)
                 if c_high_px + 1 < width and input_grid[r_high][c_high_px + 1] == c_low:
                     change_pixel = True

            # If conditions met, mark this pixel for color change
            if change_pixel:
                pixels_to_change.append((r_high, c_high_px))

        # Apply the color changes to the output grid
        for r_change, c_change in pixels_to_change:
            output_grid[r_change][c_change] = c_low

    # 3. Return the modified output grid
    return output_grid
```