import numpy as np
from collections import deque

def check_enclosure_and_get_region(grid, start_r, start_c):
    """
    Performs a BFS starting from (start_r, start_c) to find the contiguous region 
    of the same color and determine if it's enclosed by a single other non-white color.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.

    Returns:
        tuple: (is_enclosed, region_pixels)
               is_enclosed (bool): True if the region is enclosed, False otherwise.
               region_pixels (set): Set of coordinates {(r, c)} belonging to the 
                                     contiguous region starting at (start_r, start_c).
                                     Returns the region regardless of enclosure status.
    """
    H, W = grid.shape
    target_color = grid[start_r, start_c]

    # Should not be called on white pixels, but as a safeguard:
    if target_color == 0:
        return False, set()

    queue = deque([(start_r, start_c)])
    # Tracks pixels visited during this specific BFS to avoid cycles within the search
    visited_during_search = set([(start_r, start_c)]) 
    # Stores coordinates of the contiguous target_color region found
    region_pixels = set([(start_r, start_c)])
    # Stores the colors of adjacent, non-target, non-white pixels
    boundary_colors = set()
    # Flag set if the search reaches the grid edge or a white pixel 
    # *directly from* a pixel of target_color
    is_escaped = False

    while queue:
        curr_r, curr_c = queue.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check 1: Is neighbor outside the grid? -> Escape condition
            if not (0 <= nr < H and 0 <= nc < W):
                is_escaped = True
                break # Reached grid edge from a target pixel

            neighbor_color = grid[nr, nc]
            neighbor_coord = (nr, nc)

            # Check 2: Is neighbor white (background)? -> Escape condition
            if neighbor_color == 0:
                is_escaped = True
                break # Reached background from a target pixel

            # Check 3: Is neighbor the same color as the target region?
            if neighbor_color == target_color:
                # If not already visited in this search, add to queue and sets
                if neighbor_coord not in visited_during_search:
                    visited_during_search.add(neighbor_coord)
                    region_pixels.add(neighbor_coord)
                    queue.append(neighbor_coord)
            
            # Check 4: Is neighbor a different, non-white color? -> Potential boundary
            else: 
                boundary_colors.add(neighbor_color)

        # If an escape condition was met during neighbor checks, stop the BFS early
        if is_escaped:
            break 

    # Determine enclosure based on BFS results
    # Condition: Not escaped AND exactly one boundary color was found
    is_enclosed = (not is_escaped) and (len(boundary_colors) == 1)
    
    return is_enclosed, region_pixels


def transform(input_grid):
    """
    Identifies contiguous regions of pixels that are fully enclosed by a boundary 
    composed of a single, different non-white color. Changes the color of all 
    pixels within each such enclosed region to white (0). Pixels forming the 
    boundaries and pixels in regions that are not enclosed (touch the grid edge, 
    touch white pixels, or have multi-colored/no boundaries) remain unchanged.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    
    # Create a copy of the grid to modify and return
    output_grid = np.copy(grid)
    
    # Create a mask to keep track of pixels that have already been processed 
    # (either identified as enclosed or checked as part of a region).
    # This prevents redundant BFS calls for pixels in the same region.
    processed_mask = np.zeros((H, W), dtype=bool) 

    # Iterate through each pixel in the grid
    for r in range(H):
        for c in range(W):
            # Process only non-white pixels that haven't been processed yet
            if grid[r, c] != 0 and not processed_mask[r, c]:
                
                # Perform BFS to check for enclosure and get the region's pixels
                is_enclosed, region_pixels = check_enclosure_and_get_region(grid, r, c)

                # Mark all pixels in the found region as processed, regardless of enclosure status,
                # to avoid re-checking them later.
                for pr, pc in region_pixels:
                    processed_mask[pr, pc] = True

                # If the region starting at (r, c) is confirmed to be enclosed
                if is_enclosed:
                    # Iterate through all pixels identified as belonging to this enclosed region
                    for er, ec in region_pixels:
                        # Change the color of these pixels to white (0) in the output grid
                        output_grid[er, ec] = 0
                        # Note: processed_mask was already updated for these pixels above.

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()