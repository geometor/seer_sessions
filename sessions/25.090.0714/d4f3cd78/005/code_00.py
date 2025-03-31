import numpy as np
from collections import deque
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1.  Identify the single connected object composed of gray (5) pixels (the 'container').
2.  Find the vertical "gap" column within the horizontal span of the container. This is the column with the minimum number of gray pixels within the container's bounding box columns.
3.  Identify a background (0) seed pixel within the area visually enclosed by the container (often adjacent to or within the gap column).
4.  Perform a flood fill starting from the seed pixel, changing connected background (0) pixels to azure (8), stopping at the gray (5) container boundary.
5.  Determine the vertical center of mass of the gray container.
6.  Compare the container's center to the grid's vertical center.
7.  If the container is lower, draw a vertical azure (8) line upwards from the top edge of the container in the gap column to the grid boundary, overwriting only background (0) pixels.
8.  If the container is higher or centered, draw a similar line downwards from the bottom edge of the container in the gap column.
"""

# Define color constants
BACKGROUND_COLOR = 0
CONTAINER_COLOR = 5
FILL_COLOR = 8

def find_objects(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with the specified color."""
    return list(zip(*np.where(grid == color)))

def find_gap_column(grid: np.ndarray, obj_coords: List[Tuple[int, int]]) -> int:
    """
    Finds the column index corresponding to the vertical gap.
    Identified as the column within the object's horizontal bounds
    that contains the minimum number of object pixels (color specified implicitly by obj_coords).
    """
    if not obj_coords:
        return -1

    min_c = min(c for r, c in obj_coords)
    max_c = max(c for r, c in obj_coords)

    min_obj_count = float('inf')
    gap_col = -1

    obj_set = set(obj_coords)
    height = grid.shape[0]

    # Iterate through columns within the object's horizontal span
    for c in range(min_c, max_c + 1):
        count = 0
        for r in range(height):
             if (r,c) in obj_set:
                 count += 1

        # Only consider columns that actually contain object pixels
        if count > 0 and count < min_obj_count:
            min_obj_count = count
            gap_col = c
        # If counts are equal, the current logic keeps the first one found (lowest column index).

    # Fallback if no gap found within the span (e.g., solid rectangle - unlikely for this task)
    if gap_col == -1 and obj_coords:
        # Check counts at the boundary columns if they weren't picked
        min_edge_count = sum(1 for r in range(height) if (r, min_c) in obj_set)
        max_edge_count = sum(1 for r in range(height) if (r, max_c) in obj_set) if min_c != max_c else float('inf')

        if min_edge_count > 0 and min_edge_count <= max_edge_count:
             gap_col = min_c
        elif max_edge_count > 0: # Check only if different from min_c
             gap_col = max_c
        elif min_edge_count > 0: # Should have been caught by loop if min_c == max_c
             gap_col = min_c

    return gap_col

def find_interior_seed(grid: np.ndarray, obj_coords: List[Tuple[int, int]], gap_column: int) -> Optional[Tuple[int, int]]:
    """Finds a background pixel suitable for starting a flood fill inside the container."""
    if gap_column == -1 or not obj_coords:
        return None

    height, width = grid.shape
    obj_set = set(obj_coords)
    gray_rows_in_gap_col = sorted([r for r, c in obj_coords if c == gap_column])

    if not gray_rows_in_gap_col:
        return None # Gap column has no container pixels? Should not happen if find_gap_column is correct.

    min_r_gap = gray_rows_in_gap_col[0]
    max_r_gap = gray_rows_in_gap_col[-1]

    # Strategy 1: Check *within* the gap column, between the top/bottom gray pixels
    for r in range(min_r_gap + 1, max_r_gap):
        if grid[r, gap_column] == BACKGROUND_COLOR:
            return (r, gap_column)

    # Strategy 2: Check adjacent columns (left/right) next to gray pixels in the gap column
    for r in range(min_r_gap, max_r_gap + 1): # Include the boundary rows
         # Check left neighbor
         c_left = gap_column - 1
         if 0 <= c_left < width and grid[r, c_left] == BACKGROUND_COLOR and (r,c_left) not in obj_set:
             # Ensure the checked point is not part of the container itself (unlikely but safe)
             return (r, c_left)
         # Check right neighbor
         c_right = gap_column + 1
         if 0 <= c_right < width and grid[r, c_right] == BACKGROUND_COLOR and (r,c_right) not in obj_set:
             return (r, c_right)

    # If still no seed, maybe the gap is wider? This logic might need extension for complex cases,
    # but should cover the examples.
    # print("Warning: Could not find interior seed pixel.")
    return None


def flood_fill(grid: np.ndarray, seed: Tuple[int, int], target_color: int, fill_color: int):
    """Performs flood fill on the grid starting from the seed coordinate."""
    height, width = grid.shape
    if not (0 <= seed[0] < height and 0 <= seed[1] < width):
        return # Seed out of bounds
    if grid[seed[0], seed[1]] != target_color:
        return # Seed pixel is not the target color

    queue = deque([seed])
    visited = {seed}
    grid[seed[0], seed[1]] = fill_color

    while queue:
        r, c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < height and 0 <= nc < width:
                neighbor = (nr, nc)
                if neighbor not in visited and grid[nr, nc] == target_color:
                    visited.add(neighbor)
                    grid[nr, nc] = fill_color
                    queue.append(neighbor)


def calculate_vertical_center(obj_coords: List[Tuple[int, int]]) -> float:
    """Calculates the average row index (vertical center) of the object."""
    if not obj_coords:
        return -1.0
    return sum(r for r, c in obj_coords) / len(obj_coords)

def draw_vertical_line(grid: np.ndarray, column: int, start_row: int, direction: int, fill_color: int, overwrite_color: int):
    """Draws a vertical line, overwriting only pixels of a specific color."""
    height = grid.shape[0]
    r = start_row
    while 0 <= r < height:
        if grid[r, column] == overwrite_color:
            grid[r, column] = fill_color
        r += direction
        # Stop if we hit a non-background pixel? Examples suggest line goes all the way. Stick to boundary limit.


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation: fills the interior of a gray container
    and adds an exterior line aligned with the container's gap.
    """
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 1. Identify the gray container
    container_coords = find_objects(output_grid, CONTAINER_COLOR)
    if not container_coords:
        return output_grid # No container found

    # 2. Find the gap column
    gap_column = find_gap_column(output_grid, container_coords)
    if gap_column == -1:
        # print("Warning: Could not determine gap column.")
        return output_grid # Cannot proceed without gap

    # 3. Find a seed pixel for flood fill
    seed_pixel = find_interior_seed(output_grid, container_coords, gap_column)

    # 4. Perform flood fill if seed is found
    if seed_pixel:
        flood_fill(output_grid, seed_pixel, BACKGROUND_COLOR, FILL_COLOR)
    # else:
        # print("Warning: No seed pixel found, skipping fill.")

    # 5. Calculate vertical center of the container
    shape_center_r = calculate_vertical_center(container_coords)

    # 6. Determine grid's vertical center
    grid_center_r = (height - 1) / 2.0

    # 7. Determine line direction and start point
    gray_rows_in_gap_col = sorted([r for r, c in container_coords if c == gap_column])
    if not gray_rows_in_gap_col:
         # Should be caught by gap column check, but safeguard
         # print("Warning: No container pixels in gap column for line drawing.")
         return output_grid

    min_r_gap = gray_rows_in_gap_col[0]
    max_r_gap = gray_rows_in_gap_col[-1]

    line_start_row = -1
    line_direction = 0

    if shape_center_r > grid_center_r:
        # Shape is lower -> Draw line upwards
        line_start_row = min_r_gap - 1
        line_direction = -1
    else:
        # Shape is upper or centered -> Draw line downwards
        line_start_row = max_r_gap + 1
        line_direction = 1

    # 8. Draw the exterior line
    if line_direction != 0:
         draw_vertical_line(output_grid, gap_column, line_start_row, line_direction, FILL_COLOR, BACKGROUND_COLOR)

    return output_grid