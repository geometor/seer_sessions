import numpy as np
from collections import Counter

"""
Transformation Rule:
Identify a 'singleton' pixel (unique non-white color) and a 'block' of contiguous pixels (another non-white color) which are adjacent to each other, forming a combined contiguous 'span'. Rotate the sequence of pixels within this span by one position. If the singleton was originally at the left end of the span, rotate right (last element becomes first). If the singleton was at the right end, rotate left (first element becomes last). Place the rotated sequence back into the same span location in the output grid. Background pixels remain unchanged.
"""

def find_span_and_singleton_pos(row):
    """
    Identifies the combined span of the singleton and block, and the singleton's position.

    Args:
        row (np.array): The 1D input row.

    Returns:
        tuple: (span_start, span_end, singleton_pos) or (None, None, None) if pattern not found.
               singleton_pos is 'left' or 'right'.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) < 2: # Need at least one singleton and one block pixel
        return None, None, None

    non_white_colors = row[non_white_indices]
    color_counts = Counter(non_white_colors)

    singleton_color = None
    block_color = None
    singleton_index = -1

    # Identify singleton and block colors
    for color, count in color_counts.items():
        if count == 1:
            if singleton_color is not None: return None, None, None # More than one singleton type
            singleton_color = color
        else: # count > 1 implies block color (assuming only 2 non-white colors)
             if block_color is not None: return None, None, None # More than one block type
             block_color = color

    if singleton_color is None or block_color is None:
        return None, None, None # Pattern needs one singleton and one block

    # Find the index of the singleton
    try:
        # Find the index within the non_white_indices array first
        s_idx_in_non_white = np.where(non_white_colors == singleton_color)[0][0]
        singleton_index = non_white_indices[s_idx_in_non_white]
    except IndexError:
        return None, None, None # Should not happen if color_counts was correct

    # Determine span boundaries (min and max of all non-white indices)
    span_start = np.min(non_white_indices)
    span_end = np.max(non_white_indices)

    # Verify combined span contiguity
    expected_len = span_end - span_start + 1
    if len(non_white_indices) != expected_len:
        # Implies gaps or non-contiguity of the combined object
        return None, None, None

    # Determine singleton position within the span
    if singleton_index == span_start:
        singleton_pos = 'left'
    elif singleton_index == span_end:
        singleton_pos = 'right'
    else:
        # Singleton is not at either end, which contradicts the observed pattern
        return None, None, None

    return span_start, span_end, singleton_pos


def transform(input_grid):
    """
    Applies the span rotation transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.
                                     Expected to be effectively 1D (1 row).

    Returns:
        list of lists: The transformed grid.
    """
    # --- Input Validation and Initialization ---
    if not isinstance(input_grid, list) or not input_grid:
        return [] # Handle empty input
    if len(input_grid) != 1:
         # This specific task seems focused on 1-row grids based on examples.
         # If multi-row grids were possible, logic would need adjustment.
         # For now, assume valid input is 1xN. Return original if not.
         print("Warning: Input grid has more than one row. Returning original.")
         return input_grid
    if not isinstance(input_grid[0], list):
         return [] # Handle malformed input

    input_row = np.array(input_grid[0])
    output_row = input_row.copy() # Create a copy to modify

    # --- Find the Span and Singleton Position ---
    span_start, span_end, singleton_pos = find_span_and_singleton_pos(output_row)

    # If the expected pattern (singleton + adjacent block) isn't found, return original
    if span_start is None:
        # print("Pattern (singleton adjacent to block) not found. Returning original.")
        return input_grid

    # --- Extract and Rotate the Span ---
    # Extract the sequence of pixels within the identified span
    span_sequence = output_row[span_start : span_end + 1]

    # Perform rotation based on the singleton's original position
    rotated_sequence = np.zeros_like(span_sequence)
    if singleton_pos == 'left':
        # Rotate right: last element moves to the first position
        rotated_sequence = np.roll(span_sequence, 1)
    elif singleton_pos == 'right':
        # Rotate left: first element moves to the last position
        rotated_sequence = np.roll(span_sequence, -1)
    else:
         # Should not happen due to checks in find_span_and_singleton_pos
         print("Error: Invalid singleton position detected.")
         return input_grid # Return original on error

    # --- Update Output Grid ---
    # Place the rotated sequence back into the output row at the original span location
    output_row[span_start : span_end + 1] = rotated_sequence

    # --- Format and Return Output ---
    # Convert the modified numpy row back to a list and wrap in a list
    output_grid = [output_row.tolist()]

    return output_grid