import numpy as np
from collections import defaultdict

"""
Horizontally shift groups of connected non-zero numbers to the grid edges based on their initial horizontal position relative to the grid's center. 
Groups left of or at the center move to the left edge. 
Groups right of the center move to the right edge. 
The internal structure and vertical position of each group are maintained.
"""

def find_object_coords(grid, value):
    """Finds all coordinates (row, col) in the grid matching the given value."""
    coords = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == value:
                coords.append((r, c))
    return coords

def get_object_bounds(coords):
    """Calculates the minimum and maximum column indices for a set of coordinates."""
    if not coords:
        return None, None
    min_col = min(c for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by shifting non-zero objects horizontally.

    Objects left of or at the grid's center move left; objects right move right.
    """
    input_grid_np = np.array(input_grid)
    rows, cols = input_grid_np.shape
    
    # initialize output_grid with zeros
    output_grid = np.zeros_like(input_grid_np)

    # Find all unique non-zero values (potential object identifiers)
    unique_values = np.unique(input_grid_np[input_grid_np != 0])

    # Calculate the horizontal center column index of the grid
    # Use floating point division for potentially odd widths
    grid_center_col = (cols - 1) / 2.0 

    # Process each unique non-zero value as a separate object
    for value in unique_values:
        # Find all coordinates for the current value
        coords = find_object_coords(input_grid_np, value)
        
        if not coords: # Should not happen with unique_values logic, but safe check
            continue

        # Determine the horizontal bounds (min/max columns) of the object
        min_col, max_col = get_object_bounds(coords)

        # Calculate the horizontal center of the object
        object_center_col = (min_col + max_col) / 2.0

        # Determine shift direction and calculate the shift amount
        shift = 0
        if object_center_col <= grid_center_col:
            # Move to the left edge
            shift = 0 - min_col
        else:
            # Move to the right edge
            shift = (cols - 1) - max_col
            
        # Apply the shift to each coordinate of the object and update the output grid
        for r, c in coords:
            new_c = c + shift
            # Ensure the new column is within grid bounds (should be by calculation logic)
            if 0 <= new_c < cols: 
                 output_grid[r, new_c] = value

    # Convert back to list of lists if necessary, although numpy array is often preferred
    return output_grid.tolist()