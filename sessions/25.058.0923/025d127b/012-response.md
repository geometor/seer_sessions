# 025d127b • 012 • refine_coder

---
```python
"""
Identifies azure (8) pixels in the input grid.
Removes the leftmost vertically contiguous group(s) of azure pixels.
"""

import numpy as np

def get_contiguous_groups(pixels):
    """Groups vertically contiguous pixels."""
    groups = []
    visited = set()

    for r, c in pixels:
        if (r, c) not in visited:
            group = []
            stack = [(r, c)]
            while stack:
                curr_r, curr_c = stack.pop()
                if (curr_r, curr_c) not in visited:
                    visited.add((curr_r, curr_c))
                    group.append((curr_r, curr_c))
                    # Check neighbors (up and down)
                    if curr_r > 0 and (curr_r - 1, curr_c) in pixels:
                        stack.append((curr_r - 1, curr_c))
                    if curr_r < input_grid.shape[0] - 1 and (curr_r + 1, curr_c) in pixels:
                        stack.append((curr_r + 1, curr_c))
            groups.append(group)
    return groups

def transform(input_grid):
    """Transforms the input grid by removing the leftmost vertically contiguous azure group(s)."""
    output_grid = input_grid.copy()

    # Find the azure pixels
    azure_pixels = set(map(tuple, np.argwhere(input_grid == 8)))

    # Group vertically contiguous azure pixels
    groups = get_contiguous_groups(azure_pixels)
    
    if not groups:
        return output_grid

    # Find the leftmost x-coordinate of each group
    leftmost_x = float('inf')
    leftmost_groups = []
    for group in groups:
        min_x = min(pixel[1] for pixel in group)
        if min_x < leftmost_x:
            leftmost_x = min_x
            leftmost_groups = [group]
        elif min_x == leftmost_x:
            leftmost_groups.append(group)

    # Remove pixels from the leftmost group(s)
    for group in leftmost_groups:
        for r, c in group:
            output_grid[r, c] = 0

    return output_grid
```
