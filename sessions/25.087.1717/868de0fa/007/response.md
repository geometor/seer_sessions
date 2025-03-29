```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (0) in the input grid.
For each white region, it determines if it is fully enclosed by only blue pixels (1) using a Breadth-First Search (BFS). A region is considered enclosed if the BFS, starting from a pixel within the region, only encounters blue pixels (1) at its immediate 8-way adjacent boundary and does not reach the grid edge.

If a white region is enclosed:
  - It examines the neighbors of all the blue pixels forming the immediate boundary of the enclosed region (let's call this set B).
  - Specifically, it checks the *orthogonal* (up, down, left, right) neighbors of each blue pixel in B.
  - If any blue pixel in B has an *orthogonal* neighbor that is also blue (1) but is *not* part of the set B itself (i.e., an 'external' orthogonal blue neighbor), the enclosed white region is filled with red (2).
  - Otherwise (if no boundary blue pixel has such an external *orthogonal* blue neighbor), the enclosed white region is filled with orange (7).

Pixels that are not part of such an enclosed and filled white region remain unchanged.
"""

def transform(input_grid):
    """
    Fills enclosed white regions within blue loops based on the orthogonal 
    adjacency of boundary blue pixels to other 'external' blue pixels.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    # Keep track of white pixels already processed as part of a region
    visited_white = np.zeros((height, width), dtype=bool) 

    # 1. Iterate through each pixel to find starting points for potential white regions
    for r_start in range(height):
        for c_start in range(width):
            # Check if it's an unprocessed white pixel
            if input_grid_np[r_start, c_start] == 0 and not visited_white[r_start, c_start]:
                
                # Initialize data structures for BFS for this potential region
                region_pixels = set()           # Pixels belonging to the current white region
                boundary_blue_pixels = set()    # Blue pixels immediately adjacent (8-way) to the region
                q = deque([(r_start, c_start)]) # Queue for BFS
                visited_white[r_start, c_start] = True # Mark starting pixel as visited
                region_pixels.add((r_start, c_start))
                is_enclosed_by_blue = True    # Assume enclosed until proven otherwise
                hit_grid_boundary = False     # Flag if the region touches the grid edge

                # 2. Perform BFS to find region extent and immediate boundary
                while q:
                    r, c = q.popleft()

                    # Check 8 neighbors (including diagonals) for region boundary check
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = r + dr, c + dc
                            neighbor_coord = (nr, nc)

                            # Check if neighbor is outside the grid bounds
                            if not (0 <= nr < height and 0 <= nc < width):
                                hit_grid_boundary = True
                                # Continue BFS to mark all connected white pixels as visited,
                                # but we know it won't be filled.
                                continue 

                            neighbor_color = input_grid_np[nr, nc]

                            # If neighbor is white and not yet visited for *this region search*
                            if neighbor_color == 0 and not visited_white[nr, nc]:
                                visited_white[nr, nc] = True
                                region_pixels.add(neighbor_coord)
                                q.append(neighbor_coord)
                            # If neighbor is blue, add to potential immediate boundary set
                            elif neighbor_color == 1:
                                boundary_blue_pixels.add(neighbor_coord)
                            # If neighbor is neither white nor blue, the boundary is not solely blue
                            elif neighbor_color != 0: 
                                is_enclosed_by_blue = False
                                # Continue BFS to mark region visited, but it won't be filled.
                
                # 3. Check if the region qualifies for filling
                # Conditions: Fully enclosed only by blue, didn't touch grid boundary, has a blue boundary
                if is_enclosed_by_blue and not hit_grid_boundary and boundary_blue_pixels:
                    
                    # 4. Determine fill color (Orange=7 or Red=2) based on orthogonal neighbors
                    fill_color = 7 # Default to orange
                    found_external_orthogonal_blue_neighbor = False # Flag for red condition

                    # Iterate through each blue pixel forming the immediate boundary
                    for br, bc in boundary_blue_pixels:
                        # Check only 4 ORTHOGONAL neighbors for this boundary blue pixel
                        for dr_b, dc_b in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            
                            bnr, bnc = br + dr_b, bc + dc_b
                            boundary_neighbor_coord = (bnr, bnc)

                            # Check if the orthogonal neighbor is within grid bounds
                            if not (0 <= bnr < height and 0 <= bnc < width):
                                continue # Ignore out-of-bounds neighbors

                            boundary_neighbor_color = input_grid_np[bnr, bnc]

                            # Check the condition for red fill:
                            # Is the ORTHOGONAL neighbor blue (1)?
                            # AND is this blue neighbor NOT part of the immediate boundary set?
                            if boundary_neighbor_color == 1 and boundary_neighbor_coord not in boundary_blue_pixels:
                                 fill_color = 2 # Set fill to red
                                 found_external_orthogonal_blue_neighbor = True
                                 break # Found condition for red, no need to check other neighbors of this blue pixel
                        
                        if found_external_orthogonal_blue_neighbor:
                            break # Found condition for red, no need to check other boundary blue pixels

                    # 5. Fill the identified region in the output grid
                    for pr, pc in region_pixels:
                        output_grid[pr, pc] = fill_color
                
                # If the region wasn't enclosed by blue or hit the boundary, 
                # it remains white. Its pixels were marked visited_white 
                # during BFS, so they won't start a new search.

    # 6. Return the modified grid
    return output_grid.tolist()
```