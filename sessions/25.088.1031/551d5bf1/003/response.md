```python
"""
1. Identify regions of white (0) pixels that are completely enclosed by blue (1) pixels. A pixel is considered enclosed if it's white (0) and cannot be reached from the grid border by moving only through non-blue pixels (i.e., any path from the border to the pixel must cross a blue pixel).
2. Create a set of coordinates for these enclosed white pixels (`enclosed_set`).
3. Find all white (0) pixels in the original input grid that are directly adjacent (up, down, left, right) to any pixel in the `enclosed_set`. Create a set of coordinates for these adjacent white pixels (`adjacent_set`).
4. Create the output grid by copying the input grid.
5. Change the color of all pixels identified in `enclosed_set` to azure (8) in the output grid.
6. Change the color of all pixels identified in `adjacent_set` to azure (8) in the output grid. (Note: these sets might overlap, which is fine).
7. Return the modified output grid.
"""

import numpy as np
from collections import deque

def find_enclosed_regions_by_blue(grid):
    """
    Finds white (0) pixels enclosed by blue (1) pixels.
    Performs a flood fill starting from all border cells that are NOT blue.
    Any white (0) cell not visited by this flood fill is considered enclosed.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add all border cells that are NOT blue (1) to the queue and mark visited
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] != 1 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
    for c in range(1, cols - 1): # Avoid double-adding corners
        for r in [0, rows - 1]:
             if grid[r, c] != 1 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True

    # Perform BFS (flood fill) from non-blue border pixels
    while q:
        r, c = q.popleft()
        # Explore neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if neighbor is NOT blue, and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] != 1 and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    # Identify enclosed pixels (white pixels not visited by the flood fill)
    enclosed_set = set()
    for r in range(rows):
        for c in range(cols):
            # Must be white (0) and not visited by the 'outside' flood fill
            if grid[r, c] == 0 and not visited[r, c]:
                enclosed_set.add((r, c))
                
    return enclosed_set

def find_adjacent_white_to_set(grid, target_set):
    """
    Finds white (0) pixels in the grid that are adjacent (non-diagonally)
    to any pixel coordinate in the target_set.
    """
    rows, cols = grid.shape
    adjacent_set = set()
    
    # Iterate through the pixels identified as enclosed
    for r, c in target_set:
        # Check their 4 neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if the neighbor is white(0) in the original grid
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
                 # Add this white neighbor's coordinate to the set
                 # It's okay if it's also in the target_set, it will be colored azure anyway
                 adjacent_set.add((nr, nc))
                    
    return adjacent_set


def transform(input_grid):
    """
    Applies the transformation: fills white areas enclosed by blue, 
    and also fills adjacent white pixels, with azure (8).
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = input_array.copy()
    
    # 1. Find white pixels enclosed by blue (1) pixels
    enclosed_set = find_enclosed_regions_by_blue(input_array)

    # 2. Find all original white pixels adjacent to the enclosed set
    # Note: This set might include pixels already in enclosed_set if they
    # are white and adjacent to other enclosed pixels.
    adjacent_set = find_adjacent_white_to_set(input_array, enclosed_set)

    # 3. Modify the output grid: Fill enclosed regions with azure (8)
    for r, c in enclosed_set:
        output_grid[r, c] = 8

    # 4. Modify the output grid: Fill adjacent white pixels with azure (8)
    # This ensures that even if an adjacent pixel was also in the enclosed set,
    # it gets correctly colored. It also colors the white pixels *outside*
    # the blue boundary that are adjacent to the enclosed ones.
    for r, c in adjacent_set:
         output_grid[r, c] = 8
         
    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```