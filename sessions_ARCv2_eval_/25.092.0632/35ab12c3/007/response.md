```python
import numpy as np

"""
Transformation Rule Description:

1.  Identify non-white pixels (colors 1-9) in the input grid; these are "seeds".
2.  Determine the "effective fill color" for each seed: 
    - If a seed's color is magenta (6), its effective fill color is orange (7).
    - Otherwise, the effective fill color is the seed's own color.
3.  Initialize an output grid of the same size, filled with white (0).
4.  For each pixel location (r, c) in the grid:
    a. Check if the location (r, c) corresponds to an original seed location from the input grid.
    b. If it is a seed location, set the output pixel at (r, c) to the seed's *original* color.
    c. If it is not a seed location (i.e., it was white in the input):
        i. Calculate the Manhattan distance from (r, c) to every seed pixel.
        ii. Find the minimum Manhattan distance among all seeds.
        iii. Identify all seeds that are located at this minimum distance.
        iv. Collect the *effective fill colors* of these closest seeds.
        v. If there is exactly one unique effective fill color among the closest seeds, set the output pixel at (r, c) to this color.
        vi. Otherwise (if there are multiple different effective fill colors among the closest seeds, or if there are no seeds), set the output pixel at (r, c) to white (0).
5. Return the completed output grid.
"""

def calculate_manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_seeds(input_grid):
    """Identifies seeds and their properties from the input grid."""
    seeds = []
    height, width = input_grid.shape
    for r in range(height):
        for c in range(width):
            original_color = input_grid[r, c]
            if original_color != 0:
                effective_fill_color = 7 if original_color == 6 else original_color
                seeds.append({
                    'pos': (r, c),
                    'original_color': original_color,
                    'effective_fill_color': effective_fill_color
                })
    return seeds

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on proximity to seed pixels using Manhattan distance.
    Conflicts between equidistant seeds with different effective fill colors result in white pixels.
    Original seed locations retain their original color.
    """
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify seeds and their properties
    seeds = find_seeds(input_grid)

    # Handle case with no seeds
    if not seeds:
        return output_grid # Or return input_grid? Based on rule, output should be all white if no seeds.

    # Store original seed positions for quick lookup
    original_seed_locations = {seed['pos']: seed['original_color'] for seed in seeds}

    # 2. Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            current_pos = (r, c)

            # 3a. Check if the current pixel is an original seed location
            if current_pos in original_seed_locations:
                # 3b. Assign original color if it's a seed
                output_grid[r, c] = original_seed_locations[current_pos]
                continue # Move to the next pixel

            # 3c. If it's not a seed (was white in input)
            min_dist = float('inf')
            closest_seeds_fill_colors = []

            # 3c.i. Calculate distance to all seeds
            for seed in seeds:
                dist = calculate_manhattan_distance(current_pos, seed['pos'])

                # 3c.ii & iii. Find minimum distance and track closest seeds
                if dist < min_dist:
                    min_dist = dist
                    closest_seeds_fill_colors = [seed['effective_fill_color']]
                elif dist == min_dist:
                    closest_seeds_fill_colors.append(seed['effective_fill_color'])

            # 3c.iv & v & vi. Determine output color based on closest seeds' effective fill colors
            unique_fill_colors = set(closest_seeds_fill_colors)
            if len(unique_fill_colors) == 1:
                 # Assign the unique effective fill color
                output_grid[r, c] = list(unique_fill_colors)[0]
            else:
                 # Leave as white (0) if no seeds are close (inf dist) or if there's a conflict
                 output_grid[r, c] = 0

    return output_grid
```