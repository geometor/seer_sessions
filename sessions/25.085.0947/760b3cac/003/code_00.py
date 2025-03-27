import numpy as np

"""
Reflects an azure (8) object horizontally, adding the reflection to the grid while keeping the original object pixels. 
The reflection axis is determined by the parity (even/odd) of the counts of azure pixels on the leftmost and rightmost columns of the object's bounding box.

1. Make a copy of the input grid to serve as the output grid.
2. Find all azure (8) pixels. If none, return the copied grid.
3. Calculate the bounding box of the azure pixels (min/max row/col).
4. Count azure pixels in the leftmost column (`count_left`) and rightmost column (`count_right`) of the bounding box.
5. Determine the reflection axis based on parity:
   - If `count_left` is odd AND `count_right` is even, reflect across the right edge (axis at x = max_col + 0.5).
   - Otherwise, reflect across the left edge (axis at x = min_col - 0.5).
6. For each original azure pixel at (r, c):
   - Calculate its reflected column `reflected_c`.
   - If reflecting right: `reflected_c = 2 * max_col + 1 - c`.
   - If reflecting left: `reflected_c = 2 * min_col - 1 - c`.
   - If the reflected position `(r, reflected_c)` is within the grid bounds, set the pixel at that position in the output grid to azure (8).
7. Return the modified output grid.
"""

def find_pixels_by_color(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    coords = np.argwhere(grid == color)
    # np.argwhere returns [[row, col], ...], convert to list of tuples [(row, col), ...]
    return [tuple(coord) for coord in coords]

def get_bounding_box(coords):
    """Calculates the bounding box (min_r, max_r, min_c, max_c) for a list of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def transform(input_grid):
    """
    Applies the horizontal reflection transformation to the azure object in the grid based on edge pixel count parity.
    """
    input_np = np.array(input_grid, dtype=int)
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    azure_color = 8

    # 2. Find all azure pixels
    azure_pixels = find_pixels_by_color(input_np, azure_color)

    # If no azure pixels, return the original grid copy
    if not azure_pixels:
        return output_grid.tolist()

    # 3. Calculate the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(azure_pixels)

    # 4. Count azure pixels in the leftmost and rightmost columns
    count_left = sum(1 for r, c in azure_pixels if c == min_col)
    count_right = sum(1 for r, c in azure_pixels if c == max_col)

    # 5. Determine reflection side based on parity
    reflect_right = (count_left % 2 != 0) and (count_right % 2 == 0) # True if left=Odd AND right=Even

    # 6. Perform Reflection
    for r, c in azure_pixels:
        # Calculate reflected column based on reflection side
        if reflect_right:
            # Reflect across the right edge (axis at max_col + 0.5)
            reflected_col = 2 * max_col + 1 - c
        else:
            # Reflect across the left edge (axis at min_col - 0.5)
            reflected_col = 2 * min_col - 1 - c

        # Check bounds and update output grid
        if 0 <= r < height and 0 <= reflected_col < width:
            output_grid[r, reflected_col] = azure_color

    # 7. Return the modified grid as a list of lists
    return output_grid.tolist()