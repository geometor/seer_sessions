import math

"""
Transforms an input grid based on identifying a central feature and drawing a diagonal line segment.

1. Assume the background color is orange (7).
2. Determine the dimensions (height H, width W) of the input grid.
3. Calculate the coordinates of the geometric center of the grid: center_r = (H - 1) / 2, center_c = (W - 1) / 2.
4. Find the non-background pixel (r_c, c_c) closest to the geometric center using Manhattan distance. Ties are broken by smallest row index, then smallest column index.
5. Let C be the color of the identified pixel input[r_c][c_c].
6. Create an output grid of the same dimensions, filled with the background color (orange=7).
7. Calculate the anti-diagonal sum S = r_c + c_c.
8. Iterate through each cell (r, c) of the grid.
9. If r + c == S (i.e., the cell is on the anti-diagonal passing through (r_c, c_c)):
    a. If C is even: Check if r <= r_c AND c >= c_c. If true, set output[r][c] = C.
    b. If C is odd: Check if r >= r_c AND c <= c_c. If true, set output[r][c] = C.
10. Return the modified output grid.
"""

def calculate_manhattan_distance(r1, c1, r2, c2):
    """Calculates the Manhattan distance between two points."""
    return abs(r1 - r2) + abs(c1 - c2)

def find_central_pixel(input_grid: list[list[int]], background_color: int) -> tuple[int, int, int]:
    """
    Finds the non-background pixel closest to the geometric center.

    Args:
        input_grid: The input grid.
        background_color: The color considered background.

    Returns:
        A tuple containing (row, column, color) of the central pixel.
        Returns (-1, -1, -1) if no non-background pixel is found.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    center_r = (height - 1) / 2
    center_c = (width - 1) / 2

    min_dist = float('inf')
    central_pixel_r = -1
    central_pixel_c = -1
    central_pixel_color = -1

    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]
            if color != background_color:
                dist = calculate_manhattan_distance(r, c, center_r, center_c)
                # Check if this pixel is closer, or same distance but better tie-break
                if dist < min_dist:
                    min_dist = dist
                    central_pixel_r = r
                    central_pixel_c = c
                    central_pixel_color = color
                elif dist == min_dist:
                    if r < central_pixel_r:
                        central_pixel_r = r
                        central_pixel_c = c
                        central_pixel_color = color
                    elif r == central_pixel_r and c < central_pixel_c:
                        central_pixel_c = c
                        central_pixel_color = color

    return central_pixel_r, central_pixel_c, central_pixel_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 7

    # Find the central non-background pixel
    r_c, c_c, central_color = find_central_pixel(input_grid, background_color)

    # Initialize output_grid with background color
    output_grid = [[background_color for _ in range(width)] for _ in range(height)]

    # If no non-background pixel found, return the background grid (edge case)
    if r_c == -1:
        return output_grid

    # Calculate the anti-diagonal sum
    anti_diagonal_sum = r_c + c_c

    # Iterate through the grid to draw the line segment
    for r in range(height):
        for c in range(width):
            # Check if the current cell is on the target anti-diagonal
            if r + c == anti_diagonal_sum:
                # Check parity of the central color and apply direction rule
                is_even = central_color % 2 == 0
                if is_even:
                    # Even color: line goes up-right from central pixel
                    if r <= r_c and c >= c_c:
                        output_grid[r][c] = central_color
                else:
                    # Odd color: line goes down-left from central pixel
                    if r >= r_c and c <= c_c:
                        output_grid[r][c] = central_color

    return output_grid