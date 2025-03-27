```python
"""
Transforms the input grid by extracting rectangular blocks of non-white pixels,
grouping them by width, and arranging these groups horizontally in the output grid.
Rectangles within each group are stacked vertically.
"""

import numpy as np

def get_rectangles(grid):
    """
    Identifies and extracts rectangular blocks of non-white pixels from the input grid.
    """
    rectangles = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, rect_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        rect_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, rect_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                rect_coords = []
                dfs(r, c, grid[r, c], rect_coords)
                if rect_coords:
                    min_r = min(coord[0] for coord in rect_coords)
                    max_r = max(coord[0] for coord in rect_coords)
                    min_c = min(coord[1] for coord in rect_coords)
                    max_c = max(coord[1] for coord in rect_coords)
                    rectangles.append({
                        'color': grid[r, c],
                        'min_r': min_r,
                        'max_r': max_r,
                        'min_c': min_c,
                        'max_c': max_c,
                        'height': max_r - min_r + 1,
                        'width': max_c - min_c + 1,
                        'coords': rect_coords
                    })
    return rectangles

def transform(input_grid):
    """
    Transforms the input grid.
    """
    input_grid = np.array(input_grid)
    rectangles = get_rectangles(input_grid)

    # Group rectangles by width
    groups = {}
    for rect in rectangles:
        width = rect['width']
        if width not in groups:
            groups[width] = []
        groups[width].append(rect)

    # Sort groups by their first appearance (based on min_c)
    sorted_group_keys = sorted(groups.keys(), key=lambda k: min(rect['min_c'] for rect in groups[k]))

    # Calculate output dimensions
    output_width = sum(sorted_group_keys)
    output_height = 0
    for key in sorted_group_keys:
        group_height = 0
        for rect in groups[key]:
            group_height += rect['height']
        output_height = max(group_height,output_height)
        

    output_grid = np.zeros((output_height, output_width), dtype=int)

    curr_col = 0
    for group_key in sorted_group_keys:
        group = groups[group_key]
        curr_row = 0
        group_width = 0
        for rect in group:
            # Place rectangles within the group vertically
            for r in range(rect['height']):
                for c in range(rect['width']):
                    output_grid[curr_row + r, curr_col + c] = rect['color']
            curr_row += rect['height']  # Move to the next row within the group
            group_width = rect['width']
        curr_col += group_width  # Move to the next column for the next group

    return output_grid.tolist()
```