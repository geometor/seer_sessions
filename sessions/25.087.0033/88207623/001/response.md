```python
import numpy as np
import math

"""
The transformation rule identifies vertical red lines (axes) and adjacent yellow shapes in the input grid. 
For each red axis and its associated yellow shape, it finds the single, non-background, non-red, non-yellow pixel (source color pixel) that is closest to the combined axis/shape structure. 
It then reflects the yellow shape across the red axis. The reflected pixels are colored with the color of the closest source pixel. 
This reflection only changes pixels that were originally white (background) in the input grid. 
All original non-white pixels are preserved in the output.
"""

def find_pixels_with_color(grid, color):
    """Finds all pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (r1, c1) and (r2, c2)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_closest_source_pixel(target_pixels, source_pixels):
    """
    Finds the source pixel closest to any pixel in the target set.
    
    Args:
        target_pixels: List of coordinates [(r, c), ...] representing the target shape/axis.
        source_pixels: List of source pixel info [(r, c, color), ...].

    Returns:
        The color of the closest source pixel, or None if no source pixels are found.
    """
    if not source_pixels or not target_pixels:
        return None

    min_dist = float('inf')
    closest_source_color = None

    for sr, sc, scolor in source_pixels:
        current_min_dist_for_source = float('inf')
        for tr, tc in target_pixels:
            dist = manhattan_distance((sr, sc), (tr, tc))
            current_min_dist_for_source = min(current_min_dist_for_source, dist)
        
        if current_min_dist_for_source < min_dist:
            min_dist = current_min_dist_for_source
            closest_source_color = scolor
        # Note: Implicitly handles ties by taking the first one found with the min distance.

    return closest_source_color


def transform(input_grid):
    """
    Applies the reflection transformation based on red axes, yellow shapes, and source color pixels.
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

    # --- Process Red Axes ---
    
    visited_red = set() # To avoid processing parts of the same axis multiple times
    
    for r_start, c_axis in red_pixels:
        if (r_start, c_axis) in visited_red:
            continue

        # 1. Find the full vertical red axis starting from this pixel
        current_axis_pixels = []
        r = r_start
        while r < height and input_grid[r, c_axis] == 2:
            if (r, c_axis) in visited_red: # Check if part of an already processed axis
                 # If we hit a visited part, stop building this segment *but* consider it part of the current axis for finding yellow/source
                 # This handles cases where axes might be detected starting from the middle
                 r_check = r
                 while r_check < height and input_grid[r_check, c_axis] == 2:
                     current_axis_pixels.append((r_check, c_axis))
                     visited_red.add((r_check, c_axis))
                     r_check += 1
                 break # Stop extending downwards from the initial start
            current_axis_pixels.append((r, c_axis))
            visited_red.add((r, c_axis))
            r += 1
            
        # Also check upwards from start just in case we didn't start at the top
        r = r_start - 1
        while r >= 0 and input_grid[r, c_axis] == 2:
             if (r, c_axis) in visited_red: # Already processed this upper part
                 break
             # Prepend to keep order if needed, though order doesn't matter for coord list
             current_axis_pixels.insert(0, (r, c_axis)) 
             visited_red.add((r, c_axis))
             r -= 1


        if not current_axis_pixels: # Should not happen if we started with a red pixel, but safety check
            continue

        # 2. Find adjacent yellow pixels for this specific axis
        adjacent_yellow_pixels = []
        shape_side = None # 'left' or 'right'
        
        for r_ax, c_ax in current_axis_pixels:
            # Check left neighbor
            if c_ax > 0 and input_grid[r_ax, c_ax - 1] == 4:
                adjacent_yellow_pixels.append((r_ax, c_ax - 1))
                if shape_side is None: shape_side = 'left'
                elif shape_side == 'right': shape_side = 'both' # Problematic case, maybe indicates separate structures using same axis part? Let's assume simple cases first.
                
            # Check right neighbor
            if c_ax < width - 1 and input_grid[r_ax, c_ax + 1] == 4:
                adjacent_yellow_pixels.append((r_ax, c_ax + 1))
                if shape_side is None: shape_side = 'right'
                elif shape_side == 'left': shape_side = 'both'

        # Remove duplicates if a yellow pixel is adjacent to multiple axis pixels
        adjacent_yellow_pixels = list(set(adjacent_yellow_pixels))

        if not adjacent_yellow_pixels or shape_side == 'both':
             # If no yellow pixels found adjacent to this axis segment, or yellow on both sides (ambiguous/not expected by examples), skip.
            continue

        # 3. Find the closest source color for this axis + shape structure
        structure_pixels = current_axis_pixels + adjacent_yellow_pixels
        reflection_color = find_closest_source_pixel(structure_pixels, source_pixels)

        if reflection_color is None: # No source color found
            continue

        # 4. Perform reflection
        for r_yellow, c_yellow in adjacent_yellow_pixels:
            # Find the specific red pixel it's adjacent to (must exist by definition)
            c_axis = c_yellow + 1 if shape_side == 'left' else c_yellow - 1
            
            # Calculate reflected coordinates
            if shape_side == 'left':
                c_reflected = c_axis + (c_axis - c_yellow)
            else: # shape_side == 'right'
                c_reflected = c_axis - (c_yellow - c_axis)
            r_reflected = r_yellow # Row stays the same

            # Check bounds and if the original target pixel is background (white)
            if 0 <= r_reflected < height and 0 <= c_reflected < width:
                if input_grid[r_reflected, c_reflected] == 0:
                    output_grid[r_reflected, c_reflected] = reflection_color

    return output_grid
```