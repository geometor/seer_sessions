
Previous Code:
```python
import numpy as np
from collections import deque

"""
The transformation rule identifies vertical red lines (axes) and adjacent connected yellow shapes in the input grid.
For each red axis and an associated adjacent yellow shape:
1.  The 'structure' is defined as the union of all pixels in the axis and the connected yellow shape.
2.  The single 'source' pixel (non-background, non-red, non-yellow) closest (Manhattan distance) to any pixel in the 'structure' is found. Its color is the 'reflection_color'.
3.  The yellow shape is reflected across the vertical red axis.
4.  Pixels in the output grid corresponding to the reflected shape's positions are colored with the 'reflection_color', but only if those pixels were originally background (white, color 0) in the input grid.
5.  All original non-white pixels from the input grid are preserved in the output grid.
"""

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
    Handles 4-connectivity (up, down, left, right). Diagonal is not adjacency for components.
    """
    height, width = grid.shape
    component_pixels = set()
    q = deque([start_coord])
    visited_component = {start_coord} # Keep track of visited during this specific BFS

    while q:
        r, c = q.popleft()
        if grid[r, c] == target_color:
            component_pixels.add((r, c))
            # Check neighbors (4-connectivity)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width and \
                   grid[nr, nc] == target_color and (nr, nc) not in visited_component:
                    visited_component.add((nr, nc))
                    q.append((nr, nc))
                    
    return list(component_pixels)


def find_closest_source_pixel(target_pixels, source_pixels):
    """
    Finds the source pixel closest to any pixel in the target set (structure).

    Args:
        target_pixels: List of coordinates [(r, c), ...] representing the target structure (axis + shape).
        source_pixels: List of source pixel info [(r, c, color), ...].

    Returns:
        The color of the closest source pixel, or None if no source pixels are found.
    """
    if not source_pixels or not target_pixels:
        return None

    min_dist = float('inf')
    closest_source_color = None

    # Pre-calculate distances from each source to the structure
    for sr, sc, scolor in source_pixels:
        current_min_dist_for_source = float('inf')
        for tr, tc in target_pixels:
            dist = manhattan_distance((sr, sc), (tr, tc))
            current_min_dist_for_source = min(current_min_dist_for_source, dist)

        # Check if this source pixel is closer than the best found so far
        if current_min_dist_for_source < min_dist:
            min_dist = current_min_dist_for_source
            closest_source_color = scolor
        # Tie-breaking: first one found with the minimum distance wins (implicit)

    return closest_source_color


def transform(input_grid):
    """
    Applies the reflection transformation based on red axes, connected yellow shapes, and source color pixels.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- Identify components ---
    
    # Find all red pixels (potential axis parts)
    red_pixels = find_pixels_with_color(input_grid, 2)

    # Find all source color pixels (non-0, non-2, non-4)
    source_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            if color not in [0, 2, 4]:
                source_pixels.append((r, c, color))

    # --- Process Red Axes and Adjacent Shapes ---

    visited_red = set() # To avoid processing parts of the same axis multiple times
    processed_yellow_pixels = set() # To avoid processing the same shape multiple times if it touches axis at >1 point

    for r_start, c_axis in red_pixels:
        if (r_start, c_axis) in visited_red:
            continue

        # 1. Find the full vertical red axis starting from this potential point
        current_axis_pixels = []
        
        # Explore downwards
        r = r_start
        temp_down = []
        while r < height and input_grid[r, c_axis] == 2:
            if (r, c_axis) in visited_red:
                break # Stop if we hit an already processed part downwards
            temp_down.append((r, c_axis))
            r += 1
        
        # Explore upwards
        r = r_start - 1
        temp_up = []
        while r >= 0 and input_grid[r, c_axis] == 2:
            if (r, c_axis) in visited_red:
                 break # Stop if we hit an already processed part upwards
            temp_up.append((r, c_axis))
            r -= 1
            
        current_axis_pixels = temp_up[::-1] + temp_down # Combine ensuring order if needed (though set ops used later)
        
        # Mark all found axis pixels as visited
        for r_ax, c_ax in current_axis_pixels:
             visited_red.add((r_ax, c_ax))

        if not current_axis_pixels:
            continue # Should not happen if r_start, c_axis was red, but safety check

        # 2. Find *seed* yellow pixels adjacent to this axis
        adjacent_yellow_seeds = []
        shape_sides = {} # Store side ('left'/'right') for each seed: {(r,c): side}

        for r_ax, c_ax in current_axis_pixels:
            # Check left neighbor
            if c_ax > 0 and input_grid[r_ax, c_ax - 1] == 4:
                seed = (r_ax, c_ax - 1)
                if seed not in processed_yellow_pixels:
                    adjacent_yellow_seeds.append(seed)
                    shape_sides[seed] = 'left'
                    
            # Check right neighbor
            if c_ax < width - 1 and input_grid[r_ax, c_ax + 1] == 4:
                seed = (r_ax, c_ax + 1)
                if seed not in processed_yellow_pixels:
                     adjacent_yellow_seeds.append(seed)
                     shape_sides[seed] = 'right'

        # 3. Process each unique adjacent connected shape
        for seed_coord in adjacent_yellow_seeds:
            if seed_coord in processed_yellow_pixels:
                continue # Already processed this shape

            # Find the full connected yellow shape
            current_shape_pixels = find_connected_component(input_grid, seed_coord, 4)
            
            # Mark all pixels of this shape as processed to avoid redundant work
            for yp in current_shape_pixels:
                processed_yellow_pixels.add(yp)

            if not current_shape_pixels: # Should not happen if seed was yellow
                continue

            # Determine which side this shape is on (based on the seed pixel)
            shape_side = shape_sides[seed_coord]

            # 4. Find the closest source color for this axis + shape structure
            structure_pixels = current_axis_pixels + current_shape_pixels
            reflection_color = find_closest_source_pixel(structure_pixels, source_pixels)

            if reflection_color is None: # No source color found
                continue

            # 5. Perform reflection
            for r_yellow, c_yellow in current_shape_pixels:
                # Calculate reflected coordinates
                # c_axis is constant for the vertical axis
                if shape_side == 'left':
                    c_reflected = c_axis + (c_axis - c_yellow)
                else: # shape_side == 'right'
                    c_reflected = c_axis - (c_yellow - c_axis)
                r_reflected = r_yellow # Row stays the same

                # Check bounds and if the original target pixel is background (white)
                if 0 <= r_reflected < height and 0 <= c_reflected < width:
                    # IMPORTANT: Check original input grid for background color
                    if input_grid[r_reflected, c_reflected] == 0:
                        output_grid[r_reflected, c_reflected] = reflection_color

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 2 0 4 4 0 4 0 0 0 0
0 0 0 0 0 0 2 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 2 4 4 0 0 0 0 0 0 0
0 0 0 0 5 0 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 0 0 0 0 0 0 0 0 0 0
4 4 4 0 4 2 0 0 0 7 0 0 0 0 0 0
0 4 4 4 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 2 0 0 0 4 0 0 0 0 0
0 5 0 5 5 0 2 0 4 4 0 4 0 0 0 0
0 0 5 5 5 5 2 4 4 4 4 0 0 0 0 0
0 0 0 0 5 5 2 4 4 0 0 0 0 0 0 0
0 0 0 5 5 5 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 5 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 7 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 7 7 7 0 0 0 0 0 0 0
4 4 4 0 4 2 7 0 7 7 7 0 0 0 0 0
0 4 4 4 0 2 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 5 5 0 2 0 4 4 0 4 0 0 0 0
0 0 5 5 5 5 2 4 4 4 4 0 0 0 0 0
0 0 0 0 5 5 2 4 4 0 0 0 0 0 0 0
0 0 0 5 5 5 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 5 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 7 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 7 7 7 0 0 0 0 0 0 0
4 4 4 0 4 2 7 0 7 7 7 0 0 0 0 0
0 4 4 4 0 2 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.5625

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 8 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 0 4 4 2 8 8 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 3 0 3 3
0 0 0 0 0 0 0 0 4 4 0 2 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 0 4 4 2 8 8 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 3 0 0 0
0 0 0 0 0 0 0 0 4 4 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.5714285714285836
