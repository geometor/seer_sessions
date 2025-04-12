"""
Identifies the transformation rule for a grid based on the uniformity of its corner pixels.

1. Check if all four corner pixels (top-left, top-right, bottom-left, bottom-right) of the input grid have the same color.
2. If the corners DO NOT match:
   - Find the most frequent color across the entire grid (overall dominant color). Break ties by choosing the smallest color index.
   - Fill the output grid entirely with this overall dominant color.
3. If the corners DO match:
   - Identify the common corner color as the 'background_color'.
   - Identify all pixels that are NOT the background_color as 'foreground_pixels'.
   - Find the most frequent color among the foreground_pixels ('dominant_foreground_color'). Break ties by choosing the smallest color index. Handle the case where there are no foreground pixels.
   - Find the most frequent color across the entire grid ('overall_dominant_color'). Break ties similarly.
   - If the dominant_foreground_color is the same as the background_color, OR if the background_color is the same as the overall_dominant_color:
     - Fill the output grid entirely with the background_color.
   - Otherwise:
     - Create an output grid filled initially with the background_color.
     - For every position where the input grid had a foreground_pixel, set the corresponding position in the output grid to the dominant_foreground_color.
4. Return the resulting output grid.
"""

import numpy as np
from collections import Counter

def find_dominant_color(pixels: np.ndarray) -> int | None:
    """
    Finds the most frequent color in a flattened array of pixels.
    Handles ties by returning the smallest color index.
    Returns None if the input array is empty.
    """
    if pixels.size == 0:
        return None # No pixels, no dominant color

    counts = Counter(pixels.flatten())
    if not counts: # Handles cases like an array of empty lists? Should not happen with numpy arrays normally.
        return None

    # Find the maximum count
    max_count = 0
    for count in counts.values():
        if count > max_count:
            max_count = count

    # Get all colors with the maximum count
    dominant_colors = [color for color, count in counts.items() if count == max_count]

    # Return the smallest color index in case of a tie
    return min(dominant_colors)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation based on corner uniformity and dominant colors.
    """
    # Convert input list of lists to a NumPy array for easier indexing and operations
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Handle edge case of 1x1 grid
    if height == 1 and width == 1:
        return input_grid # 1x1 grid is already uniform

    # Check corner pixels
    top_left = grid_np[0, 0]
    top_right = grid_np[0, width - 1]
    bottom_left = grid_np[height - 1, 0]
    bottom_right = grid_np[height - 1, width - 1]

    corners_match = (top_left == top_right == bottom_left == bottom_right)

    if corners_match:
        # Case 1: Corners match
        background_color = top_left

        # Identify foreground pixels (pixels not matching the background)
        foreground_mask = (grid_np != background_color)
        foreground_pixels = grid_np[foreground_mask]

        # Find dominant foreground color
        dominant_foreground_color = find_dominant_color(foreground_pixels)

        # Handle case where there are no foreground pixels
        if dominant_foreground_color is None:
             # If no foreground, the grid is already uniform with the background color
             output_grid_np = np.full_like(grid_np, background_color)
             return output_grid_np.tolist() # Return early

        # Find overall dominant color
        overall_dominant_color = find_dominant_color(grid_np) # Cannot be None here unless grid is empty (checked earlier implicitly)

        # Decision logic based on colors
        if dominant_foreground_color == background_color or background_color == overall_dominant_color:
            # Fill output grid entirely with background_color
            output_grid_np = np.full_like(grid_np, background_color)
        else:
            # Initialize output with background color
            output_grid_np = np.full_like(grid_np, background_color)
            # Place dominant foreground color where foreground pixels were
            output_grid_np[foreground_mask] = dominant_foreground_color

    else:
        # Case 2: Corners do not match
        # Find the overall dominant color
        overall_dominant_color = find_dominant_color(grid_np)
        # Fill the entire output grid with the overall dominant color
        # Handle potential None case if grid was somehow empty, though unlikely
        fill_color = overall_dominant_color if overall_dominant_color is not None else 0 # Default fill if somehow empty
        output_grid_np = np.full_like(grid_np, fill_color)


    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid