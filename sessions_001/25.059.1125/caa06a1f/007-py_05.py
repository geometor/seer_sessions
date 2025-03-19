"""
1.  **Identify Regions:** Locate the magenta (6), orange (7), and green (3) regions within the input grid.
2.  **Combine Extents:** Determine the smallest rectangular area that fully contains *both* the magenta and orange regions. This combined area defines the target region.
3.  **Remove Green:** Within the target area determined by the combined magenta and orange extents, replace all green pixels.
4. **Create Checkerboard:** Fill the target area with a checkerboard pattern. Alternate orange (7) and magenta (6) pixels. The color of the top-left pixel of the target region is determined by whether its x + y coordinates are even (orange) or odd (magenta).
5.  **Background:** The area outside of the combined magenta and orange regions remains black (0). The output grid dimensions exactly match the dimensions of this combined area.
"""

import numpy as np

def get_region(grid, color):
    """Finds a region of the specified color within the grid."""
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(region1, region2):
    """Calculates the bounding box encompassing two regions."""
    if len(region1) == 0:
        min_x = np.min(region2[:, 1])
        max_x = np.max(region2[:, 1])
        min_y = np.min(region2[:, 0])
        max_y = np.max(region2[:, 0])

    elif len(region2) == 0:
        min_x = np.min(region1[:, 1])
        max_x = np.max(region1[:, 1])
        min_y = np.min(region1[:, 0])
        max_y = np.max(region1[:, 0])
    else:
        min_x = min(np.min(region1[:, 1]), np.min(region2[:, 1]))
        max_x = max(np.max(region1[:, 1]), np.max(region2[:, 1]))
        min_y = min(np.min(region1[:, 0]), np.min(region2[:, 0]))
        max_y = max(np.max(region1[:, 0]), np.max(region2[:, 0]))
    return min_x, max_x, min_y, max_y

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # Identify Regions
    magenta_region = get_region(input_grid, 6)
    orange_region = get_region(input_grid, 7)
    green_region = get_region(input_grid, 3)

    # Determine dimensions of combined non-green region
    min_x, max_x, min_y, max_y = get_bounding_box(magenta_region, orange_region)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Initialize output grid
    output_grid = np.zeros((height, width), dtype=int)

    # Checkerboard Rearrangement
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                output_grid[y, x] = 7  # Orange
            else:
                output_grid[y, x] = 6  # Magenta

    return output_grid