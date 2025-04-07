"""
Identify two non-zero shapes in the input grid. One shape is a solid rectangle, 
the other is not. Find the bounding box of the non-rectangular shape. 
Create an output grid filled with the background color (0), then fill the 
bounding box of the non-rectangular shape with its original color.
"""

import numpy as np
import copy

def find_colored_cells(grid: np.ndarray, color: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of cells with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def calculate_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a list of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def is_solid_rectangle(coords: list[tuple[int, int]], bbox: tuple[int, int, int, int]) -> bool:
    """Checks if the coordinates form a solid rectangle within the bounding box."""
    if not coords or bbox is None:
        return False
    min_r, min_c, max_r, max_c = bbox
    expected_area = (max_r - min_r + 1) * (max_c - min_c + 1)
    actual_cell_count = len(coords)
    # Also check if all cells within the bounding box *actually have* the color.
    # This check is implicitly covered by the area comparison if the shape is contiguous.
    # The area check is sufficient given the problem description.
    return actual_cell_count == expected_area

def fill_bounding_box(grid: np.ndarray, bbox: tuple[int, int, int, int], color: int) -> np.ndarray:
    """Fills the specified bounding box in the grid with the given color."""
    min_r, min_c, max_r, max_c = bbox
    grid[min_r:max_r+1, min_c:max_c+1] = color
    return grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies solid rectangular and non-rectangular shapes. 
    Returns a grid containing only the filled bounding box of the 
    non-rectangular shape, using its original color.
    """
    # Convert input to numpy array
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    
    # Initialize output grid with background color (0)
    output_grid_np = np.zeros_like(grid_np)

    # Find unique non-zero colors
    unique_colors = np.unique(grid_np)
    non_zero_colors = unique_colors[unique_colors != 0]

    non_rect_color = -1 # Initialize with invalid color
    non_rect_bbox = None

    # Iterate through each unique non-zero color to identify shapes
    for color in non_zero_colors:
        # Find all cells with this color
        coords = find_colored_cells(grid_np, color)
        
        if not coords:
            continue 

        # Calculate the bounding box for these cells
        bbox = calculate_bounding_box(coords)
        
        if bbox is None:
             continue

        # Check if the shape is NOT a solid rectangle
        if not is_solid_rectangle(coords, bbox):
            non_rect_color = color
            non_rect_bbox = bbox
            # Assuming only one non-rectangular shape based on examples
            break 
            
    # If a non-rectangular shape and its bounding box were found
    if non_rect_color != -1 and non_rect_bbox is not None:
        # Fill the bounding box of the non-rectangular shape in the output grid
        output_grid_np = fill_bounding_box(output_grid_np, non_rect_bbox, non_rect_color)

    # Convert the result back to a list of lists
    return output_grid_np.tolist()