"""
1.  **Input:** A 2D grid of integers representing colors.
2.  **Region Identification:** Divide the input grid into regions. A region is defined as a contiguous area of pixels.
3.  **Major Color Determination:** For each identified region, determine the "major" color:
    *   Count the occurrences of each color (excluding 0, which represents the background).
    *   If a single color has the highest count, it's the major color.
    *   If multiple colors share the highest count, determine if one of them is contiguous.
4. **Output Creation**: create a 3x3 grid and place the major colors of the identified input regions into the output. The logic to map regions to specific output cells is not defined.
"""

import numpy as np
from collections import Counter

def find_regions(grid):
    """
    Identifies contiguous regions within the grid.
    Uses flood fill algorithm
    """
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    def flood_fill(row, col, color, current_region):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_region.append((row, col))
        flood_fill(row + 1, col, color, current_region)
        flood_fill(row - 1, col, color, current_region)
        flood_fill(row, col + 1, color, current_region)
        flood_fill(row, col - 1, color, current_region)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                current_region = []
                flood_fill(row, col, grid[row, col], current_region)
                regions.append((grid[row,col], current_region)) #color and region
    return regions

def get_major_color(region_pixels, color):
    """
    Gets the color for the region.
    """

    if color != 0:
      return color
    
    return 0


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find regions in the input grid
    regions = find_regions(input_grid)

    # Map regions to output grid cells (This is a placeholder - needs refinement)
    # Basic idea: divide input space into 3x3 sections and map region center
    rows, cols = input_grid.shape
    
    region_data = []

    for color, pixels in regions:
        
      if not pixels:
        continue

      #find the "center"
      center_row = sum([p[0] for p in pixels]) // len(pixels)
      center_col = sum([p[1] for p in pixels]) // len(pixels)

      #determine output grid index for the "center"
      grid_row = int(center_row / rows * 3)
      grid_col = int(center_col / cols * 3)
      region_data.append( ( (grid_row, grid_col), color, len(pixels) ) )

    #sort by the count of pixels in the region, largest first
    sorted_region_data = sorted(region_data, key=lambda x: x[2], reverse=True)

    #keep track of what output cells have been filled
    filled = set()
    for (grid_row, grid_col), color, _ in sorted_region_data:
        if (grid_row,grid_col) not in filled:
          output_grid[grid_row, grid_col] = get_major_color(None,color) #just take first color
          filled.add( (grid_row, grid_col) )

    return output_grid