import numpy as np
import math

"""
Transformation Rule:
1. Identify a 'trigger point': a location (r, c) where a non-background pixel C1 is directly above a *different* non-background pixel C2 at (r+1, c).
2. Identify the 'emitter segment': the maximal horizontal contiguous segment of color C2 located at row r+1 that includes the trigger point's lower pixel.
3. Determine the emitter segment's color (C2), width, and center coordinates (row 'emitter_y = r+1', column 'emitter_center_x').
4. Based on the emitter's color and width, select a predefined pattern of relative coordinate offsets {(dy, dx)}.
5. Create the output grid by copying the input grid.
6. For each offset (dy, dx) in the pattern, calculate the target coordinates (emitter_y + dy, emitter_center_x + dx).
7. If the target coordinates are within the grid boundaries, set the pixel at the target coordinates in the output grid to the emitter's color (C2).
"""

def find_emitter_segment(grid):
    """
    Finds the emitter segment in the grid based on the trigger condition.

    The trigger condition is a non-background pixel C1 at (r, c) directly
    above a different non-background pixel C2 at (r+1, c).
    The emitter segment is the horizontal segment of color C2 at row r+1
    containing the pixel at (r+1, c).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        A tuple (emitter_y, emitter_x_min, emitter_x_max, emitter_color)
        representing the emitter segment's row, start column, end column,
        and color, or None if no emitter segment is found.
    """
    height, width = grid.shape
    for r in range(height - 1): # Iterate rows up to the second to last
        for c in range(width):
            color_above = grid[r, c]
            color_below = grid[r + 1, c]

            # Check for the trigger condition at (r, c)
            if color_above != 0 and color_below != 0 and color_above != color_below:
                # Found a trigger point. Identify the emitter segment below it.
                emitter_color = color_below
                emitter_y = r + 1
                
                # Find the horizontal extent of the segment at emitter_y containing column c
                emitter_x_min = c
                emitter_x_max = c

                # Extend to the left
                while emitter_x_min > 0 and grid[emitter_y, emitter_x_min - 1] == emitter_color:
                    emitter_x_min -= 1

                # Extend to the right
                while emitter_x_max < width - 1 and grid[emitter_y, emitter_x_max + 1] == emitter_color:
                    emitter_x_max += 1
                
                # Found the unique emitter segment (assumption based on examples)
                return emitter_y, emitter_x_min, emitter_x_max, emitter_color

    return None # No trigger point and thus no emitter found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. & 2. Identify the Emitter Segment based on trigger points
    emitter_info = find_emitter_segment(input_np)

    # If no emitter segment is found, return the original grid
    if emitter_info is None:
        return output_grid.tolist()

    # 3. Determine Emitter Properties
    emitter_y, emitter_x_min, emitter_x_max, emitter_color = emitter_info
    emitter_width = emitter_x_max - emitter_x_min + 1
    # Calculate center column using integer division
    emitter_center_x = (emitter_x_min + emitter_x_max) // 2

    # 4. Select Offset Pattern based on emitter properties
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

    # 5. & 6. & 7. Apply Offsets and Modify Output Grid
    for dy, dx in offsets:
        # Calculate target coordinates relative to the emitter's center
        target_y = emitter_y + dy
        target_x = emitter_center_x + dx

        # Check if the target coordinates are within the grid boundaries
        if 0 <= target_y < height and 0 <= target_x < width:
            # Set the pixel at the target coordinates to the emitter's color
            output_grid[target_y, target_x] = emitter_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()