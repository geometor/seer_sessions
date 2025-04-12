import numpy as np
from collections import Counter

"""
Identifies the most frequent non-white color (key_color) in the input grid (ties broken by lowest color value).
Determines the bounding box encompassing all pixels of the key_color.
Iteratively shrinks this bounding box: if any edge (top, bottom, left, right) contains exactly one pixel of the key_color, that edge is moved inwards by one step. This shrinking process repeats until no edge shrinks in a full iteration.
Creates an output grid of the same dimensions as the input, initially filled with white (0).
Draws a hollow rectangle on the output grid using the key_color, defined by the final, adjusted bounding box.
"""

def find_key_pixels(grid: np.ndarray, key_color: int) -> list[tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with the key_color."""
    locations = np.argwhere(grid == key_color)
    return [tuple(loc) for loc in locations]

def calculate_bounding_box(locations: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for given locations."""
    if not locations:
        return None
    rows = [r for r, c in locations]
    cols = [c for r, c in locations]
    return min(rows), min(cols), max(rows), max(cols)

def count_pixels_on_border(locations: list[tuple[int, int]], border_type: str, bbox: tuple[int, int, int, int]) -> int:
    """Counts how many key locations lie on a specific border of the bbox."""
    min_r, min_c, max_r, max_c = bbox
    count = 0
    if border_type == 'top':
        target_r = min_r
        for r, c in locations:
            if r == target_r and min_c <= c <= max_c:
                count += 1
    elif border_type == 'bottom':
        target_r = max_r
        for r, c in locations:
            if r == target_r and min_c <= c <= max_c:
                count += 1
    elif border_type == 'left':
        target_c = min_c
        for r, c in locations:
            if c == target_c and min_r <= r <= max_r:
                count += 1
    elif border_type == 'right':
        target_c = max_c
        for r, c in locations:
            if c == target_c and min_r <= r <= max_r:
                count += 1
    return count

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the identified rules:
    1. Find the most frequent non-white color (key_color).
    2. Find the bounding box of key_color pixels.
    3. Adjust the bounding box by shrinking edges with exactly one key_color pixel.
    4. Draw the final adjusted bounding box as a hollow frame on a white background.
    """
    input_array = np.array(input_grid, dtype=int)
    H, W = input_array.shape

    # 1. Count non-white colors and find the key_color
    color_counts = Counter()
    for r in range(H):
        for c in range(W):
            color = input_array[r, c]
            if color != 0:
                color_counts[color] += 1

    key_color = 0 # Default if no non-white colors
    max_freq = 0
    if color_counts:
        # Sort by frequency (desc), then color value (asc)
        sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
        key_color = sorted_colors[0][0]

    # 2. Find locations of key_color pixels
    key_pixel_locations = find_key_pixels(input_array, key_color)

    # Handle edge case: no key pixels found
    if not key_pixel_locations:
        # Return an all-white grid
        return np.zeros((H, W), dtype=int).tolist()

    # 3. Calculate initial bounding box
    initial_bbox = calculate_bounding_box(key_pixel_locations)
    if initial_bbox is None: # Should not happen if key_pixel_locations is not empty
         return np.zeros((H, W), dtype=int).tolist()

    final_min_r, final_min_c, final_max_r, final_max_c = initial_bbox

    # 4. Adjust bounding box iteratively
    while True:
        shrunk_this_iteration = False
        current_bbox = (final_min_r, final_min_c, final_max_r, final_max_c)

        # Check top border
        if final_min_r < final_max_r: # Check if height > 0
            top_count = count_pixels_on_border(key_pixel_locations, 'top', current_bbox)
            if top_count == 1:
                final_min_r += 1
                shrunk_this_iteration = True
                # Update bbox immediately for subsequent checks in the same iteration?
                # Let's stick to the plan: check all based on the *start* of iteration bbox
                # Update: The NL program suggests adjusting immediately. Let's re-evaluate.
                # Re-reading step 8: It suggests checking each border sequentially and updating.
                # Let's update the bbox immediately after shrinking.
                current_bbox = (final_min_r, final_min_c, final_max_r, final_max_c)


        # Check bottom border
        if final_max_r > final_min_r: # Check if height > 0
             bottom_count = count_pixels_on_border(key_pixel_locations, 'bottom', current_bbox)
             if bottom_count == 1:
                final_max_r -= 1
                shrunk_this_iteration = True
                current_bbox = (final_min_r, final_min_c, final_max_r, final_max_c)


        # Check left border
        if final_min_c < final_max_c: # Check if width > 0
            left_count = count_pixels_on_border(key_pixel_locations, 'left', current_bbox)
            if left_count == 1:
                final_min_c += 1
                shrunk_this_iteration = True
                current_bbox = (final_min_r, final_min_c, final_max_r, final_max_c)


        # Check right border
        if final_max_c > final_min_c: # Check if width > 0
             right_count = count_pixels_on_border(key_pixel_locations, 'right', current_bbox)
             if right_count == 1:
                final_max_c -= 1
                shrunk_this_iteration = True
                # No need to update current_bbox here as it's the last check in the loop


        # Exit loop if no shrinking occurred
        if not shrunk_this_iteration:
            break
        
        # Add safety break if bbox collapses completely (shouldn't happen with checks)
        if final_min_r > final_max_r or final_min_c > final_max_c:
            # This indicates an issue or an empty resulting frame. Output all white?
            # Let's default to drawing whatever shape remains, even if invalid, for now.
            # Or maybe return all white is safer.
             return np.zeros((H, W), dtype=int).tolist()


    # 5. Create output grid and draw the frame
    output_grid = np.zeros((H, W), dtype=int)

    # Check if the final box is valid before drawing
    if final_min_r <= final_max_r and final_min_c <= final_max_c:
        for r in range(final_min_r, final_max_r + 1):
            for c in range(final_min_c, final_max_c + 1):
                # Check if the pixel is on the border
                is_border = (r == final_min_r or r == final_max_r or
                             c == final_min_c or c == final_max_c)
                if is_border:
                    output_grid[r, c] = key_color

    return output_grid.tolist()