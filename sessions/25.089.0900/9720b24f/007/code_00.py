"""
Identifies contiguous regions of pixels (sharing the same non-white color) 
that are fully enclosed. Enclosure is defined by failing an "escape test": 
a region is enclosed if a search starting from within the region cannot reach 
the grid edge or any background (0) pixel, where the search is blocked *only* 
by adjacent pixels of a single, uniform, non-background color (the boundary color). 
If a region is identified as enclosed, all pixels within that region are 
changed to white (0) in the output grid. Pixels forming the boundaries 
and pixels in regions that are not enclosed remain unchanged.
"""

import numpy as np
from collections import deque

def _find_contiguous_region(grid, start_r, start_c, processed_mask):
    """
    Finds all connected pixels of the same color as the starting pixel using BFS.
    Marks found pixels as processed in the mask. Helper for transform.

    Args:
        grid (np.array): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        processed_mask (np.array): Boolean mask to mark processed pixels.

    Returns:
        tuple: (region_pixels, target_color)
               region_pixels (set): A set of coordinates {(r, c)} belonging to 
                                    the contiguous region. Empty if start pixel
                                    is background or already processed.
               target_color (int): The color of the found region, or -1 if no
                                   region found.
    """
    H, W = grid.shape
    
    # Avoid processing background or already processed pixels
    if grid[start_r, start_c] == 0 or processed_mask[start_r, start_c]:
        return set(), -1

    target_color = grid[start_r, start_c]
    region_pixels = set()
    queue = deque([(start_r, start_c)])
    
    # Mark the starting pixel as processed immediately and add to region
    processed_mask[start_r, start_c] = True
    region_pixels.add((start_r, start_c))

    while queue:
        curr_r, curr_c = queue.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_coord = (nr, nc)
                # Check if neighbor has the target color and hasn't been processed yet
                if grid[nr, nc] == target_color and not processed_mask[nr, nc]:
                    processed_mask[nr, nc] = True # Mark as processed
                    region_pixels.add(neighbor_coord)
                    queue.append(neighbor_coord)
    
    return region_pixels, target_color


def _check_enclosure(grid, region_pixels, target_color):
    """
    Checks if a given region is fully enclosed according to the escape test rules.
    Helper for transform.

    Args:
        grid (np.array): The input grid.
        region_pixels (set): Set of coordinates {(r, c)} for the region.
        target_color (int): The color of the region being checked.

    Returns:
        bool: True if the region is enclosed, False otherwise.
    """
    H, W = grid.shape
    potential_boundary_colors = set()
    
    # 1. Identify all potential boundary colors adjacent to the region
    for r, c in region_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check boundary conditions for neighbor
            if 0 <= nr < H and 0 <= nc < W:
                neighbor_coord = (nr, nc)
                # If neighbor is outside the region and not background
                if neighbor_coord not in region_pixels:
                    neighbor_color = grid[nr, nc]
                    if neighbor_color != 0: # Exclude background from boundary colors
                         potential_boundary_colors.add(neighbor_color)
            # Note: touching the edge or background directly doesn't automatically disqualify
            #       enclosure here, that's checked in the escape test.

    # 2. Check if there's exactly one potential boundary color
    if len(potential_boundary_colors) != 1:
        return False # Not enclosed if zero or multiple boundary colors
        
    the_boundary_color = potential_boundary_colors.pop() # Get the single boundary color

    # 3. Perform the Escape Test using BFS
    queue = deque(region_pixels) # Start BFS from all pixels in the region
    visited_escape_test = set(region_pixels) # Track visited cells during this test
    
    while queue:
        curr_r, curr_c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check 3a: Escape via grid edge
            if not (0 <= nr < H and 0 <= nc < W):
                return False # Escaped! Not enclosed.

            neighbor_coord = (nr, nc)
            
            # Skip if already visited during this escape test
            if neighbor_coord in visited_escape_test:
                 continue

            neighbor_color = grid[nr, nc]

            # Check 3b: Escape via background pixel
            if neighbor_color == 0:
                return False # Escaped! Not enclosed.

            # Check 3c: Blocked by the boundary color
            if neighbor_color == the_boundary_color:
                # Don't add boundary pixels to visited or queue - path is blocked here
                continue 
            
            # Check 3d: Found a non-boundary, non-background, non-region pixel?
            # This implies the region check or boundary color identification might have missed something,
            # or the grid structure is unexpected (e.g. another region touching without boundary).
            # Treat this cautiously as not enclosed. (Though this might not be strictly necessary
            # if the initial boundary check is robust). Let's assume this shouldn't happen
            # if the boundary identification is correct.
            # if neighbor_coord not in region_pixels: # Already covered by boundary check
            #      pass 

            # If neighbor is traversable (not edge, background, or boundary) and not visited, explore it
            visited_escape_test.add(neighbor_coord)
            queue.append(neighbor_coord)

    # If the BFS completes without returning False, it means no escape path was found.
    return True # Enclosed!


def transform(input_grid):
    """
    Transforms the input grid by finding enclosed regions and setting their pixels to white (0).
    """
    # Convert input list of lists to NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape
    
    # Create a copy to modify for the output
    output_grid = np.copy(grid)
    
    # Create a mask to track pixels already assigned to a processed region
    processed_mask = np.zeros((H, W), dtype=bool) 

    # Iterate through each pixel in the grid
    for r in range(H):
        for c in range(W):
            # Only start processing if the pixel is non-white and not already processed
            if grid[r, c] != 0 and not processed_mask[r, c]:
                
                # Step 1: Find the entire contiguous region starting from (r, c)
                # This function also marks the found region in processed_mask.
                region_pixels, target_color = _find_contiguous_region(grid, r, c, processed_mask)

                # Proceed only if a valid region was found
                if region_pixels: 
                    # Step 2: Check if this identified region is enclosed
                    is_enclosed = _check_enclosure(grid, region_pixels, target_color)

                    # Step 3: If the region is enclosed, change its pixels to white (0) in the output grid
                    if is_enclosed:
                        for pr, pc in region_pixels:
                            output_grid[pr, pc] = 0

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_grid.tolist()