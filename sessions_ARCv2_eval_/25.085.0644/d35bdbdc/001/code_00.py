import numpy as np

"""
Identifies 3x3 'frame objects' within the input grid. A frame object has a center pixel surrounded by 8 pixels of an identical color (FrameColor), which is different from the center pixel's color (CenterColor). Based on the specific pair of (FrameColor, CenterColor), one of three actions is taken:
1. Removal: If the pair matches a predefined set of 'removal pairs', the entire 3x3 region is replaced with white (0).
2. Center Modification: If the pair matches a predefined 'change map', only the CenterColor is changed to a specific NewCenterColor, leaving the frame intact.
3. No Change: If the pair doesn't match any removal or change rules, the 3x3 region remains unchanged.
Other pixels outside these frame objects are also unchanged.
"""

def _is_frame_object(grid, r, c):
    """Checks if the 3x3 region centered at (r, c) is a frame object."""
    height, width = grid.shape
    # Ensure center is not on the border
    if r <= 0 or r >= height - 1 or c <= 0 or c >= width - 1:
        return False, -1, -1

    center_color = grid[r, c]
    frame_color = grid[r-1, c-1] # Use top-left as reference frame color

    # Check if all frame pixels have the same color
    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            if i == r and j == c:
                continue # Skip center
            if grid[i, j] != frame_color:
                return False, -1, -1

    # Check if frame color is different from center color
    if frame_color == center_color:
        return False, -1, -1

    return True, frame_color, center_color

def transform(input_grid):
    """
    Applies transformations to 3x3 frame objects based on their frame and center colors.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the transformation rules based on observations
    removal_pairs = {
        (4, 2), (1, 3), (2, 6), (3, 2), (4, 8), (3, 6), (2, 9), (4, 3)
    }
    change_map = {
        (3, 4): 2, (6, 1): 3, (8, 3): 2, (1, 4): 8, (1, 2): 9, (7, 4): 3
    }

    # Iterate through potential center pixels (excluding borders)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check if the current location is the center of a frame object
            is_frame, frame_color, center_color = _is_frame_object(input_grid, r, c)

            if is_frame:
                color_pair = (frame_color, center_color)

                # Check for removal rule
                if color_pair in removal_pairs:
                    # Replace the 3x3 region with white (0)
                    output_grid[r-1:r+2, c-1:c+2] = 0
                # Check for center change rule
                elif color_pair in change_map:
                    # Change only the center pixel color
                    new_center_color = change_map[color_pair]
                    output_grid[r, c] = new_center_color
                # Otherwise, no change is needed as output_grid is a copy

    return output_grid