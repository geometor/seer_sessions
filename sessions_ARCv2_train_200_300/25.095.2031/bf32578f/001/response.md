```python
import math
import copy

def find_non_zero_elements(grid: list[list[int]]) -> tuple[list[tuple[int, int]], int | None]:
    """
    Finds all non-zero elements in the grid.

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
                elif color != grid[r][c]:
                    # Handle cases with multiple non-zero colors if necessary,
                    # but based on examples, assume only one.
                    pass 
                    
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

"""
Identifies the non-zero elements in the input grid to determine a color and a bounding box.
Calculates the boundaries of a new rectangle within the output grid based on the input bounding box dimensions. 
The output rectangle's top/bottom rows are inset by 1 from the input box.
The output rectangle's left column is inset by 1 from the input box.
The output rectangle's right column is calculated based on the input box's right column and width: right_col = max_c + (5 - width).
Fills this calculated rectangle in the output grid with the identified color, leaving the rest as 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the bounding box of its non-zero elements.
    
    Args:
        input_grid: A 2D list of integers representing the input state.

    Returns:
        A 2D list of integers representing the transformed output state.
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

    # Find non-zero elements and their color
    non_zero_coords, color = find_non_zero_elements(input_grid)

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
    
    # Calculate the column adjustment factor k
    # Note: The rule k = 5 - width seems specific. Let's use it directly.
    k = 5 - bbox_width

    # Define the boundaries for the output rectangle
    out_min_r = min_r + 1
    out_max_r = max_r - 1
    out_min_c = min_c + 1
    out_max_c = max_c + k  # Adjusted right boundary

    # Fill the calculated rectangle in the output grid with the color
    # Ensure the calculated rows/cols are valid ranges
    if out_min_r <= out_max_r and out_min_c <= out_max_c:
         # Iterate through the rows and columns of the target rectangle
         for r in range(out_min_r, out_max_r + 1):
             # Ensure row is within grid bounds (might be unnecessary if logic guarantees it)
             if 0 <= r < height:
                 for c in range(out_min_c, out_max_c + 1):
                     # Ensure column is within grid bounds
                     if 0 <= c < width:
                         output_grid[r][c] = color

    return output_grid
```