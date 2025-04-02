```python
import numpy as np
from typing import List, Tuple

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a given color."""
    coords = np.argwhere(grid == color)
    # Convert numpy array of [row, col] pairs to list of (row, col) tuples
    return [tuple(coord) for coord in coords]

def get_line_boundaries(coords: List[Tuple[int, int]]) -> Tuple[str or None, int or None, int or None]:
    """
    Determines if the given coordinates form two parallel vertical or horizontal lines.
    Assumes the coordinates represent pixels of a single color (e.g., red).
    Returns orientation ('vertical'/'horizontal'), the min boundary index, and the max boundary index.
    Returns None for orientation and indices if two clear parallel lines are not formed.
    """
    if not coords:
        return None, None, None # No relevant pixels found

    # Extract unique row and column indices
    rows = sorted(list(set([r for r, c in coords])))
    cols = sorted(list(set([c for r, c in coords])))

    # Check for exactly two distinct columns, indicating potential vertical lines
    if len(cols) == 2:
        # Verify that *all* provided coordinates fall onto these two columns
        if all(c in cols for r, c in coords):
            # Ensure there's more than one pixel (avoids single pixel being misinterpreted)
            # and that pixels exist in more than one row if the lines are vertical
            if len(coords) > 1: # Basic check, could be refined if needed
                 return 'vertical', cols[0], cols[1]

    # Check for exactly two distinct rows, indicating potential horizontal lines
    if len(rows) == 2:
         # Verify that *all* provided coordinates fall onto these two rows
        if all(r in rows for r, c in coords):
            # Ensure there's more than one pixel and pixels exist in more than one col
             if len(coords) > 1: # Basic check
                return 'horizontal', rows[0], rows[1]

    # If the coordinates don't form two clear parallel lines according to the criteria
    return None, None, None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies two parallel red lines (color 2, vertical or horizontal) in the input grid.
    Removes (sets to white, color 0) any yellow pixels (color 4) that are not strictly
    located between these two red lines. Keeps yellow pixels strictly between the lines,
    the red lines themselves, and the white background. If two parallel red lines
    are not found, the grid is returned unchanged.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, which will become the output
    output_np = np.copy(input_np)

    # Define colors used in this task
    RED = 2
    YELLOW = 4
    WHITE = 0

    # 1. Find all red pixels
    red_coords = find_pixels(input_np, RED)

    # 2. Determine if the red pixels form two parallel lines and get their boundaries
    orientation, min_bound, max_bound = get_line_boundaries(red_coords)

    # 3. Proceed only if two clear parallel lines were identified
    if orientation and min_bound is not None and max_bound is not None:
        # 4. Find all yellow pixels
        yellow_coords = find_pixels(input_np, YELLOW)

        # 5. Iterate through yellow pixels and check their position relative to the red lines
        for r, c in yellow_coords:
            remove = False
            if orientation == 'vertical':
                # Lines are vertical at columns min_bound and max_bound.
                # Remove yellow pixel if its column 'c' is less than or equal to the minimum
                # column boundary, or greater than or equal to the maximum column boundary.
                # It must be strictly between: min_bound < c < max_bound
                if not (min_bound < c < max_bound):
                    remove = True
            elif orientation == 'horizontal':
                # Lines are horizontal at rows min_bound and max_bound.
                # Remove yellow pixel if its row 'r' is less than or equal to the minimum
                # row boundary, or greater than or equal to the maximum row boundary.
                # It must be strictly between: min_bound < r < max_bound
                if not (min_bound < r < max_bound):
                    remove = True

            # 6. If the yellow pixel is outside the strict bounds, change it to white
            if remove:
                output_np[r, c] = WHITE

    # Convert the result back to a list of lists as expected by ARC convention
    output_grid = output_np.tolist()
    return output_grid

```