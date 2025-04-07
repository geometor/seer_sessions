"""
Identify and remove solid rectangular shapes of a single color from the input grid, 
leaving other shapes and the background intact. The background color is assumed to be 0.
A shape is considered a solid rectangle if the count of its cells equals the area 
of its bounding box.
"""

import numpy as np
import copy

def find_colored_cells(grid: np.ndarray, color: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of cells with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows.tolist(), cols.tolist())) # Convert numpy indices to standard int tuples

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
    # Calculate the area based on bounding box dimensions
    expected_area = (max_r - min_r + 1) * (max_c - min_c + 1)
    # Count the actual number of cells provided
    actual_cell_count = len(coords)
    # If the count matches the area, it's a solid rectangle
    return actual_cell_count == expected_area

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying solid rectangular shapes of a single 
    non-zero color and replacing them with the background color (0).
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a deep copy of the input NumPy array
    # We modify this array directly.
    output_grid_np = copy.deepcopy(grid_np)
    
    # Find unique non-zero colors present in the grid
    unique_colors = np.unique(grid_np)
    non_zero_colors = unique_colors[unique_colors != 0]

    # Iterate through each unique non-zero color found
    for color in non_zero_colors:
        # Find all cell coordinates (r, c) containing this color in the original grid
        coords = find_colored_cells(grid_np, color)
        
        # If no cells are found for this color, continue to the next color
        if not coords:
            continue 

        # Calculate the bounding box of these cells
        bbox = calculate_bounding_box(coords)
        
        # Safety check, should not happen if coords is not empty
        if bbox is None:
             continue 

        # Check if the shape formed by these cells is a solid rectangle
        if is_solid_rectangle(coords, bbox):
            # If it is a solid rectangle:
            # Iterate through all the cell coordinates originally found for this color
            for r, c in coords:
                # Set the color of the corresponding cell (r, c) in the *output* grid to 0
                output_grid_np[r, c] = 0
                
    # Convert the modified NumPy array back to a list of lists for the final output
    return output_grid_np.tolist()