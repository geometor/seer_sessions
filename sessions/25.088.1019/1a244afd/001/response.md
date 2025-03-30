```python
import numpy as np
import math

"""
Transforms the input grid according to the following rules:
1. Identify all Magenta (6) and Blue (1) pixels.
2. For each Magenta pixel (M), find the Blue pixel (B) closest to it using Manhattan distance.
3. Calculate the vector V from M to B (V = B - M).
4. Determine a new target coordinate (O) relative to B based on a rotation of V:
    - If V is horizontal (change in row is 0), rotate V 90 degrees counter-clockwise to get V'. O = B + V'.
    - If V is vertical (change in column is 0), rotate V 90 degrees clockwise to get V'. O = B + V'.
5. Create the output grid by copying the input grid.
6. In the output grid, change the color of the original Magenta pixel M to Azure (8).
7. If the calculated target coordinate O is within the grid boundaries, change the color of the pixel at O in the output grid to Orange (7).
"""

def find_pixels(grid, color):
    """Finds all pixels of a specific color in the grid."""
    points = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                points.append((r, c))
    return points

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (r1, c1) and (r2, c2)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Find coordinates of Magenta (6) and Blue (1) pixels
    magenta_pixels = find_pixels(grid, 6)
    blue_pixels = find_pixels(grid, 1)

    # If there are no magenta or no blue pixels, no transformation happens beyond removing magenta
    if not magenta_pixels or not blue_pixels:
        for mr, mc in magenta_pixels:
             # Change original magenta location to background color (8) in output
            output_grid[mr, mc] = 8
        return output_grid.tolist()


    orange_coords_to_place = []

    # Process each Magenta pixel
    for mr, mc in magenta_pixels:
        m_pos = (mr, mc)

        # Find the closest Blue pixel
        min_dist = float('inf')
        closest_blue = None
        for br, bc in blue_pixels:
            b_pos = (br, bc)
            dist = manhattan_distance(m_pos, b_pos)
            if dist < min_dist:
                min_dist = dist
                closest_blue = b_pos

        # If a closest blue was found (should always happen if blue_pixels is not empty)
        if closest_blue:
            br_c, bc_c = closest_blue

            # Calculate the vector V from M to B_closest
            dr = br_c - mr
            dc = bc_c - mc

            # Determine the target coordinate O based on V's rotation
            or_target, oc_target = -1, -1 # Initialize with invalid coordinates

            # Check if vector is purely horizontal
            if dr == 0 and dc != 0:
                # Rotate 90 degrees counter-clockwise: V' = (0, dc)
                # O = B + V' = (br_c + 0, bc_c + dc)
                or_target, oc_target = br_c, bc_c + dc
            # Check if vector is purely vertical
            elif dc == 0 and dr != 0:
                # Rotate 90 degrees clockwise: V' = (dr, 0)
                # O = B + V' = (br_c + dr, bc_c + 0)
                or_target, oc_target = br_c + dr, bc_c

            # Check if the target Orange coordinate is within grid bounds
            if 0 <= or_target < height and 0 <= oc_target < width:
                 orange_coords_to_place.append((or_target, oc_target))

        # Change original magenta location to background color (8) in output
        # Do this regardless of whether a valid orange target was found
        output_grid[mr, mc] = 8


    # Place the Orange (7) pixels at the calculated valid coordinates
    for or_coord, oc_coord in orange_coords_to_place:
        output_grid[or_coord, oc_coord] = 7

    # Convert the result back to a list of lists
    return output_grid.tolist()
```