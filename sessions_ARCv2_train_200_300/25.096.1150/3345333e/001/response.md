```python
"""
Identify and remove solid rectangular shapes of a single color from the input grid, 
leaving other shapes and the background intact.
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
    return actual_cell_count == expected_area

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying solid rectangular shapes of a single 
    non-zero color and replacing them with the background color (0).
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Convert to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find unique non-zero colors present in the grid
    unique_colors = np.unique(grid_np)
    non_zero_colors = unique_colors[unique_colors != 0]

    # Iterate through each unique non-zero color
    for color in non_zero_colors:
        # Find all cells with this color
        coords = find_colored_cells(grid_np, color)
        
        if not coords:
            continue # Skip if no cells found for this color

        # Calculate the bounding box for these cells
        bbox = calculate_bounding_box(coords)
        
        if bbox is None:
             continue # Should not happen if coords is not empty, but safety check

        # Check if the shape formed by these cells is a solid rectangle
        if is_solid_rectangle(coords, bbox):
            # If it is a solid rectangle, change its cells to 0 in the output grid
            for r, c in coords:
                # Modify the list-based output_grid
                output_grid[r][c] = 0
                
    # Return the modified output grid
    return output_grid
```