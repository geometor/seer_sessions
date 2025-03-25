"""
1.  **Identify Edge Pixels:** Determine all pixels located on the perimeter (first/last row, first/last column) of the input grid.

2.  **Identify Connected Regions:** For each unique color present on the edge, find all contiguous regions (blocks of pixels) of that color that include at least one edge pixel.

3.  **Preserve Edge-Connected Regions:** In the output grid, maintain the original color of all pixels that belong to a connected region identified in step 2.

4.  **Zero Out Other Pixels:** Set the color of all other pixels in the output grid to 0 (white/background). This includes both interior pixels and any edge pixels that are *not* part of a contiguous region connected to the edge for their respective color.
"""

import numpy as np
from scipy.ndimage import label

def get_edge_colors(grid):
    """Returns a set of unique colors present on the edges of the grid."""
    rows, cols = grid.shape
    edge_colors = set()
    for r in range(rows):
        edge_colors.add(grid[r, 0])
        edge_colors.add(grid[r, cols - 1])
    for c in range(cols):
        edge_colors.add(grid[0, c])
        edge_colors.add(grid[rows - 1, c])
    return edge_colors

def get_connected_regions(grid, edge_colors):
    """Finds contiguous regions of each edge color connected to the edge."""
    rows, cols = grid.shape
    connected_regions = {}

    for color in edge_colors:
        binary_grid = (grid == color).astype(int)
        labeled_array, num_features = label(binary_grid)
        connected_regions[color] = []

        for region_id in range(1, num_features + 1):
            region_mask = (labeled_array == region_id)
            coords = np.where(region_mask)
            rows_region, cols_region = coords

            # Check if the region touches the edge
            touches_edge = False
            for r, c in zip(rows_region, cols_region):
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    touches_edge = True
                    break

            if touches_edge:
                connected_regions[color].append(region_mask)

    return connected_regions

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # identify edge colors
    edge_colors = get_edge_colors(input_grid)

    # identify connected regions for each edge color
    connected_regions = get_connected_regions(input_grid, edge_colors)

    # preserve pixels in edge-connected regions
    for color, regions in connected_regions.items():
        for region_mask in regions:
            output_grid[region_mask] = color

    return output_grid