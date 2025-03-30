"""
Identifies contiguous red (2) shapes in the input grid. Calculates the center and bounding box for each shape. 
Finds pairs of shapes whose centers are aligned either horizontally (same row) or vertically (same column).
For each aligned pair, draws a blue (1) line segment in the white (0) space between their bounding boxes along the line connecting their centers.
Horizontal lines are drawn along the shared center row, and vertical lines are drawn along the shared center column.
The final output is the input grid with these blue lines added.
"""

import numpy as np
from collections import deque

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a dictionary containing:
              'pixels': A set of (row, col) tuples for the object's pixels.
              'center': A tuple (center_row, center_col) rounded to nearest int.
              'bbox': A tuple (min_row, max_row, min_col, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                sum_r, sum_c = 0, 0
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    sum_r += row
                    sum_c += col
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if obj_pixels:
                    num_pixels = len(obj_pixels)
                    center_r = round(sum_r / num_pixels)
                    center_c = round(sum_c / num_pixels)
                    objects.append({
                        'pixels': obj_pixels,
                        'center': (int(center_r), int(center_c)),
                        'bbox': (min_r, max_r, min_c, max_c)
                    })
    return objects

def transform(input_grid):
    """
    Connects aligned red shapes with blue lines.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with blue lines added.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    red_color = 2
    blue_color = 1
    background_color = 0

    # 1. Identify all red shapes, their centers, and bounding boxes
    red_objects = find_objects(grid, red_color)

    # 2. Iterate through all pairs of shapes to find alignments
    num_objects = len(red_objects)
    for i in range(num_objects):
        for j in range(i + 1, num_objects):
            obj1 = red_objects[i]
            obj2 = red_objects[j]

            center1_r, center1_c = obj1['center']
            center2_r, center2_c = obj2['center']
            bbox1 = obj1['bbox'] # min_r, max_r, min_c, max_c
            bbox2 = obj2['bbox'] # min_r, max_r, min_c, max_c

            # 3. Check for horizontal alignment (same center row)
            if center1_r == center2_r:
                draw_row = center1_r
                # Determine which object is left and which is right
                if center1_c < center2_c:
                    left_obj_bbox = bbox1
                    right_obj_bbox = bbox2
                else:
                    left_obj_bbox = bbox2
                    right_obj_bbox = bbox1
                
                # Define the column range for the line
                start_col = left_obj_bbox[3] + 1 # max_col of left object + 1
                end_col = right_obj_bbox[2]     # min_col of right object (exclusive)

                # Check if the path is clear (all background) and draw the line
                is_clear = True
                if start_col < end_col: # Ensure there's a gap
                    for c in range(start_col, end_col):
                         # Check bounds just in case center is outside grid somehow (shouldn't happen with rounding)
                        if not (0 <= draw_row < output_grid.shape[0] and 0 <= c < output_grid.shape[1]):
                            is_clear = False
                            break
                        if output_grid[draw_row, c] != background_color:
                            is_clear = False
                            break
                    if is_clear:
                        output_grid[draw_row, start_col:end_col] = blue_color

            # 4. Check for vertical alignment (same center column)
            elif center1_c == center2_c:
                draw_col = center1_c
                # Determine which object is top and which is bottom
                if center1_r < center2_r:
                    top_obj_bbox = bbox1
                    bottom_obj_bbox = bbox2
                else:
                    top_obj_bbox = bbox2
                    bottom_obj_bbox = bbox1

                # Define the row range for the line
                start_row = top_obj_bbox[1] + 1 # max_row of top object + 1
                end_row = bottom_obj_bbox[0]    # min_row of bottom object (exclusive)

                # Check if the path is clear (all background) and draw the line
                is_clear = True
                if start_row < end_row: # Ensure there's a gap
                    for r in range(start_row, end_row):
                         # Check bounds
                        if not (0 <= r < output_grid.shape[0] and 0 <= draw_col < output_grid.shape[1]):
                            is_clear = False
                            break
                        if output_grid[r, draw_col] != background_color:
                            is_clear = False
                            break
                    if is_clear:
                        output_grid[start_row:end_row, draw_col] = blue_color

    return output_grid.tolist()