"""
Identifies the non-zero elements in the input grid to determine a color and an input bounding box (min_r_in, max_r_in, min_c_in, max_c_in).
Calculates the boundaries of a new rectangle within the output grid based on the input bounding box coordinates.
The output rectangle's coordinates (out_min_r, out_max_r, out_min_c, out_max_c) are determined by the rules:
out_min_r = min_r_in + 1
out_max_r = max_r_in - 1
out_min_c = min_c_in + 1
out_max_c = max_c_in + 2
Fills this calculated rectangle in the output grid (initialized with zeros) with the identified color, respecting grid boundaries.
"""

import math
import copy

def find_non_zero_elements(grid: list[list[int]]) -> tuple[list[tuple[int, int]], int | None]:
    """
    Finds all non-zero elements in the grid and their color.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of (row, col) coordinates of non-zero elements.
        - The non-zero value (color) found, or None if none found.
          Assumes only one non-zero color exists besides 0.
    """
    coords = []
    color = None
    height = len(grid)
    if height == 0:
        return [], None
    width = len(grid[0])

    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                coords.append((r, c))
                if color is None:
                    color = grid[r][c]
                # No need to check for multiple colors based on problem constraints

    return coords, color

def calculate_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """
    Calculates the min/max row/col for the bounding box of given coordinates.

    Args:
        coords: A list of (row, col) coordinates.

    Returns:
        A tuple (min_r, max_r, min_c, max_c), or None if coords is empty.
    """
    if not coords:
        return None

    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)

    return min_r, max_r, min_c, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Find non-zero elements and their color
    non_zero_coords, color = find_non_zero_elements(input_grid)

    # If no non-zero elements, return the zero grid
    if not non_zero_coords or color is None:
        return output_grid

    # Calculate the bounding box of non-zero elements in the input
    bbox_in = calculate_bounding_box(non_zero_coords)
    if bbox_in is None: # Should not happen if non_zero_coords is not empty
         return output_grid
    min_r_in, max_r_in, min_c_in, max_c_in = bbox_in

    # Calculate the coordinates for the output rectangle based on the derived rules
    out_min_r = min_r_in + 1
    out_max_r = max_r_in - 1
    out_min_c = min_c_in + 1
    out_max_c = max_c_in + 2  # Updated rule based on analysis

    # Fill the calculated rectangle in the output grid with the color
    # Ensure the calculated row/col ranges are valid before iterating
    if out_min_r <= out_max_r and out_min_c <= out_max_c:
         # Iterate through the rows and columns of the target output rectangle
         for r in range(out_min_r, out_max_r + 1):
             # Ensure row index is within the grid's height bounds
             if 0 <= r < height:
                 for c in range(out_min_c, out_max_c + 1):
                     # Ensure column index is within the grid's width bounds
                     if 0 <= c < width:
                         output_grid[r][c] = color

    return output_grid