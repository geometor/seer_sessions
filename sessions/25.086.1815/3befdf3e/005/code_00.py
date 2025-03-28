import numpy as np
from typing import List, Tuple, Optional

"""
Transforms the input grid based on the following steps:
1.  Find the single non-white object and its bounding box.
2.  Identify the object's frame color (C1) and content color (C2).
3.  Determine the expansion amount (E) based on the object's dimensions (1 if 3x3, 2 otherwise).
4.  Create an output grid initialized with the background color (white, 0).
5.  Fill the area within the original bounding box in the output grid by swapping C1 and C2 from the input grid.
6.  Fill the expanded border area in the output grid with C1, but only along the horizontal and vertical extensions of the original object (excluding corners).
"""

def find_bbox(grid: np.ndarray, ignore_color: int = 0) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the bounding box of all pixels in the grid that do not match the ignore_color.

    Args:
        grid: A numpy array representing the grid.
        ignore_color: The color value to ignore (typically the background color).

    Returns:
        A tuple (min_r, min_c, max_r, max_c) representing the bounding box,
        or None if no non-ignored pixels are found.
    """
    rows, cols = grid.shape
    min_r, min_c = rows, cols
    max_r, max_c = -1, -1
    found = False
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color:
                found = True
                min_r = min(min_r, r)
                min_c = min(min_c, c)
                max_r = max(max_r, r)
                max_c = max(max_c, c)
    if not found:
        return None
    return min_r, min_c, max_r, max_c

def get_frame_content_colors(grid: np.ndarray, bbox: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """
    Determines the frame (C1) and content (C2) colors of an object within a bounding box.
    Assumes the frame color is the most frequent color on the boundary and
    the content color is a different color found inside.

    Args:
        grid: A numpy array representing the grid.
        bbox: The bounding box (min_r, min_c, max_r, max_c) of the object.

    Returns:
        A tuple (frame_color, content_color). Defaults content_color to frame_color
        if no distinct content color is found.
    """
    min_r, min_c, max_r, max_c = bbox
    
    # Simple assumption: frame color is at the top-left corner of the bbox
    frame_color = grid[min_r, min_c]
    content_color = frame_color # Default if no other color found

    # Search within the bounding box for a color different from the frame_color
    found_content = False
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] != frame_color and grid[r,c] != 0: # Ensure it's not background
                content_color = grid[r, c]
                found_content = True
                break
        if found_content:
            break
            
    # Refined check specifically for neighbors if initial search failed (e.g., solid color obj)
    # This part might be redundant given the broad search above, but kept for potential robustness
    if not found_content:
         potential_content_coords = []
         if min_r + 1 <= max_r: potential_content_coords.append((min_r + 1, min_c))
         if min_c + 1 <= max_c: potential_content_coords.append((min_r, min_c + 1))
         if min_r + 1 <= max_r and min_c + 1 <= max_c: potential_content_coords.append((min_r + 1, min_c + 1))
         
         for r_in, c_in in potential_content_coords:
              if 0 <= r_in < grid.shape[0] and 0 <= c_in < grid.shape[1]:
                   neighbor_color = grid[r_in, c_in]
                   if neighbor_color != frame_color and neighbor_color != 0:
                        content_color = neighbor_color
                        found_content = True
                        break

    return frame_color, content_color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)

    # 1. Find the bounding box of the non-white object
    bbox = find_bbox(input_np, ignore_color=0)
    
    # If no object found, return the empty grid
    if bbox is None:
        return output_np.tolist()

    min_r, min_c, max_r, max_c = bbox
    in_h = max_r - min_r + 1
    in_w = max_c - min_c + 1
    
    # 2. Identify frame and content colors
    frame_color, content_color = get_frame_content_colors(input_np, bbox)

    # 3. Determine expansion amount based on input size
    expansion = 1 if (in_h == 3 and in_w == 3) else 2

    # 4. Calculate output object bounding box coordinates
    out_min_r = min_r - expansion
    out_min_c = min_c - expansion
    out_max_r = max_r + expansion
    out_max_c = max_c + expansion

    # Iterate through each pixel of the grid to determine its output color
    for r in range(rows):
        for c in range(cols):
            # Check if the current coordinate (r, c) is within the output bounding box
            is_in_output_bbox = (out_min_r <= r <= out_max_r and out_min_c <= c <= out_max_c)

            if is_in_output_bbox:
                # Check if the coordinate is within the original input bounding box
                is_in_input_bbox = (min_r <= r <= max_r and min_c <= c <= max_c)

                if is_in_input_bbox:
                    # 5. Fill Swapped Interior: Process pixels within the original footprint
                    original_color = input_np[r, c]
                    if original_color == frame_color:
                        output_np[r, c] = content_color
                    elif original_color == content_color:
                        output_np[r, c] = frame_color
                    # else: leave as background (already 0) - handles background pixels within bbox
                
                else:
                    # 6. Fill Expanded Border (excluding corners)
                    # Check if it lies on the horizontal extension (same row range as input bbox)
                    is_horizontal_extension = (min_r <= r <= max_r) and \
                                              (out_min_c <= c < min_c or max_c < c <= out_max_c)
                    # Check if it lies on the vertical extension (same column range as input bbox)
                    is_vertical_extension = (min_c <= c <= max_c) and \
                                            (out_min_r <= r < min_r or max_r < r <= out_max_r)

                    if is_horizontal_extension or is_vertical_extension:
                        output_np[r, c] = frame_color
                    # else: it's a corner of the expanded box, leave as background (already 0)
            
            # else: Pixel is outside the output object's expanded bbox, remains background (already 0)

    # Convert back to list of lists for the ARC standard output format
    return output_np.tolist()