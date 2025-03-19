# ea786f4a • 005 • refine_coder

---
```python
"""
Identify the largest contiguous rectangle of a single, *non-black* color in the input grid. Create an output grid with the dimensions of the bounding box containing this rectangle. Copy the largest rectangle to the top-left corner of the output grid.
"""

import numpy as np

def find_largest_rectangle(grid):
    """
    Finds the largest rectangle of a single non-black color in a grid.
    """
    grid = np.array(grid)
    rows, cols = grid.shape
    max_area = 0
    best_rect = None

    for color in np.unique(grid):
        if color == 0:  # Skip black
            continue

        # Create a binary mask for the current color
        color_mask = (grid == color)

        # Find the largest rectangle within the binary mask
        for r1 in range(rows):
            for c1 in range(cols):
                if color_mask[r1, c1]:
                    for r2 in range(r1, rows):
                        for c2 in range(c1, cols):
                            if not color_mask[r1:r2+1, c1:c2+1].all():
                                break  # Not a rectangle of the current color

                            area = (r2 - r1 + 1) * (c2 - c1 + 1)
                            if area > max_area:
                                max_area = area
                                best_rect = {
                                    'color': color,
                                    'top_left': (r1, c1),
                                    'height': r2 - r1 + 1,
                                    'width': c2 - c1 + 1,
                                }
    return best_rect

def transform(input_grid):
    # Find the largest non-black rectangle
    largest_rect = find_largest_rectangle(input_grid)

    if largest_rect is None:
        return [] # Return empty grid if no non-black rectangle is found

    # Extract rectangle information
    color = largest_rect['color']
    top_left_row, top_left_col = largest_rect['top_left']
    height = largest_rect['height']
    width = largest_rect['width']

    # Create the output grid
    output_grid = np.full((height, width), color)

    return output_grid
```
