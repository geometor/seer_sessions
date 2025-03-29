import numpy as np
from collections import deque

"""
Identify closed loops formed by blue (1) pixels that enclose only white (0) pixels.
Determine the fill color for the enclosed white (0) region based on the surroundings of the blue (1) loop boundary.
If any pixel on the blue (1) boundary is adjacent (including diagonals) to any pixel that is *not* white (0) and *not* blue (1), fill the enclosed white (0) region with red (2).
Otherwise (if the blue (1) boundary is only adjacent to white (0) or other blue (1) pixels), fill the enclosed white (0) region with orange (7).
Pixels that are not part of such an enclosed white region remain unchanged.
"""

def find_contiguous_regions(grid, target_color):
    """
    Finds all contiguous regions of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the regions to find.

    Returns:
        list[set]: A list of sets, where each set contains the (row, col) tuples
                   of pixels belonging to a contiguous region.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                region = set()
                q = deque([(r, c)])
                visited[r, c] = True
                region.add((r, c))

                while q:
                    row, col = q.popleft()
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                region.add((nr, nc))
                                q.append((nr, nc))
                if region:
                    regions.append(region)
    return regions

def get_neighbors(grid, r, c, connectivity=8):
    """Gets neighbors of a cell."""
    height, width = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            # Restrict to 4-connectivity if specified (not needed here based on analysis)
            # if connectivity == 4 and abs(dr) + abs(dc) != 1:
            #    continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(((nr, nc), grid[nr, nc]))
            else: # Consider out-of-bounds as a distinct 'neighbor' type if needed
                 pass 
    return neighbors


def transform(input_grid):
    """
    Fills enclosed white regions within blue loops based on boundary adjacency.

    Identifies regions of white (0) pixels. For each region, it checks if it is
    fully enclosed by blue (1) pixels. If so, it determines the fill color:
    - Red (2) if any boundary blue pixel is adjacent (8-connectivity) to a
      non-white, non-blue pixel.
    - Orange (7) otherwise.
    The identified white region is then filled with the determined color in the output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Find all contiguous regions of white pixels
    white_regions = find_contiguous_regions(input_grid_np, 0)

    for region in white_regions:
        is_enclosed = True
        boundary_blue_pixels = set()
        
        # 1. Check if the white region is fully enclosed by blue (1) pixels
        for r, c in region:
            # Check 8 neighbors for each white pixel in the region
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc

                    # Check bounds
                    if not (0 <= nr < height and 0 <= nc < width):
                         # Touches grid boundary, not fully enclosed by definition here
                         # (Though problem description implies boundary acts like white)
                         # Let's assume touching boundary is allowed unless it breaks loop
                         # For simplicity, we require a *pixel* boundary.
                         # If it touches boundary AND is not enclosed by blue, it's not an interior.
                         # Revisit if edge cases fail. For now, assume boundary doesn't break enclosure concept.
                         continue 

                    neighbor_color = input_grid_np[nr, nc]
                    neighbor_coord = (nr, nc)

                    if neighbor_color == 1:
                        # If neighbor is blue, add it to potential boundary
                        if neighbor_coord not in region: # Ensure it's not part of the same white region
                           boundary_blue_pixels.add(neighbor_coord)
                    elif neighbor_color == 0:
                        # If neighbor is white, check if it's part of the current region
                        if neighbor_coord not in region:
                             # Found adjacent white pixel outside current region - means not enclosed?
                             # This check might be too strict if multiple white regions are adjacent.
                             # Let's rely on checking non-white/non-blue neighbors.
                             pass
                    else:
                        # If neighbor is neither white (0) nor blue (1), it's not enclosed by blue
                        is_enclosed = False
                        break # No need to check other neighbors for this pixel
            if not is_enclosed:
                break # No need to check other pixels in this region

        # If the region was not enclosed by only blue (or other white pixels from the same region), skip it
        if not is_enclosed or not boundary_blue_pixels:
            continue

        # 2. Determine fill color based on neighbors of the boundary blue pixels
        fill_color = 7 # Default to orange

        boundary_is_clean = True
        for br, bc in boundary_blue_pixels:
             # Check 8 neighbors for each boundary blue pixel
            for dr_b in [-1, 0, 1]:
                for dc_b in [-1, 0, 1]:
                    if dr_b == 0 and dc_b == 0:
                        continue
                    
                    bnr, bnc = br + dr_b, bc + dc_b

                    # Check bounds
                    if not (0 <= bnr < height and 0 <= bnc < width):
                        continue # Ignore out-of-bounds neighbors

                    boundary_neighbor_color = input_grid_np[bnr, bnc]
                    boundary_neighbor_coord = (bnr, bnc)

                    # If a neighbor of a boundary blue is NOT white(0) and NOT blue(1)
                    # and NOT part of the original white region being filled
                    if boundary_neighbor_color not in [0, 1] and boundary_neighbor_coord not in region:
                         fill_color = 2 # Set fill to red
                         boundary_is_clean = False
                         break # Found a disqualifying neighbor
            if not boundary_is_clean:
                 break # No need to check other boundary blues

        # 3. Fill the enclosed region in the output grid
        for r, c in region:
            output_grid[r, c] = fill_color

    return output_grid.tolist()