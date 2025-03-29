import numpy as np
import collections

"""
Transformation Rule:
1. Identify a rectangular frame within the input grid. This frame is characterized by having all its border pixels (top row, bottom row, left column, right column) composed of a single, uniform color. This framing color is unique for each task example (e.g., red, green, magenta). Common background colors like white (0) are typically not the frame color.
2. Determine the coordinates (top row, left column, bottom row, right column) of this identified frame.
3. Extract the subgrid enclosed by and including the frame from the input grid.
4. The extracted subgrid is the output grid.
"""

def find_frame(grid):
    """
    Scans the input grid to locate a rectangular frame formed by a single color.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple (min_r, min_c, max_r, max_c, frame_color) representing the 
               top-left and bottom-right coordinates and the color of the frame, 
               or None if no such frame is found.
    """
    rows, cols = grid.shape
    # Get unique colors present, excluding white (0) as it's unlikely to be the frame
    # Based on examples, red(2), green(3), magenta(6) were frames. Gray(5) seems structural.
    # Let's prioritize non-zero colors.
    candidate_colors = sorted([c for c in np.unique(grid) if c != 0])

    for color in candidate_colors:
        # Find all coordinates where the current color appears
        pixel_coords = np.argwhere(grid == color)
        if len(pixel_coords) < 4:  # Need at least 4 pixels for a minimal frame
            continue

        # Determine the bounding box of these pixels
        min_r = np.min(pixel_coords[:, 0])
        max_r = np.max(pixel_coords[:, 0])
        min_c = np.min(pixel_coords[:, 1])
        max_c = np.max(pixel_coords[:, 1])

        # Check if this bounding box forms a valid frame of the current color
        is_frame = True

        # Check top edge
        if not np.all(grid[min_r, min_c:max_c+1] == color):
            is_frame = False
        # Check bottom edge
        if is_frame and not np.all(grid[max_r, min_c:max_c+1] == color):
            is_frame = False
        # Check left edge
        if is_frame and not np.all(grid[min_r:max_r+1, min_c] == color):
             is_frame = False
        # Check right edge
        if is_frame and not np.all(grid[min_r:max_r+1, max_c] == color):
            is_frame = False

        # If all edges match the color, we found the frame
        if is_frame:
            # Verify that *only* frame pixels within the bounding box have the frame color
            # (this helps distinguish from solid blocks of the same color)
            is_solid_block = True
            for r in range(min_r + 1, max_r):
                for c in range(min_c + 1, max_c):
                    if grid[r, c] != color:
                        is_solid_block = False
                        break
                if not is_solid_block:
                    break
            
            # A frame should not be a solid block of the frame color.
            # (Unless the inside is 1x1 or 0xN etc., handled by edge checks)
            if max_r > min_r + 1 and max_c > min_c + 1 and is_solid_block:
                 continue # Skip solid blocks mistaken for frames

            # We found a valid frame
            return min_r, min_c, max_r, max_c, color

    # If no frame found after checking all candidate colors
    return None

def extract_subgrid(grid, frame_coords):
    """
    Extracts the subgrid defined by the frame coordinates.

    Args:
        grid (np.array): The input grid.
        frame_coords (tuple): (min_r, min_c, max_r, max_c) coordinates of the frame.

    Returns:
        np.array: The extracted subgrid.
    """
    min_r, min_c, max_r, max_c = frame_coords
    return grid[min_r : max_r + 1, min_c : max_c + 1]

def transform(input_grid):
    """
    Identifies a single-color rectangular frame in the input grid and extracts 
    the subgrid defined by that frame.
    
    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid (the extracted subgrid).
    """
    # Find the frame coordinates and color
    frame_info = find_frame(input_grid)

    if frame_info:
        min_r, min_c, max_r, max_c, _ = frame_info
        # Extract the subgrid based on the frame coordinates
        output_grid = extract_subgrid(input_grid, (min_r, min_c, max_r, max_c))
        return output_grid
    else:
        # Handle error case: No frame found (shouldn't happen based on examples)
        # Returning the input grid or an empty grid might be options,
        # but for ARC, it implies the logic is wrong. Let's return input for now.
        print("Warning: No frame found in the input grid.")
        return input_grid # Or raise an error, or return None/empty array
