```python
import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1. Identify all potential "frames" in the input grid. A frame is a rectangular, hollow structure, exactly one pixel thick, composed of a single non-white color, validated against its own bounding box.
2. Select the "main frame" from the candidates, typically the one with the largest area. If no frames are found, return the input grid.
3. Determine the set of "background colors" which includes white (0) plus all unique colors found immediately adjacent to the *outside* perimeter of the selected main frame.
4. Calculate the dimensions of the region strictly inside the main frame.
5. Create a new output grid sized to fit this inner region plus a 1-pixel border, initialized to white (0).
6. Draw the border of the output grid using the main frame's color.
7. Iterate through the inner region of the input grid. For each pixel, if its color is *not* one of the determined background colors, copy it to the corresponding position in the output grid's interior.
8. Return the completed output grid.
"""


def _find_potential_frames(grid: np.ndarray) -> List[Tuple[int, int, int, int, int]]:
    """
    Finds all potential 1-pixel thick, single-color, non-white, hollow rectangular frames.
    Validation is based on the bounding box derived from the pixels of that color.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of tuples (frame_color, outer_min_r, outer_min_c, outer_max_r, outer_max_c)
        for each potential frame found.
    """
    rows, cols = grid.shape
    potential_frames = []

    for color in range(1, 10):  # Iterate through possible frame colors (1-9)
        coords = np.argwhere(grid == color)
        if coords.size == 0:
            continue

        min_r, min_c = coords.min(axis=0)
        max_r, max_c = coords.max(axis=0)

        # Potential frame dimensions
        height = max_r - min_r + 1
        width = max_c - min_c + 1

        # Frame must be at least 3x3 to be hollow
        if height < 3 or width < 3:
            continue

        # Check 1: Verify all pixels on the exact perimeter match the color
        is_perimeter_complete = True
        try:
            # Top row
            if not np.all(grid[min_r, min_c:max_c + 1] == color): is_perimeter_complete = False
            # Bottom row
            if is_perimeter_complete and not np.all(grid[max_r, min_c:max_c + 1] == color): is_perimeter_complete = False
            # Left column (excluding corners)
            if is_perimeter_complete and height > 2 and not np.all(grid[min_r + 1:max_r, min_c] == color): is_perimeter_complete = False
            # Right column (excluding corners)
            if is_perimeter_complete and height > 2 and not np.all(grid[min_r + 1:max_r, max_c] == color): is_perimeter_complete = False
        except IndexError:
             is_perimeter_complete = False # Safety check for bounds

        if not is_perimeter_complete:
             continue # The bounding box perimeter isn't solely the frame color

        # Check 2: Hollow. Ensure no pixels *inside* the perimeter have the frame color.
        if height > 2 and width > 2:
            inner_slice = grid[min_r + 1:max_r, min_c + 1:max_c]
            if np.any(inner_slice == color):
                continue # Frame color found inside

        # Check 3: Thickness 1 (External check). Ensure no adjacent pixels *outside* the frame have the frame color.
        is_thick = False
        # Check row above
        if not is_thick and min_r > 0 and np.any(grid[min_r - 1, min_c:max_c + 1] == color): is_thick = True
        # Check row below
        if not is_thick and max_r < rows - 1 and np.any(grid[max_r + 1, min_c:max_c + 1] == color): is_thick = True
        # Check column left (full side)
        if not is_thick and min_c > 0 and np.any(grid[min_r:max_r + 1, min_c - 1] == color): is_thick = True
        # Check column right (full side)
        if not is_thick and max_c < cols - 1 and np.any(grid[min_r:max_r + 1, max_c + 1] == color): is_thick = True

        if is_thick:
            continue # Frame appears thicker than 1 pixel externally

        # If all checks pass, add to potential frames
        potential_frames.append((color, min_r, min_c, max_r, max_c))

    return potential_frames


def _find_best_frame(grid: np.ndarray) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Finds the best frame among potential candidates, typically the largest one by area.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        The best frame tuple (color, min_r, min_c, max_r, max_c) or None if no valid frames.
    """
    potential_frames = _find_potential_frames(grid)
    if not potential_frames:
        return None

    # Select the frame with the largest area
    best_frame = max(potential_frames, key=lambda f: (f[3] - f[1] + 1) * (f[4] - f[2] + 1))
    return best_frame


def _get_adjacent_outside_colors(grid: np.ndarray, min_r: int, min_c: int, max_r: int, max_c: int) -> Set[int]:
    """
    Gets unique colors immediately adjacent to the *outside* of a bounding box perimeter.

    Args:
        grid: The input grid.
        min_r, min_c, max_r, max_c: Outer bounds of the frame.

    Returns:
        A set of unique integer colors found adjacent to the outside.
    """
    rows, cols = grid.shape
    adjacent_colors = set()

    # Check row above (r = min_r - 1)
    if min_r > 0:
        r_check = min_r - 1
        c_start = max(0, min_c)
        c_end = min(cols, max_c + 1)
        if c_start < c_end: # Ensure valid slice range
             adjacent_colors.update(np.unique(grid[r_check, c_start:c_end]))

    # Check row below (r = max_r + 1)
    if max_r < rows - 1:
        r_check = max_r + 1
        c_start = max(0, min_c)
        c_end = min(cols, max_c + 1)
        if c_start < c_end:
             adjacent_colors.update(np.unique(grid[r_check, c_start:c_end]))

    # Check column left (c = min_c - 1)
    if min_c > 0:
        c_check = min_c - 1
        r_start = max(0, min_r) # Include corners
        r_end = min(rows, max_r + 1)
        if r_start < r_end:
             adjacent_colors.update(np.unique(grid[r_start:r_end, c_check]))

    # Check column right (c = max_c + 1)
    if max_c < cols - 1:
        c_check = max_c + 1
        r_start = max(0, min_r) # Include corners
        r_end = min(rows, max_r + 1)
        if r_start < r_end:
             adjacent_colors.update(np.unique(grid[r_start:r_end, c_check]))

    # Convert numpy types to standard Python ints if necessary for set operations later
    return {int(c) for c in adjacent_colors}


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: finds the largest valid frame, determines background
    colors based on exterior adjacency, filters the inner content, and constructs the output.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. & 2. Identify and Select Main Frame
    best_frame = _find_best_frame(grid_np)

    # If no frame found, return original grid
    if best_frame is None:
        return input_grid

    frame_color, frame_min_r, frame_min_c, frame_max_r, frame_max_c = best_frame

    # 3. Determine Background Colors
    adjacent_colors = _get_adjacent_outside_colors(grid_np, frame_min_r, frame_min_c, frame_max_r, frame_max_c)
    background_colors = adjacent_colors.union({0}) # Always include white (0)

    # 4. Calculate Inner Dimensions
    # Check for valid inner region (should be guaranteed by frame finding checks)
    if frame_min_r + 1 > frame_max_r - 1 or frame_min_c + 1 > frame_max_c - 1:
        # This case means frame is not hollow (height/width < 3), which _find_best_frame should prevent.
        # If it happens somehow, maybe return input or an empty grid? Returning input seems safer.
        return input_grid
    inner_min_r = frame_min_r + 1
    inner_max_r = frame_max_r - 1
    inner_min_c = frame_min_c + 1
    inner_max_c = frame_max_c - 1

    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1

    # 5. Create Output Grid
    output_height = inner_height + 2
    output_width = inner_width + 2
    output_grid_np = np.zeros((output_height, output_width), dtype=int) # Init with white (0)

    # 6. Draw Border
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 7. Process Inner Content
    for r_in in range(inner_min_r, inner_max_r + 1):
        for c_in in range(inner_min_c, inner_max_c + 1):
            input_pixel_color = grid_np[r_in, c_in]

            # Calculate corresponding output coordinates (offset by 1 for the border)
            r_out = r_in - inner_min_r + 1
            c_out = c_in - inner_min_c + 1

            # Check if the input color is a background color
            if input_pixel_color not in background_colors:
                # Copy the original color if it's not background
                 output_grid_np[r_out, c_out] = input_pixel_color
            # Else: leave it as 0 (white), which was the initialization value

    # 8. Return Output
    return output_grid_np.tolist()
```