import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1.  Identify the most prominent rectangular, hollow frame in the input grid that is exactly one pixel thick and composed of a single, non-white color. "Prominent" might mean largest perimeter or area. Record the frame's color and its outer bounding box coordinates.
2.  Determine the set of 'background colors'. This set includes white (0) and all unique colors found immediately adjacent to the *outside* perimeter of the identified frame.
3.  Create a new output grid. Its dimensions are determined by the size of the region strictly *inside* the identified frame, plus a one-pixel border on all sides.
4.  Fill the one-pixel border of the output grid with the frame's color identified in step 1. Initialize the interior of the output grid to white (0).
5.  Iterate through each pixel within the inner region of the input grid (the area inside the frame).
6.  For each input pixel, check if its color is present in the set of 'background colors' identified in step 2.
7.  If the input pixel's color *is* a background color, leave the corresponding pixel in the output grid's interior as white (0).
8.  Otherwise (if the input pixel's color is *not* a background color), copy the input pixel's original color to the corresponding position within the output grid's interior.
9.  Return the constructed output grid. If no suitable frame is found, return the original input grid.
"""

def _find_potential_frames(grid: np.ndarray) -> List[Tuple[int, int, int, int, int]]:
    """
    Finds all potential 1-pixel thick, single-color, non-white, hollow rectangular frames.

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
            if is_perimeter_complete and not np.all(grid[min_r + 1:max_r, min_c] == color): is_perimeter_complete = False
            # Right column (excluding corners)
            if is_perimeter_complete and not np.all(grid[min_r + 1:max_r, max_c] == color): is_perimeter_complete = False
        except IndexError:
             is_perimeter_complete = False # Should not happen if bounds are correct, but safety check

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
        if min_r > 0 and np.any(grid[min_r - 1, min_c:max_c + 1] == color): is_thick = True
        # Check row below
        if not is_thick and max_r < rows - 1 and np.any(grid[max_r + 1, min_c:max_c + 1] == color): is_thick = True
        # Check column left
        if not is_thick and min_c > 0 and np.any(grid[min_r:max_r + 1, min_c - 1] == color): is_thick = True
        # Check column right
        if not is_thick and max_c < cols - 1 and np.any(grid[min_r:max_r + 1, max_c + 1] == color): is_thick = True

        if is_thick:
            continue # Frame appears thicker than 1 pixel

        # If all checks pass, add to potential frames
        potential_frames.append((color, min_r, min_c, max_r, max_c))

    return potential_frames


def _get_adjacent_outside_colors(grid: np.ndarray, min_r: int, min_c: int, max_r: int, max_c: int) -> Set[int]:
    """Gets unique colors adjacent to the *outside* of a bounding box."""
    rows, cols = grid.shape
    adjacent_colors = set()

    # Check row above (r = min_r - 1)
    if min_r > 0:
        r_check = min_r - 1
        for c_check in range(max(0, min_c), min(cols, max_c + 1)):
             adjacent_colors.add(grid[r_check, c_check])

    # Check row below (r = max_r + 1)
    if max_r < rows - 1:
        r_check = max_r + 1
        for c_check in range(max(0, min_c), min(cols, max_c + 1)):
             adjacent_colors.add(grid[r_check, c_check])

    # Check column left (c = min_c - 1)
    if min_c > 0:
        c_check = min_c - 1
        # Exclude corners already checked by row checks
        for r_check in range(max(0, min_r + 1), min(rows, max_r)):
             adjacent_colors.add(grid[r_check, c_check])

    # Check column right (c = max_c + 1)
    if max_c < cols - 1:
        c_check = max_c + 1
        # Exclude corners already checked by row checks
        for r_check in range(max(0, min_r + 1), min(rows, max_r)):
             adjacent_colors.add(grid[r_check, c_check])

    return adjacent_colors


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule: extracts content within a frame,
    filters out background colors (adjacent to frame + white), and adds frame border.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Find potential frames
    potential_frames = _find_potential_frames(grid_np)

    # If no frames found, return original grid
    if not potential_frames:
        #print("Debug: No valid frames found.")
        return input_grid

    # Select the best frame (e.g., largest perimeter or area). Let's use area.
    best_frame = max(potential_frames, key=lambda f: (f[3] - f[1] + 1) * (f[4] - f[2] + 1))
    frame_color, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c = best_frame
    #print(f"Debug: Selected Frame Color {frame_color} at ({frame_outer_min_r},{frame_outer_min_c})->({frame_outer_max_r},{frame_outer_max_c})")


    # Define inner region coordinates
    inner_min_r = frame_outer_min_r + 1
    inner_min_c = frame_outer_min_c + 1
    inner_max_r = frame_outer_max_r - 1
    inner_max_c = frame_outer_max_c - 1

    # Check for valid inner region (should be guaranteed by find_frame)
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
         #print("Debug: Invalid inner region derived.")
         return input_grid # Should not happen

    # 2. Identify background colors (adjacent outside + white)
    adjacent_colors = _get_adjacent_outside_colors(grid_np, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c)
    background_colors = adjacent_colors.union({0}) # Add white
    #print(f"Debug: Background Colors Identified: {background_colors}")

    # 3. Create the output grid dimensions
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    output_height = inner_height + 2
    output_width = inner_width + 2

    # 4. Initialize output grid and draw border
    output_grid_np = np.zeros((output_height, output_width), dtype=int) # Init with white (0)
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 5-8. Process the inner region
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

    # 9. Return the completed grid
    return output_grid_np.tolist()