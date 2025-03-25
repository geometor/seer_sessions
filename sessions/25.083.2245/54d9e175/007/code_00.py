"""
1.  **Examine First Row:** Analyze *only* the first row of the input grid.

2.  **Identify Segments:** Within this first row, locate horizontal segments. A segment is a contiguous sequence of digits that is either:
    *   Bounded on both sides by the digit '5'.
    *   Bounded on one side by the digit '5' and on the other side by the edge of the grid.
    *   Bounded on both sides by the edges of the grid (if no '5's are present).

3.  **Map Segments:** For each identified segment:
    *   Extract the sequence of digits within the segment, *excluding* the bounding '5's (or grid edges).
    *   Apply the following mapping to determine the replacement digit:
        *   If the sequence is `0, 1, 0`, the replacement digit is `6`.
        *   If the sequence is `0, 2, 0`, the replacement digit is `7`.
        *   If the sequence is `0, 3, 0`, the replacement digit is `8`.
        *   If the sequence is `0, 4, 0`, the replacement digit is `9`.

4.  **Transform First Row:** Create a transformed version of the first row. Replace all digits within each segment of the original first row with its corresponding replacement digit determined in the previous step.

5.  **Replicate and Output:** Create the final output grid by replicating the *transformed* first row three times. The height of the output grid will be three times the height of the input, but the transformation logic is based *solely* on segments found in the input grid's first row. Return this output.
"""

import numpy as np

def find_segments(row):
    """Finds horizontal segments in a row delimited by 5 or edges."""
    segments = []
    start = 0
    for i, val in enumerate(row):
        if val == 5:
            if i > start:
                segments.append((start, i))  # Store start and end indices
            start = i + 1
    if start < len(row):
        segments.append((start, len(row)))  # Store start and end indices
    return segments

def get_replacement(segment_values):
    """Determines the replacement digit based on the segment values."""
    if segment_values == [0, 1, 0]:
        return 6
    elif segment_values == [0, 2, 0]:
        return 7
    elif segment_values == [0, 3, 0]:
        return 8
    elif segment_values == [0, 4, 0]:
        return 9
    else:
        return None

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    input_grid = np.array(input_grid)
    first_row = input_grid[0]

    # Identify Segments in the first row
    segments = find_segments(first_row)

    # Transform the first row
    transformed_row = np.copy(first_row)
    for start, end in segments:
        segment_values = list(first_row[start:end])
        replacement = get_replacement(segment_values)
        if replacement is not None:
            transformed_row[start:end] = replacement

    # Replicate the transformed row
    output_grid = np.tile(transformed_row, (3, 1))

    return output_grid