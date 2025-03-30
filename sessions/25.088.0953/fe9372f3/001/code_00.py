import numpy as np
from typing import List, Tuple

"""
Transformation Rule:

1.  Identify the single red (+) shape in the input grid. Find the coordinates (r_c, c_c) of its center pixel (the pixel with 4 red neighbors).
2.  Create an output grid of the same dimensions as the input grid, initially filled with white (0).
3.  Iterate through each pixel (r, c) of the grid.
4.  Determine the color of the output pixel (r, c) based on its relationship to the center (r_c, c_c) and the original input grid:
    a.  If the corresponding pixel in the input grid `input_grid[r][c]` is red (2), the output pixel `output_grid[r][c]` is also red (2).
    b.  Otherwise, calculate the row difference `dr = r - r_c` and column difference `dc = c - c_c`.
    c.  If the pixel lies on a diagonal line passing through the center (i.e., `abs(dr) == abs(dc)`), the output pixel is blue (1).
    d.  If the pixel lies on the horizontal or vertical line passing through the center (i.e., `dr == 0` or `dc == 0`), calculate the Manhattan distance `dist = abs(dr) + abs(dc)`:
        i.  If the distance is 4 or greater, and the remainder of `(dist - 4)` divided by 3 is 0 (i.e., `dist >= 4 and (dist - 4) % 3 == 0`), the output pixel is yellow (4).
        ii. Otherwise (for pixels on the horizontal/vertical line not matching the yellow condition), the output pixel is azure (8).
    e.  If none of the above conditions are met (the pixel is not part of the original red shape, not on the diagonals, and not on the horizontal/vertical lines through the center), the output pixel remains white (0).
"""

def find_center(grid: np.ndarray) -> Tuple[int, int]:
    """Finds the center of the red '+' shape."""
    height, width = grid.shape
    red_pixels = np.argwhere(grid == 2)
    
    if len(red_pixels) != 5:
        # Basic check, assumes the shape is always a '+' of 5 pixels
        # A more robust check might be needed for variations
         pass # Might need more robust error handling or shape detection

    for r, c in red_pixels:
        # Check for 4 red neighbors (up, down, left, right)
        # Boundary checks are implicitly handled if the center is not on the edge
        neighbor_count = 0
        if r > 0 and grid[r - 1, c] == 2:
            neighbor_count += 1
        if r < height - 1 and grid[r + 1, c] == 2:
            neighbor_count += 1
        if c > 0 and grid[r, c - 1] == 2:
            neighbor_count += 1
        if c < width - 1 and grid[r, c + 1] == 2:
            neighbor_count += 1
            
        if neighbor_count == 4:
            return r, c
            
    # Fallback or error if center not found (should not happen based on examples)
    # Let's try finding the median coordinate if the 4-neighbor check fails
    if len(red_pixels) > 0:
        median_r = int(np.median([p[0] for p in red_pixels]))
        median_c = int(np.median([p[1] for p in red_pixels]))
        # Verify this median is actually a red pixel
        if grid[median_r, median_c] == 2:
             return median_r, median_c

    raise ValueError("Could not find the center of the red '+' shape.")


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Finds the center of the red '+' shape, then draws diagonal (blue), 
    horizontal/vertical (azure) lines, placing yellow markers at specific intervals 
    (distance 4, then every 3 steps) on the horizontal/vertical lines, 
    while preserving the original red shape.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with white (0)
    output_np = np.zeros_like(input_np)

    # Find the center of the red '+'
    try:
        r_c, c_c = find_center(input_np)
    except ValueError as e:
        print(f"Error finding center: {e}")
        # Handle error case, maybe return input or an empty grid
        return input_grid # Or raise the error further up

    # Iterate through each pixel to determine its color in the output grid
    for r in range(height):
        for c in range(width):
            # Calculate differences from the center
            dr = r - r_c
            dc = c - c_c
            
            # 1. Preserve original red pixels
            if input_np[r, c] == 2:
                output_np[r, c] = 2
                continue # Move to next pixel

            # 2. Check for diagonals (excluding center if it wasn't red originally)
            if abs(dr) == abs(dc) and (dr != 0 or dc != 0): # dr!=0 or dc!=0 excludes the center itself
                output_np[r, c] = 1 # Blue
                continue

            # 3. Check for horizontal or vertical lines (excluding center)
            if (dr == 0 or dc == 0) and (dr != 0 or dc != 0):
                dist = abs(dr) + abs(dc) # Manhattan distance from center
                
                # Check for yellow condition: dist >= 4 and (dist-4) is a multiple of 3
                if dist >= 4 and (dist - 4) % 3 == 0:
                    output_np[r, c] = 4 # Yellow
                else:
                    output_np[r, c] = 8 # Azure
                continue
                
            # 4. Otherwise, the pixel remains white (0) - already initialized

    # Convert numpy array back to list of lists
    output_grid = output_np.tolist()
    return output_grid
