```python
import numpy as np
from typing import List, Tuple

"""
The transformation identifies non-white (0) and non-gray (5) pixels in the input grid. 
For each such pixel, it finds the closest gray (5) pixel (anchor) using Manhattan distance. 
If the pixel is within the 3x3 neighborhood (including diagonals) centered on its closest anchor, 
it is mapped to the corresponding relative position in a 3x3 output grid. 
The center of the output grid (1, 1) is always set to gray (5) at the end.
"""

def _manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on proximity to gray anchor points.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid (3x3) with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find coordinates of all gray anchor pixels (value 5)
    anchor_points = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 5:
                anchor_points.append((r, c))

    # Handle the case where there are no anchor points (though unlikely based on examples)
    if not anchor_points:
        # Return an empty or default grid, perhaps? For now, return the initial white grid.
        # Setting the center to gray as per the rule, even if no mapping occurs.
        output_grid[1, 1] = 5 
        return output_grid.tolist()

    # Iterate through each pixel in the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]

            # Process only non-white (0) and non-gray (5) pixels
            if pixel_color != 0 and pixel_color != 5:
                current_pos = (r, c)
                min_dist = float('inf')
                closest_anchor = None

                # Find the closest anchor point
                for anchor_pos in anchor_points:
                    dist = _manhattan_distance(current_pos, anchor_pos)
                    if dist < min_dist:
                        min_dist = dist
                        closest_anchor = anchor_pos
                    # Simple tie-breaking: first one found wins

                # Calculate relative offset from the closest anchor
                if closest_anchor:
                    anchor_r, anchor_c = closest_anchor
                    dr = r - anchor_r
                    dc = c - anchor_c

                    # Check if the pixel is within the 3x3 neighborhood of the anchor
                    if abs(dr) <= 1 and abs(dc) <= 1:
                        # Map the pixel to the output grid based on relative position
                        # Output grid coordinates: (1 + dr, 1 + dc) maps the [-1, 1] range to [0, 2]
                        output_r = 1 + dr
                        output_c = 1 + dc
                        output_grid[output_r, output_c] = pixel_color

    # Finally, set the center pixel of the output grid to gray (5)
    output_grid[1, 1] = 5

    # Return the output grid as a list of lists
    return output_grid.tolist()
```