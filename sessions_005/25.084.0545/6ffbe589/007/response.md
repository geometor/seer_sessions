```python
"""
The transformation rule involves finding the bounding box for each distinct
non-zero color in the input grid, and then reconstructing an output that
represents the layout of non-zero objects.
"""

import numpy as np

def get_bounding_box_per_color(grid):
    """
    Finds the bounding box of each distinct non-zero color in a grid.

    Args:
        grid: A 2D numpy array.

    Returns:
        A dictionary where keys are colors (integers) and values are tuples
        (min_row, max_row, min_col, max_col) representing the bounding box.
        Returns empty dict if no objects found.
    """
    bounding_boxes = {}
    unique_colors = np.unique(grid)

    for color in unique_colors:
        if color != 0:  # Ignore background color
            rows, cols = np.where(grid == color)
            if rows.size and cols.size:
                min_row, max_row = np.min(rows), np.max(rows)
                min_col, max_col = np.min(cols), np.max(cols)
                bounding_boxes[color] = (min_row, max_row, min_col, max_col)
    return bounding_boxes


def transform(input_grid):
    """
    Transforms the input grid by finding bounding boxes for each distinct color,
    and reconstruct the output grid.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the output grid.
    """
    input_grid = np.array(input_grid)
    color_bboxes = get_bounding_box_per_color(input_grid)

    if not color_bboxes:
        return []

    # Find overall bounding box encompassing all color-specific boxes
    all_min_row = min(bbox[0] for bbox in color_bboxes.values())
    all_max_row = max(bbox[1] for bbox in color_bboxes.values())
    all_min_col = min(bbox[2] for bbox in color_bboxes.values())
    all_max_col = max(bbox[3] for bbox in color_bboxes.values())
    
    output_grid = np.zeros((all_max_row - all_min_row + 1, all_max_col - all_min_col + 1), dtype=int)

    for color, (min_row, max_row, min_col, max_col) in color_bboxes.items():
      # copy object into the output grid using the bounding box dimensions and
      # location
      object_rows, object_cols = np.where(input_grid == color)
      
      # compute relative position of each element
      relative_rows = object_rows - all_min_row
      relative_cols = object_cols - all_min_col
      
      # copy each element to the new grid
      output_grid[relative_rows, relative_cols] = color
    
    return output_grid.tolist()
```