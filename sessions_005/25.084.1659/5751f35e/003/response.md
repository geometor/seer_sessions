```python
import numpy as np
from collections import Counter

"""
Fill specific white pixels based on nearest non-white pixels using Manhattan distance.

Rule:
1. Check if the input grid has a complete, connected, single-pixel-wide border consisting only of white (0) pixels.
2. Identify the white pixels to be filled ('target pixels'):
    - If a complete white border exists, targets are all white pixels NOT on this border.
    - Otherwise, targets are ALL white pixels.
3. For each target white pixel:
    a. Find all non-white pixels in the original input grid.
    b. Calculate the Manhattan distance from the target pixel to all non-white pixels.
    c. Identify the minimum distance found.
    d. Collect the colors of all non-white pixels that are at this minimum distance.
    e. Apply tie-breaking to determine the fill color:
        i. If green (3) is among the tied colors, the fill color is green (3).
        ii. Else, count the occurrences of each tied color. If one color has a strictly higher count, use that color.
        iii. Else (counts are tied, or only one nearest pixel), use the color with the lowest numerical index among the tied colors.
    f. Set the target white pixel's color in the output grid to the determined fill color.
4. Non-target white pixels and original non-white pixels retain their color.
"""

def _has_complete_white_border(grid: np.ndarray) -> bool:
    """Checks if the grid has a complete, connected, single-pixel white border."""
    height, width = grid.shape
    if height <= 1 or width <= 1: # Cannot have a complete border
        return False

    border_coords = set()
    # Check top and bottom rows
    for c in range(width):
        if grid[0, c] != 0: return False
        border_coords.add((0, c))
        if grid[height - 1, c] != 0: return False
        border_coords.add((height - 1, c))
    # Check left and right columns (excluding corners already checked)
    for r in range(1, height - 1):
        if grid[r, 0] != 0: return False
        border_coords.add((r, 0))
        if grid[r, width - 1] != 0: return False
        border_coords.add((r, width - 1))

    # Verify connectivity (optional but good for robustness, assuming border pixels are correct)
    # Simple check: are all expected border pixels white? Already done above.
    # A full connectivity check (BFS/DFS) could be added if needed, but
    # the initial checks cover the "all white" and "single-pixel-wide" aspects implicitly.
    # If any non-white pixel exists on the border, the first checks return False.
    return True # If we passed all checks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the nearest non-white pixel filling rule with border preservation
    and complex tie-breaking to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Check for complete white border
    has_border = _has_complete_white_border(input_grid)

    # 2. Identify target white pixels
    target_coords = []
    border_pixel_locations = set()
    if has_border:
        for c in range(width):
            border_pixel_locations.add((0, c))
            border_pixel_locations.add((height - 1, c))
        for r in range(1, height - 1):
            border_pixel_locations.add((r, 0))
            border_pixel_locations.add((r, width - 1))

    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 0:
                is_on_border = (r,c) in border_pixel_locations
                if has_border and is_on_border:
                    continue # Skip border white pixels if a complete border exists
                else:
                    target_coords.append((r, c)) # Target all others

    # 4. Find coordinates and colors of non-white pixels
    non_white_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] != 0:
                non_white_pixels.append(((r, c), input_grid[r, c]))

    # If there are no non-white pixels, no filling can occur
    if not non_white_pixels:
        return output_grid

    # 5. Process each target white pixel
    for r_white, c_white in target_coords:
        min_distance = float('inf')
        nearest_pixels_info = [] # Stores (distance, color)

        # 5a-c. Calculate distances and find minimum
        for (r_non_white, c_non_white), color in non_white_pixels:
            distance = abs(r_white - r_non_white) + abs(c_white - c_non_white)
            if distance < min_distance:
                min_distance = distance
                nearest_pixels_info = [(distance, color)]
            elif distance == min_distance:
                nearest_pixels_info.append((distance, color))

        # 5d. Collect tied colors
        tied_colors = [info[1] for info in nearest_pixels_info]

        # 5e. Apply tie-breaking rules
        final_color = 0 # Should always be replaced if non_white_pixels exist
        if not tied_colors: # Should not happen if non_white_pixels exist
             continue

        if 3 in tied_colors: # i. Green wins
            final_color = 3
        else:
            if len(tied_colors) == 1:
                 final_color = tied_colors[0] # No tie
            else:
                 # ii. Check counts
                 color_counts = Counter(tied_colors)
                 max_count = 0
                 max_freq_colors = []
                 for color, count in color_counts.items():
                     if count > max_count:
                         max_count = count
                         max_freq_colors = [color]
                     elif count == max_count:
                         max_freq_colors.append(color)

                 if len(max_freq_colors) == 1:
                     final_color = max_freq_colors[0] # One color had max frequency
                 else:
                     # iii. Tie in counts, use lowest index
                     final_color = min(max_freq_colors)

        # 5f. Update the output grid
        output_grid[r_white, c_white] = final_color

    # 6. Return the modified output grid
    return output_grid
```