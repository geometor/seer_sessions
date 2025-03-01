# a64e4611 • 012 • refine_coder

---
```python
"""
1. Identify all blue (1) pixels in the input grid.
2. Determine if the blue pixels form one or more complete rectangles. A complete rectangle has a continuous blue border with no gaps.
3. If multiple complete blue rectangles are present, select the outermost rectangle. The outermost rectangle is the one that is not contained within any other rectangle.
4. If no or incomplete rectangle are present, do nothing.
5. If a single, complete, outermost blue rectangle is found, identify the white (0) pixels enclosed within this rectangle.
6. Replace the enclosed white pixels with green (3) pixels.
7. Pixels outside the outermost blue rectangle, including the blue pixels forming the rectangle, remain unchanged.
"""

import numpy as np

def get_bounding_box(pixels):
    """
    Returns the bounding box (min_row, min_col, max_row, max_col) of a list of pixels.
    """
    if not pixels:
        return None
    min_row = min(pixel[0] for pixel in pixels)
    max_row = max(pixel[0] for pixel in pixels)
    min_col = min(pixel[1] for pixel in pixels)
    max_col = max(pixel[1] for pixel in pixels)
    return (min_row, min_col, max_row, max_col)

def is_complete_rectangle(blue_pixels, bbox):
    """
    Checks if the given blue pixels form a complete rectangular boundary defined by the bounding box.
    """
    if not blue_pixels or bbox is None:
        return False

    min_row, min_col, max_row, max_col = bbox

    # Check if the number of blue pixels matches the perimeter of the rectangle
    expected_count = 2 * (max_row - min_row + 1) + 2 * (max_col - min_col + 1) - 4
    if len(blue_pixels) != expected_count:
        return False

    # check the boundary condition
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col+1):
            if (r == min_row or r == max_row) or (c == min_col or c == max_col):
                if (r,c) not in blue_pixels:
                    return False
    return True
    
def is_outermost_rectangle(bbox, all_bboxes):
    """
    Checks if a given bounding box is the outermost among a list of bounding boxes.
    """
    if not all_bboxes:
        return True

    min_row, min_col, max_row, max_col = bbox

    for other_bbox in all_bboxes:
        if bbox == other_bbox:
            continue

        other_min_row, other_min_col, other_max_row, other_max_col = other_bbox

        if (other_min_row <= min_row and other_min_col <= min_col and
                other_max_row >= max_row and other_max_col >= max_col):
            return False  # The current bbox is contained within another bbox

    return True

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find blue pixels
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                blue_pixels.append((r, c))

    # Find all potential bounding boxes
    all_bboxes = []
    
    # Get all possible rectangles
    for r1 in range(rows):
        for c1 in range(cols):
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    all_bboxes.append((r1, c1, r2, c2))
    
    complete_rect_bboxes = []
    for bbox in all_bboxes:
        # Extract blue pixels that might form this rectangle
        rect_blue_pixels = [p for p in blue_pixels if (p[0] == bbox[0] or p[0] == bbox[2]) and bbox[1] <= p[1] <= bbox[3] or (p[1] == bbox[1] or p[1] == bbox[3]) and bbox[0] <= p[0] <= bbox[2]]
        if is_complete_rectangle(rect_blue_pixels, bbox):
           complete_rect_bboxes.append(bbox)
           
    outermost_bbox = None
    for bbox in complete_rect_bboxes:
        if is_outermost_rectangle(bbox, complete_rect_bboxes):
            outermost_bbox = bbox
            break

    # If an outermost complete rectangle is found, fill the enclosed white region
    if outermost_bbox:
        min_row, min_col, max_row, max_col = outermost_bbox
        for r in range(min_row + 1, max_row):
            for c in range(min_col + 1, max_col):
                if output_grid[r, c] == 0:
                    output_grid[r, c] = 3

    return output_grid
```
