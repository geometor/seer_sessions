```python
import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (0) in the input grid.
For each white region, it determines if it is fully enclosed by blue pixels (1) using a Breadth-First Search (BFS). A region is considered enclosed if the BFS, starting from a pixel within the region, only encounters blue pixels (1) at its immediate boundary and does not reach the grid edge.
If a white region is enclosed:
  - It examines the neighbors (8-connectivity) of all the blue pixels forming the immediate boundary of the enclosed region (let's call this set B).
  - If any blue pixel in B has a neighbor that is also blue (1) but is *not* part of the set B itself (i.e., an 'external' blue neighbor), the enclosed white region is filled with red (2).
  - Otherwise (if all neighbors of the boundary blue pixels are either white (0), part of the enclosed white region, part of the boundary set B, or non-blue colors), the enclosed white region is filled with orange (7).
Pixels that are not part of such an enclosed and filled white region remain unchanged.
"""

def transform(input_grid):
    """
    Fills enclosed white regions within blue loops based on the adjacency 
    of boundary blue pixels to other 'external' blue pixels.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    visited_white = np.zeros((height, width), dtype=bool) # Keep track of white pixels already processed as part of a region

    # Iterate through each pixel to find starting points for potential white regions
    for r_start in range(height):
        for c_start in range(width):
            # Check if it's an unprocessed white pixel
            if input_grid_np[r_start, c_start] == 0 and not visited_white[r_start, c_start]:
                
                # Initialize data structures for BFS for this potential region
                region_pixels = set()           # Pixels belonging to the current white region
                boundary_blue_pixels = set()    # Blue pixels immediately adjacent to the region
                q = deque([(r_start, c_start)]) # Queue for BFS
                visited_white[r_start, c_start] = True # Mark starting pixel as visited
                region_pixels.add((r_start, c_start))
                is_enclosed_by_blue = True    # Assume enclosed until proven otherwise
                hit_grid_boundary = False     # Flag if the region touches the grid edge

                # --- Step 3: Perform BFS to find region extent and boundary ---
                while q:
                    r, c = q.popleft()

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = r + dr, c + dc
                            neighbor_coord = (nr, nc)

                            # Check if neighbor is outside the grid bounds
                            if not (0 <= nr < height and 0 <= nc < width):
                                hit_grid_boundary = True
                                # If we hit the boundary, the region cannot be enclosed.
                                # We continue the BFS to mark all connected white pixels as visited,
                                # but we know it won't be filled.
                                continue 

                            neighbor_color = input_grid_np[nr, nc]

                            # If neighbor is white and not yet visited for *this region search*
                            if neighbor_color == 0 and not visited_white[nr, nc]:
                                visited_white[nr, nc] = True
                                region_pixels.add(neighbor_coord)
                                q.append(neighbor_coord)
                            # If neighbor is blue, add to potential boundary set
                            elif neighbor_color == 1:
                                boundary_blue_pixels.add(neighbor_coord)
                            # If neighbor is neither white nor blue, it means the boundary is not solely blue
                            elif neighbor_color != 0: # Could be any color other than 0 or 1
                                is_enclosed_by_blue = False
                                # Continue BFS to mark region visited, but it won't be filled.
                
                # --- Step 4: Check if the region qualifies for filling ---
                # Conditions: Fully enclosed only by blue, didn't touch boundary, has a boundary
                if is_enclosed_by_blue and not hit_grid_boundary and boundary_blue_pixels:
                    
                    # --- Step 4a-h: Determine fill color (Orange=7 or Red=2) ---
                    fill_color = 7 # Default to orange
                    found_external_blue_neighbor = False # Flag for red condition

                    # Iterate through each blue pixel forming the immediate boundary
                    for br, bc in boundary_blue_pixels:
                        # Check 8 neighbors for this boundary blue pixel
                        for dr_b in [-1, 0, 1]:
                            for dc_b in [-1, 0, 1]:
                                if dr_b == 0 and dc_b == 0:
                                    continue # Skip self
                                
                                bnr, bnc = br + dr_b, bc + dc_b
                                boundary_neighbor_coord = (bnr, bnc)

                                # Check if the neighbor is within grid bounds
                                if not (0 <= bnr < height and 0 <= bnc < width):
                                    continue # Ignore out-of-bounds neighbors

                                boundary_neighbor_color = input_grid_np[bnr, bnc]

                                # Check the condition for red fill:
                                # Is the neighbor blue (1)?
                                # AND is this blue neighbor NOT part of the immediate boundary set?
                                if boundary_neighbor_color == 1 and boundary_neighbor_coord not in boundary_blue_pixels:
                                     fill_color = 2 # Set fill to red
                                     found_external_blue_neighbor = True
                                     break # Found condition for red, no need to check other neighbors of this blue pixel
                        
                        if found_external_blue_neighbor:
                            break # Found condition for red, no need to check other boundary blue pixels

                    # --- Step 4i: Fill the identified region in the output grid ---
                    for pr, pc in region_pixels:
                        output_grid[pr, pc] = fill_color
                
                # If the region wasn't enclosed by blue or hit the boundary, 
                # it remains white (or its original color). Its pixels were marked 
                # visited_white during BFS, so they won't start a new search.

    # --- Step 5: Return the modified grid ---
    return output_grid.tolist()
```