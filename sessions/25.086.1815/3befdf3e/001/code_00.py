import numpy as np
from typing import List, Tuple, Optional

"""
Expands a two-color framed object found in the input grid by one pixel in all directions, 
swaps the inner content color and the frame color within the original object's footprint, 
and uses the original frame color for the new expanded border.

1.  Identify the single contiguous non-white object in the input grid.
2.  Determine the bounding box of this object.
3.  Identify the color of the object's outer frame (frame_color) and the color of its inner content (content_color).
4.  Calculate the bounding box for the output object by expanding the input object's bounding box by 1 pixel outwards.
5.  Create an output grid initialized with the background color (white, 0).
6.  Iterate through each cell (r, c) within the calculated output bounding box:
    a.  If (r, c) lies on the outermost border of the output bounding box, set the output cell color to the original frame_color.
    b.  If (r, c) lies inside the outermost border:
        i.   Look up the color of the cell at the same coordinate (r, c) in the *input* grid (this corresponds to a pixel within the original object). Let this be original_color.
        ii.  If original_color matches the input frame_color, set the output cell color to the input content_color.
        iii. If original_color matches the input content_color, set the output cell color to the input frame_color.
        iv.  (Edge case) If original_color matches neither (e.g., background pixel somehow inside), leave it as background.
7. Return the constructed output grid.
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

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the expansion and color-swapping rule.
    """
    # Convert input to numpy array for easier manipulation
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
    
    # Handle edge case: object is smaller than 2x2 (cannot have distinct frame/content)
    # In such cases, the rule is ambiguous. Based on examples, assume >= 3x3 structure.
    # If the object is 1 pixel wide/high, treat frame/content as the same?
    # The examples show clear frame/content, so we proceed assuming that structure.
    if max_r - min_r < 1 or max_c - min_c < 1:
         # If it's a line or dot, just expand it? Let's stick to the frame/content swap logic.
         # It might behave strangely but follows the derived rule best.
         # If it's 1xN or Nx1, the first pixel is frame, others are content? Unclear.
         # Let's get frame from corner and content from adjacent if possible.
        frame_color = input_np[min_r, min_c]
        if max_r > min_r : # vertical line or block
             content_color = input_np[min_r + 1, min_c]
        elif max_c > min_c: # horizontal line or block
             content_color = input_np[min_r, min_c + 1]
        else: # single pixel
             content_color = frame_color
    else:
        # 2. Identify frame and content colors (assuming frame is 1px thick)
        frame_color = input_np[min_r, min_c]
        content_color = input_np[min_r + 1, min_c + 1] # Color inside the frame

    # 3. Calculate output object bounding box (expanded by 1 pixel)
    # Note: No boundary checks needed based on ARC examples/constraints (output fits)
    out_min_r = min_r - 1
    out_min_c = min_c - 1
    out_max_r = max_r + 1
    out_max_c = max_c + 1

    # 4. Construct the output object within the output grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel (r, c) falls within the output object's bounding box
            if out_min_r <= r <= out_max_r and out_min_c <= c <= out_max_c:
                
                # Check if it's on the new outer frame (the border of the output bbox)
                is_outer_frame = (r == out_min_r or r == out_max_r or 
                                  c == out_min_c or c == out_max_c)
                
                if is_outer_frame:
                    # Set color to the original frame color for the new border
                    output_np[r, c] = frame_color
                else:
                    # Pixel is inside the new outer frame. 
                    # Its color depends on the color at the *same coordinate* in the *input* grid.
                    original_color = input_np[r, c]
                    
                    # Swap colors based on the original color at this position
                    if original_color == frame_color:
                        output_np[r, c] = content_color
                    elif original_color == content_color:
                        output_np[r, c] = frame_color
                    else:
                        # If the original color was neither (e.g., background), keep background.
                        # This handles cases where the input object might not be perfectly rectangularly filled.
                        output_np[r, c] = 0 
            # else: Pixel is outside the output object, remains background (already initialized)

    # Convert back to list of lists for the ARC standard output format
    return output_np.tolist()