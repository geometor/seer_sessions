```python
import numpy as np
from collections import deque

"""
The transformation rule identifies vertical red lines (axes) and adjacent connected yellow shapes in the input grid. Yellow shapes are identified using 8-way connectivity (including diagonals).
For each red axis and an associated adjacent yellow shape:
1.  The 'structure' is defined as the union of all pixels in the axis and the connected yellow shape.
2.  The single 'source' pixel (non-background, non-red, non-yellow) closest (Manhattan distance) to any pixel in the 'structure' is found. Its color is the 'reflection_color'.
3.  The yellow shape is reflected across the vertical red axis.
4.  Pixels in the output grid corresponding to the reflected shape's positions are colored with the 'reflection_color', but only if those pixels were originally background (white, color 0) in the input grid.
5.  All original non-white pixels from the input grid are preserved in the output grid.
"""

# Helper functions

def find_pixels_with_color(grid, color):
    """Finds all pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (r1, c1) and (r2, c2)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_connected_component(grid, start_coord, target_color):
    """
    Finds all connected pixels of target_color starting from start_coord using BFS.
    Uses 8-connectivity (up, down, left, right, and diagonals).
    """
    height, width = grid.shape
    component_pixels = set()
    q = deque([start_coord])
    visited_component = {start_coord} # Keep track of visited during this specific BFS

    while q:
        r, c = q.popleft()
        # Ensure the starting pixel itself matches the target color
        if grid[r, c] == target_color:
            component_pixels.add((r, c))
            # Check neighbors (8-connectivity)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue # Skip self
                    nr, nc = r + dr, c + dc
                    # Check bounds, target color, and if not visited
                    if 0 <= nr < height and 0 <= nc < width and \
                       grid[nr, nc] == target_color and (nr, nc) not in visited_component:
                        visited_component.add((nr, nc))
                        q.append((nr, nc))
                        
    # Return list for consistency with previous usage, though set might be fine
    return list(component_pixels) 


def find_closest_source_pixel(target_pixels, source_pixels):
    """
    Finds the source pixel closest to any pixel in the target set (structure).

    Args:
        target_pixels: List of coordinates [(r, c), ...] representing the target structure (axis + shape).
        source_pixels: List of source pixel info [(r, c, color), ...].

    Returns:
        The color of the closest source pixel, or None if no source pixels are found or target_pixels is empty.
    """
    if not source_pixels or not target_pixels:
        return None

    min_dist = float('inf')
    closest_source_color = None

    # Iterate through each source pixel
    for sr, sc, scolor in source_pixels:
        current_min_dist_for_source = float('inf')
        # Find the minimum distance from this source to any pixel in the target structure
        for tr, tc in target_pixels:
            dist = manhattan_distance((sr, sc), (tr, tc))
            current_min_dist_for_source = min(current_min_dist_for_source, dist)
        
        # Update the overall minimum distance and corresponding color if this source is closer
        # Implicit tie-breaking: the first source encountered with the minimum distance wins.
        if current_min_dist_for_source < min_dist:
            min_dist = current_min_dist_for_source
            closest_source_color = scolor

    return closest_source_color


def transform(input_grid):
    """
    Applies the reflection transformation based on red axes, connected yellow shapes (8-way), and source color pixels.
    """
    # 1. Initialization: Create output grid by copying input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify Components
    # Find all red pixels (potential axis parts)
    red_pixels = find_pixels_with_color(input_grid, 2) # Red color is 2

    # Find all source color pixels (non-0, non-2, non-4)
    source_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            if color not in [0, 2, 4]: # 0=white, 2=red, 4=yellow
                source_pixels.append((r, c, color))

    # 3. Process Reflections
    visited_red_axis_pixels = set() # To avoid processing parts of the same axis multiple times
    processed_yellow_pixels = set() # To avoid processing the same shape multiple times

    # Iterate through potential starting points of red axes
    for r_start, c_axis in red_pixels:
        if (r_start, c_axis) in visited_red_axis_pixels:
            continue

        # 3a. Find the full vertical red axis containing (r_start, c_axis)
        current_axis_pixels = []
        q = deque([(r_start, c_axis)])
        visited_for_this_axis = set([(r_start, c_axis)])

        while q:
             r, c = q.popleft()
             # Check if pixel is red and within the same column
             if input_grid[r, c] == 2 and c == c_axis:
                 current_axis_pixels.append((r,c))
                 visited_red_axis_pixels.add((r, c)) # Mark globally visited

                 # Explore vertically (up and down)
                 for dr in [-1, 1]:
                     nr = r + dr
                     # Check bounds and if not visited for this axis search
                     if 0 <= nr < height and (nr, c) not in visited_for_this_axis:
                         # Check if the neighbor is also red
                         if input_grid[nr, c] == 2:
                              visited_for_this_axis.add((nr, c))
                              q.append((nr, c))

        if not current_axis_pixels:
            continue # Should not happen if starting pixel was red, but safety check

        # Sort axis pixels for clarity if needed (optional)
        # current_axis_pixels.sort() 
        
        # 3b. Find yellow seed pixels adjacent (cardinally) to this axis
        adjacent_yellow_seeds = []
        shape_sides = {} # Store side ('left'/'right') for each seed: {(r,c): side}

        for r_ax, c_ax in current_axis_pixels:
            # Check left neighbor (c_ax - 1)
            if c_ax > 0:
                seed_coord = (r_ax, c_ax - 1)
                if input_grid[r_ax, c_ax - 1] == 4 and seed_coord not in processed_yellow_pixels:
                    adjacent_yellow_seeds.append(seed_coord)
                    shape_sides[seed_coord] = 'left'
                    
            # Check right neighbor (c_ax + 1)
            if c_ax < width - 1:
                 seed_coord = (r_ax, c_ax + 1)
                 if input_grid[r_ax, c_ax + 1] == 4 and seed_coord not in processed_yellow_pixels:
                     adjacent_yellow_seeds.append(seed_coord)
                     shape_sides[seed_coord] = 'right'

        # 3c. Process each unique adjacent connected shape found from seeds
        for seed_coord in adjacent_yellow_seeds:
            if seed_coord in processed_yellow_pixels:
                continue # Already processed this shape via another seed or axis part

            # 3c.i. Find Full Shape (using 8-connectivity)
            current_shape_pixels = find_connected_component(input_grid, seed_coord, 4) # Yellow color is 4
            
            if not current_shape_pixels: # Should not happen if seed was yellow
                continue

            # Mark all pixels of this shape as globally processed
            for yp in current_shape_pixels:
                processed_yellow_pixels.add(yp)

            # Determine which side this shape is predominantly on (use the seed's side)
            # This assumes a shape doesn't cross the axis, which seems true in examples
            shape_side = shape_sides[seed_coord] 

            # 3c.ii. Define Structure
            structure_pixels = current_axis_pixels + current_shape_pixels

            # 3c.iii. Find Closest Source Color
            reflection_color = find_closest_source_pixel(structure_pixels, source_pixels)

            if reflection_color is None: # No source color found or no source pixels exist
                continue

            # 3c.iv. Apply Reflection
            for r_yellow, c_yellow in current_shape_pixels:
                # Calculate reflected coordinates
                if shape_side == 'left':
                    # Shape is left of axis, reflect to the right
                    # distance = c_axis - c_yellow
                    # c_reflected = c_axis + distance
                    c_reflected = c_axis + (c_axis - c_yellow) 
                else: # shape_side == 'right'
                    # Shape is right of axis, reflect to the left
                    # distance = c_yellow - c_axis
                    # c_reflected = c_axis - distance
                    c_reflected = c_axis - (c_yellow - c_axis)
                
                r_reflected = r_yellow # Row stays the same for vertical reflection

                # Check bounds and if the original target pixel is background (white)
                if 0 <= r_reflected < height and 0 <= c_reflected < width:
                    # IMPORTANT: Check original input grid for background color
                    if input_grid[r_reflected, c_reflected] == 0: # White color is 0
                        output_grid[r_reflected, c_reflected] = reflection_color

    # 4. Return Output
    return output_grid
```