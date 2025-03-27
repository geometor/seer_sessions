import numpy as np
import math

"""
Transformation Rule:
1. Identify a horizontal, contiguous segment of a single non-background color ('emitter_color') where each pixel in the segment is directly above a pixel of a *different* non-background color.
2. Determine the emitter segment's color, width, and center coordinates (row 'emitter_y', column 'emitter_center_x').
3. Based on the emitter's color and width, select a predefined pattern of relative coordinate offsets {(dy, dx)}.
4. Create the output grid by copying the input grid.
5. For each offset (dy, dx) in the pattern, calculate the target coordinates (emitter_y + dy, emitter_center_x + dx).
6. If the target coordinates are within the grid boundaries, set the pixel at the target coordinates in the output grid to the 'emitter_color'.
"""

def find_emitter_segment(grid):
    """
    Finds the emitter segment in the grid.

    Returns:
        A tuple (emitter_y, emitter_x_min, emitter_x_max, emitter_color)
        or None if no emitter segment is found.
    """
    height, width = grid.shape
    for r in range(height - 1): # Iterate rows up to the second to last
        for c in range(width):
            pixel_color = grid[r, c]
            pixel_below_color = grid[r + 1, c]

            # Check for emitter condition at (r, c)
            if pixel_color != 0 and pixel_below_color != 0 and pixel_color != pixel_below_color:
                # Found a potential start of an emitter segment
                emitter_color = pixel_color
                emitter_y = r
                emitter_x_min = c
                emitter_x_max = c

                # Extend to the left
                while emitter_x_min > 0 and \
                      grid[r, emitter_x_min - 1] == emitter_color and \
                      grid[r + 1, emitter_x_min - 1] != 0 and \
                      grid[r, emitter_x_min - 1] != grid[r + 1, emitter_x_min - 1]:
                    emitter_x_min -= 1

                # Extend to the right
                while emitter_x_max < width - 1 and \
                      grid[r, emitter_x_max + 1] == emitter_color and \
                      grid[r + 1, emitter_x_max + 1] != 0 and \
                      grid[r, emitter_x_max + 1] != grid[r + 1, emitter_x_max + 1]:
                    emitter_x_max += 1

                # Verify the entire segment meets the condition
                segment_valid = True
                for check_c in range(emitter_x_min, emitter_x_max + 1):
                     if not (grid[r, check_c] == emitter_color and \
                             grid[r + 1, check_c] != 0 and \
                             grid[r, check_c] != grid[r + 1, check_c]):
                         segment_valid = False
                         break
                
                if segment_valid:
                    return emitter_y, emitter_x_min, emitter_x_max, emitter_color
                else:
                    # If verification failed, continue searching from the next potential start
                    # This handles cases where a segment partially meets the criteria
                    # but the initial trigger point wasn't the actual start of a valid full segment
                    continue 
                    
    return None # No emitter found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np)

    # 1. Identify the Emitter Segment
    emitter_info = find_emitter_segment(input_np)

    if emitter_info is None:
        # No emitter found, return the original grid
        return output_grid.tolist()

    emitter_y, emitter_x_min, emitter_x_max, emitter_color = emitter_info

    # 2. Calculate Emitter Properties
    emitter_width = emitter_x_max - emitter_x_min + 1
    # Calculate center column using integer division
    emitter_center_x = (emitter_x_min + emitter_x_max) // 2

    # 3. Determine the Offset Pattern
    offsets = []
    if emitter_color == 1 and emitter_width == 3: # Blue, Width 3
        offsets = [(-2, -2), (-2, +2)]
    elif emitter_color == 3 and emitter_width == 1: # Green, Width 1
        offsets = [(-3, -2), (-3, +2), (-2, -1), (-2, +1)]
    elif emitter_color == 4 and emitter_width == 3: # Yellow, Width 3
        offsets = [(-3, -3), (-3, +3), (-2, -2), (-2, +2)]
    elif emitter_color == 4 and emitter_width == 1: # Yellow, Width 1
        offsets = [(-2, -1), (-2, +1)]
    # Add more patterns here if discovered in new examples

    # 4. & 5. Apply Offsets and Modify Output Grid
    for dy, dx in offsets:
        target_y = emitter_y + dy
        target_x = emitter_center_x + dx

        # 6. Check boundaries and update pixel
        if 0 <= target_y < height and 0 <= target_x < width:
            output_grid[target_y, target_x] = emitter_color

    return output_grid.tolist()
