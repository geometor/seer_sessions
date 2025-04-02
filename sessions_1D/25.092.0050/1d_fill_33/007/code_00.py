"""
Transforms a single-row grid by finding two non-white 'marker' pixels and filling
the segment between them (inclusive) with the marker color. Pixels outside this
segment remain unchanged (white).
"""

import copy

def find_markers(row):
    """
    Finds the indices and color of non-white marker pixels in a row.

    Args:
        row: A list of integers representing a row of pixels.

    Returns:
        A tuple (marker_indices, marker_color) where:
        - marker_indices: A list of column indices where non-white pixels are found.
        - marker_color: The color (integer value) of the non-white pixels.
                       Returns 0 if no non-white pixels are found. Assumes all
                       non-white pixels found share the same color based on task constraints.
    """
    marker_indices = []
    marker_color = 0 # Default to background color (white)
    first_marker_found = False

    # Scan the row for non-white pixels
    for index, pixel in enumerate(row):
        if pixel != 0:  # Found a non-white pixel
            marker_indices.append(index)
            # Capture the color of the first marker found
            if not first_marker_found:
                marker_color = pixel
                first_marker_found = True
            # Note: Based on problem constraints, we don't need to check
            # if subsequent markers have the same color, but in a more
            # general case, a check `elif pixel != marker_color:` might be needed.

    return marker_indices, marker_color

def transform(input_grid):
    """
    Applies the segment fill transformation to the input grid.

    Args:
        input_grid: A list containing a single list (the row) of integers (pixels).
                    Expected to conform to task constraints: single row, exactly two
                    non-white pixels of the same color.

    Returns:
        A list containing a single list (the transformed row) of integers.
        Returns a deep copy of the input if the expected format or marker
        count constraint is not met.
    """

    # --- Input Validation ---
    # Check if input is a list containing exactly one list (the row)
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Return a copy if the format is not [[row_data]]
        return copy.deepcopy(input_grid)

    # --- Initialization ---
    # Extract the single row from the input grid
    input_row = input_grid[0]

    # --- Step 1 & 2: Find markers, their color, and indices ---
    # Use the helper function to identify non-white pixels
    marker_indices, marker_color = find_markers(input_row)

    # --- Step 3: Verify exactly two markers ---
    # Check if the number of found markers matches the task constraint
    if len(marker_indices) != 2:
        # If not exactly two markers, return an unmodified copy of the input
        return copy.deepcopy(input_grid)

    # --- Step 4: Determine segment boundaries ---
    # Find the minimum and maximum index among the markers to define the segment
    start_index = min(marker_indices)
    end_index = max(marker_indices) # Using min/max handles cases where markers might be found out of order

    # --- Step 5: Create output grid (copy of input) ---
    # Create a deep copy to modify, ensuring the original input is untouched
    output_grid = copy.deepcopy(input_grid)
    # Get a reference to the row within the copied structure
    output_row = output_grid[0]

    # --- Step 6 & 7: Fill the segment ---
    # Iterate through the column indices from start_index to end_index (inclusive)
    for i in range(start_index, end_index + 1):
        # Set the pixel color in the output row to the identified marker color
        output_row[i] = marker_color
        
    # Pixels outside this loop range implicitly retain their original color
    # because we started with a copy of the input row.

    # --- Step 8: Return the modified grid ---
    return output_grid