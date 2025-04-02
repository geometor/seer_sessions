```python
import numpy as np
import itertools

"""
Identifies the background color (azure, 8). Finds all non-background pixels ("feature pixels").
Creates a copy of the input grid.
Generates all unique pairs of feature pixel coordinates.
For each pair, calculates the coordinates of the pixels forming a straight line between them using Bresenham's algorithm.
For each pixel coordinate on the calculated line:
  If the pixel in the original input grid at this coordinate was the background color (azure, 8), 
  change the color of the pixel at this coordinate in the output grid copy to red (2).
Returns the modified grid copy.
"""

def get_line_pixels(r1, c1, r2, c2):
    """
    Calculates the coordinates of pixels forming a line between (r1, c1) and (r2, c2)
    using Bresenham's line algorithm.
    Handles horizontal, vertical, and diagonal lines.
    """
    points = []
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    # Determine step direction for row and column
    sr = 1 if r1 < r2 else -1 if r1 > r2 else 0
    sc = 1 if c1 < c2 else -1 if c1 > c2 else 0

    r, c = r1, c1
    
    # Determine initial error based on dominant axis
    # Adapted Bresenham's algorithm
    if dc > dr:  # Line is more horizontal (or horizontal)
        err = dc / 2.0
        while True:
            points.append((r, c))
            if c == c2: # Reached end column
                 # Ensure the final row is correct, especially for steep lines handled here
                 if r != r2: 
                     # This adjustment might be needed if the standard loop terminates early on column match
                     # but let's test without first, standard Bresenham should handle it.
                     # If issues arise, we might need to force the last point.
                     pass # Assume standard loop is correct for now
                 break 
            err -= dr
            if err < 0:
                r += sr # Move vertically
                err += dc
            c += sc # Always move horizontally (dominant axis)
            # Check loop termination condition again, in case we stepped onto the target
            # This helps ensure termination for lines ending exactly at c2
            if c == c2 and r == r2 and (r,c) not in points:
                 points.append((r, c)) # Add final point if exactly reached after step
                 break

    else:  # Line is more vertical (or vertical, or diagonal 45 deg)
        err = dr / 2.0
        while True:
            points.append((r, c))
            if r == r2: # Reached end row
                 # Similar check for column if needed
                 # if c != c2:
                 #     pass 
                 break
            err -= dc
            if err < 0:
                c += sc # Move horizontally
                err += dr
            r += sr # Always move vertically (dominant axis)
            # Check loop termination condition again
            if c == c2 and r == r2 and (r,c) not in points:
                 points.append((r, c)) # Add final point if exactly reached after step
                 break
                 
    # Ensure the absolute final point is included if the loop terminated slightly early 
    # or due to edge cases. Standard Bresenham should cover this, but double-check.
    if not points or points[-1] != (r2, c2):
         # A simpler loop termination might be `while True:` and `if r == r2 and c == c2: break` inside
         # Let's ensure the last point is always added manually if missing.
         if (r2, c2) not in points:
             points.append((r2, c2))
             
    return points

def transform(input_grid):
    """
    Draws red lines connecting all pairs of non-azure pixels, 
    only coloring over original azure pixels.
    """
    # Make a copy to modify
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define colors based on observations
    background_color = 8  # Azure
    line_color = 2        # Red

    # Find coordinates of all "feature" pixels (non-background)
    feature_pixels_coords = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] != background_color:
                feature_pixels_coords.append((r, c))

    # If there are fewer than 2 feature pixels, no lines can be drawn
    if len(feature_pixels_coords) < 2:
        return output_grid

    # Generate all unique pairs of feature pixel coordinates
    # Uses itertools.combinations to avoid duplicate pairs (like (A,B) and (B,A))
    # and pairs of a point with itself (like (A,A))
    pixel_pairs = list(itertools.combinations(feature_pixels_coords, 2))

    # Process each pair to draw a line
    for pair in pixel_pairs:
        (r1, c1), (r2, c2) = pair
        
        # Get all pixels coordinates forming the line between the pair
        line_coords = get_line_pixels(r1, c1, r2, c2)

        # Color the line pixels on the output grid
        for r, c in line_coords:
            # Check bounds (Bresenham should stay within reasonable bounds, but safety check)
            if 0 <= r < height and 0 <= c < width:
                # IMPORTANT: Only change the color if the pixel in the ORIGINAL grid was background
                # This prevents overwriting the feature pixels themselves.
                if input_grid[r, c] == background_color:
                    output_grid[r, c] = line_color
            # Else: Pixel is out of bounds (shouldn't happen with correct Bresenham)
            # Or Pixel was a feature pixel (don't overwrite)

    return output_grid
```