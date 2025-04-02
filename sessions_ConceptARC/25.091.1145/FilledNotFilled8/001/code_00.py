import numpy as np
from typing import Tuple, Set, List

"""
This code solves ARC task a8c383ab.
The transformation identifies the non-background color pixels in the input.
It calculates the minimal bounding diamond (using Manhattan distance) that encloses all these pixels.
It then determines if the input pixels perfectly match all pixels within this theoretical diamond.
If the input pixels DO NOT match the theoretical filled diamond (e.g., they are scattered points), the output is the complete, filled diamond using the identified color.
If the input pixels DO match the theoretical filled diamond, the output is the perimeter of that diamond, keeping only the pixels that are adjacent (8-way) to a background pixel or the grid edge.
"""

def _find_shape_pixels(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]]]:
    """Finds the non-background color and coordinates of shape pixels."""
    non_background_pixels = np.where(grid != 0)
    if len(non_background_pixels[0]) == 0:
        return 0, set()  # No shape found, return background color and empty set

    # Assume only one non-background color
    shape_color = int(grid[non_background_pixels[0][0], non_background_pixels[1][0]])
    
    pixel_coords = set(zip(non_background_pixels[0], non_background_pixels[1]))
    return shape_color, pixel_coords

def _manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def _calculate_diamond_params(pixels: Set[Tuple[int, int]]) -> Tuple[Tuple[float, float], int]:
    """Calculates the center and radius of the minimal bounding diamond."""
    if not pixels:
        return (0, 0), -1 # Indicate no pixels

    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]

    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Calculate center based on the bounding box midpoints
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0
    center = (center_r, center_c)
    
    # Find the maximum Manhattan distance from the *integer* pixel coordinates
    # closest to the calculated center to any pixel in the set.
    # Test the four potential integer centers around the float center.
    potential_centers = [
        (int(np.floor(center_r)), int(np.floor(center_c))),
        (int(np.floor(center_r)), int(np.ceil(center_c))),
        (int(np.ceil(center_r)), int(np.floor(center_c))),
        (int(np.ceil(center_r)), int(np.ceil(center_c))),
    ]

    best_center = None
    min_max_dist = float('inf')

    # Refined approach: Find the tightest diamond.
    # The center must be the average of the extrema in row+col and row-col coordinates.
    # Let u = r + c, v = r - c
    u_coords = [r + c for r, c in pixels]
    v_coords = [r - c for r, c in pixels]
    min_u, max_u = min(u_coords), max(u_coords)
    min_v, max_v = min(v_coords), max(v_coords)
    
    # Center calculation from u,v extrema:
    # center_r + center_c = (min_u + max_u) / 2
    # center_r - center_c = (min_v + max_v) / 2
    # Adding: 2 * center_r = (min_u + max_u + min_v + max_v) / 2
    # Subtracting: 2 * center_c = (min_u + max_u - min_v - max_v) / 2
    center_r = (min_u + max_u + min_v + max_v) / 4.0
    center_c = (min_u + max_u - min_v - max_v) / 4.0
    center = (center_r, center_c)
    
    # The radius k is related to the span of u and v
    # k = max(|r - center_r| + |c - center_c|)
    # This can also be expressed as:
    radius = (max(max_u - min_u, max_v - min_v)) / 2.0

    # Find the max distance from the *closest integer coordinate* center
    # Need to handle float centers and radii carefully. Check integer grid points.
    int_center_r = round(center_r)
    int_center_c = round(center_c)
    int_center = (int_center_r, int_center_c)
    
    max_dist = 0
    for pixel in pixels:
         dist = _manhattan_distance(pixel, int_center)
         max_dist = max(max_dist, dist)

    # It's possible the true center is slightly offset, affecting radius.
    # A more robust radius calculation is needed if center is float.
    # Let's stick to the max distance from the rounded integer center for now.
    radius_k = max_dist 

    return int_center, radius_k


def _generate_diamond_pixels(center: Tuple[int, int], radius: int, grid_shape: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Generates all pixel coordinates within the diamond defined by center and radius."""
    diamond_pixels = set()
    center_r, center_c = center
    rows, cols = grid_shape
    
    # Iterate through a bounding box around the diamond
    min_r_bound = max(0, center_r - radius)
    max_r_bound = min(rows, center_r + radius + 1)
    min_c_bound = max(0, center_c - radius)
    max_c_bound = min(cols, center_c + radius + 1)

    for r in range(min_r_bound, max_r_bound):
        for c in range(min_c_bound, max_c_bound):
            if _manhattan_distance((r, c), center) <= radius:
                diamond_pixels.add((r, c))
    return diamond_pixels

def _is_perimeter(r: int, c: int, grid_shape: Tuple[int, int], diamond_pixels: Set[Tuple[int, int]]) -> bool:
    """Checks if a pixel (r, c) within the diamond is adjacent to a non-diamond pixel."""
    rows, cols = grid_shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self
            
            nr, nc = r + dr, c + dc

            # Check if neighbor is outside grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                return True # Adjacent to edge
            
            # Check if neighbor is not part of the diamond
            if (nr, nc) not in diamond_pixels:
                return True # Adjacent to background or other shape
                
    return False # All neighbors are within the diamond

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the diamond fill/hollow logic.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_np = np.zeros_like(input_np) # Initialize with background color 0

    # 1. Identify Shape Pixels
    shape_color, input_shape_pixels = _find_shape_pixels(input_np)

    if not input_shape_pixels:
        return input_grid # Return original if no shape found

    # 2. Determine Bounding Diamond Parameters
    center, radius = _calculate_diamond_params(input_shape_pixels)
    
    # Check if valid parameters were found
    if radius < 0:
         return input_grid # Should not happen if pixels were found, but safety check

    # 3. Generate Theoretical Diamond Pixels
    theoretical_diamond_pixels = _generate_diamond_pixels(center, radius, (rows, cols))

    # 4. Compare Input Pixels with Theoretical Diamond
    is_filled_diamond_input = (input_shape_pixels == theoretical_diamond_pixels)

    # 5. Apply Transformation based on comparison
    if not is_filled_diamond_input:
        # Mode 1: Fill the diamond (Input was scattered/incomplete)
        for r, c in theoretical_diamond_pixels:
             if 0 <= r < rows and 0 <= c < cols:
                 output_np[r, c] = shape_color
    else:
        # Mode 2: Hollow the diamond (Input was already a filled diamond)
        for r, c in theoretical_diamond_pixels:
             # Keep pixel if it's on the perimeter
             if _is_perimeter(r, c, (rows, cols), theoretical_diamond_pixels):
                 if 0 <= r < rows and 0 <= c < cols: # Redundant check, but safe
                     output_np[r, c] = shape_color

    return output_np.tolist()