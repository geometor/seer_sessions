"""
1.  **Find Azure Components:** Identify all contiguous groups (components) of azure (8) colored pixels in the input grid.  Pixels are considered adjacent if they share a side (horizontally or vertically, but not diagonally).

2.  **Classify Component Shape:** For each identified azure component, determine its shape classification:
    *   **Horizontal:** If the component extends more in the horizontal direction than the vertical.
    *   **Vertical:** If the component extends more in the vertical direction than the horizontal.
    *   **Single:** If the component consists of only one pixel.

3.  **Add Blue Pixels based on shape:** For each azure pixel in each component, add a blue pixel as follows:
    *   **Horizontal Component:** Add a blue (1) pixel to the immediate right of each azure pixel *unless* there is another azure pixel to its immediate right, *or* the pixel is on the right edge of the grid.
    *   **Vertical Component:** Add a blue (1) pixel immediately below each azure pixel *unless* there is another azure pixel immediately below it, *or* the pixel is on the bottom edge of the grid.
    *   **Single Pixel Component:** Add a blue (1) pixel to the immediate right of the azure pixel *unless* the pixel is on the right edge of the grid.

4.  **Copy Background:** Copy all pixels that are *not* azure (8) from the input grid to the output grid, maintaining their original positions. The azure components are preserved.
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

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find azure components
    components = find_azure_components(input_grid)

    # Add blue pixel based on component orientation and neighbor check
    for component in components:
        orientation = get_component_orientation(component)

        for r, c in component:
            if orientation == "horizontal":
                if c + 1 < cols and input_grid[r, c + 1] != 8:  # Check right neighbor and bounds
                    output_grid[r, c + 1] = 1
            elif orientation == "vertical":
                if r + 1 < rows and input_grid[r + 1, c] != 8:  # Check bottom neighbor and bounds
                    output_grid[r + 1, c] = 1
            elif orientation == "single":
                if c + 1 < cols: # Check bounds
                    output_grid[r, c + 1] = 1

    return output_grid