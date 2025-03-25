"""
1.  **Identify Corner Colors:** Find single-pixel colors in the four corners of the input grid.
2.  **Identify Objects:** Identify connected components (objects) of the same color within the entire input grid (not just a subgrid). These are groups of adjacent pixels (including diagonals) that have the same color.
3.  **Copy and Compress Objects:** Copy each identified object to the output grid.  Preserve the general shape of the objects during the copy, but compress them. The compression should maintain connectivity and relative positions of pixels within an object. *Do not* simply reduce each object to a single pixel. The amount of compression and the output grid size appears to be related to the size and complexity of the input, although the exact relationship is not yet clear.
4.  **Position Objects:** Preserve the spatial arrangements between copied objects.
5. **Preserve Corner Colors:** Place the identified corner colors from the input grid into the corresponding corners of the output grid. The output grid dimensions may vary so adjust appropriately.
"""

import numpy as np

def get_corners(grid):
    """Finds isolated single-pixel colors in the corners of the grid."""
    rows, cols = grid.shape
    corners = {}

    # Check top-left corner
    if grid[0, 0] != 0:
        corners[(0, 0)] = grid[0, 0]

    # Check top-right corner
    if grid[0, cols - 1] != 0:
        corners[(0, cols - 1)] = grid[0, cols - 1]

    # Check bottom-left corner
    if grid[rows - 1, 0] != 0:
        corners[(rows - 1, 0)] = grid[rows - 1, 0]

    # Check bottom-right corner
    if grid[rows - 1, cols - 1] != 0:
        corners[(rows - 1, cols - 1)] = grid[rows - 1, cols - 1]

    return corners

def find_connected_components(grid):
    """Identifies connected components (objects) in a grid, including diagonal connections."""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(r, c, color, component):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        component.append((r, c))
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, color, component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                component = []
                dfs(r, c, grid[r, c], component)
                components.append((grid[r, c], component))
    return components

def compress_component(component, scale_factor=0.5):
    """Compresses a component while preserving its shape."""
    if not component:
        return []

    # Find bounding box
    min_row = min(p[0] for p in component)
    max_row = max(p[0] for p in component)
    min_col = min(p[1] for p in component)
    max_col = max(p[1] for p in component)

    # Calculate new dimensions
    new_height = int(round((max_row - min_row + 1) * scale_factor))
    new_width = int(round((max_col - min_col + 1) * scale_factor))
    
    # if new dimensions are zero, set minimum size
    new_height = max(1, new_height)
    new_width = max(1, new_width)

    # Create a mapping from old to new coordinates
    new_component = []
    for r, c in component:
        new_r = int(round((r - min_row) * (new_height - 1) / max(1, (max_row - min_row))))  if max_row > min_row else 0
        new_c = int(round((c - min_col) * (new_width - 1) / max(1, (max_col - min_col)))) if max_col > min_col else 0
        new_component.append((new_r, new_c))
    
    return list(set(new_component))  # Remove duplicates


def estimate_output_size(input_grid, components):
    """Estimates output grid size based on input and components."""
    input_rows, input_cols = input_grid.shape
    
    # Start with a base size, here, taking half of the max dimension of the input grid.
    base_size = max(input_rows, input_cols) // 2
    
    # Adjust base size if it's zero
    base_size = max(1, base_size)
    
    # find number of objects
    num_objects = len(components)

    # refine by number of objects
    scale_factor = 1 + (num_objects // 4) # for every four objects scale up by one

    # find average size of components
    total_pixels = sum(len(c) for _, c in components)
    if (len(components) > 0):
      avg_pixels = total_pixels // len(components)
    else:
      avg_pixels = 0

    # refine by pixel count
    pixel_factor = 1+ (avg_pixels // 5)
    
    height = base_size + scale_factor + pixel_factor
    width = base_size + scale_factor + pixel_factor

    return height, width

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # 1. Identify Corner Colors
    corners = get_corners(input_grid)

    # 2. Identify Objects
    components = find_connected_components(input_grid)

    # Estimate output size
    output_rows, output_cols = estimate_output_size(input_grid, components)

    # 3. Copy and Compress Objects
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    for color, component in components:
        compressed_component = compress_component(component)
        for r, c in compressed_component:
            if r < output_rows and c < output_cols:
                output_grid[r, c] = color

    # 4. Preserve Corner Colors (adjusting for output grid dimensions)
    for corner, color in corners.items():
        r, c = corner
        if r == 0 and c == 0:
            output_grid[0, 0] = color  # Top-left
        if r == 0 and c == input_grid.shape[1] - 1:
            output_grid[0, output_cols - 1] = color  # Top-right
        if r == input_grid.shape[0] - 1 and c == 0:
            output_grid[output_rows - 1, 0] = color  # Bottom-left
        if r == input_grid.shape[0] - 1 and c == input_grid.shape[1] - 1:
            output_grid[output_rows - 1, output_cols - 1] = color  # Bottom-right

    return output_grid