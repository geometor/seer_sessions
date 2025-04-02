import numpy as np
from typing import Tuple, Set, List, Optional
import math

"""
This code solves ARC task a8c383ab.
The transformation identifies the non-background color pixels in the input grid.
It determines the parameters (center and radius) of a diamond shape based on the bounding box of these input pixels.
It then generates all pixels that would belong to a perfect diamond with these parameters.
If the set of input pixels is identical to the set of pixels in the generated theoretical diamond, the output is the perimeter (hollow diamond) of this shape.
Otherwise (if the input pixels are scattered or form an incomplete diamond), the output is the completely filled theoretical diamond.
The background color is assumed to be 0. Only one non-background color is expected per input grid.
"""

def _find_shape_pixels(grid: np.ndarray) -> Tuple[Optional[int], Set[Tuple[int, int]]]:
    """Finds the non-background color and coordinates of shape pixels."""
    # Find coordinates where the grid is not equal to the background color (0)
    non_background_indices = np.where(grid != 0)
    
    # If no non-background pixels are found, return None for color and an empty set
    if len(non_background_indices[0]) == 0:
        return None, set()

    # Extract the coordinates as a set of (row, col) tuples
    pixel_coords = set(zip(non_background_indices[0], non_background_indices[1]))
    
    # Get the color of the first non-background pixel found (assuming only one color)
    shape_color = int(grid[non_background_indices[0][0], non_background_indices[1][0]])
    
    return shape_color, pixel_coords

def _calculate_diamond_params_from_bbox(pixels: Set[Tuple[int, int]]) -> Tuple[Tuple[int, int], int]:
    """
    Calculates the center and radius of a diamond based on the bounding box of the pixels.
    Returns ((center_r, center_c), radius).
    """
    if not pixels:
        # Should not happen if called after checking for pixels, but defensive check
        return (0, 0), -1 

    # Extract row and column coordinates
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]

    # Find the min/max row and column to define the bounding box
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Calculate the center coordinates by averaging the min/max and rounding
    # Using integer division // for robustness if sum is odd
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2
    center = (center_r, center_c)

    # Calculate the radius based on the larger dimension of the bounding box
    # This defines the 'size' of the diamond related to the bbox extent
    # Using integer division // 2
    radius = max(max_r - min_r, max_c - min_c) // 2
    
    # Alternative center calculation: check if averaging produces .5
    # center_r_float = (min_r + max_r) / 2.0
    # center_c_float = (min_c + max_c) / 2.0
    # center_r = int(round(center_r_float)) # Round to nearest int
    # center_c = int(round(center_c_float)) # Round to nearest int
    # We use the integer division approach first as it seemed to work for examples.

    return center, radius

def _generate_diamond_pixels(center: Tuple[int, int], radius: int, grid_shape: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Generates all pixel coordinates within the diamond defined by center and radius."""
    diamond_pixels = set()
    center_r, center_c = center
    rows, cols = grid_shape
    
    # Iterate through potential pixels within the grid boundaries
    # No need to calculate tight bounds, just check distance for all grid cells
    # (Optimization possible by iterating only within bounding box of diamond)
    min_r_bound = max(0, center_r - radius)
    max_r_bound = min(rows, center_r + radius + 1)
    min_c_bound = max(0, center_c - radius)
    max_c_bound = min(cols, center_c + radius + 1)

    for r in range(min_r_bound, max_r_bound):
        for c in range(min_c_bound, max_c_bound):
            # Calculate Manhattan distance from the pixel to the center
            distance = abs(r - center_r) + abs(c - center_c)
            # If the distance is within the radius, add it to the set
            if distance <= radius:
                diamond_pixels.add((r, c))
                
    return diamond_pixels

def _is_perimeter(r: int, c: int, grid_shape: Tuple[int, int], diamond_pixels: Set[Tuple[int, int]]) -> bool:
    """Checks if a pixel (r, c) within the diamond is adjacent (8-way) to a non-diamond pixel or grid edge."""
    rows, cols = grid_shape
    # Iterate through all 8 neighbors and self (checking self is redundant but harmless)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self

            nr, nc = r + dr, c + dc

            # Check if the neighbor is outside the grid boundaries
            if not (0 <= nr < rows and 0 <= nc < cols):
                return True # Pixel is adjacent to the grid edge

            # Check if the neighbor is NOT part of the diamond pixel set
            if (nr, nc) not in diamond_pixels:
                return True # Pixel is adjacent to a background/non-diamond pixel

    # If none of the neighbors were outside the diamond or grid, it's an interior pixel
    return False

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on detecting a diamond shape.
    If the input perfectly matches a filled diamond derived from its bounding box,
    the output is the hollow perimeter of that diamond.
    Otherwise, the output is the filled diamond derived from the bounding box.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize the output grid with the background color (0)
    output_np = np.zeros_like(input_np)

    # 1. Find the shape's color and the coordinates of its pixels
    shape_color, input_shape_pixels = _find_shape_pixels(input_np)

    # If no shape pixels are found, return the original grid
    if shape_color is None:
        return input_grid

    # 2. Calculate the diamond parameters (center, radius) based on the bounding box
    center, radius = _calculate_diamond_params_from_bbox(input_shape_pixels)

    # If radius calculation failed (e.g., no pixels), return original grid
    if radius < 0:
         return input_grid 

    # 3. Generate the set of pixels for a theoretical perfect diamond with these parameters
    theoretical_diamond_pixels = _generate_diamond_pixels(center, radius, (rows, cols))

    # 4. Compare the actual input pixels with the theoretical diamond pixels
    is_perfect_diamond_input = (input_shape_pixels == theoretical_diamond_pixels)

    # 5. Determine the output based on whether the input was a perfect diamond
    if not is_perfect_diamond_input:
        # Mode 1: Input was scattered or incomplete. Output is the filled theoretical diamond.
        for r, c in theoretical_diamond_pixels:
             # Ensure coordinates are within grid bounds (should be, but safety check)
             if 0 <= r < rows and 0 <= c < cols:
                 output_np[r, c] = shape_color
    else:
        # Mode 2: Input was a perfect filled diamond. Output is the perimeter.
        for r, c in theoretical_diamond_pixels:
             # Check if the current pixel is on the perimeter
             if _is_perimeter(r, c, (rows, cols), theoretical_diamond_pixels):
                 # Ensure coordinates are within grid bounds
                 if 0 <= r < rows and 0 <= c < cols:
                     output_np[r, c] = shape_color

    # Convert the final NumPy array back to a list of lists and return
    return output_np.tolist()