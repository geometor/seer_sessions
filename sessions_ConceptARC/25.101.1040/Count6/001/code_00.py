import numpy as np
from collections import Counter

"""
1. Identify the frame: Find the most frequent non-background color in the input grid; this represents the frame's color.
2. Determine the frame's bounding box: Find the minimum and maximum row and column indices occupied by the frame pixels.
3. Count inner pixels: Iterate through the area strictly inside the frame's bounding box (excluding the frame pixels themselves). Count the number of pixels (N) whose color is neither the background color (0) nor the frame's color.
4. Generate output grid: Create a 7x1 grid. Fill the top N cells with yellow (4) and the remaining cells with white (0).
"""

def find_bounding_box(pixels: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return 0, 0, 0, 0
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Counts specific colored pixels within a framed region and represents the count 
    vertically in a fixed-size output grid.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Identify the frame color
    # Flatten the grid, filter out background (0), and find the most common color
    non_background_pixels = grid[grid != 0]
    if non_background_pixels.size == 0:
        # Handle empty or all-background grid
        output_grid = np.zeros((7, 1), dtype=int)
        return output_grid.tolist()
        
    color_counts = Counter(non_background_pixels)
    # Assume the most frequent non-background color is the frame
    frame_color = color_counts.most_common(1)[0][0]

    # Find all pixels belonging to the frame
    frame_pixels_coords = set()
    for r in range(height):
        for c in range(width):
            if grid[r, c] == frame_color:
                frame_pixels_coords.add((r, c))
                
    if not frame_pixels_coords:
         # Handle cases where the assumed frame color wasn't actually found (shouldn't happen with most_common logic)
        output_grid = np.zeros((7, 1), dtype=int)
        return output_grid.tolist()


    # 2. Determine the frame's bounding box
    min_r, min_c, max_r, max_c = find_bounding_box(frame_pixels_coords)

    # 3. Count inner pixels
    inner_pixel_count = 0
    # Iterate strictly *inside* the bounding box
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            pixel_color = grid[r, c]
            # Check if the pixel is not background and not part of the frame
            if pixel_color != 0 and pixel_color != frame_color:
                inner_pixel_count += 1

    # 4. Generate output grid
    output_grid = np.zeros((7, 1), dtype=int)  # Initialize with background color (0)
    
    # Fill the top 'inner_pixel_count' cells with yellow (4)
    # Ensure count doesn't exceed the output grid height
    count_to_fill = min(inner_pixel_count, 7) 
    output_grid[:count_to_fill, 0] = 4 # Yellow

    return output_grid.tolist()