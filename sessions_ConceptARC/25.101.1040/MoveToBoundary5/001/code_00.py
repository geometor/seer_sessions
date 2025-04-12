import copy

"""
1. Identify the single contiguous object composed of non-white pixels in the input grid.
2. Determine the coordinates (row `min_r`, column `min_c`) of the top-leftmost pixel belonging to this object.
3. Compare `min_r` and `min_c`.
4. If `min_r` is less than `min_c`, determine the translation vector as (3 rows down, 0 columns across).
5. If `min_c` is less than or equal to `min_r`, determine the translation vector as (0 rows down, 3 columns right).
6. Create a new output grid of the same dimensions as the input, initialized with the background color (white).
7. For every pixel belonging to the identified object in the input grid, copy its color to the corresponding position in the output grid, shifted according to the determined translation vector.
"""

def find_object_pixels(grid: list[list[int]]) -> list[tuple[int, int, int]]:
    """
    Finds all non-background pixels and returns their coordinates and color.
    Assumes a single object and a known background color (0).
    """
    pixels = []
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            color = grid[r][c]
            if color != 0: # Non-background pixel
                pixels.append((r, c, color))
    return pixels

def find_top_left_pixel(pixels: list[tuple[int, int, int]]) -> tuple[int, int]:
    """
    Finds the top-leftmost coordinate among the given pixels.
    """
    if not pixels:
        return -1, -1 # Should not happen based on task description

    min_r = min(p[0] for p in pixels)
    min_c = min(p[1] for p in pixels if p[0] == min_r) # Find min col only among those with min row

    # Re-evaluate min_c based on all pixels to find true top-left
    min_r_overall = min(p[0] for p in pixels)
    min_c_overall = min(p[1] for p in pixels)
    
    # Find the actual top-leftmost pixel coordinate
    top_left_r = float('inf')
    top_left_c = float('inf')
    for r, c, _ in pixels:
        if r < top_left_r:
            top_left_r = r
            top_left_c = c
        elif r == top_left_r and c < top_left_c:
            top_left_c = c
            
    return top_left_r, top_left_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by translating the single non-background object.
    The translation direction (down or right by 3 cells) depends on whether the
    object's top-leftmost pixel is closer to the top edge (min_r < min_c -> move down)
    or closer/equidistant to the left edge (min_c <= min_r -> move right).
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    background_color = 0

    # Initialize output_grid with background color
    output_grid = [[background_color for _ in range(cols)] for _ in range(rows)]

    # 1. Find all pixels belonging to the object
    object_pixels = find_object_pixels(input_grid)

    if not object_pixels:
        return output_grid # Return background if no object found

    # 2. Determine the coordinates of the top-leftmost pixel
    min_r, min_c = find_top_left_pixel(object_pixels)

    # 3, 4, 5. Determine the translation vector based on min_r and min_c
    delta_r, delta_c = 0, 0
    shift_amount = 3
    if min_r < min_c:
        # Closer to top edge -> shift down
        delta_r = shift_amount
        delta_c = 0
    elif min_c <= min_r:
         # Closer to or equidistant from left edge -> shift right
        delta_r = 0
        delta_c = shift_amount
    # Note: The case min_r == min_c falls into the second condition (shift right).

    # 7. Apply the translation to each object pixel
    for r, c, color in object_pixels:
        new_r = r + delta_r
        new_c = c + delta_c

        # Place the pixel in the output grid if within bounds
        if 0 <= new_r < rows and 0 <= new_c < cols:
            output_grid[new_r][new_c] = color

    return output_grid