import numpy as np
from collections import deque

"""
Identifies enclosed regions (holes) within structures defined by red (2) pixels.
An enclosed region is a connected area of non-red pixels that does not touch the border of the grid.
If an enclosed region contains at least one red (2) pixel within its area in the input grid, 
all white (0) pixels within that specific region are changed to blue (1) in the output grid.
Red pixels and non-red pixels in regions that touch the border or do not contain internal red pixels remain unchanged.
"""

def find_non_red_regions(input_grid):
    """
    Finds all connected regions of non-red pixels using BFS.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              and contains 'pixels' (a list of (row, col) tuples) and 
              'touches_border' (a boolean).
    """
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    regions = []
    
    for r in range(height):
        for c in range(width):
            # Start BFS if pixel is not red and not visited
            if input_grid[r, c] != 2 and not visited[r, c]:
                component_pixels = []
                touches_border = False
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels.append((curr_r, curr_c))
                    
                    # Check if the current pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True
                        
                    # Explore neighbors (4-way adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is not red and not visited
                            if input_grid[nr, nc] != 2 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                regions.append({'pixels': component_pixels, 'touches_border': touches_border})
                
    return regions

def transform(input_grid):
    """
    Transforms the input grid based on the rule: Fill enclosed regions containing 
    red pixels with blue.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all connected regions of non-red pixels
    regions = find_non_red_regions(input_grid)

    # Process each region
    for region in regions:
        # Check if the region is enclosed (does not touch the border)
        if not region['touches_border']:
            contains_internal_red = False
            pixels_to_fill = [] # Store original white pixels in this region

            # Check if any pixel location within this region corresponds to a red pixel in the original grid
            # Also collect the locations of original white pixels within this region
            for r, c in region['pixels']:
                original_value = input_grid[r, c]
                if original_value == 2:
                    contains_internal_red = True
                    # Optimization: if we find one red pixel, we know we need to fill
                    # but we still need to iterate through all pixels to find the white ones to fill.
                elif original_value == 0:
                     pixels_to_fill.append((r, c))

            # If the enclosed region contains at least one internal red pixel
            if contains_internal_red:
                # Change all original white pixels in this region to blue (1)
                for r, c in pixels_to_fill:
                    output_grid[r, c] = 1
                    
    return output_grid
