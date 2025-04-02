import math
import collections # Not strictly needed now, but good practice for potential future complex counting/grouping

"""
Transforms the input grid by moving the largest contiguous block of a
single color (excluding white 0 and red 2) to immediately precede
the single red 2 pixel, filling the rest of the grid with white 0.
The red 2 pixel retains its original position.
"""

# Define constants for clarity based on the color map and problem description
BACKGROUND_COLOR = 0
ANCHOR_COLOR = 2
# Colors excluded when searching for the payload block
EXCLUDED_COLORS = {BACKGROUND_COLOR, ANCHOR_COLOR}

def find_largest_payload_block(grid):
    """
    Finds the largest contiguous block of a single color in the grid, 
    excluding specified background and anchor colors. If there's a tie
    in length, the block encountered first is returned.

    Args:
        grid (list[int]): The input grid represented as a 1D list of color values.

    Returns:
        tuple(int, int) or tuple(None, 0): A tuple containing the color
                                           and length of the largest valid
                                           payload block found. Returns 
                                           (None, 0) if no such block exists.
    """
    max_len = 0
    max_color = None
    current_len = 0
    current_color = None

    # Iterate through the grid to find contiguous blocks
    for i, pixel in enumerate(grid):
        # Check if the current pixel can be part of a payload block
        is_payload_pixel = pixel not in EXCLUDED_COLORS

        if is_payload_pixel:
            # If it's a payload pixel
            if pixel == current_color:
                # Continue the existing block
                current_len += 1
            else:
                # Different payload color, or start of the first block.
                # First, check if the *previous* block was the largest found so far.
                if current_color is not None and current_len > max_len:
                     max_len = current_len
                     max_color = current_color
                
                # Start tracking the new block
                current_color = pixel
                current_len = 1
        else:
            # Pixel is background or anchor, which ends any current payload block.
            # Check if the just-ended block was the largest found so far.
            if current_color is not None and current_len > max_len:
                 max_len = current_len
                 max_color = current_color
            
            # Reset tracking as this pixel breaks any payload sequence
            current_color = None
            current_len = 0

    # After the loop, check if the last tracked block was the largest.
    # This handles cases where the largest block extends to the end of the grid.
    if current_color is not None and current_len > max_len:
        max_len = current_len
        max_color = current_color

    return max_color, max_len


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[int]): The input grid represented as a 1D list of color values.

    Returns:
        list[int]: The transformed grid.
    """

    # Ensure input is mutable list and get its size
    input_grid = list(input_grid)
    grid_size = len(input_grid)

    # --- Step 1: Initialize output grid ---
    # Create a new grid of the same size, filled entirely with the background color.
    output_grid = [BACKGROUND_COLOR] * grid_size

    # --- Step 2: Locate the anchor pixel ---
    # Find the index of the single red (2) pixel.
    try:
        anchor_index = input_grid.index(ANCHOR_COLOR)
    except ValueError:
        # According to the problem description and examples, the anchor should always exist.
        # If not found, returning the original grid might be a fallback.
        print(f"Error: Anchor color {ANCHOR_COLOR} not found in input grid.")
        return input_grid # Return original grid or raise error as appropriate

    # --- Step 3: Identify the payload block ---
    # Find the color and length of the largest contiguous block of a single color
    # (excluding background and anchor colors).
    payload_color, payload_length = find_largest_payload_block(input_grid)

    # --- Step 4: Construct the output grid (Place Payload) ---
    # Proceed only if a valid payload block was found.
    if payload_color is not None and payload_length > 0:
        # Calculate the target start and end indices for placing the payload block.
        # The payload block should end at the index immediately preceding the anchor pixel.
        payload_end_index = anchor_index - 1
        # The payload block starts 'payload_length' cells before its end.
        payload_start_index = anchor_index - payload_length

        # Check if the calculated start position is valid (within grid bounds).
        # The examples suggest the payload will always fit before the anchor.
        if payload_start_index >= 0:
             # Place the payload block into the output grid.
             for i in range(payload_start_index, payload_end_index + 1):
                 output_grid[i] = payload_color
        else:
             # This case implies the payload block is too long to fit before the anchor.
             # Based on problem constraints/examples, this might not occur.
             # If it did, the behavior is undefined; we choose to not place the payload.
             print(f"Warning: Payload block (color {payload_color}, length {payload_length}) "
                   f"does not fit entirely before anchor at index {anchor_index}. Payload not placed.")

    # --- Step 5: Place the anchor pixel ---
    # Place the anchor (red 2) pixel into the output grid at its original position.
    # This happens regardless of whether a payload was placed.
    # Ensure the anchor index is valid before writing (it should be, based on find).
    if 0 <= anchor_index < grid_size:
        output_grid[anchor_index] = ANCHOR_COLOR

    # --- Step 6: Return the result ---
    return output_grid
