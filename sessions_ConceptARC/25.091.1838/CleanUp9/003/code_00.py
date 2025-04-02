import numpy as np
from collections import Counter

"""
Identifies the most frequent non-background color (frame_color) in the input grid.
Determines an initial bounding box encompassing all pixels of the frame_color.
Refines this bounding box by iteratively removing sides (top, bottom, left, right) 
if that side contains only a single pixel of the frame_color within the current box's extent.
Creates an output grid of the same dimensions as the input, filled with the background color (0).
Draws a hollow rectangle on the output grid using the frame_color along the perimeter defined 
by the final, refined bounding box.
"""

# Imports handled by the execution environment (numpy, collections.Counter assumed available)

def find_most_frequent_non_background_color(grid):
    """Finds the most frequent color in the grid, excluding the background color 0."""
    counts = Counter()
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            pixel = grid[r, c]
            if pixel != 0:  # Exclude background color (0)
                counts[pixel] += 1
    
    if not counts:
        return None # No non-background colors found
        
    # Find the color with the maximum count.
    most_common_color = counts.most_common(1)[0][0]
    return most_common_color

def find_initial_bounding_box(grid, color):
    """Finds the initial bounding box (min_row, max_row, min_col, max_col) for a given color."""
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return None # Color not found
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def refine_bounding_box(grid, color, initial_bbox):
    """Refines the bounding box by removing sides with only one pixel of the target color."""
    if initial_bbox is None:
        return None

    min_r, max_r, min_c, max_c = initial_bbox

    while True:
        changed = False
        
        # Check Top Row: if only one 'color' pixel exists in this row within the current box cols
        if min_r <= max_r:
             top_row_segment = grid[min_r, min_c:max_c+1]
             if np.count_nonzero(top_row_segment == color) == 1:
                 min_r += 1
                 changed = True
                 # Ensure box remains valid after shrinking
                 if min_r > max_r: break 

        # Check Bottom Row: if only one 'color' pixel exists in this row within the current box cols
        if min_r <= max_r:
             bottom_row_segment = grid[max_r, min_c:max_c+1]
             if np.count_nonzero(bottom_row_segment == color) == 1:
                 max_r -= 1
                 changed = True
                 # Ensure box remains valid after shrinking
                 if min_r > max_r: break

        # Check Left Column: if only one 'color' pixel exists in this col within the current box rows
        if min_c <= max_c:
            left_col_segment = grid[min_r:max_r+1, min_c]
            if np.count_nonzero(left_col_segment == color) == 1:
                min_c += 1
                changed = True
                # Ensure box remains valid after shrinking
                if min_c > max_c: break

        # Check Right Column: if only one 'color' pixel exists in this col within the current box rows
        if min_c <= max_c:
            right_col_segment = grid[min_r:max_r+1, max_c]
            if np.count_nonzero(right_col_segment == color) == 1:
                max_c -= 1
                changed = True
                # Ensure box remains valid after shrinking
                if min_c > max_c: break

        if not changed:
            break
            
    # Check if the box became invalid (e.g., min > max)
    if min_r > max_r or min_c > max_c:
        return None # Indicate an empty or invalid final box

    return min_r, max_r, min_c, max_c


def transform(input_grid):
    # Convert input list of lists to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    background_color = 0

    # Initialize output grid with background color
    output_array = np.full((height, width), background_color, dtype=int)

    # Step 1: Find the most frequent non-background color
    frame_color = find_most_frequent_non_background_color(input_array)

    # If no frame color is found (e.g., grid is all background), return the background grid
    if frame_color is None:
        return output_array.tolist()

    # Step 2: Find the initial bounding box of the frame color
    initial_bbox = find_initial_bounding_box(input_array, frame_color)

    # Step 3: Refine the bounding box iteratively
    final_bbox = refine_bounding_box(input_array, frame_color, initial_bbox)

    # If no valid bounding box could be determined (initial or final), return the background grid
    if final_bbox is None:
         return output_array.tolist()

    min_row, max_row, min_col, max_col = final_bbox

    # Step 4: Draw the hollow rectangle on the output grid using the final bounding box
    # Ensure indices are within valid range before drawing
    if 0 <= min_row < height and 0 <= max_row < height and 0 <= min_col < width and 0 <= max_col < width:
        # Draw top border
        output_array[min_row, min_col:max_col+1] = frame_color
        # Draw bottom border
        output_array[max_row, min_col:max_col+1] = frame_color
        # Draw left border
        output_array[min_row:max_row+1, min_col] = frame_color
        # Draw right border
        output_array[min_row:max_row+1, max_col] = frame_color

    # Convert the final numpy array back to a list of lists
    return output_array.tolist()