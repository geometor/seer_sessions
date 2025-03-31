import numpy as np
from collections import defaultdict

"""
Transformation Rule:
1. Identify the grid's border color.
2. Scan the inner area (excluding the border) to find a pair of pixels that have the same color (TargetColor), are not background, and are on the same row (TargetRow) at columns Col1 and Col2.
3. Erase all pixels in the grid that are NOT the border color, NOT the TargetColor, and NOT the background color (0).
4. Draw a new 'H' shape using TargetColor, positioned based on TargetRow, Col1, and Col2. The 'H' consists of a horizontal bar from Col1 to Col2 on TargetRow, and two 3-pixel vertical bars centered on TargetRow at columns Col1 and Col2.
"""

def find_isolated_pair(grid_np, border_color):
    """
    Scans the inner area of the grid to find the isolated pair.

    Args:
        grid_np: The input grid as a numpy array.
        border_color: The color of the border pixels.

    Returns:
        A tuple (target_color, target_row, col1, col2) if found,
        otherwise raises ValueError.
    """
    height, width = grid_np.shape
    inner_pixels_by_color = defaultdict(list)

    # Scan inner grid (rows 1 to height-2, cols 1 to width-2)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            color = grid_np[r, c]
            # Ignore background and border colors found inside (shouldn't happen based on examples)
            if color != 0 and color != border_color:
                inner_pixels_by_color[color].append((r, c))

    # Find the color associated with exactly two pixels
    for color, pixels in inner_pixels_by_color.items():
        if len(pixels) == 2:
            p1_row, p1_col = pixels[0]
            p2_row, p2_col = pixels[1]
            # Check if they are on the same row
            if p1_row == p2_row:
                target_color = color
                target_row = p1_row
                col1 = min(p1_col, p2_col)
                col2 = max(p1_col, p2_col)
                return target_color, target_row, col1, col2

    raise ValueError("Isolated pixel pair not found in the inner grid.")


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # 1. Identify Border Color
    border_color = input_grid_np[0, 0]

    # 2. Find Isolated Pair properties
    try:
        target_color, target_row, col1, col2 = find_isolated_pair(input_grid_np, border_color)
    except ValueError as e:
        print(f"Error finding isolated pair: {e}")
        # Return unmodified grid or handle error as appropriate
        return input_grid # Return original if pattern not found

    # 3. Erase the old shape
    # Iterate through the entire grid
    for r in range(height):
        for c in range(width):
            current_color = input_grid_np[r, c]
            # Check if the color is not border, not target, and not background
            if current_color != border_color and \
               current_color != target_color and \
               current_color != 0:
                output_grid[r, c] = 0 # Set to background color

    # 4. Draw the new 'H' shape
    # Draw horizontal bar (ensure within bounds)
    if 0 <= target_row < height:
        for c in range(col1, col2 + 1):
            if 0 <= c < width:
                output_grid[target_row, c] = target_color

    # Draw left vertical bar (3 pixels high, ensure within bounds)
    if 0 <= col1 < width:
        for r_offset in [-1, 0, 1]:
            r = target_row + r_offset
            if 0 <= r < height:
                output_grid[r, col1] = target_color

    # Draw right vertical bar (3 pixels high, ensure within bounds)
    if 0 <= col2 < width:
        for r_offset in [-1, 0, 1]:
            r = target_row + r_offset
            if 0 <= r < height:
                output_grid[r, col2] = target_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()