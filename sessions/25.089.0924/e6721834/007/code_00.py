import numpy as np
from collections import Counter

"""
Creates an output grid using the dimensions and background color from one half of the input grid 
(the "canvas target" half, which has fewer foreground pixels) and overlays the foreground pixels 
from the other half (the "pattern source" half, which has more or equal foreground pixels).

1. Split the input grid into two halves (vertically if Width >= Height, horizontally otherwise).
2. Identify the background color (most frequent) of each half.
3. Count the number of non-background (foreground) pixels in each half.
4. Determine the "pattern source" half (the one with >= foreground pixels) and the "canvas target" half.
5. Create an output grid with the dimensions of the canvas target half.
6. Fill the output grid with the background color of the canvas target half.
7. Overlay the foreground pixels from the pattern source half onto the output grid,
   maintaining their relative positions within the source half.
"""

# --- Helper Functions ---

def find_most_frequent_color(grid_section):
    """
    Finds the most frequent color in a grid section (numpy array).
    Handles ties by returning the smallest color index.
    Returns 0 (white) for empty input.
    """
    if grid_section.size == 0:
        return 0 # Default for empty section
    colors, counts = np.unique(grid_section, return_counts=True)
    # np.argmax returns the index of the first maximum value in case of ties.
    # Since np.unique returns sorted colors, this selects the smallest color index.
    most_frequent_color = colors[np.argmax(counts)]
    return int(most_frequent_color) # Ensure standard int type

def count_non_background_pixels(grid_section, background_color):
    """
    Counts the number of pixels in the grid section that are not the background color.
    """
    if grid_section.size == 0:
        return 0
    return int(np.sum(grid_section != background_color)) # Ensure standard int type

# --- Main Transformation Function ---

def transform(input_grid):
    """Applies the transformation rule to the input grid."""

    # Convert input list of lists to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # --- 1. Split into Halves ---
    # np.array_split handles odd dimensions; the first array might be smaller or equal.
    if H > W:
        # Split horizontally into Top (half_A) and Bottom (half_B)
        axis_split = 0
        half_A, half_B = np.array_split(input_np, 2, axis=axis_split)
    else:
        # Split vertically (includes H == W) into Left (half_A) and Right (half_B)
        axis_split = 1
        half_A, half_B = np.array_split(input_np, 2, axis=axis_split)

    # --- 2. Identify Background Colors ---
    bg_A = find_most_frequent_color(half_A)
    bg_B = find_most_frequent_color(half_B)

    # --- 3. Count Foreground Pixels ---
    count_A = count_non_background_pixels(half_A, bg_A)
    count_B = count_non_background_pixels(half_B, bg_B)

    # --- 4. Determine Pattern Source and Target Canvas ---
    # Pattern source has greater than or equal foreground pixels. Tie goes to A (Top/Left).
    if count_A >= count_B:
        pattern_source_half = half_A
        bg_pattern = bg_A
        canvas_target_half = half_B
        bg_canvas = bg_B
    else:
        pattern_source_half = half_B
        bg_pattern = bg_B
        canvas_target_half = half_A
        bg_canvas = bg_A

    # --- 5. & 6. Create Output Grid with Target Canvas Background ---
    # The output grid takes the shape of the canvas target half.
    output_shape = canvas_target_half.shape
    output_grid = np.full(output_shape, bg_canvas, dtype=int)

    # --- 7. Overlay Foreground Pixels from Pattern Source ---
    # Iterate through the pattern source half using its local coordinates (r, c).
    # Determine the bounds for overlaying to prevent errors if halves have different sizes
    # (due to odd input dimensions)
    overlay_rows = min(pattern_source_half.shape[0], output_grid.shape[0])
    overlay_cols = min(pattern_source_half.shape[1], output_grid.shape[1])

    for r in range(overlay_rows):
        for c in range(overlay_cols):
            # Get pixel value from the source pattern half
            pixel_value = pattern_source_half[r, c]
            # Check if the pixel in the pattern source half is a foreground pixel
            if pixel_value != bg_pattern:
                # Place the foreground pixel onto the output grid at the same relative coordinate (r, c)
                output_grid[r, c] = pixel_value

    # Convert final numpy array back to standard list of lists format
    return output_grid.tolist()