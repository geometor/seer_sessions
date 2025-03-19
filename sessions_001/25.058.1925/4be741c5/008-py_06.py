"""
1.  **Process Input Row by Row:** Iterate through each row of the input grid independently.
2.  **Identify Contiguous Regions:** Within each row, identify contiguous regions (runs) of pixels having the same color.  A new region starts when a different color is encountered, or the end of the row.
3.  **Create Output Segments:** For each input row, create a corresponding segment (a 1D array) for the output. Each element in the segment corresponds to a region, and its value equals to that region's color.
4.  **Combine:** Create the output grid. The number of rows in the output should match the number of contiguous regions found in *all* input rows, concatenated together. Each cell in the output should be the color of the region it represents.
"""

import numpy as np

def get_contiguous_regions_in_row(row):
    """Identifies contiguous regions of the same color within a single row."""
    regions = []
    current_region = []
    for cell in row:
        if not current_region or cell == current_region[-1]:
            current_region.append(cell)
        else:
            regions.append(current_region[0])  # Add the color of the region
            current_region = [cell]
    if current_region:
        regions.append(current_region[0])
    return regions

def transform(input_grid):
    # initialize output_grid
    output_segments = []

    # Process each row
    for row in input_grid:
        # Identify contiguous regions in the current row.
        regions = get_contiguous_regions_in_row(row)
        output_segments.extend(regions)

    # Create the output grid (1 x N).
    output_grid = np.array([output_segments], dtype=int)
    
    return output_grid