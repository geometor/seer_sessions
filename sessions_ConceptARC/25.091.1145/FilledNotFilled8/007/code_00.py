import numpy as np
from typing import Tuple, Set, List, Optional

"""
Transforms an input grid based on a diamond shape derived from its non-background pixels.

The transformation identifies the single non-background color (ShapeColor) and the set of pixels with this color (InputShapePixels).
It calculates the minimum and maximum values for u = row + col and v = row - col based on InputShapePixels.
Using these bounds (min_u, max_u, min_v, max_v), it generates a theoretical set of pixels (TheoreticalDiamondPixels) within the grid that satisfy min_u <= r+c <= max_u, min_v <= r-c <= max_v, and where r+c and r-c have the same parity (which is always true if r, c are integers).

If InputShapePixels is identical to TheoreticalDiamondPixels, the input is considered a 'perfect' filled diamond. The output grid will contain only the boundary pixels of this diamond, colored with ShapeColor. A boundary pixel is one within the diamond that satisfies r+c = min_u OR r+c = max_u OR r-c = min_v OR r-c = max_v.

If InputShapePixels is not identical to TheoreticalDiamondPixels (e.g., the input pixels are scattered or form an incomplete diamond), the output grid will be the completely filled TheoreticalDiamondPixels, colored with ShapeColor.

The background color is assumed to be 0.
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

def _calculate_uv_bounds(pixels: Set[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """Calculates the min/max bounds for u=r+c and v=r-c."""
    if not pixels:
        return None # No pixels, no bounds
    # Calculate u = r+c for all pixels
    u_coords = [r + c for r, c in pixels]
    # Calculate v = r-c for all pixels
    v_coords = [r - c for r, c in pixels]
    # Return the min/max of u and v
    return min(u_coords), max(u_coords), min(v_coords), max(v_coords)

def _generate_diamond_pixels_uv(uv_bounds: Tuple[int, int, int, int], grid_shape: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Generates pixels within the diamond defined by u,v bounds."""
    min_u, max_u, min_v, max_v = uv_bounds
    rows, cols = grid_shape
    diamond_pixels = set()
    
    # Iterate through all grid pixels
    for r in range(rows):
        for c in range(cols):
            u = r + c
            v = r - c
            # Check if the pixel's u,v fall within the calculated bounds
            # Also need parity check: u and v must have the same parity
            # This is automatically true if r and c are integers:
            # u+v = 2r (even), u-v = 2c (even). So u and v must have same parity.
            if min_u <= u <= max_u and min_v <= v <= max_v:
                 # Check the parity constraint: (r+c) and (r-c) must have same parity.
                 # Simplified: check if (u - v) % 2 == 0 which is same as 2*c % 2 == 0 (always true)
                 # Or check if (u + v) % 2 == 0 which is same as 2*r % 2 == 0 (always true)
                 # The original description's parity check is slightly redundant for integer grids but conceptually correct
                 # if we consider the continuous diamond shape. For discrete grids, the bounds are sufficient.
                 # Let's stick to the bounds check for integer grids.
                 # Re-check: The parity check *is* needed if the bounds allow points where u,v have different parity.
                 # Example: min_u=1, max_u=1, min_v=0, max_v=0. Point (0,1) has u=1, v=-1 (both odd). Point (1,0) has u=1, v=1 (both odd).
                 # Point (0.5, 0.5) has u=1, v=0 (different parity) - but not an integer point.
                 # If min_u=1, max_u=2, min_v=0, max_v=1. Point (1,1) has u=2, v=0 (both even).
                 # The check ensures the 'checkerboard' pattern of the diamond grid.
                 if (u % 2) == (v % 2):
                     diamond_pixels.add((r, c))
                     
    return diamond_pixels

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the diamond fill/hollow transformation based on u,v bounds.
    """
    # Convert input to NumPy array
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize the output grid with background color 0
    output_np = np.zeros_like(input_np)

    # 1. Find the shape color and input pixel coordinates
    shape_color, input_shape_pixels = _find_shape_pixels(input_np)

    # If no shape pixels are found, return the original grid
    if shape_color is None:
        return input_grid

    # 2. Calculate the u,v bounds from the input pixels
    uv_bounds = _calculate_uv_bounds(input_shape_pixels)
    if uv_bounds is None: # Should not happen if shape_color is not None
         return input_grid 
    min_u, max_u, min_v, max_v = uv_bounds

    # 3. Generate the set of pixels for the theoretical diamond based on u,v bounds
    theoretical_diamond_pixels = _generate_diamond_pixels_uv(uv_bounds, (rows, cols))

    # 4. Compare the actual input pixels with the theoretical diamond pixels
    is_perfect_diamond_input = (input_shape_pixels == theoretical_diamond_pixels)

    # 5. Determine the output based on the comparison
    if not is_perfect_diamond_input:
        # Mode 1: Input was scattered or incomplete. Fill the theoretical diamond.
        for r, c in theoretical_diamond_pixels:
             # Check bounds just in case, though _generate ensures this
             if 0 <= r < rows and 0 <= c < cols:
                 output_np[r, c] = shape_color
    else:
        # Mode 2: Input was a perfect filled diamond. Hollow it (keep only boundary).
        for r, c in theoretical_diamond_pixels:
            u = r + c
            v = r - c
            # Check if the pixel lies on the boundary defined by min/max u/v
            if u == min_u or u == max_u or v == min_v or v == max_v:
                 # Check bounds just in case
                 if 0 <= r < rows and 0 <= c < cols:
                     output_np[r, c] = shape_color

    # Convert the final NumPy array back to a list of lists and return
    return output_np.tolist()