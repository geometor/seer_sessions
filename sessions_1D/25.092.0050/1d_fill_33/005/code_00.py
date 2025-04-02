"""
Transforms a single-row grid by finding two non-white 'marker' pixels and filling
the segment between them (inclusive) with the marker color. Pixels outside this
segment remain unchanged (white).
"""

import copy
# No other specific libraries like numpy are strictly necessary for this logic,
# but copy is essential for creating a modifiable output without altering the input.

def find_markers(row):
    """
    Finds the indices and color of non-white marker pixels in a row.

    Args:
        row: A list of integers representing a row of pixels.

    Returns:
        A tuple (marker_indices, marker_color) where:
        - marker_indices: A list of column indices where non-white pixels are found.
        - marker_color: The color (integer value) of the non-white pixels.
                       Returns 0 if no non-white pixels are found or if multiple
                       different non-white colors are found (though the task
                       constraint implies this won't happen).
    """
    marker_indices = []
    marker_color = 0 # Default to background color (white)
    first_marker_found = False

    for index, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            marker_indices.append(index)
            if not first_marker_found:
                marker_color = pixel # Capture the color of the first marker found
                first_marker_found = True
            # Optional: Could add a check here to ensure all markers have the same color
            # elif pixel != marker_color:
            #    print("Warning: Found markers of different colors.")
            #    return [], 0 # Or handle error as appropriate

    return marker_indices, marker_color

def transform(input_grid):
    """
    Applies the segment fill transformation to the input grid.

    Args:
        input_grid: A list containing a single list (the row) of integers (pixels).
                    It's expected that the input row contains exactly two
                    non-white pixels, and they share the same color.

    Returns:
        A list containing a single list (the transformed row) of integers.
        Returns a deep copy of the input if the expected format or marker
        count is not met.
    """

    # --- Input Validation ---
    # Check if input is a list containing exactly one list (the row)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle unexpected input format, returning a copy as a safe default
        return copy.deepcopy(input_grid)

    input_row = input_grid[0]

    # --- Step 1 & 2: Find markers, their color, and indices ---
    # Use the helper function
    marker_indices, marker_color = find_markers(input_row)

    # --- Step 2 (cont.): Verify exactly two markers ---
    if len(marker_indices) != 2:
        # Handle case where the constraint of exactly two markers isn't met
        # Returning a copy is a reasonable default for ARC tasks
        return copy.deepcopy(input_grid)

    # --- Step 3: Determine segment boundaries ---
    # Find the minimum and maximum index among the markers
    start_index = min(marker_indices)
    end_index = max(marker_indices) # max() is robust even if indices were found out of order

    # --- Step 4: Create output grid (copy of input) ---
    output_grid = copy.deepcopy(input_grid)
    # Get a reference to the row within the copied structure to modify it
    output_row = output_grid[0]

    # --- Step 5 & 6: Fill the segment ---
    # Iterate through the indices from start to end (inclusive)
    for i in range(start_index, end_index + 1):
        # Set the pixel in the output row to the marker color
        output_row[i] = marker_color

    # --- Step 7 is implicit: Pixels outside the loop retain original color ---
    # --- Step 8: Return the modified grid ---
    return output_grid