"""
The input grid is divided into six distinct rectangular regions of uniform color.
The output grid is a 3x2 grid where each cell represents one of these regions,
maintaining the relative spatial arrangement and color. The output consists of color pairs.
"""

import numpy as np

def get_regions(grid):
    # Find the boundaries of the colored regions.
    rows, cols = grid.shape
    h_lines = []
    v_lines = []

    # Find horizontal lines
    for r in range(1, rows):
        if np.all(grid[r] != grid[r-1]):
            h_lines.append(r)

    # Find vertical lines
    for c in range(1, cols):
        if np.all(grid[:, c] != grid[:, c-1]):
            v_lines.append(c)
    
    regions = []
    r_start = 0
    for r_end in h_lines:
        c_start = 0
        for c_end in v_lines:
            region_color = grid[r_start, c_start]
            regions.append(((r_start, c_start, r_end, c_end), region_color))
            c_start = c_end
        r_start = r_end

    return regions
            

def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Get the distinct regions and their colors
    regions = get_regions(grid)
    
    # Create the output grid
    output_grid = np.zeros((3, 2), dtype=int)

    # sort regions
    regions.sort(key=lambda x: (x[0][0], x[0][1]))  # Sort by row, then column

    # iterate in pairs
    for i in range(0, len(regions), 2):
        output_grid[i // 2, 0] = regions[i][1]
        output_grid[i // 2, 1] = regions[i+1][1]

    return output_grid.tolist()