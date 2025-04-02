import numpy as np
from collections import deque

"""
Identifies contiguous regions enclosed by a single-colored border. 
If any pixel on the border is adjacent to both the enclosed region and a third, different colored region (the 'adjacent' color), 
then the entire enclosed region is flood-filled with this adjacent color. 
Otherwise, the grid remains unchanged.
"""

def get_neighbors(grid, r, c):
    """ Gets valid 4-directional neighbors for a cell (r, c) """
    neighbors = []
    height, width = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_regions(grid):
    """ Finds all contiguous regions of the same color in the grid. """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
                region_color = grid[r, c]
                region_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    region_coords.add((curr_r, curr_c))

                    for nr, nc in get_neighbors(grid, curr_r, curr_c):
                        if not visited[nr, nc] and grid[nr, nc] == region_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if region_coords: # Ensure we don't add empty regions if logic changes
                     regions.append({'coords': region_coords, 'color': region_color})
    return regions

def check_enclosure_and_leak(grid, region_info):
    """
    Checks if a region is enclosed by a single border color and if a leak point exists.

    Args:
        grid (np.array): The input grid.
        region_info (dict): A dictionary containing 'coords' (set of (r, c) tuples) 
                             and 'color' for the region.

    Returns:
        int or None: The color to flood-fill with if a leak is found, otherwise None.
                     Returns None if the region is not enclosed or no leak is found.
    """
    region_coords = region_info['coords']
    region_color = region_info['color']
    height, width = grid.shape
    
    border_coords_set = set()
    first_border_color = None
    is_potentially_enclosed = True

    # 1. Find all immediate neighbors outside the region and check for single border color
    for r, c in region_coords:
        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in region_coords:
                neighbor_color = grid[nr, nc]
                
                # Cannot be enclosed if border color is same as region color
                if neighbor_color == region_color:
                    return None 
                    
                if first_border_color is None:
                    first_border_color = neighbor_color
                elif neighbor_color != first_border_color:
                    is_potentially_enclosed = False
                    break # Found more than one border color
                
                border_coords_set.add((nr, nc))
        if not is_potentially_enclosed:
            break

    # Region is not enclosed if it wasn't potentially enclosed, or has no border found
    # (e.g., single pixel grid, or touches grid edge in a way that prevents enclosure)
    if not is_potentially_enclosed or first_border_color is None:
        return None

    border_color = first_border_color

    # 2. Check border pixels for leaks
    for br, bc in border_coords_set:
        has_inner_neighbor = False
        leak_color_candidate = None
        
        # Check neighbors of the border pixel
        for nbr, nbc in get_neighbors(grid, br, bc):
            neighbor_coord = (nbr, nbc)
            neighbor_color = grid[nbr, nbc]

            # Is this neighbor inside the original region?
            if neighbor_coord in region_coords:
                has_inner_neighbor = True

            # Is this neighbor neither the region color nor the border color?
            # This is a potential leak source.
            if neighbor_color != region_color and neighbor_color != border_color:
                 # Make sure this adjacent color pixel is not part of the border itself
                 # (though this check might be redundant if border is contiguous and single-colored)
                 # if neighbor_coord not in border_coords_set: # <-- This check might be overly strict depending on interpretation. Let's try without first.
                 leak_color_candidate = neighbor_color

        # If this border pixel touches BOTH the inner region AND a third color, it's a leak point
        if has_inner_neighbor and leak_color_candidate is not None:
            return leak_color_candidate # Found the leak color

    # If we checked all border pixels and found no leak
    return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on the enclosure and leak rule.
    Finds enclosed regions, checks if they have a single-colored border,
    determines if a leak point exists from an adjacent third color across the border,
    and if so, flood-fills the enclosed region with the third color.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # Find all distinct regions in the input grid
    regions = find_regions(input_grid)

    # Process each region found
    for region_info in regions:
        # Check if this region is enclosed and find the leak color, if any
        leak_color = check_enclosure_and_leak(input_grid, region_info)
        
        # If a leak color was determined
        if leak_color is not None:
            # Modify the output grid by changing the color of all pixels in the region
            region_coords = region_info['coords']
            for r, c in region_coords:
                output_grid[r, c] = leak_color
                
    return output_grid
