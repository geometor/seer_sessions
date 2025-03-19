# 41e4d17e • 006 • refine_coder

---
```python
"""
The transformation outlines blue shapes with magenta.  If a blue shape is not a
single horizontal line, a vertical magenta line is drawn at the y-coordinate of the
leftmost blue pixel of the shape, extending to the top and bottom.  Single
horizontal lines of blue are outlined in magenta, but no additional vertical line is added.
"""

import numpy as np

def find_blue_shapes(grid):
    """Finds all blue (1) pixels and returns their coordinates."""
    blue_pixels = np.argwhere(grid == 1)
    return blue_pixels

def get_leftmost_y(pixels):
    """Calculates the y-coordinate of the leftmost pixel."""
    if len(pixels) == 0:
        return None
    y_coords = pixels[:, 1]
    return np.min(y_coords)

def is_horizontal_line(pixels):
    """Checks if a set of pixels forms a single horizontal line."""
    if len(pixels) == 0:
        return False
    rows = pixels[:, 0]
    return np.all(rows == rows[0])

def get_connected_components(pixels):
    """
    Groups pixels into connected components.  This is crucial for handling
    multiple blue shapes separately.  Uses a simple flood-fill approach.
    """
    if len(pixels) == 0:
        return []

    components = []
    unvisited_pixels = set(map(tuple, pixels))

    def flood_fill(r, c, current_component):
        if (r, c) not in unvisited_pixels:
            return
        unvisited_pixels.remove((r, c))
        current_component.append((r, c))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            flood_fill(nr, nc, current_component)

    while unvisited_pixels:
        start_r, start_c = next(iter(unvisited_pixels))
        current_component = []
        flood_fill(start_r, start_c, current_component)
        components.append(np.array(current_component))

    return components

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find blue shapes
    blue_pixels = find_blue_shapes(input_grid)

    # Group into connected components
    components = get_connected_components(blue_pixels)

    for component in components:
        # Outline each component
        for r, c in component:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < output_grid.shape[0] and 0 <= nc < output_grid.shape[1] and output_grid[nr, nc] != 1:
                    output_grid[nr, nc] = 6

        # Vertical line for components that are not horizontal lines
        if not is_horizontal_line(component):
            y_leftmost = get_leftmost_y(component)
            if y_leftmost is not None:
                for x in range(output_grid.shape[0]):
                    output_grid[x, y_leftmost] = 6

    return output_grid
```
