"""
Connect aligned pairs of blue pixels (1) with azure lines (8) if the path between them consists solely of white pixels (0).

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all locations of blue pixels (color 1).
3.  Iterate through all unique pairs of these blue pixel locations.
4.  For each pair:
    a.  Check if they are horizontally aligned (same row).
    b.  If horizontally aligned, check if the path between them (excluding endpoints) contains only white pixels (0) in the input grid.
    c.  If the horizontal path is clear, change the intermediate pixels to azure (8) in the output grid.
    d.  Check if they are vertically aligned (same column).
    e.  If vertically aligned, check if the path between them (excluding endpoints) contains only white pixels (0) in the input grid.
    f.  If the vertical path is clear, change the intermediate pixels to azure (8) in the output grid.
5.  Return the modified output grid.
"""

import numpy as np
from itertools import combinations

def transform(input_grid):
    """
    Connects horizontally or vertically aligned blue pixels (1) with azure (8) 
    if the path between them is clear (only white pixels 0).
    """
    # Convert input list of lists to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy()
    height, width = input_np.shape

    # Find coordinates of all blue pixels (1)
    blue_pixels = []
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 1:
                blue_pixels.append((r, c))

    # Iterate through all unique pairs of blue pixels
    for (r1, c1), (r2, c2) in combinations(blue_pixels, 2):
        
        # Check for horizontal alignment
        if r1 == r2:
            # Determine the start and end columns (exclusive of endpoints)
            start_c = min(c1, c2) + 1
            end_c = max(c1, c2)
            
            # Check if the path between them is clear (all white)
            is_clear = True
            if start_c < end_c: # Only check if there are intermediate pixels
                if not np.all(input_np[r1, start_c:end_c] == 0):
                    is_clear = False
            
            # If clear, fill the path with azure (8) in the output grid
            if is_clear and start_c < end_c:
                output_np[r1, start_c:end_c] = 8

        # Check for vertical alignment
        elif c1 == c2:
            # Determine the start and end rows (exclusive of endpoints)
            start_r = min(r1, r2) + 1
            end_r = max(r1, r2)

            # Check if the path between them is clear (all white)
            is_clear = True
            if start_r < end_r: # Only check if there are intermediate pixels
                 if not np.all(input_np[start_r:end_r, c1] == 0):
                    is_clear = False
            
            # If clear, fill the path with azure (8) in the output grid
            if is_clear and start_r < end_r:
                 output_np[start_r:end_r, c1] = 8

    # Convert the numpy array back to a list of lists for the final output
    return output_np.tolist()