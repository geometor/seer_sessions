Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Identifies a sequence of nested colors in the input grid, starting from an 
approximate center and expanding outwards layer by layer based on adjacency. 
The output grid is a square whose size is determined by the number of nested 
colors (N), with dimensions (2*N - 1) x (2*N - 1). This grid is filled 
with concentric square frames of the identified colors, with the innermost 
color at the center and the outermost color forming the border.
"""

def find_center_and_color_sequence(input_grid):
    """
    Finds the geometric center of non-background pixels and identifies
    the sequence of nested colors expanding outwards from the center color.

    The BFS explores layer by layer. When moving from pixels of color A to pixels
    of color B, color B is considered the next layer outwards.

    Returns:
        list: Sequence of colors from outermost (C1) to innermost (CK).
              Returns an empty list if no non-background pixels are found or
              sequence cannot be determined.
    """
    h, w = input_grid.shape
    non_background_pixels = np.argwhere(input_grid != 0)
    
    if non_background_pixels.size == 0:
        return [] # No non-background pixels

    # Calculate geometric center of non-background pixels
    min_r, min_c = non_background_pixels.min(axis=0)
    max_r, max_c = non_background_pixels.max(axis=0)
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2

    # Find the nearest non-background pixel to the geometric center to start BFS
    q_center = deque([(center_r, center_c)])
    visited_center_find = set([(center_r, center_c)])
    start_pixel = None

    while q_center:
        r, c = q_center.popleft()
        if input_grid[
---
