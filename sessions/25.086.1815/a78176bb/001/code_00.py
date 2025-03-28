import numpy as np
from typing import List, Tuple

"""
Identify the primary non-gray, non-white color ("signal color") and the gray color (5).
Find all coordinates of the signal color pixels and the gray color pixels.
Determine the top-leftmost coordinate (minimum row, then minimum column) for both the signal pixels (sr, sc) and the gray pixels (gr, gc).
Calculate a translation vector (dr, dc) based on these top-left coordinates:
  - dc = -gc if gc == sc, otherwise dc = gc
  - dr = (3 - gr - 2 * sr) // 2
Initialize the output grid as a copy of the input grid.
Set all gray pixels in the output grid to white (0).
For each original signal pixel at (r, c):
  Calculate the translated coordinates (nr, nc) = (r + dr, c + dc).
  If (nr, nc) is within the grid boundaries, set the pixel at (nr, nc) in the output grid to the signal color.
Return the modified output grid.
"""

def find_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    coords = np.argwhere(grid == color)
    # Convert to list of tuples [(row, col), ...]
    return [tuple(coord) for coord in coords]

def find_top_leftmost(coords: List[Tuple[int, int]]) -> Tuple[int, int] | None:
    """Finds the top-leftmost coordinate (min row, then min col)."""
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    # Find the minimum column among all points that share the minimum row
    min_col = min(c for r, c in coords if r == min_row)
    return (min_row, min_col)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by removing gray pixels and adding a translated copy
    of the non-gray shape, where the translation vector depends on the relative
    positions of the top-leftmost gray and non-gray pixels.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Find the signal color (first non-zero, non-five color)
    signal_color = -1
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r, c] != 5:
                signal_color = grid[r, c]
                break
        if signal_color != -1:
            break
            
    if signal_color == -1:
        # No signal color found, maybe just return input or empty grid?
        # Based on examples, signal color always exists.
        # Let's handle the gray removal part anyway.
        output_grid[output_grid == 5] = 0
        return output_grid.tolist()


    # Find coordinates of signal and gray pixels
    signal_coords = find_pixels(grid, signal_color)
    gray_coords = find_pixels(grid, 5)

    # Remove gray pixels from the output
    output_grid[output_grid == 5] = 0

    # Proceed only if both signal and gray pixels exist
    if not signal_coords or not gray_coords:
         # Only gray removal happened
        return output_grid.tolist()

    # Find top-leftmost coordinates
    sr, sc = find_top_leftmost(signal_coords)
    gr, gc = find_top_leftmost(gray_coords)

    # Calculate translation vector (dr, dc)
    dc = -gc if gc == sc else gc
    # Using integer division as per observation
    dr = (3 - gr - 2 * sr) // 2

    # Apply translation to signal pixels
    for r, c in signal_coords:
        nr, nc = r + dr, c + dc
        # Check if the new coordinates are within bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            output_grid[nr, nc] = signal_color

    return output_grid.tolist()