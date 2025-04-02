
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions (Inner Region) enclosed by a single-colored border (Border Region). 
If any pixel on the border is adjacent (non-diagonally) to both a pixel in the Inner Region 
and a pixel of a third, non-background color (Adjacent Color), then the entire Inner Region 
is flood-filled with this Adjacent Color in the output grid. Otherwise, the region remains unchanged.
"""

def get_neighbors(grid_shape, r, c):
    """ Gets valid 4-directional neighbors for a cell (r, c) within grid bounds. """
    neighbors = []
    height, width = grid_shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_regions(grid):
    """ 
    Finds all distinct contiguous regions of the same color in the grid.
    Returns a list of dictionaries, each containing 'coords' (set of (r, c) tuples) 
    and 'color' for a region.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                region_color = grid[r, c]
                # Skip background regions if they are treated differently (optional, depends on task)
                # if region_color == 0: 
                #    visited[r,c] = True
                #    continue 
                    
                region_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    region_coords.add((curr_r, curr_c))

                    for nr, nc in get_neighbors(grid.shape, curr_r, curr_c):
                        if not visited[nr, nc] and grid[nr, nc] == region_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if region_coords: # Should always be true here unless starting on visited
                     regions.append({'coords': region_coords, 'color': region_color})
    return regions

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the enclosure and leak rule.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape
    
    # Find all distinct contiguous regions in the input grid
    all_regions = find_regions(input_grid)

    # Iterate through each potential inner region found
    for region_info in all_regions:
        inner_region_coords = region_info['coords']
        c_inner = region_info['color']
        
        # Optimization: skip background color as inner region
        if c_inner == 0:
             continue

        border_pixels = set()
        neighbor_colors = set()
        
        # 1. Find all immediate neighbors outside the region
        for r, c in inner_region_coords:
            for nr, nc in get_neighbors(grid_shape, r, c):
                if (nr, nc) not in inner_region_coords:
                    border_pixels.add((nr, nc))
                    neighbor_colors.add(input_grid[nr, nc])

        # 2. Check for single-color enclosure condition
        is_enclosed = False
        c_border = -1 # Use -1 to indicate no valid border color found yet
        if len(neighbor_colors) == 1:
            potential_border_color = list(neighbor_colors)[0]
            if potential_border_color != c_inner:
                is_enclosed = True
                c_border = potential_border_color

        # 3. If enclosed, check for leak points
        leaking_color = None
        if is_enclosed:
            # Iterate through each identified border pixel
            for br, bc in border_pixels:
                # Check neighbors of the border pixel
                for nbr, nbc in get_neighbors(grid_shape, br, bc):
                    neighbor_coord = (nbr, nbc)
                    c_adjacent = input_grid[nbr, nbc]

                    # Check if this neighbor is the potential 'leaking' color source
                    # Conditions: Not inner color, not border color, not background(0)
                    # AND it's not part of the border itself or the inner region
                    if (neighbor_coord not in inner_region_coords and 
                        neighbor_coord not in border_pixels and 
                        c_adjacent != c_inner and 
                        c_adjacent != c_border and 
                        c_adjacent != 0):
                        
                        # Found a valid leak source adjacent to this border pixel.
                        # Check if this border pixel also touches the inner region (should be true by definition of border_pixels)
                        touches_inner = False
                        for b_neighbor_r, b_neighbor_c in get_neighbors(grid_shape, br, bc):
                            if (b_neighbor_r, b_neighbor_c) in inner_region_coords:
                                touches_inner = True
                                break 
                        
                        if touches_inner: # Confirm adjacency for robustness
                            leaking_color = c_adjacent
                            break # Stop searching for leaks for this region

                if leaking_color is not None:
                    break # Stop iterating through border pixels once leak is found
        
        # 4. Apply flood fill transformation if leak was found
        if leaking_color is not None:
            # Modify the output grid: change color of all inner region pixels
            for r, c in inner_region_coords:
                output_grid[r, c] = leaking_color
                
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 3 3 3 3 3 3 3 0 0
1 2 2 2 2 1 0 0 0 0 0 0 3 0 0
1 1 1 1 1 1 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
1 2 2 2 2 1 0 0 0 0 0 0 0 0 0
1 2 3 3 3 3 3 3 3 3 3 3 3 0 0
1 2 3 2 2 1 0 0 0 0 0 0 3 0 0
1 1 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
1 3 3 3 3 1 0 0 0 0 0 0 0 0 0
1 3 3 3 3 1 3 3 3 3 3 3 3 0 0
1 3 3 3 3 1 0 0 0 0 0 0 3 0 0
1 1 1 1 1 1 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 3 0 0 0 0 0 0 0 0 0 3 0 0
0 0 3 3 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.833333333333343

## Example 2:
Input:
```
0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 4 4 4 8 0 0 0 0 0 0
0 6 6 6 6 6 8 4 4 4 8 6 6 6 6 6 0
0 6 0 6 0 6 8 8 8 8 8 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 4 4 4 8 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 6 0 6 0 6 8 6 8 6 8 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 6 6 6 8 0 0 0 0 0 0
0 6 6 6 6 6 8 6 6 6 8 6 6 6 6 6 0
0 6 0 6 0 6 8 8 8 8 8 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6 0
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.486631016042793
