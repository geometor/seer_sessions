"""
Transforms input grids by expanding certain colored regions based on specific rules,
often involving adjacency and overwriting.  The process generally involves
identifying "anchor" regions of a specific color, then expanding those regions,
replacing other colors in their path based on a set of rules that may involve
adjacency and stopping conditions (e.g., encountering a specific color).
"""

import numpy as np

def find_regions(grid, color):
    """Finds contiguous regions of a given color in the grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    regions = []

    def dfs(row, col):
        """Depth-first search to find contiguous region."""
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return []

        visited[row, col] = True
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                regions.append(dfs(r, c))
    return regions

def expand_region(grid, region, fill_color, overwrite_colors, stop_colors):
    """Expands a region, replacing specified colors and stopping at others."""
    expanded_region = set(region)  # Use a set for efficient membership checking
    queue = region[:]
    rows, cols = grid.shape

    while queue:
        row, col = queue.pop(0)
        # Consider neighbors (up, down, left, right)
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for nr, nc in neighbors:
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in expanded_region):
                pixel_color = grid[nr, nc]
                if pixel_color in overwrite_colors:
                    expanded_region.add((nr, nc))
                    queue.append((nr, nc))
                elif pixel_color in stop_colors:  #stop the spread, dont add to queue
                    continue

    return list(expanded_region)


def apply_transformation_pass(input_grid, anchor_color, fill_color, overwrite_colors, stop_colors):
    """Applies a single pass of the transformation."""
    output_grid = np.copy(input_grid)
    anchor_regions = find_regions(input_grid, anchor_color)

    for region in anchor_regions:
      expanded = expand_region(input_grid, region, fill_color, overwrite_colors, stop_colors)
      for r, c in expanded:
        output_grid[r,c] = fill_color

    return output_grid
    

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)

    # From observation, transformations often involve multiple "passes".
    # We'll try a few different passes based on the training examples.

    # Pass 1:  Based on Examples 1, 2, and 3's general behavior.
    #       Expand some color, overwriting others but stopping at specific colors.

    # determine if "2 pass transform" based on distinct regions
    # top half of the grid
    output_grid_top = apply_transformation_pass(input_grid[:input_grid.shape[0]//2, :], 3, 3, [0], [1,2,4,5,6,7,8,9])

    # bottom half of the grid
    output_grid_bottom = apply_transformation_pass(input_grid[input_grid.shape[0]//2:, :], 7, 7, [0], [1,2,3,4,5,6,8,9])

    if not np.array_equal(output_grid_top, input_grid[:input_grid.shape[0]//2, :]):
      # overwrite top half
      output_grid[:input_grid.shape[0]//2, :] = output_grid_top

    if not np.array_equal(output_grid_bottom, input_grid[input_grid.shape[0]//2:, :]):
        # overwrite bottom half
        output_grid[input_grid.shape[0]//2:, :] = output_grid_bottom

    # Pass 2 (global, whole array, overwrite all but 1 and 2)
    output_grid = apply_transformation_pass(output_grid, 6, 6, [0,3,4,5,7,8,9], [1,2])
    
    # Pass 3 (global, whole array, overwrite all but 1 and 3)
    output_grid = apply_transformation_pass(output_grid, 4, 4, [0,5,6,7,8,9], [1,2,3])

    return output_grid.tolist()