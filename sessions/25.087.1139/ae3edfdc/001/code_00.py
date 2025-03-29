import numpy as np

"""
Transformation rule:
1. Identify the locations of all blue (1) and red (2) pixels ("center" pixels) and all orange (7) and green (3) pixels ("partner" pixels) in the input grid.
2. Initialize an output grid of the same dimensions as the input, filled with white (0).
3. For each blue center pixel at (r, c):
    a. Find the two orange partner pixels closest to it using Manhattan distance. Use scan order (top-to-bottom, left-to-right) as a tie-breaker.
    b. Place the blue pixel at (r, c) in the output grid.
    c. Place orange pixels (7) at (r-1, c) (above) and (r+1, c) (below) in the output grid, if these positions are within the grid boundaries.
4. For each red center pixel at (r, c):
    a. Find the two green partner pixels closest to it using Manhattan distance, with the same tie-breaking rule.
    b. Place the red pixel at (r, c) in the output grid.
    c. Place green pixels (3) at (r, c-1) (left) and (r+1, c) (below) in the output grid, if these positions are within the grid boundaries.
5. Return the resulting output grid.
"""

def find_pixels(grid, color):
    """Finds all pixels of a specific color in the grid."""
    locations = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color:
                locations.append((r, c))
    return locations

def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points (row, col)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize with white (0)

    # Find center and partner pixels
    blue_centers = find_pixels(input_np, 1)
    red_centers = find_pixels(input_np, 2)
    orange_partners = find_pixels(input_np, 7)
    green_partners = find_pixels(input_np, 3)

    # --- Process Blue Centers (1) and Orange Partners (7) ---
    for center_r, center_c in blue_centers:
        # Place the blue center pixel in the output
        output_grid[center_r, center_c] = 1

        # Calculate distances to orange partners and include scan order index for tie-breaking
        orange_distances = []
        if orange_partners: # Only proceed if there are orange partners
            for r, c in orange_partners:
                dist = manhattan_distance((center_r, center_c), (r, c))
                scan_order_index = r * width + c # Tie-breaker
                orange_distances.append({'pos': (r, c), 'dist': dist, 'scan_index': scan_order_index})

            # Sort by distance, then by scan order index
            orange_distances.sort(key=lambda x: (x['dist'], x['scan_index']))

            # Select the two closest (if available)
            closest_partners = orange_distances[:2] # Get up to two closest

            # Place the corresponding orange pixels in the output grid
            # Based on the examples, it seems fixed positions relative to blue are used,
            # not the original positions of the closest orange pixels.
            # The task is to *move* the closest ones *conceptually* to these fixed relative spots.

            # Position 1: Above
            target_r, target_c = center_r - 1, center_c
            if 0 <= target_r < height and 0 <= target_c < width:
                 # We only place if there was at least one partner found
                 if len(closest_partners) >= 1:
                     output_grid[target_r, target_c] = 7

            # Position 2: Below
            target_r, target_c = center_r + 1, center_c
            if 0 <= target_r < height and 0 <= target_c < width:
                 # We only place if there were at least two partners found
                 if len(closest_partners) >= 2:
                     output_grid[target_r, target_c] = 7


    # --- Process Red Centers (2) and Green Partners (3) ---
    for center_r, center_c in red_centers:
        # Place the red center pixel in the output
        output_grid[center_r, center_c] = 2

        # Calculate distances to green partners and include scan order index
        green_distances = []
        if green_partners: # Only proceed if there are green partners
            for r, c in green_partners:
                dist = manhattan_distance((center_r, center_c), (r, c))
                scan_order_index = r * width + c # Tie-breaker
                green_distances.append({'pos': (r, c), 'dist': dist, 'scan_index': scan_order_index})

            # Sort by distance, then by scan order index
            green_distances.sort(key=lambda x: (x['dist'], x['scan_index']))

            # Select the two closest (if available)
            closest_partners = green_distances[:2]

            # Place the corresponding green pixels in the output grid
            # Similar to blue/orange, place at fixed relative positions.

            # Position 1: Left
            target_r, target_c = center_r, center_c - 1
            if 0 <= target_r < height and 0 <= target_c < width:
                # Place if at least one partner found
                if len(closest_partners) >= 1:
                    output_grid[target_r, target_c] = 3

            # Position 2: Below
            target_r, target_c = center_r + 1, center_c
            if 0 <= target_r < height and 0 <= target_c < width:
                 # Place if at least two partners found
                 if len(closest_partners) >= 2:
                     output_grid[target_r, target_c] = 3


    # Return the output grid, converting back to list of lists if needed by the framework
    return output_grid.tolist()
