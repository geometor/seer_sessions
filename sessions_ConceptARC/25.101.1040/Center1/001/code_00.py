import numpy as np
import copy

"""
Identifies hollow rectangular frames (1 pixel thick, single non-white color) in the input grid.
If a frame is 3x3, fills the entire 3x3 area (frame and interior) with the frame's color.
If a frame is larger than 3x3, fills the single centermost pixel of the hollow interior with the frame's color.
Pixels not part of identified frames or their modified interiors remain unchanged.
"""

def _is_valid(r, c, height, width):
    """Check if coordinates are within grid boundaries."""
    return 0 <= r < height and 0 <= c < width

def _find_frames(grid: np.ndarray) -> list[tuple[int, int, int, int, int]]:
    """
    Finds all hollow rectangular frames in the grid.

    A frame is defined by:
    - A 1-pixel thick border of a single non-white color.
    - A rectangular interior filled entirely with the background color (0).

    Returns:
        A list of tuples, where each tuple represents a frame:
        (top_row, left_col, height, width, frame_color)
    """
    frames = []
    height, width = grid.shape
    visited_corners = set() # To avoid detecting the same frame multiple times from different corners

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Potential top-left corner: non-white pixel
            if color != 0 and (r, c) not in visited_corners:
                # Check potential frame properties starting from this corner
                
                # 1. Find potential width (w) along the top edge
                potential_w = 0
                for i in range(c, width):
                    if grid[r, i] == color:
                        potential_w += 1
                    else:
                        break
                if potential_w < 3: continue # Minimum frame width is 3

                # 2. Find potential height (h) along the left edge
                potential_h = 0
                for j in range(r, height):
                    if grid[j, c] == color:
                        potential_h += 1
                    else:
                        break
                if potential_h < 3: continue # Minimum frame height is 3

                # 3. Verify if it's a hollow rectangle
                is_frame = True
                # Check right edge
                for j in range(r, r + potential_h):
                    if not _is_valid(j, c + potential_w - 1, height, width) or grid[j, c + potential_w - 1] != color:
                        is_frame = False
                        break
                if not is_frame: continue

                # Check bottom edge
                for i in range(c, c + potential_w):
                     if not _is_valid(r + potential_h - 1, i, height, width) or grid[r + potential_h - 1, i] != color:
                        is_frame = False
                        break
                if not is_frame: continue

                # Check interior (must be background color 0)
                for row_inner in range(r + 1, r + potential_h - 1):
                    for col_inner in range(c + 1, c + potential_w - 1):
                        if not _is_valid(row_inner, col_inner, height, width) or grid[row_inner, col_inner] != 0:
                            is_frame = False
                            break
                    if not is_frame: break
                if not is_frame: continue

                # If all checks pass, it's a frame
                frames.append((r, c, potential_h, potential_w, color))
                # Mark corners to avoid re-detection
                visited_corners.add((r, c))
                visited_corners.add((r, c + potential_w - 1))
                visited_corners.add((r + potential_h - 1, c))
                visited_corners.add((r + potential_h - 1, c + potential_w - 1))

    return frames


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on identified hollow rectangular frames.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Find all hollow rectangular frames
    frames = _find_frames(input_np)

    # Process each found frame
    for r, c, h, w, color in frames:
        # Condition: Frame size is 3x3
        if h == 3 and w == 3:
            # Action: Fill the entire 3x3 area with the frame's color
            for i in range(r, r + 3):
                for j in range(c, c + 3):
                    # Check boundaries just in case, though find_frames should ensure validity
                    if _is_valid(i, j, height, width):
                        output_np[i, j] = color
        # Condition: Frame size is greater than 3x3
        elif h > 3 and w > 3:
            # Action: Fill the center of the hollow interior
            # Calculate interior dimensions and top-left corner
            interior_r = r + 1
            interior_c = c + 1
            interior_h = h - 2
            interior_w = w - 2

            # Calculate the geometric center of the interior
            # // is integer division, equivalent to floor for positive results
            center_r = interior_r + (interior_h - 1) // 2
            center_c = interior_c + (interior_w - 1) // 2

            # Change the color of the center pixel
            if _is_valid(center_r, center_c, height, width):
                 output_np[center_r, center_c] = color

    # Convert the result back to a list of lists
    output_grid = output_np.tolist()
    return output_grid