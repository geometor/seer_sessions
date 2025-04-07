Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Transforms an input grid based on rules derived from its structure.
The core transformation involves:
1. Identifying the largest connected component made of gray (5) pixels, assumed to be the frame.
2. Determining the bounding box of this frame.
3. Identifying the background color present *inside* the frame.
4. Finding all connected blocks of color located strictly *outside* the frame's bounding box, excluding the frame color (gray 5) and the identified inner background color.
5. Deriving a color mapping: If an eligible block of color C1 is found directly above another eligible block of color C2 (sharing a horizontal boundary segment), a rule C1 -> C2 is created. The first such rule found for C1 is used.
6. Creating an output grid with dimensions matching the identified frame.
7. Filling the output grid's border with the frame color (gray 5).
8. Copying the content from *inside* the input frame to the *inside* of the output grid, applying the derived color mapping to each pixel. Pixels with the inner background color or colors not found in the mapping rules remain unchanged.
"""

def _find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color using BFS.
    Returns a list of components, each represented as a dict with coords, bbox, color, size.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                component_coords_rows = []
                component_coords_cols = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                component_size = 0

                while q:
                    row, col = q.popleft()
                    component_coords_rows.append(row)
                    component_coords_cols.append(col)
                    min_r, max_r = min(min_r, row), max(max_r, row)
                    min_c, max_c = min(min_c, col), max(max_c, col)
                    component_size += 1

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if component_size > 0:
                    components.append({
                        'coords': (tuple(component_coords_rows), tuple(component_coords_cols)),
                        'bbox': (min_r, min_c, max_r, max_c), # min_row, min_col, max_row, max_col
                        'color': target_color,
                        'size': component_size
                    })
    return components

def _find_all_blocks(grid, exclude_colors):
    """
    Finds all connected components (blocks) for all colors, excluding specified colors.
    Uses BFS. Returns a list of block dictionaries.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(rows):
        for c in range(cols):
            current_color = grid[r, c]
            # Process if not visited and not an excluded color
            if not visited[r, c] and current_color not in exclude_colors:
                component_coords_rows = []
                component_coords_cols = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                component_size = 0

                while q:
                    row, col = q.popleft()
                    component_coords_rows.append(row)
                    component_coords_cols.append(col)
                    min_r, max_r = min(min_r, row), max(max_r, row)
                    min_c, max_c = min(
---
