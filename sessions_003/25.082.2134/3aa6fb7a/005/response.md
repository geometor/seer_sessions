```python
"""
1.  **Identify Azure Components:** Find all contiguous components (groups of adjacent pixels) of azure (8) color in the input grid.  Adjacency includes both horizontal and vertical neighbors.

2.  **Determine Component Orientation:** For each azure component, determine if it's primarily horizontal, vertical, or a single pixel.
    *   A component is **horizontal** if it extends more in the horizontal direction than the vertical.
    *   A component is **vertical** if it extends more in the vertical direction than the horizontal.
    *   A component is **single** if it consists of only one pixel.

3.  **Add Blue Pixel:**  For each azure component, add a single blue (1) pixel to the output grid based on its orientation:
    *   **Horizontal:** Place the blue pixel immediately to the *right* of the right-most azure pixel in the component.
    *   **Vertical:** Place the blue pixel immediately *below* the bottom-most azure pixel in the component.
    * **Single:** Place the blue pixel immediately to the *right* of the single azure pixel.

4. **Copy Background:** Copy all non-azure pixels directly from the input grid to the output grid in the same position. Azure pixels in the original components remain.
"""

import numpy as np

def find_azure_components(grid):
    """Finds contiguous components of azure pixels (horizontally or vertically)."""
    rows, cols = grid.shape
    components = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_component):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != 8:
            return

        visited.add((r, c))
        current_component.append((r, c))

        # Explore adjacent cells
        dfs(r + 1, c, current_component)  # Down
        dfs(r - 1, c, current_component)  # Up
        dfs(r, c + 1, current_component)  # Right
        dfs(r, c - 1, current_component)  # Left

    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 8 and (r,c) not in visited:
                current_component = []
                dfs(r,c,current_component)
                if len(current_component) > 0:
                    components.append(current_component)
    return components

def get_component_orientation(component):
    """Determines if a component is horizontal, vertical, or single."""
    if len(component) == 1:
        return "single"

    rows = [r for r, c in component]
    cols = [c for r, c in component]
    row_range = max(rows) - min(rows)
    col_range = max(cols) - min(cols)

    if col_range > row_range:
        return "horizontal"
    else:
        return "vertical"  # Treat equal range as vertical

def get_rightmost_pixel(component):
    """Returns the (row, col) of the right-most pixel in a component."""
    return max(component, key=lambda x: x[1])

def get_bottommost_pixel(component):
   """Returns the (row, col) of the bottom-most pixel in a component"""
   return max(component, key=lambda x:x[0])

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find azure components
    components = find_azure_components(input_grid)

    # Add blue pixel based on component orientation
    for component in components:
        orientation = get_component_orientation(component)

        if orientation == "horizontal":
            rightmost_pixel = get_rightmost_pixel(component)
            r, c = rightmost_pixel
            if c + 1 < cols: #ensure within bounds
                output_grid[r, c + 1] = 1
        elif orientation == "vertical":
            bottommost_pixel = get_bottommost_pixel(component)
            r,c = bottommost_pixel
            if r + 1 < rows:
                output_grid[r+1,c] = 1
        else:  # Single
            r, c = component[0]
            if c + 1 < cols:
                output_grid[r, c + 1] = 1

    return output_grid
```