"""
1.  **Identify Red Regions:** Find all contiguous regions of red pixels in the input grid. A contiguous region is defined as a group of red pixels connected horizontally or vertically.
2.  **Determine Interior:** For each red region, identify its interior. The interior consists of all non-red pixels that are completely enclosed by the red region's boundary. Use a flood-fill algorithm, starting from outside the red region's bounding box, to ensure accurate interior identification, even for complex shapes with concavities or holes.
3.  **Fill Interior with Blue:** Change the color of all identified interior pixels within each red region to blue.
4.  **Preserve Other Pixels:** All pixels that are not part of a red region's interior (including the red boundary pixels) should remain unchanged.
"""

import numpy as np

def describe_red_regions(grid):
    """
    Identifies and describes contiguous red regions in the grid.
    Returns a list of dictionaries, each describing a region.
    """
    red_regions = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, region_pixels):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != 2:
            return
        visited[r, c] = True
        region_pixels.append((r, c))
        # Explore adjacent cells (up, down, left, right)
        dfs(r + 1, c, region_pixels)
        dfs(r - 1, c, region_pixels)
        dfs(r, c + 1, region_pixels)
        dfs(r, c - 1, region_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2 and not visited[r, c]:
                region_pixels = []
                dfs(r, c, region_pixels)
                if region_pixels:
                    # basic description
                    min_r = min(p[0] for p in region_pixels)
                    max_r = max(p[0] for p in region_pixels)
                    min_c = min(p[1] for p in region_pixels)
                    max_c = max(p[1] for p in region_pixels)
                    region_description = {
                        'pixels': region_pixels,
                        'min_row': min_r,
                        'max_row': max_r,
                        'min_col': min_c,
                        'max_col': max_c,
                        'height': max_r-min_r + 1,
                        'width' : max_c - min_c + 1,
                    }

                    red_regions.append(region_description)
    return red_regions

def flood_fill_outside(grid, red_region, temp_color=7):
    """
    Flood fills the area outside the red region with a temporary color.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    min_r = max(0, red_region['min_row'] - 1)  # Expand bounding box by 1
    max_r = min(rows - 1, red_region['max_row'] + 1)
    min_c = max(0, red_region['min_col'] - 1)
    max_c = min(cols - 1, red_region['max_col'] + 1)

    def is_valid(r, c):
        return min_r <= r <= max_r and min_c <= c <= max_c

    def dfs(r, c):
        if not is_valid(r, c) or visited[r, c]:
            return
        visited[r, c] = True
        # Only fill if it's not part of the red region
        if (r, c) not in red_region['pixels']:
          grid[r,c] = temp_color
        else:
          return # don't go past red pixels
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Start flood fill from the corners of the expanded bounding box
    if is_valid(min_r,min_c) and grid[min_r, min_c] != 2:
      dfs(min_r, min_c)
    if is_valid(min_r, max_c) and grid[min_r,max_c] != 2:
      dfs(min_r, max_c)
    if is_valid(max_r, min_c) and grid[max_r,min_c] != 2:
      dfs(max_r, min_c)
    if is_valid(max_r, max_c) and grid[max_r,max_c] != 2:
      dfs(max_r, max_c)

def fill_interior(grid, red_region):
    """
    Fills the interior of a single red region with blue, using flood fill.
    """
    temp_color = 7 # temporary color not otherwise in use
    
    # Make a copy for flood filling.
    flood_grid = np.copy(grid)
    flood_fill_outside(flood_grid, red_region, temp_color)
    
    min_r = red_region['min_row']
    max_r = red_region['max_row']
    min_c = red_region['min_col']
    max_c = red_region['max_col']

    # Iterate and fill
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r,c) not in red_region['pixels'] and flood_grid[r,c] != temp_color:
                grid[r,c] = 1


def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all contiguous red regions
    red_regions = describe_red_regions(input_grid)

    # Fill the interior of each red region with blue
    for region in red_regions:
        fill_interior(output_grid, region)

    return output_grid