import numpy as np
from collections import deque

"""
Transforms a 10x10 grid according to the following rules:
1. Identifies a shape outlined by a specific color (5) on a background color (0).
2. Locates a specific horizontal gap pattern [5, 0, 5] centered in a predefined column (5).
3. Performs a flood fill starting from an interior point adjacent to the gap, changing background pixels (0) to a fill color (8). The fill respects the shape color (5) as an impenetrable boundary.
4. Determines the vertical extent (min/max rows) of the filled area (8), or falls back to the shape (5) bounds if no fill occurred.
5. Draws a vertical line using the fill color (8) in the gap column (5). The line extends from the gap's row towards the nearest grid edge (top or bottom), in the direction away from the main filled/shape area. This line overwrites background pixels (0) or existing fill pixels (8), but crucially does *not* overwrite the original shape boundary pixels (5).
"""

# --- Helper Functions ---

def find_gap_row(grid: np.ndarray, shape_color: int, background_color: int, gap_col: int) -> int | None:
    """
    Finds the row index containing the specific gap pattern [shape, background, shape]
    horizontally centered at gap_col.
    """
    height, width = grid.shape
    for r in range(height):
        # Check if gap_col is within bounds to have neighbors
        if 0 < gap_col < width - 1:
            # Check the specific pattern
            if (grid[r, gap_col] == background_color and
                    grid[r, gap_col - 1] == shape_color and
                    grid[r, gap_col + 1] == shape_color):
                return r
    return None # Return None if no such row is found

def find_interior_seed_point(grid: np.ndarray, gap_row: int, gap_col: int, background_color: int) -> tuple[int, int] | None:
    """
    Finds a suitable background_color seed point adjacent (preferably vertically) to the gap,
    assumed to be inside the shape.
    """
    height, width = grid.shape
    # Check below first
    if gap_row + 1 < height and grid[gap_row + 1, gap_col] == background_color:
        return (gap_row + 1, gap_col)
    # Check above next
    if gap_row - 1 >= 0 and grid[gap_row - 1, gap_col] == background_color:
        return (gap_row - 1, gap_col)
        
    # Add fallbacks for less common cases if needed, e.g., adjacent columns
    # Check adjacent columns in row below
    if gap_row + 1 < height:
        if gap_col - 1 >= 0 and grid[gap_row + 1, gap_col - 1] == background_color: return (gap_row + 1, gap_col - 1)
        if gap_col + 1 < width and grid[gap_row + 1, gap_col + 1] == background_color: return (gap_row + 1, gap_col + 1)
    # Check adjacent columns in row above
    if gap_row - 1 >= 0:
        if gap_col - 1 >= 0 and grid[gap_row - 1, gap_col - 1] == background_color: return (gap_row - 1, gap_col - 1)
        if gap_col + 1 < width and grid[gap_row - 1, gap_col + 1] == background_color: return (gap_row - 1, gap_col + 1)
        
    return None # Return None if no suitable point is found nearby

def flood_fill_interior(grid: np.ndarray, start_row: int, start_col: int, fill_color: int, target_color: int, boundary_color: int):
    """
    Performs flood fill starting from (start_row, start_col) on the grid.
    Fills target_color with fill_color, treating boundary_color as impassable.
    Modifies the grid in place.
    """
    height, width = grid.shape
    # Check if start point is valid and is the target color
    if not (0 <= start_row < height and 0 <= start_col < width and grid[start_row, start_col] == target_color):
        return # Do nothing if the start point isn't correct

    q = deque([(start_row, start_col)])
    visited = set([(start_row, start_col)]) # Keep track to avoid cycles and redundant checks
    grid[start_row, start_col] = fill_color # Fill the starting point

    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if not (0 <= nr < height and 0 <= nc < width):
                continue

            # Check if already visited
            if (nr, nc) in visited:
                continue
                
            visited.add((nr, nc)) # Mark as visited now

            # Check if it's a valid cell to fill (target color)
            if grid[nr, nc] == target_color:
                grid[nr, nc] = fill_color
                q.append((nr, nc))
            # Don't queue boundary or already filled cells

def get_filled_or_shape_area_bounds(grid: np.ndarray, fill_color: int, shape_color: int, default_row: int) -> tuple[int, int]:
    """
    Finds the min/max row indices containing fill_color, falling back to shape_color.
    Returns (default_row, default_row) if neither is found.
    """
    fill_rows = np.where(np.any(grid == fill_color, axis=1))[0]
    if len(fill_rows) > 0:
        return int(np.min(fill_rows)), int(np.max(fill_rows))

    shape_rows = np.where(np.any(grid == shape_color, axis=1))[0]
    if len(shape_rows) > 0:
        return int(np.min(shape_rows)), int(np.max(shape_rows))

    # Fallback if neither fill nor shape color is present
    return default_row, default_row


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original for checks
    output_grid = grid.copy()
    height, width = grid.shape

    # Define constants based on observations
    shape_color = 5
    background_color = 0
    fill_color = 8
    gap_col = 5 # The specific column where the gap pattern is expected

    # 1. Find the row containing the gap pattern [5, 0, 5] in the gap column
    gap_row = find_gap_row(grid, shape_color, background_color, gap_col)

    # If the required gap pattern isn't found, return the original grid copy
    if gap_row is None:
        return output_grid.tolist()

    # 2. Find a starting point for flood fill inside the shape, adjacent to the gap
    seed_point = find_interior_seed_point(grid, gap_row, gap_col, background_color)

    # 3. If a seed point is found, perform flood fill on the output grid
    if seed_point is not None:
        seed_row, seed_col = seed_point
        flood_fill_interior(output_grid, seed_row, seed_col, fill_color, background_color, shape_color)
    # else: fill step is skipped if no seed point found

    # 4. Determine the vertical bounds of the filled area (or the shape area as fallback)
    # Pass gap_row as default if neither fill nor shape exists (unlikely but safe)
    min_bound_row, max_bound_row = get_filled_or_shape_area_bounds(output_grid, fill_color, shape_color, gap_row)

    # 5. Draw the vertical line in the gap column
    # Determine direction: away from the main filled/shape area relative to the gap row
    if gap_row < min_bound_row:
        # Gap is above the main area, draw line upwards from row 0 to gap_row
        for r in range(0, gap_row + 1):
            # Crucially, check the ORIGINAL grid value. Only overwrite if it wasn't part of the shape boundary.
            if grid[r, gap_col] != shape_color:
                output_grid[r, gap_col] = fill_color
    elif gap_row > max_bound_row:
        # Gap is below the main area, draw line downwards from gap_row to the bottom edge
        for r in range(gap_row, height):
             # Crucially, check the ORIGINAL grid value.
            if grid[r, gap_col] != shape_color:
                output_grid[r, gap_col] = fill_color
    else:
        # Gap is within or adjacent to the main area bounds.
        # The flood fill might have already filled the gap pixel.
        # Explicitly fill the gap pixel if it was originally background.
        if grid[gap_row, gap_col] == background_color:
             output_grid[gap_row, gap_col] = fill_color

    # Convert the final numpy array back to a list of lists for the output
    return output_grid.tolist()