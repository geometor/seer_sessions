import numpy as np
from collections import deque

"""
Transformation Rule: Boundary Projection

1. Identify "seed" pixels: non-gray (8) and non-green (3) pixels in the input.
2. Identify green (3) pixels, which act as boundary interfaces.
3. For each seed pixel, find adjacent green pixels (8-way connectivity).
4. For each pair of seed pixel (sr, sc) with color C and adjacent green pixel (gr, gc):
   a. Determine the projection direction (dr, dc) = (gr - sr, gc - sc).
   b. Define the ray starting position (start_r, start_c) = (gr + dr, gc + dc).
   c. Cast a ray from (start_r, start_c) in the direction (dr, dc).
5. Ray Casting Logic:
   a. Starting from (r, c) = (start_r, start_c), proceed in steps of (dr, dc).
   b. At each step (r, c):
      i. If (r, c) is outside the grid, stop the ray.
      ii. If the pixel input_grid[r, c] is green (3), stop the ray.
      iii. If the pixel input_grid[r, c] is gray (8), change output_grid[r, c] to the seed color C.
      iv. If the pixel input_grid[r, c] is non-gray and non-green, stop the ray.
      v. Continue to the next step: (r + dr, c + dc).
6. The final output grid contains the original non-gray pixels and the gray pixels colored by the rays. If multiple rays color the same gray pixel, the outcome depends on the order of processing, but the examples suggest a consistent result, implying either non-overlapping projections or a deterministic overwrite rule (e.g., based on proximity or seed color value - although the latter seems unlikely). This implementation assumes overwriting is acceptable, processed ray by ray.
"""

def transform(input_grid):
    """
    Projects colors from seed pixels outwards from adjacent green boundary pixels.

    Args:
        input_grid (np.array): The input 2D grid.

    Returns:
        np.array: The transformed 2D grid.
    """
    # Constants
    GRAY = 8
    GREEN = 3
    height, width = input_grid.shape

    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Define 8 directions for adjacency checks and ray casting
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Store unique rays to cast: set of (start_r, start_c, dr, dc, color)
    rays_to_cast = set()

    # Step 1 & 2: Identify seed pixels and find adjacent green boundaries
    for r in range(height):
        for c in range(width):
            seed_color = input_grid[r, c]
            # Check if it's a seed pixel
            if seed_color != GRAY and seed_color != GREEN:
                # Step 3: Check neighbors for green pixels
                for dr_adj, dc_adj in directions:
                    nr, nc = r + dr_adj, c + dc_adj
                    # Check bounds and if neighbor is green
                    if 0 <= nr < height and 0 <= nc < width and input_grid[nr, nc] == GREEN:
                        # Found an adjacent green boundary pixel (nr, nc)
                        # Step 4a: Determine projection direction
                        proj_dr, proj_dc = dr_adj, dc_adj # Direction is from seed to green
                        # Step 4b: Define ray starting position (first pixel beyond green)
                        start_r, start_c = nr + proj_dr, nc + proj_dc
                        # Add ray details to the set (ensures uniqueness)
                        rays_to_cast.add((start_r, start_c, proj_dr, proj_dc, seed_color))

    # Step 5 & 6: Cast all unique rays
    for start_r, start_c, dr, dc, color in rays_to_cast:
        curr_r, curr_c = start_r, start_c
        # Keep casting while within bounds
        while 0 <= curr_r < height and 0 <= curr_c < width:
            # Check the color of the pixel in the *original* grid
            pixel_in_input = input_grid[curr_r, curr_c]

            if pixel_in_input == GREEN:
                # Stop ray if it hits a green barrier
                break
            elif pixel_in_input == GRAY:
                # Color the gray pixel in the output grid
                output_grid[curr_r, curr_c] = color
            else: # Hit another non-gray, non-green color
                 # Stop the ray (as specified by examples like Ex1 where rays stop)
                 # Alternative: could continue if output[curr_r, curr_c] is gray
                 # but let's stick to stopping based on input content first.
                 break # Stop ray if it hits any non-GRAY, non-GREEN pixel in the input

            # Move to the next pixel along the ray
            curr_r += dr
            curr_c += dc

    return output_grid