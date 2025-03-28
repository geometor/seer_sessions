"""
Identify the gray object (color 5) and all other non-white scattered pixels (colors 1-4, 6-9).
For each scattered pixel, calculate its minimum Manhattan distance to any pixel of the gray object.
Find the overall minimum distance among all scattered pixels.
Identify all scattered pixels that are at this minimum distance.
From these closest pixels, select the one with the highest numerical color value.
Create an output grid of the same size, initially all white (0).
Copy the shape and position of the original gray object onto the output grid, but use the selected color.
"""

import numpy as np
from typing import List, Tuple

Grid = List[List[int]]

def find_pixels_by_color(grid: np.ndarray, colors: List[int]) -> List[Tuple[int, int, int]]:
    """Finds coordinates and colors of pixels matching specified colors."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in colors:
                pixels.append((r, c, grid[r, c]))
    return pixels

def find_object_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds coordinates of pixels belonging to an object of a specific color."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                pixels.append((r, c))
    return pixels

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid: Grid) -> Grid:
    """
    Transforms the input grid by finding the gray object, identifying the closest
    non-gray, non-white pixel (breaking ties by highest color value), and
    coloring the gray object's shape with that pixel's color in the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize output grid with white (0)

    # 1. Identify the target object (gray pixels)
    target_object_pixels = find_object_pixels(input_np, 5)
    if not target_object_pixels:
        # No gray object found, return the empty grid
        return output_grid.tolist()

    # 2. Identify color source pixels (non-white, non-gray)
    source_colors = [c for c in range(1, 10) if c != 5]
    color_source_pixels = find_pixels_by_color(input_np, source_colors)
    if not color_source_pixels:
        # No source pixels found, return the empty grid
        return output_grid.tolist()

    # 3. Calculate minimum distance for each source pixel to the target object
    source_distances = []
    for sr, sc, scolor in color_source_pixels:
        min_dist_to_target = float('inf')
        for gr, gc in target_object_pixels:
            dist = manhattan_distance((sr, sc), (gr, gc))
            min_dist_to_target = min(min_dist_to_target, dist)
        source_distances.append({'coords': (sr, sc), 'color': scolor, 'min_dist': min_dist_to_target})

    # 4. Find the overall minimum distance
    if not source_distances: # Should not happen if color_source_pixels is not empty, but check anyway
         return output_grid.tolist()
    overall_min_distance = min(d['min_dist'] for d in source_distances)

    # 5. Filter source pixels having the overall minimum distance
    closest_pixels = [d for d in source_distances if d['min_dist'] == overall_min_distance]

    # 6. Select the replacement color (tie-breaking by highest color value)
    if not closest_pixels: # Should not happen
        return output_grid.tolist()
    replacement_color = max(p['color'] for p in closest_pixels)

    # 7. Apply the transformation: color the target shape with the replacement color
    for r, c in target_object_pixels:
        output_grid[r, c] = replacement_color

    return output_grid.tolist()