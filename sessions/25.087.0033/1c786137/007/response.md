```python
import numpy as np
from typing import List, Tuple, Optional

"""
Identifies a rectangular frame defined by the bounding box of a single non-white color 
whose pixels exclusively form the 1-pixel thick perimeter of that bounding box within 
the grid. It then extracts the content (subgrid) located strictly inside this frame. 
If multiple such valid frames exist (potentially of different colors), the one whose 
bounding box encloses the largest area (height * width) is chosen. If no such frame 
is found, or if the selected frame is too small (less than 3x3) to contain any content, 
an empty grid (represented as an empty list) is returned.
"""

def _find_bounding_box(grid: np.ndarray, color: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the minimum and maximum row and column indices for a given color in the grid.

    Args:
        grid: The input numpy array grid.
        color: The color to find the bounding box for.

    Returns:
        A tuple (min_row, min_col, max_row, max_col) if the color exists, otherwise None.
    """
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return None
    return rows.min(), cols.min(), rows.max(), cols.max()

def _is_valid_frame(grid: np.ndarray, color: int, r1: int, c1: int, r2: int, c2: int) -> bool:
    """
    Checks if the pixels of the specified 'color' perfectly and exclusively form 
    the 1-pixel thick perimeter of the bounding box defined by r1, c1, r2, c2.

    Args:
        grid: The input numpy array grid.
        color: The color of the potential frame.
        r1, c1, r2, c2: The bounding box coordinates.

    Returns:
        True if it's a valid frame, False otherwise.
    """
    box_h = r2 - r1 + 1
    box_w = c2 - c1 + 1

    # Calculate the expected number of pixels on the perimeter
    if box_h == 1 and box_w == 1:
        expected_perimeter_pixels = 1
    elif box_h == 1:
        expected_perimeter_pixels = box_w
    elif box_w == 1:
        expected_perimeter_pixels = box_h
    else:
        expected_perimeter_pixels = 2 * box_h + 2 * box_w - 4 # Subtract 4 corners counted twice

    # Count the total number of pixels of 'color' in the entire grid
    total_color_pixels = np.count_nonzero(grid == color)

    # If the total count doesn't match the expected perimeter count, it can't be a valid frame
    if total_color_pixels != expected_perimeter_pixels:
        return False

    # Verify that all pixels *on* the perimeter within the bounding box match the color.
    # If the counts match, we just need to confirm they are *in the right place*.

    # Check top row
    if not np.all(grid[r1, c1:c2+1] == color):
        return False
        
    # Check bottom row (only if height > 1)
    if box_h > 1 and not np.all(grid[r2, c1:c2+1] == color):
        return False
        
    # Check left column (excluding corners, only if height > 2)
    if box_h > 2 and not np.all(grid[r1+1:r2, c1] == color):
        return False
        
    # Check right column (excluding corners, only if height > 2 and width > 1)
    # Note: The check `box_w > 1` is important here. If width is 1, the right col is the same as the left.
    if box_h > 2 and box_w > 1 and not np.all(grid[r1+1:r2, c2] == color):
        return False

    # If all checks passed (count matches and perimeter pixels are correct), it's a valid frame
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
    # Handle empty input grid early
    if not input_grid or not input_grid[0]:
        return []

    # Convert input to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Find unique non-white colors (potential frame colors)
    # Use grid[grid != 0] to efficiently get non-zero values before finding unique ones
    potential_frame_colors = np.unique(grid[grid != 0]) 

    best_frame_coords = None # Store as (min_row, min_col, max_row, max_col)
    max_frame_area = -1

    # 1. Iterate through each potential frame color
    for color in potential_frame_colors:
        # 2. Determine the bounding box of this color
        bbox = _find_bounding_box(grid, color)
        if bbox is None:
            continue # Should not happen given how potential_frame_colors is derived, but safe check
            
        min_r, min_c, max_r, max_c = bbox

        # 3. Validate that this color forms a perfect and exclusive frame
        if _is_valid_frame(grid, color, min_r, min_c, max_r, max_c):
            # Calculate the area enclosed by this frame's bounding box
            area = (max_r - min_r + 1) * (max_c - min_c + 1)

            # 4. Update if this is the largest valid frame found so far
            if area > max_frame_area:
                max_frame_area = area
                best_frame_coords = (min_r, min_c, max_r, max_c)
            # Note: Tie-breaking for area is implicit - the first largest frame encountered wins.
            # If a different tie-breaking rule is needed (e.g., smallest color index), 
            # it would need to be added here.

    # 5. Process the selected frame (if any)
    if best_frame_coords:
        min_r, min_c, max_r, max_c = best_frame_coords

        # 6. Check if the frame can contain content (size > 2x2)
        # Frame needs height > 2 and width > 2 to have something strictly inside
        if max_r > min_r + 1 and max_c > min_c + 1:
            # 7. Extract the content strictly inside the frame
            # Numpy slicing end index is exclusive
            content_grid_np = grid[min_r + 1 : max_r, min_c + 1 : max_c]
            
            # Convert the numpy array back to a list of lists for the final output
            output_grid = content_grid_np.tolist()
            return output_grid
        else:
            # 8. Frame exists but is too small to contain anything (e.g., a line or 2xN rect). 
            # Return empty grid.
             return [] 
    else:
        # 5. Handle No Frame: No valid frame found after checking all colors. 
        # Return empty grid.
        return []
```