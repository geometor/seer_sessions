"""
Transforms an input grid by performing a point reflection of specific objects 
through the center of a unique marker object, preserving both the original 
objects and their reflections.

1. Initialize the output grid with the same dimensions as the input grid, 
   filled entirely with the background color (0).
2. Identify the unique 5-pixel diagonal cross ('x' shape) reflector object 
   in the input grid, including its 5 pixel coordinates and its center 
   coordinate (r_c, c_c).
3. Copy the 5 pixels of the reflector object from their input coordinates to 
   the same coordinates in the output grid.
4. Iterate through each pixel (r, c) of the input grid.
5. Check if the pixel at (r, c) is a 'reflected object' (i.e., has a 
   non-background color and is not part of the reflector object).
6. If it is a reflected object:
   a. Copy the color of the input pixel at (r, c) to the output grid at the 
      same coordinate (r, c) (preserving the original).
   b. Calculate the reflected coordinate (r', c') using the point reflection 
      formula: r' = 2 * r_c - r and c' = 2 * c_c - c, with center (r_c, c_c).
   c. If the calculated coordinate (r', c') is within the bounds of the grid, 
      copy the color of the input pixel at (r, c) to the output grid at the 
      reflected coordinate (r', c') (adding the reflection).
7. Return the final output grid.
"""

import numpy as np
from typing import List, Tuple, Set

# Type definitions for clarity
Grid = List[List[int]]
Coord = Tuple[int, int]

def find_diagonal_reflector(grid: np.ndarray) -> Tuple[Coord | None, Set[Coord] | None]:
    """
    Scans the grid to find a 5-pixel diagonal cross ('x' shape) reflector.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple containing:
        - The center coordinate (r_c, c_c) of the reflector, or None if not found.
        - A set containing the coordinates of all 5 reflector pixels, or None if not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Potential center must be non-background
            if color == 0:
                continue

            # Define potential diagonal neighbor coordinates
            neighbors_coords = [
                (r - 1, c - 1), (r - 1, c + 1),
                (r + 1, c - 1), (r + 1, c + 1)
            ]

            # Check if all neighbors are within bounds and have the same color
            is_reflector_center = True
            reflector_pixels: Set[Coord] = {(r, c)}
            for nr, nc in neighbors_coords:
                if not (0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color):
                    is_reflector_center = False
                    break
                reflector_pixels.add((nr, nc))

            # If all checks pass, we found the reflector
            if is_reflector_center:
                # Verify size is exactly 5 
                if len(reflector_pixels) == 5:
                     return (r, c), reflector_pixels

    # If no reflector found after checking all pixels
    return None, None


def transform(input_grid: Grid) -> Grid:
    """
    Applies the point reflection transformation based on the identified reflector.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # 1. Initialize output grid with background color
    output_np = np.zeros_like(input_np)

    # 2. Find the reflector and its center
    center_coord, reflector_coords = find_diagonal_reflector(input_np)

    # If no reflector is found (handle defensively)
    if center_coord is None or reflector_coords is None:
        # Return the original input grid if no reflector is present
        # This might need adjustment based on task specification for such cases
        return input_grid 

    r_c, c_c = center_coord

    # 3. Copy the reflector pixels to the output grid
    for r_ref, c_ref in reflector_coords:
        output_np[r_ref, c_ref] = input_np[r_ref, c_ref]

    # 4. Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # 5. Check if the pixel should be reflected
            original_color = input_np[r, c]
            coord = (r, c)

            # Check if non-background and not part of the reflector
            if original_color != 0 and coord not in reflector_coords:
                
                # 6a. Copy the original pixel to the output grid
                output_np[r, c] = original_color 

                # 6b. Calculate reflected coordinates
                r_prime = 2 * r_c - r
                c_prime = 2 * c_c - c

                # 6c. Check if reflected coordinate is within bounds
                if 0 <= r_prime < rows and 0 <= c_prime < cols:
                    # 6d. Copy the original color to the reflected position in the output grid
                    output_np[r_prime, c_prime] = original_color

    # 7. Return the modified output grid converted back to list of lists
    return output_np.tolist()