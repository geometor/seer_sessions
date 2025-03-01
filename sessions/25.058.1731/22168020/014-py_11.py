"""
1.  **Identify Regions:** Find all contiguous regions of blue (color 1) and yellow (color 4) pixels.  A region is defined as one or more adjacent pixels of the same color.
2.  **Horizontal Expansion:** For every blue and yellow region, extend that region to the left and right edges of the grid.
3. If any blue or yellow region is found, extend the full height of the grid.
"""

import numpy as np

def get_regions(grid, colors):
    # find regions of specific colors in a grid
    regions = {}
    for color in colors:
        regions[color] = []
        visited = np.zeros_like(grid, dtype=bool)
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color and not visited[r, c]:
                    region = []
                    stack = [(r, c)]
                    while stack:
                        row, col = stack.pop()
                        if 0 <= row < rows and 0 <= col < cols and grid[row, col] == color and not visited[row, col]:
                            visited[row, col] = True
                            region.append((row, col))
                            stack.extend([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
                    regions[color].append(region)
    return regions

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.full_like(input_grid, 0) # Initialize with all white (0)
    rows, cols = output_grid.shape

    # Identify Regions of blue and yellow.
    regions = get_regions(input_grid, [1, 4])

    # expand blue regions
    for region in regions[1]:
        for r in range(rows):
            for c in range(cols):
                output_grid[r,c] = 1

    # expand yellow regions
    for region in regions[4]:
        for r in range(rows):
            for c in range (cols):
                output_grid[r,c] = 4

    return output_grid.tolist()