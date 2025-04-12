import numpy as np # numpy can be useful for array operations, although not strictly needed for this logic

"""
Transforms an input grid (I) into an output grid (O) based on the following rules:

1.  **Output Size & Tiling:** The output grid O has dimensions twice those of the input grid I (2H x 2W). It is constructed by tiling a 'base tile' (T) of size HxW in a 2x2 arrangement. Specifically, O[r][c] = T[r % H][c % W].

2.  **Base Tile Generation (T):** The base tile T is generated from the input grid I:
    a.  **Foreground Preservation:** Non-white pixels (colors 1-9) from I are directly copied to their corresponding positions in T. If I[r][c] != 0, then T[r][c] = I[r][c].
    b.  **Background Transformation (Hypothesis 2):** White pixels (color 0) from I are transformed in T based on their adjacency (orthogonally or diagonally) to non-white pixels in I:
        i.  **Adjacent Background:** If a white pixel I[r][c] == 0 is adjacent to *any* non-white pixel in I, its value in the base tile T[r][c] is determined by a standard checkerboard pattern: T[r][c] = azure (8) if the sum of coordinates (r + c) is even, and T[r][c] = white (0) if (r + c) is odd.
        ii. **Non-Adjacent Background:** If a white pixel I[r][c] == 0 is *not* adjacent to any non-white pixel in I, its value in the base tile T[r][c] is set to white (0).

*Disclaimer: This transformation rule accurately reproduces training examples 3 and 4. However, it produces known discrepancies compared to the expected outputs for training examples 1 (minor difference) and 2 (significant difference). The true rule for handling background pixels, especially with multiple non-white elements or specific colors (like magenta in Ex2), might be more complex or conditional.*
"""


def find_non_white_pixels(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Finds the coordinates (row, col) of all non-white (1-9) pixels in the grid."""
    coords = []
    height = len(grid)
    if height == 0:
        return coords
    # Assume grid is rectangular, check width of first row
    if not grid[0]:
        return coords # No width
    width = len(grid[0])

    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                coords.append((r, c))
    return coords

def is_adjacent(r: int, c: int, target_coords: list[tuple[int, int]]) -> bool:
    """
    Checks if the coordinate (r, c) is orthogonally or diagonally adjacent
    to any coordinate in the target_coords list.
    """
    for tr, tc in target_coords:
        # Check 8 neighbors (including diagonals) using Chebyshev distance <= 1
        if abs(r - tr) <= 1 and abs(c - tc) <= 1:
            # Ensure it's not the exact same pixel we are checking against
            # (although logic elsewhere ensures we check white against non-white)
            if r == tr and c == tc:
                continue
            return True # Found an adjacent non-white pixel
    return False # No adjacent non-white pixels found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: create a base tile based on adjacency-modified
    checkerboard pattern, then tile it 2x2.
    """

    # 1. Determine the height (H) and width (W) of the input grid.
    input_height = len(input_grid)
    if input_height == 0:
        return [] # Handle empty input grid

    # Handle case where rows might be empty lists
    if not input_grid[0]:
         input_width = 0
         # Output should be 2H x 0
         return [[] for _ in range(input_height * 2)]
    else:
        input_width = len(input_grid[0])


    # 2. Identify the coordinates of all non-white pixels in the input grid.
    non_white_coords = find_non_white_pixels(input_grid)

    # 3. Create a new "base tile" grid (T) with dimensions H x W.
    # Initialize with 0s (white), which is the default for non-adjacent background
    base_tile = [[0 for _ in range(input_width)] for _ in range(input_height)]

    # 4. Iterate through each cell (r, c) of the input grid (I) to populate the base tile.
    for r in range(input_height):
        for c in range(input_width):
            # 5a. Get the value v = I[r][c].
            input_value = input_grid[r][c]

            # 5b. If v is not white (v != 0), copy it to the base tile T[r][c].
            if input_value != 0:
                base_tile[r][c] = input_value
            # 5c. If v is white (v == 0): Check adjacency and apply rule
            else:
                # 5ci. Check if the current cell (r, c) is adjacent to any non-white pixel.
                if is_adjacent(r, c, non_white_coords):
                    # 5cii. If adjacent: Apply standard checkerboard pattern.
                    coord_sum = r + c
                    if coord_sum % 2 == 0: # even sum
                        base_tile[r][c] = 8 # azure
                    else: # odd sum
                        base_tile[r][c] = 0 # white (already initialized, but explicit)
                # 5ciii. If not adjacent: Set to white (already initialized to 0).
                # else: base_tile[r][c] = 0 # No action needed due to initialization

    # 6. Create the final output grid (O) with dimensions 2H x 2W.
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = [[0 for _ in range(output_width)] for _ in range(output_height)]

    # 7. Iterate through each cell (r_out, c_out) of the output grid (O).
    for r_out in range(output_height):
        for c_out in range(output_width):
            # 8. Set the output cell value using the base tile and modulo arithmetic for tiling.
            # O[r_out][c_out] = T[r_out % H][c_out % W].
            r_base = r_out % input_height
            c_base = c_out % input_width
            output_grid[r_out][c_out] = base_tile[r_base][c_base]

    # 9. Return the completed output grid O.
    return output_grid