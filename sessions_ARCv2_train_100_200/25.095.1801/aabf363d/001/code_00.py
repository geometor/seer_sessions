"""
Identifies a 'marker' color (appears once) and a 'target' color (most frequent non-zero color) in the input grid.
Creates an output grid where all instances of the 'target' color are replaced by the 'marker' color,
and the original cell containing the 'marker' color is replaced by 0 (background).
Background cells (0) remain unchanged.
"""

import numpy as np
from collections import Counter

def find_marker_and_target_colors(grid: np.ndarray) -> tuple[int, int]:
    """
    Identifies the marker color (occurs once) and target color (most frequent non-zero, excluding marker).

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple containing (marker_color, target_color).
    """
    # Flatten the grid and filter out zeros
    non_zero_elements = grid[grid != 0]

    if non_zero_elements.size == 0:
        # Handle case with no non-zero elements if necessary, though unlikely based on examples
        return -1, -1 # Indicate error or default

    # Count occurrences of each non-zero element
    counts = Counter(non_zero_elements)

    marker_color = -1
    target_color = -1
    max_freq = 0

    # Find the marker color (frequency 1)
    for color, count in counts.items():
        if count == 1:
            marker_color = color
            break # Assume only one marker color based on description

    # Find the target color (most frequent, excluding the marker)
    for color, count in counts.items():
        if color != marker_color:
            if count > max_freq:
                max_freq = count
                target_color = color

    # Handle edge cases like only marker color present
    if target_color == -1 and marker_color != -1 and len(counts) == 1:
         # If only the marker color exists, there's no target to replace.
         # This case might need clarification based on desired behavior.
         # For now, let's assume target requires frequency > 1 or > marker freq.
         pass # No target color found based on criteria

    return marker_color, target_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on replacing the target color with the marker color
    and zeroing out the original marker position.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Convert input to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Identify the marker and target colors
    marker_color, target_color = find_marker_and_target_colors(input_np)

    # Check if colors were found successfully (handle potential edge cases)
    if marker_color == -1 or target_color == -1:
        # If marker or target not found as expected, return a copy or handle error
        # Based on examples, they should always be present.
        # Returning a copy preserves the input if rules don't apply.
        print("Warning: Marker or Target color not identified as expected.")
        return input_np.tolist()


    # Initialize output_grid as a copy of the input grid
    output_np = np.copy(input_np)

    # Perform transformations using boolean indexing for efficiency

    # Find where the input grid equals the target color
    target_mask = (input_np == target_color)
    # Replace those locations in the output grid with the marker color
    output_np[target_mask] = marker_color

    # Find where the input grid equals the marker color
    marker_mask = (input_np == marker_color)
    # Replace that location in the output grid with 0 (background)
    output_np[marker_mask] = 0

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid