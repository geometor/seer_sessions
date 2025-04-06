"""
Transforms an input grid based on a propagation pattern originating from the
topmost cell containing the value 7 (the seed). The pattern's extent is
determined by the Manhattan distance between the topmost and bottommost
cells containing 7 in the input. Within this distance limit, cells in the
output grid are assigned values 7 or 8 based on the parity of their
horizontal distance (absolute difference in column index) from the seed cell
(7 for even horizontal distance, 8 for odd). Cells outside this distance
limit remain 0.
"""

import numpy as np
from typing import Optional, Tuple, List

def find_extremal_seeds(grid: np.ndarray) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds the coordinates of the topmost (first encountered) and bottommost
    (last encountered) cells containing the value 7.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple containing two tuples: (topmost_coords, bottommost_coords),
        or None if no 7 is found.
    """
    rows, cols = grid.shape
    seed_coords: Optional[Tuple[int, int]] = None
    limit_coords: Optional[Tuple[int, int]] = None
    found_coords: List[Tuple[int, int]] = []

    # Find all '7' coordinates
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                found_coords.append((r, c))

    if not found_coords:
        return None # No '7' found

    # Topmost is the first one found
    seed_coords = found_coords[0]
    # Bottommost is the last one found
    limit_coords = found_coords[-1]

    return seed_coords, limit_coords

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the distance-limited, column-parity-based value propagation.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    if rows == 0 or cols == 0:
        return input_grid # Handle empty grids

    # Initialize output_grid with zeros
    output_array = np.zeros_like(input_array)

    # Find the coordinates of the topmost and bottommost seeds
    extremal_seeds = find_extremal_seeds(input_array)

    # If no seeds were found, return the grid of zeros
    if extremal_seeds is None:
        return output_array.tolist()

    seed_coords, limit_coords = extremal_seeds
    seed_row, seed_col = seed_coords

    # Calculate the maximum propagation distance based on the extremal seeds
    max_dist = manhattan_distance(seed_coords, limit_coords)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the Manhattan distance from the current cell to the seed
            current_coords = (r, c)
            current_dist = manhattan_distance(seed_coords, current_coords)

            # Check if the cell is within the maximum allowed distance
            if current_dist <= max_dist:
                # Calculate the absolute horizontal distance from the seed column
                col_diff = abs(c - seed_col)

                # Assign 7 for even horizontal distance, 8 for odd horizontal distance
                if col_diff % 2 == 0:
                    output_array[r, c] = 7
                else:
                    output_array[r, c] = 8
            # Cells outside max_dist remain 0 (already initialized)

    # Convert the result back to a list of lists
    return output_array.tolist()