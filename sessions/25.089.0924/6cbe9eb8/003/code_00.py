import numpy as np
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1.  Identify a rectangular, hollow frame in the input grid that is exactly one pixel thick and composed of a single, non-white color. Record the frame's color and the bounding box of the region strictly inside it.
2.  Determine the set of 'background colors' containing white (0) and all unique pixel colors present in the input grid strictly *outside* the identified frame's bounding box.
3.  Create a new output grid whose dimensions are sized to fit the inner region identified in step 1, plus a one-pixel border on all sides.
4.  Fill the one-pixel border of the output grid with the frame's color identified in step 1. Initialize the interior to white (0).
5.  Iterate through each pixel within the inner region of the input grid.
6.  For each pixel, check if its color is in the set of 'background colors' identified in step 2.
7.  If the pixel's color is a background color, keep the corresponding output pixel as white (0).
8.  Otherwise (if the pixel's color is not a background color), copy the pixel's original color to the corresponding position within the output grid's interior.
9.  Return the constructed output grid.
"""

def find_frame_coords(grid: np.ndarray) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Finds a 1-pixel thick, single-color, non-white, hollow rectangular frame.
    Focuses on checking perimeter count and shape.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (frame_color, outer_min_r, outer_min_c, outer_max_r, outer_max_c)
        representing the frame's color and the outer bounding box of the frame itself,
        or None if no such frame is found.
    """
    rows, cols = grid.shape
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

        # Check 1: Count pixels. Should match perimeter length for a hollow rect.
        # Perimeter count = 2 * height + 2 * width - 4 (accounts for corners)
        expected_perimeter_pixels = 2 * height + 2 * width - 4
        if coords.shape[0] != expected_perimeter_pixels:
             continue # Pixel count doesn't match perimeter

        # Check 2: Shape. Verify all pixels on the perimeter have the correct color.
        is_perimeter_correct = True
        try: # Add try-except for boundary checks
            # Top/Bottom rows
            if not np.all(grid[min_r, min_c:max_c+1] == color) or \
               not np.all(grid[max_r, min_c:max_c+1] == color):
                is_perimeter_correct = False
            # Left/Right columns (excluding corners already checked)
            if is_perimeter_correct and height > 1: # Check columns if height > 1
                 if not np.all(grid[min_r+1:max_r, min_c] == color) or \
                    not np.all(grid[min_r+1:max_r, max_c] == color):
                     is_perimeter_correct = False
        except IndexError:
            is_perimeter_correct = False # Index out of bounds means shape is wrong

        if not is_perimeter_correct:
            continue # Pixels forming the bounding box don't all match the color

        # Check 3: Hollow. Ensure no pixels *inside* the perimeter have the frame color.
        if height > 2 and width > 2: # Only check inner slice if it exists
            inner_slice = grid[min_r + 1 : max_r, min_c + 1 : max_c]
            if np.any(inner_slice == color):
                 continue # Frame color found inside the perimeter

        # Check 4: Thickness 1 (Outer check - optional but good sanity check)
        # Ensure pixels immediately outside the frame are not the frame color
        outer_thick = False
        # Check above (if possible)
        if min_r > 0 and np.any(grid[min_r - 1, min_c:max_c+1] == color): outer_thick = True
        # Check below (if possible)
        if not outer_thick and max_r < rows - 1 and np.any(grid[max_r + 1, min_c:max_c+1] == color): outer_thick = True
        # Check left (if possible)
        if not outer_thick and min_c > 0 and np.any(grid[min_r:max_r+1, min_c - 1] == color): outer_thick = True
        # Check right (if possible)
        if not outer_thick and max_c < cols - 1 and np.any(grid[min_r:max_r+1, max_c + 1] == color): outer_thick = True

        if outer_thick:
            continue # Frame appears thicker than 1 pixel externally

        # If all checks pass, we found our frame
        # Return frame color and OUTER bounds
        return color, min_r, min_c, max_r, max_c

    return None # No frame found


def get_background_colors(grid: np.ndarray, frame_outer_min_r: int, frame_outer_min_c: int, frame_outer_max_r: int, frame_outer_max_c: int) -> Set[int]:
    """
    Identifies colors outside the frame's outer bounding box.

    Args:
        grid: The input grid as a numpy array.
        frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c: Coordinates defining
            the outer bounding box of the frame itself.

    Returns:
        A set containing 0 (white) and all unique colors found strictly outside the frame.
    """
    rows, cols = grid.shape
    background_colors = set([0]) # Always include white

    # Create a mask that is True *inside* the frame's outer box, False otherwise
    mask = np.zeros(grid.shape, dtype=bool)
    # Ensure indices are within grid bounds before slicing
    r_start = max(0, frame_outer_min_r)
    r_end = min(rows, frame_outer_max_r + 1)
    c_start = max(0, frame_outer_min_c)
    c_end = min(cols, frame_outer_max_c + 1)
    
    if r_start < r_end and c_start < c_end:
        mask[r_start:r_end, c_start:c_end] = True 

    # Select pixels where the mask is False (i.e., outside the frame)
    outside_pixels = grid[~mask]
    
    # Get unique colors from the outside pixels
    if outside_pixels.size > 0:
        unique_outside = np.unique(outside_pixels)
        for color in unique_outside:
            background_colors.add(int(color)) # Add numpy int to set

    return background_colors


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Find the frame and its outer coordinates
    frame_info = find_frame_coords(grid_np)
    if frame_info is None:
        # If no frame found, return the input grid unmodified as per some ARC task conventions
        # or handle as an error case (e.g., raise ValueError or return empty list).
        # Returning input seems safer if unsure about specific task requirements.
        # print("Debug: No frame found.")
        return input_grid

    frame_color, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c = frame_info

    # Define inner region coordinates (1 pixel inside the outer frame)
    inner_min_r = frame_outer_min_r + 1
    inner_min_c = frame_outer_min_c + 1
    inner_max_r = frame_outer_max_r - 1
    inner_max_c = frame_outer_max_c - 1

    # Check if inner region is valid (should be guaranteed by find_frame checks)
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
         # This case should ideally not happen if find_frame works correctly
         # print("Debug: Invalid inner region derived.")
         return input_grid # Return input if something went wrong

    # 2. Identify background colors (strictly outside the frame)
    background_colors = get_background_colors(grid_np, frame_outer_min_r, frame_outer_min_c, frame_outer_max_r, frame_outer_max_c)
    # print(f"Debug: Found Frame Color {frame_color} at ({frame_outer_min_r},{frame_outer_min_c})->({frame_outer_max_r},{frame_outer_max_c})")
    # print(f"Debug: Background Colors Identified: {background_colors}")


    # 3. Create the output grid
    inner_height = inner_max_r - inner_min_r + 1
    inner_width = inner_max_c - inner_min_c + 1
    output_height = inner_height + 2
    output_width = inner_width + 2

    # Initialize with white (0) - border will be overwritten later
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 4. Draw the border with frame_color
    output_grid_np[0, :] = frame_color          # Top row
    output_grid_np[-1, :] = frame_color         # Bottom row
    output_grid_np[:, 0] = frame_color          # Left column
    output_grid_np[:, -1] = frame_color         # Right column

    # 5-8. Iterate through the inner region of the input grid, filter, and place in output
    for r_in in range(inner_min_r, inner_max_r + 1):
        for c_in in range(inner_min_c, inner_max_c + 1):
            # Ensure we don't read out of input bounds (shouldn't happen)
            if not (0 <= r_in < rows and 0 <= c_in < cols):
                 continue

            input_pixel_color = grid_np[r_in, c_in]

            # Calculate corresponding output coordinates (offset by 1 for the border)
            r_out = r_in - inner_min_r + 1
            c_out = c_in - inner_min_c + 1

            # Ensure we don't write out of output bounds (shouldn't happen)
            if not (1 <= r_out < output_height - 1 and 1 <= c_out < output_width - 1):
                 continue

            # Check if the input color is a background color
            if input_pixel_color in background_colors:
                # Already initialized to 0, so no action needed, but explicit for clarity
                output_grid_np[r_out, c_out] = 0 # Set to white
            else:
                # Copy the original color if it's not background
                output_grid_np[r_out, c_out] = input_pixel_color

    # 9. Return the completed grid as a list of lists
    return output_grid_np.tolist()