import numpy as np
from collections import deque

"""
Fill specific background (White/0) areas adjacent to a main structure (most frequent non-background color) with a checkerboard pattern. 
The filling starts from existing 'seed' pixels (pixels with the pattern colors) in the input grid.
The checkerboard pattern colors are determined by the seed pixels: either Blue(1)/Yellow(4) or Red(2)/Green(3).
The specific color applied to a background pixel depends on the parity of the sum of its coordinates (row + col).
A background pixel is filled only if it's adjacent (8-connectivity) to the structure color AND adjacent to a pixel that is already part of the growing pattern (either a seed or a previously filled pixel).
"""

def is_valid(r, c, rows, cols):
    """Checks if coordinates (r, c) are within the grid bounds."""
    return 0 <= r < rows and 0 <= c < cols

def has_neighbor_color(grid, r, c, color, rows, cols):
    """
    Checks if cell (r, c) has any neighbor (including diagonals) 
    with the specified color in the given grid.
    """
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc, rows, cols) and grid[nr, nc] == color:
                return True
    return False

def transform(input_grid):
    """
    Applies a checkerboard pattern flood fill to background pixels adjacent 
    to a main structure, starting from seed pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    background_color = 0

    # --- 1. Analyze Input ---
    
    # Find unique non-background colors and their counts
    unique_colors, counts = np.unique(input_grid[input_grid != background_color], return_counts=True)
    
    # Handle edge case: No non-background colors or only one type
    if len(unique_colors) <= 1:
        return output_grid # Nothing to pattern or no seeds

    # Determine the structure_color (most frequent non-background)
    color_counts = dict(zip(unique_colors, counts))
    structure_color = max(color_counts, key=color_counts.get)

    # Identify pattern colors (seeds) and their locations
    pattern_colors = set()
    seed_pixels = []
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != background_color and color != structure_color:
                pattern_colors.add(color)
                seed_pixels.append((r, c))

    # Handle edge case: No seed pixels found
    if not seed_pixels:
        return output_grid

    # Determine the pattern_type based on present pattern colors
    use_pattern_1_4 = 1 in pattern_colors or 4 in pattern_colors
    use_pattern_3_2 = 3 in pattern_colors or 2 in pattern_colors

    # Handle edge case: Pattern colors don't match expected pairs
    if not use_pattern_1_4 and not use_pattern_3_2:
         return output_grid

    # --- 2. Initialize Fill Process ---
    
    process_queue = deque(seed_pixels)
    # visited_coords stores coordinates of background pixels that have been 
    # processed (colored) or added to the queue. Seed pixels are not background,
    # so they aren't added here initially, only their background neighbors will be.
    visited_coords = set() 

    # --- 3. Flood Fill Execution ---
    
    while process_queue:
        r, c = process_queue.popleft()

        # Examine 8 neighbors of the current pixel (from the queue)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                nr, nc = r + dr, c + dc

                # Check Validity: Within grid bounds?
                if not is_valid(nr, nc, rows, cols):
                    continue

                # Check Target: Is it a background pixel in the *original* grid?
                if input_grid[nr, nc] != background_color:
                    continue

                # Check Visited: Has this background pixel already been processed?
                if (nr, nc) in visited_coords:
                    continue

                # Check Structure Adjacency: Is it adjacent to the structure color?
                if not has_neighbor_color(input_grid, nr, nc, structure_color, rows, cols):
                    continue
                    
                # --- Fill and Enqueue ---
                # Mark as visited *before* adding to queue
                visited_coords.add((nr, nc)) 

                # Calculate parity
                parity = (nr + nc) % 2

                # Determine fill color based on pattern type and parity
                fill_color = -1 # Default invalid color
                if use_pattern_1_4:
                    # Pattern blue(1)/yellow(4): Even sum -> blue(1), Odd sum -> yellow(4)
                    fill_color = 1 if parity == 0 else 4
                elif use_pattern_3_2:
                    # Pattern green(3)/red(2): Even sum -> red(2), Odd sum -> green(3)
                    fill_color = 2 if parity == 0 else 3
                
                # Update the output grid
                output_grid[nr, nc] = fill_color
                
                # Add the newly colored background pixel to the queue 
                # so its neighbors can be checked
                process_queue.append((nr, nc))

    # --- 4. Return Output ---
    return output_grid