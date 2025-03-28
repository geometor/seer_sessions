```python
import numpy as np
from typing import List, Tuple, Optional

"""
Identifies a rectangular frame defined by the bounding box of a single non-white color 
whose pixels exclusively occupy the perimeter of that bounding box within the grid. 
It then extracts the content (subgrid) located strictly inside this frame, excluding 
the frame pixels themselves. If multiple such frames exist, the one enclosing the 
largest area is chosen. If no such frame is found, or if the frame is too thin 
(less than 3x3) to contain any content, an empty grid is returned.

Note: This logic successfully explains Examples 1 and 2 of task 'aec13089', but 
it predicts an incorrect output for Example 3. The extraction rule might need 
further refinement to handle all cases.
"""

def _is_perimeter_correct(grid: np.ndarray, color: int, r1: int, c1: int, r2: int, c2: int) -> bool:
    """
    Checks if all grid cells on the perimeter of the given bounding box match the specified color.

    Args:
        grid: The input grid as a numpy array.
        color: The color value expected on the perimeter.
        r1: Minimum row index of the bounding box (inclusive).
        c1: Minimum column index of the bounding box (inclusive).
        r2: Maximum row index of the bounding box (inclusive).
        c2: Maximum column index of the bounding box (inclusive).

    Returns:
        True if all perimeter cells match the color, False otherwise.
    """
    height, width = grid.shape

    # Check top and bottom rows
    for c in range(c1, c2 + 1):
        if not (0 <= r1 < height and 0 <= c < width and grid[r1, c] == color):
            return False
        # Avoid double-checking corners if height is 1
        if r1 != r2 and not (0 <= r2 < height and 0 <= c < width and grid[r2, c] == color):
            return False
            
    # Check left and right columns (excluding corners already checked)
    for r in range(r1 + 1, r2):
        if not (0 <= r < height and 0 <= c1 < width and grid[r, c1] == color):
             return False
        # Avoid double-checking if width is 1
        if c1 != c2 and not (0 <= r < height and 0 <= c2 < width and grid[r, c2] == color):
            return False

    return True


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Extracts the content inside the largest valid rectangular frame.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the extracted content subgrid, or an empty list 
        if no suitable frame is found or the frame contains no content.
    """
    if not input_grid or not input_grid[0]:
        return []

    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Find unique non-white colors (potential frame colors)
    potential_frame_colors = np.unique(grid[grid != 0])

    best_frame_coords = None # Store as (min_row, min_col, max_row, max_col)
    max_frame_area = -1

    # Iterate through each potential frame color
    for color in potential_frame_colors:
        # Find all coordinates where this color appears
        rows, cols = np.where(grid == color)

        if rows.size == 0:  # No pixels of this color found
            continue

        # Determine the bounding box of this color
        min_r, max_r = rows.min(), rows.max()
        min_c, max_c = cols.min(), cols.max()

        # Verify that this color forms the perimeter of its bounding box
        if _is_perimeter_correct(grid, color, min_r, min_c, max_r, max_c):
            # Check if all pixels of this color *only* lie on the perimeter
            # This prevents selecting solid rectangles mistaken as frames
            is_only_perimeter = True
            for r_idx, c_idx in zip(rows, cols):
                if not (r_idx == min_r or r_idx == max_r or c_idx == min_c or c_idx == max_c):
                    is_only_perimeter = False
                    break
            
            if is_only_perimeter:
                # Calculate the area enclosed by this frame
                # Using bounding box dimensions for area comparison
                area = (max_r - min_r + 1) * (max_c - min_c + 1)

                # Update if this is the largest valid frame found so far
                if area > max_frame_area:
                    max_frame_area = area
                    best_frame_coords = (min_r, min_c, max_r, max_c)

    # If a frame was found
    if best_frame_coords:
        min_r, min_c, max_r, max_c = best_frame_coords

        # Check if the frame has inner content (i.e., it's at least 3x3)
        # The frame needs to be wider/taller than 2 pixels to have content inside
        if max_r > min_r + 1 and max_c > min_c + 1:
            # Extract the content strictly inside the frame
            # The slice end indices are exclusive
            content_grid = grid[min_r + 1 : max_r, min_c + 1 : max_c]
            # Convert the numpy array back to a list of lists
            output_grid = content_grid.tolist()
            return output_grid
        else:
            # Frame exists but is too small to contain anything (e.g., a line or 2xN rect)
            # Return empty grid according to ARC convention
             return [] 
    else:
        # No suitable frame found
        # Return empty grid according to ARC convention
        return []
```