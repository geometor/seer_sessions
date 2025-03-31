import numpy as np
import copy

"""
Identifies non-background pixels (any color other than orange/7) in the input grid.
Calculates the maximum row and column index of these non-background pixels.
Determines the column for a new vertical gray (5) segment, which is two columns to the right of the maximum column index found.
Determines the start and end rows for the gray segment based on the vertical positions of the highest azure (8) and red (2) pixels:
  - The segment ends at the maximum row index of any non-background pixel.
  - The segment starts based on these rules:
    - If no red pixels exist, it starts at row index 1.
    - If red pixels exist:
        - Find the minimum row index of azure pixels (min_r_azure) and red pixels (min_r_red).
        - If the highest azure pixel is above the highest red pixel (min_r_azure < min_r_red), the segment starts at the end row (effectively a single pixel).
        - Otherwise (highest red is above or at the same level as highest azure), the segment starts at min_r_red + 2.
Adds the calculated gray vertical segment to the output grid, preserving the original content.
If no non-background pixels are found, the output is identical to the input.
"""

def find_colored_pixels(grid, colors):
    """Finds coordinates of pixels with specified colors."""
    coords = []
    rows, cols = grid.shape
    target_colors = set(colors)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in target_colors:
                coords.append((r, c))
    return coords

def transform(input_grid):
    """
    Adds a vertical gray segment to the grid based on the position and colors
    of existing non-background objects.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape
    background_color = 7
    gray_color = 5
    red_color = 2
    azure_color = 8

    # 1. Identify all non-background pixels
    non_background_coords = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] != background_color:
                non_background_coords.append((r, c))

    # If no non-background pixels, return the original grid
    if not non_background_coords:
        return output_grid.tolist()

    # 2. Determine max_c and max_r
    max_r = -1
    max_c = -1
    for r, c in non_background_coords:
        if r > max_r:
            max_r = r
        if c > max_c:
            max_c = c

    # 3. Calculate target column for gray segment
    gray_c = max_c + 2

    # Check if gray column is within grid bounds
    if gray_c >= cols:
        # If the calculated column is outside, maybe we don't add anything,
        # or the logic needs adjustment based on unseen examples.
        # For now, let's assume it stays within bounds based on training data.
        # If it does go out, we'll return the grid unmodified for safety,
        # although this might be incorrect for some test cases.
         print(f"Warning: Calculated gray column {gray_c} is outside grid width {cols}. Returning unmodified grid.")
         # return output_grid.tolist() # Option 1: return unmodified
         # Or clamp it? Let's proceed assuming it fits based on examples.
         pass # Keep going, assuming it fits or numpy indexing handles it (it won't gracefully)
         # Better check:
    if gray_c >= cols:
       print(f"Calculated gray column {gray_c} is out of bounds (width {cols}). No segment added.")
       return output_grid.tolist()


    # 4. Set the ending row
    R_end_idx = max_r

    # 5. Determine the starting row (R_start_idx)
    red_coords = find_colored_pixels(input_np, [red_color])
    azure_coords = find_colored_pixels(input_np, [azure_color])

    min_r_red_idx = float('inf')
    if red_coords:
        min_r_red_idx = min(r for r, c in red_coords)

    min_r_azure_idx = float('inf')
    if azure_coords:
        min_r_azure_idx = min(r for r, c in azure_coords)

    # Determine R_start_idx based on the rules
    if not red_coords:
        # a. No red pixels exist
        # Rule says start at row index 1. Check if grid height allows.
        if rows > 1:
             R_start_idx = 1
        else:
             # If grid is only 1 row high, start must be 0 if end is 0
             R_start_idx = 0 if R_end_idx == 0 else 1 # Adjust if R_end is also 0
             if R_start_idx > R_end_idx: # Prevent invalid range if R_end is 0
                 R_start_idx = R_end_idx

    else:
        # b. Red pixels exist
        if min_r_azure_idx < min_r_red_idx:
            # i. Azure starts higher than red
            R_start_idx = R_end_idx
        else:
            # ii. Red starts higher or at the same row as azure
            R_start_idx = min_r_red_idx + 2
            # Ensure start index is not out of bounds or past the end index
            if R_start_idx >= rows:
                 R_start_idx = rows - 1 # Clamp to last row index if overshoot
            if R_start_idx > R_end_idx:
                 R_start_idx = R_end_idx # Ensure start <= end

    # 6. Draw the gray segment
    # Ensure start/end indices are valid and start <= end
    if R_start_idx < 0: R_start_idx = 0
    if R_end_idx < 0: R_end_idx = 0 # Should not happen if non_bg pixels exist
    if R_start_idx > R_end_idx:
        # This can happen if R_start = R_end_idx (single pixel case)
        # Or if clamping/adjustments caused issues. Re-evaluate if needed.
        # If start > end, draw nothing? Or draw single pixel at R_end?
        # The case min_r_azure < min_r_red leads to R_start = R_end, which means loop range(R_end, R_end+1) works.
        # Let's adjust the loop range slightly
        pass # Loop range below handles start == end correctly. If start > end, range is empty.


    for r in range(R_start_idx, R_end_idx + 1):
        # Double-check row bounds before drawing
        if 0 <= r < rows:
            output_grid[r, gray_c] = gray_color

    return output_grid.tolist()