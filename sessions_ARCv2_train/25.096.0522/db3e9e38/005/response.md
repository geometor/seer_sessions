```python
"""
Transforms an input grid based on a propagation pattern originating from the
topmost cell containing the value 7 (the seed). The pattern's extent is
determined by the Manhattan distance between the topmost and bottommost
cells containing 7 in the input. Within this distance limit, cells in the
output grid are assigned values 7 or 8 based on the parity of their
Manhattan distance from the seed cell (7 for even distance, 8 for odd).
Cells outside this distance limit remain 0.
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
    topmost_coords: Optional[Tuple[int, int]] = None
    bottommost_coords: Optional[Tuple[int, int]] = None

    # Find topmost seed (first 7 encountered in row-major order)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                topmost_coords = (r, c)
                break
        if topmost_coords is not None:
            break

    # If no 7 found at all
    if topmost_coords is None:
        return None

    # Find bottommost seed (last 7 encountered in row-major order)
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r, c] == 7:
                bottommost_coords = (r, c)
                break
        if bottommost_coords is not None:
            break
            
    # Should theoretically always find bottommost if topmost was found,
    # but handle potential edge cases if grid structure is unusual.
    if bottommost_coords is None:
        bottommost_coords = topmost_coords # If only one seed, it's both top and bottom

    return topmost_coords, bottommost_coords

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the distance-limited, alternating value propagation.

    Args:
        input_grid: The input 2D list of integers.

    Returns:
        The transformed 2D list of integers.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

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
            dist = manhattan_distance(seed_coords, current_coords)

            # Check if the cell is within the maximum allowed distance
            if dist <= max_dist:
                # Assign 7 for even distance, 8 for odd distance
                if dist % 2 == 0:
                    output_array[r, c] = 7
                else:
                    output_array[r, c] = 8
            # Cells outside max_dist remain 0 (already initialized)

    # Convert the result back to a list of lists
    return output_array.tolist()
```