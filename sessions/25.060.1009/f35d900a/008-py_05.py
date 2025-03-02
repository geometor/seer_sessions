"""
1.  **Determine Output Grid Size:** Calculate the dimensions of the output grid. The output grid's height and width are each 2 units larger than the corresponding dimensions of the input grid.
2.  **Identify Red and Green Pixels:** Find all pixels in the input grid that are red (value 2) or green (value 3).
3.  **Create Squares:** For each red and green pixel:
    *   Create a 3x3 square in the output grid with the same color as the original pixel.
    *   Center the 3x3 square on the location of the original pixel, using the *input* grid's coordinates.
4.  **Handle Overlap:** Examine every cell in the output grid. If any cell is within *both* a red 3x3 square and a green 3x3 square, change its value to 5 (gray).
5.  **Blank Cells:** Any cells in the output grid that weren't filled by the above steps remain 0 (white/blank).
"""

import numpy as np

def _get_square_coords(center_row, center_col, height, width):
    """Calculates the coordinates of a 3x3 square given the center and grid dimensions."""
    coords = []
    for i in range(max(0, center_row - 1), min(height, center_row + 2)):
        for j in range(max(0, center_col - 1), min(width, center_col + 2)):
            coords.append((i, j))
    return coords

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape

    # 1. Determine Output Grid Size
    output_height = input_height + 2
    output_width = input_width + 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 2. Identify Red and Green Pixels
    red_pixels = []
    green_pixels = []
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i, j] == 2:
                red_pixels.append((i, j))
            elif input_grid[i, j] == 3:
                green_pixels.append((i, j))

    # 3. Create Squares (Red)
    red_squares = []
    for r_row, r_col in red_pixels:
        square_coords = _get_square_coords(r_row + 1, r_col + 1, output_height, output_width) # +1 offset for output grid
        red_squares.append(square_coords)
        for r_i, r_j in square_coords:
            output_grid[r_i, r_j] = 2

    # 3. Create Squares (Green)
    green_squares = []
    for g_row, g_col in green_pixels:
        square_coords = _get_square_coords(g_row + 1, g_col + 1, output_height, output_width) # +1 offset for output grid
        green_squares.append(square_coords)
        for g_i, g_j in square_coords:
            output_grid[g_i, g_j] = 3

    # 4. Handle Overlap
    for i in range(output_height):
        for j in range(output_width):
            in_red_square = False
            in_green_square = False

            for red_square in red_squares:
                if (i, j) in red_square:
                    in_red_square = True
                    break

            for green_square in green_squares:
                if (i, j) in green_square:
                    in_green_square = True
                    break

            if in_red_square and in_green_square:
                output_grid[i, j] = 5

    return output_grid.tolist()