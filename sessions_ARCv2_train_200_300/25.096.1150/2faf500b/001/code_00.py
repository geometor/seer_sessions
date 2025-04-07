import numpy as np
from typing import List, Tuple, Set

"""
Transforms an input grid by finding all cells with the value 6. 
These '6' cells, along with any adjacent (up, down, left, right) cells containing the value 9, 
are then set to 0 in the output grid. All other cell values are copied directly from the input to the output.
"""

def _find_value_locations(grid: np.ndarray, value: int) -> List[Tuple[int, int]]:
    """Finds all locations (row, col) of a specific value in the grid."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def _get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Gets valid neighbor coordinates (up, down, left, right) for a given cell."""
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: zeros out cells with value 6 and 
    any adjacent 9s.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_array = input_array.copy()

    # Find locations of all '6' markers
    marker_locations = _find_value_locations(input_array, 6)

    # Create a set to store coordinates of cells to be changed to 0
    # Using a set automatically handles duplicates
    coords_to_zero: Set[Tuple[int, int]] = set()

    # Add all marker locations to the set
    for r, c in marker_locations:
        coords_to_zero.add((r, c))

    # Iterate through each marker location
    for r, c in marker_locations:
        # Examine its neighbors
        neighbors = _get_neighbors(r, c, height, width)
        for nr, nc in neighbors:
            # If a neighbor is a '9' in the original input grid, add it to the set
            if input_array[nr, nc] == 9:
                coords_to_zero.add((nr, nc))

    # Iterate through the collected coordinates and set the corresponding cells in the output grid to 0
    for r_change, c_change in coords_to_zero:
        output_array[r_change, c_change] = 0

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid