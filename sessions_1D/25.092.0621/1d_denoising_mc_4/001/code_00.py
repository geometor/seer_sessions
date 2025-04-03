import numpy as np
from collections import Counter

"""
Identifies the contiguous segment of non-white (non-zero) pixels in the input row.
Determines the most frequent color within this segment (the dominant color).
Replaces all pixels within the identified segment in the output grid with this dominant color.
Keeps the surrounding white (zero) pixels unchanged.
"""

def find_non_white_segment(row):
    """Finds the start and end indices of the first contiguous non-white segment."""
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None, None  # No non-white pixels
    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    # Ensure it's contiguous - check if all indices between start and end are present
    # Although the examples seem to guarantee this, it's safer.
    # However, the core logic just needs the start and end of the *span* containing non-whites.
    return start_index, end_index

def find_dominant_color(segment):
    """Finds the most frequent color in a given segment."""
    if len(segment) == 0:
        return 0 # Or handle as an error/edge case, default to white if segment is empty?
    
    # Filter out any potential zeros if the definition is strictly non-white *within* the segment span
    non_zero_segment = segment[segment != 0]
    if len(non_zero_segment) == 0:
         # This case might occur if the segment span contains only zeros,
         # which contradicts find_non_white_segment logic, but handle defensively.
         # Or if the original logic intended to include zeros in the count if they fall within the span.
         # Based on description "within this segment", let's stick to non-zeros found.
         # If no non-zeros exist in the identified span, perhaps return the first color encountered?
         # Let's stick to the most frequent non-zero. If none, maybe default?
         # Revisit based on examples: Examples clearly show segments *start* and *end* with non-whites.
         # Let's assume the segment passed here will contain non-whites.
         return 0 # Fallback, though unlikely given segment definition.

    counts = Counter(non_zero_segment)
    # Find the color with the maximum count. If ties, Counter returns one arbitrarily.
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Transforms the input grid by finding the dominant color in the non-white
    segment and making the entire segment that color.
    """
    # Assuming input is always 1xN or Nx1, but examples are 1xN.
    # Let's handle the general case but expect 1 row based on examples.
    if input_grid.shape[0] != 1:
         # This specific solution is tailored for 1D rows as per examples.
         # Could be extended, but sticking to observed pattern.
         print("Warning: This solution expects a 1-row input grid based on examples.")
         # Attempt to process the first row anyway for robustness.
         # Or return input_grid unchanged if assumption is strict.
         # return input_grid # Stricter approach
         
    # Work with the first row (index 0)
    input_row = input_grid[0, :]
    output_row = np.copy(input_row) # Start with a copy

    # 1. Identify the contiguous segment of non-white pixels.
    start_index, end_index = find_non_white_segment(input_row)

    # Proceed only if a non-white segment was found
    if start_index is not None and end_index is not None:
        # 2. Extract the segment (including any potential zeros within the span)
        segment = input_row[start_index : end_index + 1]

        # 3. Determine the dominant color within the segment (ignoring zeros for dominance calculation)
        dominant_color = find_dominant_color(segment)

        # 4. Create the output row: Fill the segment span with the dominant color.
        output_row[start_index : end_index + 1] = dominant_color

    # Reshape the output row back into the original grid shape (e.g., 1xN)
    output_grid = output_row.reshape(input_grid.shape)

    return output_grid