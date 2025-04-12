import copy

"""
Transforms an input grid by first creating a 'base tile' of the same dimensions. 
Non-white pixels from the input are copied directly to the base tile. 
White pixels in the input are replaced in the base tile by either azure (8) or white (0) 
based on a checkerboard pattern determined by the parity of the sum of their coordinates (r+c). 
Specifically, if (r+c) is even, the pixel becomes azure (8); if odd, it becomes white (0). 
Finally, the output grid is constructed by tiling this base tile in a 2x2 arrangement, 
resulting in an output grid with dimensions twice those of the input (2H x 2W).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule described above.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """

    # 1. Determine the height (H) and width (W) of the input grid.
    input_height = len(input_grid)
    if input_height == 0:
        return [] # Handle empty input grid
    input_width = len(input_grid[0])
    if input_width == 0:
        # Handle grids with 0 width but potentially non-zero height
        return [[] for _ in range(input_height * 2)]

    # 2. Create a new "base tile" grid (T) with the same dimensions (H x W).
    # Initialize with zeros, will be overwritten.
    base_tile = [[0 for _ in range(input_width)] for _ in range(input_height)]

    # 3. Iterate through each cell (r, c) of the input grid (I).
    for r in range(input_height):
        for c in range(input_width):
            # 4. For the current cell (r, c):
            # a. Get the value v = I[r][c].
            input_value = input_grid[r][c]

            # b. If v is not white (i.e., v != 0), set T[r][c] = v.
            if input_value != 0:
                base_tile[r][c] = input_value
            # c. If v is white (i.e., v == 0):
            else:
                # i. Calculate the sum of the coordinates: s = r + c.
                coord_sum = r + c
                # ii. If s is even (s % 2 == 0), set T[r][c] to azure (8).
                if coord_sum % 2 == 0:
                    base_tile[r][c] = 8
                # iii. If s is odd (s % 2 == 1), set T[r][c] to white (0).
                else:
                    base_tile[r][c] = 0

    # 5. Create the output grid (O) with dimensions 2H x 2W.
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = [[0 for _ in range(output_width)] for _ in range(output_height)]

    # 6. Iterate through each cell (r, c) of the output grid (O).
    for r_out in range(output_height):
        for c_out in range(output_width):
            # 7. Set O[r][c] by copying from the base tile using modulo arithmetic.
            # O[r][c] = T[r % H][c % W].
            r_base = r_out % input_height
            c_base = c_out % input_width
            output_grid[r_out][c_out] = base_tile[r_base][c_base]

    # 8. Return the output grid O.
    return output_grid