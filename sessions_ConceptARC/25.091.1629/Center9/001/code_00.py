import numpy as np
from collections import Counter

"""
Identifies two parallel lines (horizontal or vertical) and a single 'mover' pixel in the input grid.
The background color is assumed to be the most frequent color (typically white/0).
The lines and background remain unchanged in the output.
The mover pixel is moved along the axis perpendicular to the lines.
The direction of movement is away from the closer line and towards the farther line.
The distance moved is calculated as half the difference between the distance to the farther line and the distance to the closer line (using integer division).
"""

def transform(input_grid):
    """
    Transforms the input grid by moving a single pixel based on its proximity to two parallel lines.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Create a copy for the output grid
    output_grid = np.copy(grid)

    # Find the background color (most frequent color, usually 0)
    pixels = grid.flatten()
    background_color = Counter(pixels).most_common(1)[0][0]

    # Find non-background pixels and their coordinates
    non_background_pixels = {}
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color:
                if color not in non_background_pixels:
                    non_background_pixels[color] = []
                non_background_pixels[color].append((r, c))

    # Identify the mover pixel (color with only one occurrence) and line color
    mover_color = -1
    mover_pos = None
    line_color = -1
    line_coords = []

    if len(non_background_pixels) != 2:
         # Handle edge case or unexpected input: if not exactly two non-bg colors
         # This logic might need adjustment based on more complex scenarios,
         # but for the given examples, we expect two distinct non-bg elements.
         # For now, assume the single pixel is the one with count 1.
         for color, coords in non_background_pixels.items():
             if len(coords) == 1:
                 mover_color = color
                 mover_pos = coords[0]
                 break
         # If mover found, assume the other color is the line color
         if mover_color != -1:
            for color, coords in non_background_pixels.items():
                if color != mover_color:
                    line_color = color
                    line_coords = coords
                    break
         else:
             # If no single pixel found, cannot proceed with the logic
             # Return the original grid or handle error appropriately
             return input_grid # Or raise ValueError("Could not identify mover pixel")

    else: # Exactly two non-background colors found
        for color, coords in non_background_pixels.items():
            if len(coords) == 1:
                mover_color = color
                mover_pos = coords[0]
            else:
                line_color = color
                line_coords = coords

    if mover_pos is None or line_color == -1:
         # If identification failed after checks
         return input_grid # Or raise ValueError("Could not identify lines or mover pixel")


    # Determine line orientation and indices
    rows = sorted(list(set(r for r, c in line_coords)))
    cols = sorted(list(set(c for r, c in line_coords)))

    line1_idx = -1
    line2_idx = -1
    is_horizontal = False

    if len(rows) == 2 and len(cols) == width : # Horizontal lines
        is_horizontal = True
        line1_idx = rows[0]
        line2_idx = rows[1]
    elif len(cols) == 2 and len(rows) == height: # Vertical lines
        is_horizontal = False
        line1_idx = cols[0]
        line2_idx = cols[1]
    else:
        # If lines are not perfectly horizontal/vertical or don't span the grid
        # This might indicate an unexpected input format
        return input_grid # Or raise ValueError("Lines are not clearly horizontal or vertical")

    # Get mover pixel coordinates
    r, c = mover_pos

    # Erase the mover pixel from its original position in the output
    output_grid[r, c] = background_color

    # Calculate new position
    new_r, new_c = r, c

    if is_horizontal:
        # Lines are horizontal (at rows line1_idx and line2_idx)
        dist1 = abs(r - line1_idx)
        dist2 = abs(r - line2_idx)
        
        if dist1 < dist2: # Closer to line1
            d_close = dist1
            d_far = dist2
            move_direction = 1 # Move away from line1 (increase row index)
        elif dist2 < dist1: # Closer to line2
            d_close = dist2
            d_far = dist1
            move_direction = -1 # Move away from line2 (decrease row index)
        else: # Equidistant
             d_close = dist1
             d_far = dist2
             move_direction = 0 # Don't move

        if d_far > d_close:
             # Calculate move distance using integer division
             d_move = (d_far - d_close) // 2
             new_r = r + (move_direction * d_move)
        # else: new_r remains r (already handled by move_direction=0)

    else:
        # Lines are vertical (at columns line1_idx and line2_idx)
        dist1 = abs(c - line1_idx)
        dist2 = abs(c - line2_idx)

        if dist1 < dist2: # Closer to line1
            d_close = dist1
            d_far = dist2
            move_direction = 1 # Move away from line1 (increase column index)
        elif dist2 < dist1: # Closer to line2
            d_close = dist2
            d_far = dist1
            move_direction = -1 # Move away from line2 (decrease column index)
        else: # Equidistant
            d_close = dist1
            d_far = dist2
            move_direction = 0 # Don't move

        if d_far > d_close:
             # Calculate move distance using integer division
             d_move = (d_far - d_close) // 2
             new_c = c + (move_direction * d_move)
        # else: new_c remains c (already handled by move_direction=0)

    # Ensure new coordinates are within bounds (shouldn't be necessary if logic is correct)
    new_r = max(0, min(new_r, height - 1))
    new_c = max(0, min(new_c, width - 1))

    # Place the mover pixel at the new position
    output_grid[new_r, new_c] = mover_color

    # Convert output back to list of lists
    return output_grid.tolist()