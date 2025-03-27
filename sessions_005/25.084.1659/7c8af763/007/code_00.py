"""
Transforms the input grid by performing a conditional flood fill on white (0) pixels within contiguous regions bounded by gray (5) pixels. The fill color for each distinct region is determined by the presence and priority of marker pixels (red=2, blue=1) within that region in the input grid. Red markers have higher priority than blue markers. If a region contains only white (0) pixels, it defaults to being filled with blue (1). Gray (5) boundary pixels and original marker pixels (1 and 2) within the regions remain unchanged.
"""

import numpy as np
from collections import deque

def find_regions_and_determine_fills(grid):
    """
    Identifies contiguous regions of non-gray pixels using Breadth-First Search (BFS),
    determines the fill color for each region based on marker priority, and
    identifies the coordinates of originally white pixels within each region.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries. Each dictionary represents a region and contains:
        - 'fill_color': The color (1 or 2) to fill the white pixels in this region.
        - 'white_coords': A list of (row, col) tuples for pixels that were originally
                          white (0) in this region.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions_data = []
    gray_color = 5
    white_color = 0
    blue_color = 1
    red_color = 2

    for r in range(rows):
        for c in range(cols):
            # Start a BFS if the pixel is not gray and not yet visited
            if grid[r, c] != gray_color and not visited[r, c]:
                current_region_white_coords = []
                markers_present = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Process the starting pixel itself
                pixel_value = grid[r, c]
                if pixel_value == white_color:
                    current_region_white_coords.append((r, c))
                elif pixel_value == blue_color or pixel_value == red_color:
                    markers_present.add(pixel_value)

                # Perform BFS to find all connected pixels in the region
                while q:
                    row, col = q.popleft()

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is valid for the region
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != gray_color and not visited[nr, nc]:
                            
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                            # Check the color of the neighbor to update region info
                            neighbor_value = grid[nr, nc]
                            if neighbor_value == white_color:
                                current_region_white_coords.append((nr, nc))
                            elif neighbor_value == blue_color or neighbor_value == red_color:
                                markers_present.add(neighbor_value)
                
                # After exploring the whole region, determine the fill color
                if red_color in markers_present:
                    fill_color = red_color # Red priority
                elif blue_color in markers_present:
                    fill_color = blue_color # Blue secondary
                else:
                    # Default case: If region contains only white (0), fill with blue.
                    fill_color = blue_color

                # Store the results for this region
                if current_region_white_coords: # Only store if there's something to fill
                     regions_data.append({
                        'fill_color': fill_color,
                        'white_coords': current_region_white_coords
                     })
                     
    return regions_data

def transform(input_grid):
    """
    Applies the conditional flood fill transformation based on marker priorities
    within regions, filling only originally white pixels.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid.
    # Gray pixels and original marker pixels will remain unchanged by default.
    output_grid = np.copy(input_grid)
    
    # Step 1: Identify all distinct contiguous regions of non-gray pixels,
    # determine the fill color for each based on markers, and find coordinates
    # of white pixels within each region.
    regions_fill_info = find_regions_and_determine_fills(input_grid)

    # Step 2: Apply the determined fill color to the originally white pixels
    # within each region in the output grid.
    for region_info in regions_fill_info:
        fill_color = region_info['fill_color']
        white_coords = region_info['white_coords']
        
        for r, c in white_coords:
            output_grid[r, c] = fill_color

    # Step 3: Return the modified output grid.
    return output_grid