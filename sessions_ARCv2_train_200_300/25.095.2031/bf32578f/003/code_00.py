"""
Identifies the non-zero elements in the input grid to determine a color, count, and a bounding box.
Calculates the boundaries of a new rectangle within the output grid based on the input bounding box dimensions and the count of non-zero points.
The output rectangle's top/bottom rows are inset by 1 from the input box (min_r + 1, max_r - 1).
The output rectangle's left column is inset by 1 from the input box (min_c + 1).
The output rectangle's right column is calculated based on the input box's right column (max_c), width (w = max_c - min_c + 1), and the count of non-zero points (N). A base offset k_base = 4 - w is calculated. If N > 6, the final offset k = k_base + 1, otherwise k = k_base. The final right column is max_c + k.
Fills this calculated rectangle in the output grid with the identified color, leaving the rest as 0.
"""

import math
import copy

def find_non_zero_elements(grid: list[list[int]]) -> tuple[list[tuple[int, int]], int | None, int]:
    """
    Finds all non-zero elements in the grid, their count, and the color.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of (row, col) coordinates of non-zero elements.
        - The non-zero value (color) found, or None if none found.
          Assumes only one non-zero color exists besides 0.
        - The count (N) of non-zero elements.
    """
    coords = []
    color = None
    count = 0
    height = len(grid)
    if height == 0:
        return [], None, 0
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                coords.append((r, c))
                count += 1
                if color is None:
                    color = grid[r][c]
                # No need to check for multiple colors based on problem constraints
                    
    return coords, color, count

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
    """
    Transforms the input grid based on the bounding box and count of its non-zero elements.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Find non-zero elements, their color, and their count
    non_zero_coords, color, non_zero_count = find_non_zero_elements(input_grid)

    # If no non-zero elements, return the zero grid
    if not non_zero_coords or color is None:
        return output_grid

    # Calculate the bounding box of non-zero elements
    bbox = calculate_bounding_box(non_zero_coords)
    if bbox is None: # Should not happen if non_zero_coords is not empty
         return output_grid 
    min_r, max_r, min_c, max_c = bbox

    # Calculate the width of the input bounding box
    bbox_width = max_c - min_c + 1
    
    # Calculate the base column adjustment factor k_base
    k_base = 4 - bbox_width

    # Calculate the final column adjustment factor k based on count N
    if non_zero_count > 6:
      k = k_base + 1
    else:
      k = k_base
      
    # Define the boundaries for the output rectangle
    out_min_r = min_r + 1
    out_max_r = max_r - 1
    out_min_c = min_c + 1
    out_max_c = max_c + k  # Adjusted right boundary based on width and count

    # Fill the calculated rectangle in the output grid with the color
    # Ensure the calculated rows/cols define a valid rectangle
    if out_min_r <= out_max_r and out_min_c <= out_max_c:
         # Iterate through the rows and columns of the target rectangle
         for r in range(out_min_r, out_max_r + 1):
             # Ensure row is within grid bounds (important check)
             if 0 <= r < height:
                 for c in range(out_min_c, out_max_c + 1):
                     # Ensure column is within grid bounds (important check)
                     if 0 <= c < width:
                         output_grid[r][c] = color

    return output_grid