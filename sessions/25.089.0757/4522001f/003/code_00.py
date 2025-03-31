import numpy as np
from typing import List, Tuple

"""
The transformation rule maps a 3x3 input grid containing white (0), red (2), and green (3) pixels to a 9x9 output grid. The placement of two 4x4 green blocks in the output depends on the relative position of the center of the green pixels compared to the single red pixel in the input.

1.  **Initialization**: Create a 9x9 output grid filled with white (0).
2.  **Locate Pixels**:
    *   Find the coordinates (r_red, c_red) of the single red pixel (2) in the input grid.
    *   Find the coordinates of all green pixels (3) in the input grid.
3.  **Check for Green Pixels**: If there are no green pixels in the input, return the initialized white 9x9 grid.
4.  **Calculate Green Center**: Calculate the average row (r_green_avg) and average column (c_green_avg) of all green pixel coordinates. This represents the 'center of mass' of the green pixels.
5.  **Determine Relative Position**: Compare the green center coordinates (r_green_avg, c_green_avg) to the red pixel coordinates (r_red, c_red) to determine the relative direction (quadrant) of the green center with respect to the red pixel.
6.  **Select Output Block Locations**: Based on the relative position determined in the previous step, select a pair of top-left coordinates for the two 4x4 green blocks to be drawn in the output grid:
    *   If Green Center is North-West (NW) of Red (r_green_avg < r_red, c_green_avg < c_red): Blocks start at (0,0) and (4,4).
    *   If Green Center is North-East (NE) of Red (r_green_avg < r_red, c_green_avg > c_red): Blocks start at (1,4) and (4,1).
    *   If Green Center is South-West (SW) of Red (r_green_avg > r_red, c_green_avg < c_red): Blocks start at (0,5) and (5,0).
    *   If Green Center is South-East (SE) of Red (r_green_avg > r_red, c_green_avg > c_red): Blocks start at (1,1) and (5,5).
    *   (Note: The exact boundary cases where r_green_avg == r_red or c_green_avg == c_red are not covered by the examples, so strict inequality is used based on observations).
7.  **Draw Green Blocks**: Draw two 4x4 blocks of green (3) pixels onto the output grid starting at the selected top-left coordinates.
8.  **Return Output**: Return the final 9x9 output grid.
"""

def find_pixel_locations(grid: np.ndarray, color_value: int) -> List[Tuple[int, int]]:
    """Finds all locations (row, col) of a specific color_value in the grid."""
    locations = np.argwhere(grid == color_value)
    # Convert to list of tuples [(row, col), ...]
    return [tuple(loc) for loc in locations]

def calculate_center(locations: List[Tuple[int, int]]) -> Tuple[float, float]:
    """Calculates the average row and column for a list of locations."""
    if not locations:
        return (0.0, 0.0) # Or raise an error, depending on expected input
    avg_r = sum(r for r, c in locations) / len(locations)
    avg_c = sum(c for r, c in locations) / len(locations)
    return (avg_r, avg_c)

def draw_block(grid: np.ndarray, r_start: int, c_start: int, height: int, width: int, color_value: int):
    """Draws a block of a given color in the grid."""
    grid[r_start:r_start+height, c_start:c_start+width] = color_value

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the relative position of the green pixel
    center to the red pixel.
    """
    input_np = np.array(input_grid, dtype=int)
    output_height, output_width = 9, 9
    green_color = 3
    red_color = 2
    block_size = 4

    # Initialize output_grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the red pixel location (assuming exactly one)
    red_locations = find_pixel_locations(input_np, red_color)
    if not red_locations:
        # Should not happen based on examples, but handle defensively
        return output_grid.tolist() 
    r_red, c_red = red_locations[0]

    # Find green pixel locations
    green_locations = find_pixel_locations(input_np, green_color)

    # If no green pixels, return the blank output grid
    if not green_locations:
        return output_grid.tolist()

    # Calculate the center of the green pixels
    r_green_avg, c_green_avg = calculate_center(green_locations)

    # Determine the pair of block locations based on relative position
    block_starts = []
    if r_green_avg < r_red and c_green_avg < c_red: # NW
        block_starts = [(0, 0), (4, 4)]
    elif r_green_avg < r_red and c_green_avg > c_red: # NE
        block_starts = [(1, 4), (4, 1)]
    elif r_green_avg > r_red and c_green_avg < c_red: # SW
        block_starts = [(0, 5), (5, 0)]
    elif r_green_avg > r_red and c_green_avg > c_red: # SE
        block_starts = [(1, 1), (5, 5)]
    # Handle cases where center aligns horizontally or vertically if needed
    # Based on current examples, strict inequalities cover all cases.
    # If block_starts is still empty, something unexpected happened
    # or an edge case needs definition. Return blank grid for now.
    if not block_starts:
         return output_grid.tolist()


    # Draw the selected blocks
    for r_start, c_start in block_starts:
        draw_block(output_grid, r_start, c_start, block_size, block_size, green_color)

    return output_grid.tolist()