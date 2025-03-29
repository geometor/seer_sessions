import numpy as np
from collections import deque

"""
Identifies contiguous regions of white pixels (0) in the input grid.
For each white region, it determines if it is fully enclosed by blue pixels (1) using a Breadth-First Search (BFS). A region is considered enclosed if the BFS, starting from a pixel within the region, only encounters blue pixels (1) at its immediate boundary and does not reach the grid edge.
If a white region is enclosed:
  - It checks the neighbors (8-connectivity) of all the blue pixels forming the immediate boundary of the enclosed region.
  - If any of these boundary blue pixels has a neighbor (that is not part of the enclosed white region itself) with a color other than white (0) or blue (1), the enclosed white region is filled with red (2).
  - Otherwise (if all neighbors of the boundary blue pixels are either white (0), blue (1), or part of the enclosed white region), the enclosed white region is filled with orange (7).
Pixels that are not part of such an enclosed and filled white region remain unchanged.
"""

def transform(input_grid):
    """
    Fills enclosed white regions within blue loops based on boundary adjacency.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    visited_white = np.zeros((height, width), dtype=bool) # Keep track of white pixels already processed

    # Iterate through each pixel to find starting points for potential white regions
    for r_start in range(height):
        for c_start in range(width):
            # Check if it's a white pixel and hasn't been visited/processed yet
            if input_grid_np[r_start, c_start] == 0 and not visited_white[r_start, c_start]:
                
                # Initialize data structures for BFS for this potential region
                region_pixels = set()
                boundary_blue_pixels = set()
                q = deque([(r_start, c_start)])
                visited_white[r_start, c_start] = True
                region_pixels.add((r_start, c_start))
                is_enclosed_by_blue = True # Assume enclosed until proven otherwise
                hit_grid_boundary = False # Flag if the region touches the edge

                # Perform BFS to find the extent of the white region and its immediate neighbors
                while q:
                    r, c = q.popleft()

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            
                            nr, nc = r + dr, c + dc

                            # Check if neighbor is within grid bounds
                            if not (0 <= nr < height and 0 <= nc < width):
                                hit_grid_boundary = True
                                continue # Continue BFS but note boundary contact

                            neighbor_coord = (nr, nc)
                            neighbor_color = input_grid_np[nr, nc]

                            # If neighbor is white and not yet visited for *any* region
                            if neighbor_color == 0 and not visited_white[nr, nc]:
                                visited_white[nr, nc] = True
                                region_pixels.add(neighbor_coord)
                                q.append(neighbor_coord)
                            # If neighbor is blue, add to potential boundary
                            elif neighbor_color == 1:
                                boundary_blue_pixels.add(neighbor_coord)
                            # If neighbor is neither white nor blue, region is not enclosed solely by blue
                            elif neighbor_color != 0: # Color is not 0 and not 1
                                is_enclosed_by_blue = False
                                # We can continue the BFS to mark all region pixels visited,
                                # but we know it's not enclosed by only blue.
                
                # After BFS for the region, decide if it needs filling
                if is_enclosed_by_blue and not hit_grid_boundary and boundary_blue_pixels:
                    # Region is enclosed by blue and doesn't touch the boundary.
                    # Now determine the fill color based on boundary blue neighbors.
                    fill_color = 7 # Default to orange
                    
                    found_non_white_blue_neighbor = False
                    for br, bc in boundary_blue_pixels:
                        # Check 8 neighbors for this boundary blue pixel
                        for dr_b in [-1, 0, 1]:
                            for dc_b in [-1, 0, 1]:
                                if dr_b == 0 and dc_b == 0:
                                    continue
                                
                                bnr, bnc = br + dr_b, bc + dc_b
                                boundary_neighbor_coord = (bnr, bnc)

                                # Check bounds for the boundary neighbor
                                if not (0 <= bnr < height and 0 <= bnc < width):
                                    continue # Ignore out-of-bounds neighbors

                                # Ignore if the neighbor is part of the white region we are filling
                                if boundary_neighbor_coord in region_pixels:
                                    continue

                                boundary_neighbor_color = input_grid_np[bnr, bnc]

                                # If a neighbor of a boundary blue is NOT white(0) and NOT blue(1)
                                if boundary_neighbor_color not in [0, 1]:
                                     fill_color = 2 # Set fill to red
                                     found_non_white_blue_neighbor = True
                                     break # Found a disqualifying neighbor for this blue pixel
                        if found_non_white_blue_neighbor:
                            break # No need to check other boundary blue pixels

                    # Fill the identified region in the output grid
                    for pr, pc in region_pixels:
                        output_grid[pr, pc] = fill_color
                
                # If not enclosed or hit boundary, the region remains white (or its original color),
                # and its pixels are marked as visited_white, so we don't re-process them.

    return output_grid.tolist()