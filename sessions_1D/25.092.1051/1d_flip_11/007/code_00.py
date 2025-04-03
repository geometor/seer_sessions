import numpy as np
from collections import Counter

"""
Transformation Rule:
Identify a contiguous horizontal span of non-white pixels (colors other than 0) 
in the input row. This span must satisfy several conditions:
1. It must be truly contiguous (no background pixels within).
2. It must consist of exactly two distinct non-white colors.
3. One of these colors (the 'singleton') must appear exactly once within the span.
4. The other color (the 'block') must appear one or more times within the span.
5. The singleton pixel must be located at either the leftmost or the rightmost 
   position of this contiguous span.

If all these conditions are met, the transformation involves performing a 
circular shift (numpy.roll) on the sequence of pixels *within the identified span*.
- If the singleton pixel was originally at the left end of the span, the sequence 
  is shifted LEFT by one position (np.roll(sequence, -1)).
- If the singleton pixel was originally at the right end of the span, the sequence 
  is shifted RIGHT by one position (np.roll(sequence, 1)).

The resulting shifted sequence replaces the original sequence within the span's 
location in the output grid. All pixels outside this span (background pixels) 
remain unchanged. If the input does not match the described pattern, the original 
input grid is returned.
"""

def _find_span_and_singleton_pos(row):
    """
    Identifies the contiguous non-white span, its boundaries, and the singleton's position.

    Args:
        row (np.array): The 1D input row.

    Returns:
        tuple: (span_start, span_end, singleton_pos) or (None, None, None) if pattern not found.
               singleton_pos is 'left' or 'right'. Returns None if conditions (contiguity, 
               exactly one singleton at an end, exactly two colors) are not met.
    """
    # Find indices of all non-white pixels (colors != 0)
    non_white_indices = np.where(row != 0)[0]

    # Check if there are at least two non-white pixels needed for a singleton and a block
    if len(non_white_indices) < 2:
        # print("Debug: Less than 2 non-white pixels.")
        return None, None, None

    # Determine the potential start and end of the contiguous span
    span_start = np.min(non_white_indices)
    span_end = np.max(non_white_indices)

    # Verify that the identified span is truly contiguous (no background pixels within)
    # The number of non-white pixels must equal the length of the span
    expected_len = span_end - span_start + 1
    if len(non_white_indices) != expected_len:
        # print(f"Debug: Non-contiguity detected. Span {span_start}-{span_end}, Expected len {expected_len}, Actual non-white count {len(non_white_indices)}")
        # Implies gaps (background pixels) within the span
        return None, None, None

    # Extract the sequence of pixels within the span
    span_sequence = row[span_start : span_end + 1]

    # Count the occurrences of each color within the span
    color_counts = Counter(span_sequence)

    # Verify exactly two distinct non-white colors exist in the span
    if len(color_counts) != 2:
        # print(f"Debug: Expected 2 distinct colors in span, found {len(color_counts)}: {color_counts}")
        return None, None, None
        
    # Identify the singleton color (the one with count 1)
    singleton_color = None
    block_color = None
    singleton_count_check = 0
    block_color_check = None # Store the color identified as block

    for color, count in color_counts.items():
        if count == 1:
            singleton_count_check += 1
            singleton_color = color # Assign the color with count 1
        elif count > 1:
            block_color_check = color # Assign potential block color
        # else count == 0? Should not happen with Counter on span_sequence

    # Verify exactly one singleton color and infer block color
    if singleton_count_check != 1:
        # print(f"Debug: Expected exactly 1 singleton color, found check count {singleton_count_check}")
        return None, None, None
    
    # The block color must be the other color present
    block_color = block_color_check # Assign confirmed block color
    if block_color is None:
         # This case implies the counts were {color_A: 1, color_B: 1}, handled by len(color_counts) != 2?
         # Let's double check. If span is [7, 6], counts are {7:1, 6:1}. len=2. singleton_count_check=2 -> returns None. Correct.
         # If span is [7, 7], counts is {7:2}. len=1 -> returns None. Correct.
         # If span is [7, 6, 6], counts {7:1, 6:2}. len=2. s_count=1, b_color=6. block_color gets 6. Correct.
         # If span is [7, 7, 6], counts {7:2, 6:1}. len=2. s_count=1, s_color=6, b_color=7. block_color gets 7. Correct.
         # If block_color is None here, it means no color had count > 1, which was covered by the s_count!=1 check if len==2.
         # print(f"Debug: Could not definitively identify block color.") # Should be unreachable
         return None, None, None


    # Determine singleton position ('left' or 'right') based on its index in the original row
    singleton_pos = None
    if row[span_start] == singleton_color:
        singleton_pos = 'left'
    elif row[span_end] == singleton_color:
        singleton_pos = 'right'
    else:
         # Singleton is not at either end of the span, pattern mismatch
         # print(f"Debug: Singleton color {singleton_color} not found at ends ({span_start}, {span_end}) of span.")
         return None, None, None

    # If all checks passed, return the span boundaries and singleton position
    # print(f"Debug: Found pattern: Span {span_start}-{span_end}, Singleton Pos: {singleton_pos}")
    return span_start, span_end, singleton_pos


def transform(input_grid):
    """
    Applies the span rotation transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.
                                     Expected to be effectively 1D (1 row).

    Returns:
        list of lists: The transformed grid, or the original grid if the
                       specific pattern is not found.
    """
    # --- Input Validation and Initialization ---
    if not isinstance(input_grid, list) or not input_grid:
        # print("Warning: Input grid is not a list or is empty.")
        return input_grid # Return original for invalid input format

    if len(input_grid) < 1:
         # print("Warning: Input grid has no rows.")
         return input_grid # Return original

    if len(input_grid) > 1:
        # print("Warning: Input grid has more than one row. This function expects a single row. Returning original.")
        return input_grid # This task seems constrained to 1 row based on examples

    if not isinstance(input_grid[0], list):
         # print("Warning: First element of input grid is not a list.")
         return input_grid # Return original for malformed input

    # Convert the first (and only) row to a NumPy array for efficient processing
    input_row = np.array(input_grid[0])
    # Create a copy of the input row to modify for the output
    output_row = input_row.copy()

    # --- Find the Span and Singleton Position ---
    # Call the helper function to identify the relevant pattern components
    span_start, span_end, singleton_pos = _find_span_and_singleton_pos(output_row) # Use output_row for analysis is fine as it's a copy

    # If the expected pattern (contiguous span, 2 colors, singleton at end) isn't found,
    # the helper returns None. In this case, return the original grid unchanged.
    if span_start is None:
        # print("Pattern not found. Returning original grid.") # Optional debug message
        return input_grid

    # --- Extract and Rotate the Span ---
    # Extract the sequence of pixels within the identified span from the *output* row (which we will modify)
    span_sequence = output_row[span_start : span_end + 1]

    # Perform circular shift (roll) based on the singleton's original position
    rotated_sequence = None
    if singleton_pos == 'left':
        # If singleton was on the left, roll the sequence LEFT by 1
        # Example: [S, B, B] -> [B, B, S] (roll amount = -1)
        # print(f"Debug: Rolling left (amount -1) on sequence: {span_sequence.tolist()}")
        rotated_sequence = np.roll(span_sequence, -1)
    elif singleton_pos == 'right':
        # If singleton was on the right, roll the sequence RIGHT by 1
        # Example: [B, B, S] -> [S, B, B] (roll amount = 1)
        # print(f"Debug: Rolling right (amount 1) on sequence: {span_sequence.tolist()}")
        rotated_sequence = np.roll(span_sequence, 1)
    # No else needed as singleton_pos is guaranteed 'left' or 'right' if span_start is not None

    # --- Update Output Grid ---
    # Place the rotated sequence back into the output row at the original span location
    if rotated_sequence is not None:
         # print(f"Debug: Placing rotated sequence {rotated_sequence.tolist()} into slice {span_start}:{span_end + 1}")
         output_row[span_start : span_end + 1] = rotated_sequence
    else:
         # Should not happen if logic above is correct
         # print("Error: Rotation failed unexpectedly.")
         return input_grid # Return original if rotation somehow failed

    # --- Format and Return Output ---
    # Convert the modified numpy row back to a list
    output_list = output_row.tolist()
    # Wrap the list in another list to match the required output format [[]]
    output_grid = [output_list]

    return output_grid