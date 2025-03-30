import numpy as np
from typing import List

"""
Transformation Rule:

1. Identify the color (B) of the single-pixel border frame in the input grid.
2. Identify the pair of identical, non-border, non-background pixels located at columns 1 and 18 (0-based index) on the same row (R). Record their color (C) and row (R). These are the 'anchor' pixels.
3. Create a new output grid of the same dimensions as the input, initially filled with the background color (white, 0).
4. Draw the border onto the output grid using the identified border color B.
5. Select the specific H-like output shape pattern, its height (H), its center row offset (CRO), and its starting column (Col) based *only* on the anchor pixel color (C):
    * If C is Orange (7): Use the 5x3 H shape [[7,0,7],[7,0,7],[7,7,7],[7,0,7],[7,0,7]], H=5, CRO=2, Col=13.
    * If C is Magenta (6): Use the 6x3 H shape [[6,6,6],[6,0,6],[6,6,6],[6,0,6],[6,0,6],[6,6,6]], H=6, CRO=2, Col=2.
    * If C is Red (2): Use the 5x3 H shape [[2,0,2],[0,2,0],[2,2,2],[0,2,0],[2,0,2]], H=5, CRO=2, Col=6.
    * If C is Blue (1): Use the 3x3 H shape [[1,0,1],[1,1,1],[1,0,1]], H=3, CRO=1, Col=14.
6. Calculate the starting row for placing the shape in the output grid: start_row = R - CRO.
7. Draw the selected shape onto the output grid. The top-left corner of the shape pattern is placed at (start_row, start_col). Use the anchor color C for the non-background pixels of the shape pattern when drawing.
"""

import numpy as np
from typing import List

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies border and anchor pixels, then draws a specific H-shaped pattern
    in the output grid based on the anchor pixels' color and row.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0 # White

    # 3. Initialize output_grid with background color
    output_np = np.full_like(input_np, background_color)

    # 1. Identify border color (assuming top-left is border)
    # Also handles edge case where grid might be 1x1
    if height > 0 and width > 0:
        border_color = input_np[0, 0]
    else:
        return input_grid # Return empty/invalid grid as is

    # 4. Draw the border onto the output grid
    if height > 1 and width > 1:
        output_np[0, :] = border_color
        output_np[-1, :] = border_color
        output_np[:, 0] = border_color
        output_np[:, -1] = border_color
    elif height == 1 and width > 0:
         output_np[0, :] = border_color
    elif width == 1 and height > 0:
        output_np[:, 0] = border_color
    # If 1x1, the full_like already handled it, or the checks above did.

    # 2. Identify anchor pixels (color C, row R)
    anchor_color = -1
    anchor_row = -1
    # Iterate through rows (excluding borders)
    # Ensure there are non-border rows and columns 1 and 18 exist
    if height > 2 and width > 18: # Need at least row 1, and col 1 and 18
        for r in range(1, height - 1):
            # Check columns 1 and 18 (0-based index)
            pixel1 = input_np[r, 1]
            pixel18 = input_np[r, 18]
            # Check if they match, are not background, and not border
            if pixel1 == pixel18 and pixel1 != background_color and pixel1 != border_color:
                anchor_color = pixel1
                anchor_row = r
                break # Found the anchors

    # If no anchors found, return the grid with just the border
    if anchor_color == -1:
        # This might be expected if input doesn't conform
        # print("Warning: Anchor pixels not found or grid too small!")
        return output_np.tolist()

    # 5. Define H-shapes, offsets, and start columns based on anchor color
    # Note: Shape patterns themselves don't need the color, only the structure.
    # We use the anchor_color C when drawing.
    shape_definitions = {
        7: {'shape': np.array([[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]]), 'offset': 2, 'col': 13}, # Orange
        6: {'shape': np.array([[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,1,1]]), 'offset': 2, 'col': 2}, # Magenta
        2: {'shape': np.array([[1,0,1],[0,1,0],[1,1,1],[0,1,0],[1,0,1]]), 'offset': 2, 'col': 6}, # Red
        1: {'shape': np.array([[1,0,1],[1,1,1],[1,0,1]]),             'offset': 1, 'col': 14}  # Blue
    }

    # Check if a shape is defined for the found anchor color
    if anchor_color not in shape_definitions:
        # print(f"Warning: No shape defined for anchor color {anchor_color}")
        return output_np.tolist() # Return grid with just border

    # Get the definition for the specific anchor color
    selected_shape_info = shape_definitions[anchor_color]
    shape_pattern = selected_shape_info['shape']
    center_row_offset = selected_shape_info['offset']
    start_col = selected_shape_info['col']
    shape_height, shape_width = shape_pattern.shape

    # 6. Calculate the starting row for the shape
    start_row = anchor_row - center_row_offset

    # 7. Draw the selected shape onto the output grid
    for r_idx in range(shape_height):
        for c_idx in range(shape_width):
            # Check if the pixel in the shape pattern is non-background (represented by 1)
            if shape_pattern[r_idx, c_idx] != background_color: # Using 0 for background in pattern too
                # Calculate the target coordinates in the output grid
                output_row = start_row + r_idx
                output_col = start_col + c_idx

                # Check bounds before drawing to avoid errors
                if 0 <= output_row < height and 0 <= output_col < width:
                    # Draw using the ANCHOR color
                    output_np[output_row, output_col] = anchor_color

    # Convert back to list of lists for the required output format
    output_grid = output_np.tolist()
    return output_grid