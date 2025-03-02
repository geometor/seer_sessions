"""
The transformation divides the input grid into regions based on blue lines, identifies colored objects within those regions (excluding blue and white),
and maps these objects to specific positions in a 4x4 output grid. The output grid primarily uses the first and third rows.
"""

import numpy as np

def find_regions(grid):
    """
    Divides the grid into regions based on blue lines (color 1).
    This function doesn't strictly enforce four quadrants; it adapts to the layout suggested by the blue lines.
    """
    height, width = grid.shape
    mid_x = width // 2
    mid_y = height // 2

    regions = {
      'top_left': [],
      'top_right': [],
      'bottom_left': [],
      'bottom_right': []
    }

    # Top-left region
    for y in range(mid_y):
        for x in range(mid_x):
          if grid[y][x] != 1 and grid[y][x] !=0:
            regions['top_left'].append((y,x,grid[y][x]))

    # Top-right region
    for y in range(mid_y):
        for x in range(mid_x, width):
            if grid[y][x] != 1 and grid[y][x] !=0:
                regions['top_right'].append((y,x,grid[y][x]))

    # Bottom-left region
    for y in range(mid_y, height):
        for x in range(mid_x):
            if grid[y][x] != 1 and grid[y][x] !=0:
                regions['bottom_left'].append((y,x,grid[y][x]))


    # Bottom-right region
    for y in range(mid_y, height):
        for x in range(mid_x, width):
            if grid[y][x] != 1 and grid[y][x] !=0:
                regions['bottom_right'].append((y,x,grid[y][x]))

    return regions

def get_objects(regions):
    """
        Get the objects in each region.
    """
    objects = {}
    for region_key,pixels in regions.items():
        objects[region_key] = []
        region_colors = []
        for (y,x,color) in pixels:
            if color not in region_colors:
                objects[region_key].append(color)
                region_colors.append(color)

    return objects
def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Find regions based on blue lines
    regions = find_regions(grid)

    # Get objects within each region
    objects = get_objects(regions)

    # Initialize output grid (4x4, filled with zeros)
    output_grid = np.zeros((4, 4), dtype=int)

    # Map objects to output grid
    # Top row: top-left and top-right objects
    if 'top_left' in objects and objects['top_left']:
        output_grid[0, 0] = objects['top_left'][0]
        if len(objects['top_left']) > 1:
            output_grid[0, 1] = objects['top_left'][1]

    if 'top_right' in objects and objects['top_right']:
        output_grid[0, 2] = objects['top_right'][0]
        if len(objects['top_right']) > 1:
          output_grid[0,3] = objects['top_right'][1]

    # Third row: bottom-left and bottom-right objects
    if 'bottom_left' in objects and objects['bottom_left']:
        output_grid[2, 0] = objects['bottom_left'][0]
        if len(objects['bottom_left']) > 1:
            output_grid[2,1] = objects['bottom_left'][1]

    if 'bottom_right' in objects and objects['bottom_right']:
        output_grid[2, 2] = objects['bottom_right'][0]
        if len(objects['bottom_right']) > 1:
          output_grid[2,3] = objects['bottom_right'][1]
    return output_grid.tolist()