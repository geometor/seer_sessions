import numpy as np
from collections import deque

"""
Transforms the input grid by finding contiguous regions of white (0) pixels bounded by blue (1) pixels or grid edges.
It then identifies the overall bounding box encompassing all white pixels.
White regions touching the edges of this bounding box are filled with red (2).
White regions fully contained within the bounding box (not touching its edges) are filled with green (3).
Blue (1) pixels remain unchanged.
"""

def find_contiguous_regions(grid, target_color):
    """
    Finds all contiguous regions of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the pixels to find regions of.

    Returns:
        list: A list of sets, where each set contains (row, col) tuples
              representing the coordinates of a contiguous region.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) for a new region
                region = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    region.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if neighbor is target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if region:
                    regions.append(region)
                    
    return regions

def transform(input_grid):
    """
    Fills white regions based on their position relative to the bounding box of all white regions.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # 1. Identify all distinct contiguous regions of white (0) pixels
    white_regions = find_contiguous_regions(input_grid, 0)
    
    # 2. If no white regions are found, return the copied grid.
    if not white_regions:
        return output_grid
        
    # 3. Find the overall bounding box of all white pixels
    all_white_pixels = set().union(*white_regions)
    if not all_white_pixels: # Should be redundant due to step 2, but safe
         return output_grid

    min_r = min(r for r, c in all_white_pixels)
    max_r = max(r for r, c in all_white_pixels)
    min_c = min(c for r, c in all_white_pixels)
    max_c = max(c for r, c in all_white_pixels)

    # 4. Iterate through each identified white region and determine fill color
    for region in white_regions:
        is_boundary_region = False
        # 5a. Check if any pixel within this region touches the bounding box edge
        for r, c in region:
            if r == min_r or r == max_r or c == min_c or c == max_c:
                is_boundary_region = True
                break
        
        # 5b/c. Determine the fill color based on classification
        fill_color = 2 if is_boundary_region else 3 # red for boundary, green for interior
        
        # 6. Update the output grid for the pixels in this region
        for r, c in region:
            output_grid[r, c] = fill_color
            
    # 7. Return the modified output grid
    return output_grid
