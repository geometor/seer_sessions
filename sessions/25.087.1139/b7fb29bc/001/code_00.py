import numpy as np

"""
Fill the area inside a green rectangular frame based on the Manhattan distance 
from internal green 'seed' pixels. The frame itself and the seed pixels remain 
unchanged. White pixels inside the frame are colored based on their minimum 
Manhattan distance (d) to any seed pixel: yellow (4) if d is odd, red (2) if d 
is even and positive. Pixels outside the frame remain white.
"""

def find_frame_and_seeds(grid):
    """
    Identifies the frame boundaries and the locations of seed pixels (green pixels inside the frame).
    Assumes a single rectangular frame made of green pixels (3).
    """
    green_pixels = np.argwhere(grid == 3)
    if green_pixels.size == 0:
        return None, None, [] # No frame found

    min_r, min_c = green_pixels.min(axis=0)
    max_r, max_c = green_pixels.max(axis=0)

    # Frame boundaries (inclusive)
    frame_bounds = (min_r, min_c, max_r, max_c)
    # Inner area boundaries (exclusive of frame)
    inner_bounds = (min_r + 1, min_c + 1, max_r - 1, max_c - 1)

    seeds = []
    for r, c in green_pixels:
        # Check if the green pixel is strictly inside the outer frame boundaries
        if min_r < r < max_r and min_c < c < max_c:
            # Ensure it's not part of the frame itself (check if neighbors are also green)
            # A simpler check for these examples: is it surrounded by non-green inside the frame area?
            # Or, even simpler: assume any green pixel strictly inside the min/max bounds is a seed.
            # Let's refine this: identify frame pixels first.
            is_frame_pixel = (r == min_r or r == max_r or c == min_c or c == max_c)
            if not is_frame_pixel:
                 seeds.append((r, c))

    # Re-check frame pixels, they can't be seeds
    # This simple identification might mistake internal structures for seeds
    # Let's redefine seeds as *isolated* green pixels within the inner bounds.
    potential_seeds = []
    for r in range(inner_bounds[0], inner_bounds[2] + 1):
         for c in range(inner_bounds[1], inner_bounds[3] + 1):
             if grid[r, c] == 3:
                 potential_seeds.append((r,c))

    # If a green pixel inside has green neighbors (part of frame line), it's not a seed
    seeds = []
    for r, c in potential_seeds:
        is_isolated = True
        # Check 4 neighbors (not diagonal)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds just in case, though they should be within frame
            if min_r <= nr <= max_r and min_c <= nc <= max_c:
                 # If a neighbor is green AND is on the frame boundary, this pixel might still be a seed.
                 # If a neighbor is green AND is *not* on the frame boundary, this pixel is not isolated.
                 is_neighbor_on_frame = (nr == min_r or nr == max_r or nc == min_c or nc == max_c)
                 if grid[nr, nc] == 3 and not is_neighbor_on_frame:
                     is_isolated = False
                     break
        if is_isolated:
            seeds.append((r,c))


    return frame_bounds, inner_bounds, seeds


def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points (r1, c1) and (r2, c2)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Transforms the input grid by filling the area inside a green frame
    based on the distance to internal green seed pixels.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the green frame boundaries and the seed pixels inside it
    frame_bounds, inner_bounds, seeds = find_frame_and_seeds(input_grid)

    # If no frame or no seeds are found, return the original grid
    if frame_bounds is None or not seeds:
        return output_grid

    min_r_inner, min_c_inner, max_r_inner, max_c_inner = inner_bounds

    # Iterate through the pixels *inside* the frame
    for r in range(min_r_inner, max_r_inner + 1):
        for c in range(min_c_inner, max_c_inner + 1):
            # Only process pixels that are currently white (0)
            if output_grid[r, c] == 0:
                min_dist = float('inf')
                current_pos = (r, c)

                # Calculate distance to all seed pixels
                for seed_pos in seeds:
                    dist = manhattan_distance(current_pos, seed_pos)
                    min_dist = min(min_dist, dist)

                # Color the pixel based on the minimum distance
                if min_dist != float('inf'): # Check if a distance was actually found
                    if min_dist > 0: # Don't change seeds themselves (though we only target white pixels)
                        if min_dist % 2 != 0: # Odd distance
                            output_grid[r, c] = 4 # Yellow
                        else: # Even distance
                            output_grid[r, c] = 2 # Red

    return output_grid