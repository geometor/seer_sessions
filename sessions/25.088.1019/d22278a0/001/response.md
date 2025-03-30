```python
import numpy as np

"""
For each pixel in the output grid, determine its color based on the proximity 
to non-white 'seed' pixels in the input grid using Manhattan distance. 

1. Identify the location (row, column) and color of all non-white pixels ('seeds') in the input grid.
2. Create an output grid of the same dimensions as the input, initialized to white (0).
3. For each pixel location (target_row, target_col) in the grid:
    a. Calculate the Manhattan distance from this pixel to every seed.
    b. Find the minimum distance calculated.
    c. Identify all seeds that are at this minimum distance.
    d. If exactly one seed is closest, set the output pixel at (target_row, target_col) to the color of that seed.
    e. If multiple seeds are equidistant and closest, keep the output pixel white (0).
4. Return the resulting output grid.
"""

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Transforms the input grid based on the proximity to seed pixels using Manhattan distance.
    """
    input_np = np.array(input_grid)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np)

    # 1. Identify seed pixels (non-white)
    seeds = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] != 0:
                seeds.append(((r, c), input_np[r, c])) # Store ((row, col), color)

    # If there are no seeds, return an empty grid (or the original, depending on interpretation - returning empty based on observed outputs)
    if not seeds:
        return output_grid.tolist() # Return list of lists

    # 3. Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            target_pixel = (r, c)
            
            # a. Calculate distances to all seeds
            distances = []
            for seed_pos, seed_color in seeds:
                dist = manhattan_distance(target_pixel, seed_pos)
                distances.append({'distance': dist, 'color': seed_color})
                
            # b. Find the minimum distance
            if not distances: # Should not happen if seeds exist, but safe check
                continue 
                
            min_distance = min(d['distance'] for d in distances)
            
            # c. Identify all seeds at the minimum distance
            closest_seeds = [d for d in distances if d['distance'] == min_distance]
            
            # d. If exactly one seed is closest, assign its color
            if len(closest_seeds) == 1:
                output_grid[r, c] = closest_seeds[0]['color']
            # e. If multiple seeds are equidistant and closest, leave it white (0) - already initialized

    # 4. Return the completed output grid
    return output_grid.tolist() # Convert back to list of lists for consistency
```