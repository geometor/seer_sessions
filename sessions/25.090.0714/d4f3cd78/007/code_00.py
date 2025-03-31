import numpy as np
from collections import deque
from typing import List, Tuple, Optional, Dict

# Define color constants
BACKGROUND_COLOR = 0
CONTAINER_COLOR = 5
FILL_COLOR = 8

"""
Transformation Rule:
1.  Identify the single connected object composed of gray (5) pixels (the 'container').
2.  Find the vertical "gap" column within the horizontal span of the container. This is the column with the minimum number (>0) of gray pixels within the container's bounding box columns.
3.  Identify a background (0) seed pixel within the area visually enclosed by the container by searching the gap column within the container's vertical bounds.
4.  Perform a flood fill starting from the seed pixel, changing connected background (0) pixels to azure (8), stopping at the gray (5) container boundary.
5.  Determine the vertical center of mass of the gray container.
6.  Compare the container's center to the grid's vertical center.
7.  If the container is lower, draw a vertical azure (8) line upwards from the top edge of the container in the gap column to the grid boundary, overwriting only background (0) pixels.
8.  If the container is higher or centered, draw a similar line downwards from the bottom edge of the container in the gap column, overwriting only background (0) pixels.
"""

def find_objects(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with the specified color."""
    return list(zip(*np.where(grid == color)))

def get_bounding_box(coords: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """Calculates the min_row, max_row, min_col, max_col for the given coordinates."""
    if not coords:
        return None
    rows, cols = zip(*coords)
    return min(rows), max(rows), min(cols), max(cols)

def find_gap_column(grid: np.ndarray, obj_coords: List[Tuple[int, int]], bbox: Tuple[int, int, int, int]) -> int:
    """
    Finds the column index corresponding to the vertical gap.
    Identified as the column within the object's horizontal bounds (bbox)
    that contains the minimum number (>0) of object pixels.
    """
    min_r, max_r, min_c, max_c = bbox
    min_obj_count = float('inf')
    gap_col = -1

    obj_set = set(obj_coords)
    height = grid.shape[0]

    # Iterate through columns within the object's horizontal span
    for c in range(min_c, max_c + 1):
        count = 0
        # Count object pixels within the bounding box rows for this column
        # Actually, need to count in the whole column, as bbox doesn't guarantee shape is filled
        for r in range(height):
             if (r,c) in obj_set:
                 count += 1

        # Only consider columns that actually contain object pixels
        if 0 < count < min_obj_count:
            min_obj_count = count
            gap_col = c
        # Tie-breaking: keep the first column (lowest index) found with the minimum count.

    return gap_col

def find_interior_seed(grid: np.ndarray, bbox: Tuple[int, int, int, int], gap_column: int) -> Optional[Tuple[int, int]]:
    """
    Finds a background pixel suitable for starting a flood fill inside the container.
    Searches the gap column within the object's vertical bounds.
    """
    if gap_column == -1:
        return None

    min_r, max_r, _, _ = bbox

    # Strategy: Scan the gap column within the vertical bounds for a background pixel
    for r in range(min_r, max_r + 1):
        if grid[r, gap_column] == BACKGROUND_COLOR:
            return (r, gap_column)

    # Fallback (optional, might not be needed based on examples): check adjacent columns
    # width = grid.shape[1]
    # c_left = gap_column - 1
    # c_right = gap_column + 1
    # for r in range(min_r, max_r + 1):
    #     if 0 <= c_left < width and grid[r, c_left] == BACKGROUND_COLOR: return (r, c_left)
    #     if 0 <= c_right < width and grid[r, c_right] == BACKGROUND_COLOR: return (r, c_right)

    # print(f"Warning: Could not find interior seed pixel in gap column {gap_column} between rows {min_r} and {max_r}.")
    return None


def flood_fill(grid: np.ndarray, seed: Tuple[int, int], target_color: int, fill_color: int):
    """
    Performs flood fill on the grid starting from the seed coordinate.
    Modifies the grid in place.
    """
    height, width = grid.shape
    if not (0 <= seed[0] < height and 0 <= seed[1] < width):
        return # Seed out of bounds
    if grid[seed[0], seed[1]] != target_color:
        return # Seed pixel is not the target color

    queue = deque([seed])
    # No visited set needed if we change color in place, as we only queue target_color pixels
    grid[seed[0], seed[1]] = fill_color

    while queue:
        r, c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr, nc] == target_color:
                    grid[nr, nc] = fill_color
                    queue.append((nr, nc))


def calculate_vertical_center(obj_coords: List[Tuple[int, int]]) -> float:
    """Calculates the average row index (vertical center) of the object."""
    if not obj_coords:
        return -1.0 # Should not happen if called after finding coords
    return sum(r for r, c in obj_coords) / len(obj_coords)

def draw_vertical_line(grid: np.ndarray, column: int, start_row: int, direction: int, fill_color: int, overwrite_color: int):
    """Draws a vertical line, overwriting only pixels of a specific color."""
    height = grid.shape[0]
    r = start_row
    while 0 <= r < height:
        if grid[r, column] == overwrite_color:
            grid[r, column] = fill_color
        else:
            # Optional: Stop if we hit a non-background pixel?
            # The examples seem to imply drawing only continues over background.
            # Let's assume we only overwrite background for now. If the first pixel
            # isn't background, the loop condition `grid[r, column] == overwrite_color`
            # handles it. If a later pixel isn't background, this `else` is not strictly
            # necessary with the current logic, but makes intent clear.
            pass
        r += direction


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
        # print("No container found.")
        return output_grid # No container found, return original grid

    # 2. Determine container bounding box
    bbox = get_bounding_box(container_coords)
    if bbox is None: # Should not happen if container_coords is not empty
        return output_grid

    # 3. Find the gap column
    gap_column = find_gap_column(output_grid, container_coords, bbox)
    if gap_column == -1:
        # print("Warning: Could not determine gap column.")
        return output_grid # Cannot proceed without gap

    # 4. Find a seed pixel for flood fill
    seed_pixel = find_interior_seed(output_grid, bbox, gap_column)

    # 5. Perform flood fill if seed is found
    if seed_pixel:
        flood_fill(output_grid, seed_pixel, BACKGROUND_COLOR, FILL_COLOR)
    # else:
        # print("Warning: No seed pixel found, skipping fill.")
        # Continue anyway to draw the line if possible

    # 6. Calculate vertical center of the container
    shape_center_r = calculate_vertical_center(container_coords)

    # 7. Determine grid's vertical center
    grid_center_r = (height - 1) / 2.0

    # 8. Find min/max container rows within the gap column
    gray_rows_in_gap_col = sorted([r for r, c in container_coords if c == gap_column])
    if not gray_rows_in_gap_col:
         # This might happen if gap finding has issues or shape is unexpected
         # print(f"Warning: No container pixels in gap column {gap_column} for line drawing.")
         return output_grid # Cannot determine line start without these points

    min_r_gap = gray_rows_in_gap_col[0]
    max_r_gap = gray_rows_in_gap_col[-1]

    # 9. Determine line start row and direction
    line_start_row = -1
    line_direction = 0

    if shape_center_r > grid_center_r:
        # Shape center is lower than grid center -> Draw line upwards
        line_start_row = min_r_gap - 1
        line_direction = -1
    else:
        # Shape center is higher or centered -> Draw line downwards
        line_start_row = max_r_gap + 1
        line_direction = 1

    # 10. Draw the exterior line
    if line_direction != 0:
         draw_vertical_line(output_grid, gap_column, line_start_row, line_direction, FILL_COLOR, BACKGROUND_COLOR)

    return output_grid