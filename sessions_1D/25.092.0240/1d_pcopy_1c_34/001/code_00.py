import numpy as np

"""
Identifies the first contiguous sequence of a non-background color (the pattern)
in the input row.
Scans the input grid starting immediately after this initial pattern.
When a pixel matching the pattern's color is found at index `i` during the scan,
it replaces the segment in the *output* grid starting at index `i-1`
(one position before the found pixel) and extending for the pattern's length
with the pattern sequence itself.
Replacements happen on a copy of the grid, referencing the original input
for marker locations. Boundary conditions are handled, ensuring replacements
do not exceed the grid width.
"""

def find_first_pattern(grid):
    """
    Finds the first contiguous block of non-zero color in a 1D grid.

    Args:
        grid (np.array): A 1D numpy array representing the input row.

    Returns:
        tuple: (pattern_color, pattern_start_index, pattern_length, pattern_sequence)
               Returns (None, -1, 0, None) if no pattern (non-zero color) is found.
    """
    pattern_color = 0
    pattern_start_index = -1
    pattern_length = 0
    pattern_sequence = []

    # Find the start index and color of the pattern
    for i, pixel in enumerate(grid):
        if pixel != 0:  # Assuming 0 is the background color
            pattern_color = pixel
            pattern_start_index = i
            break

    # If no non-zero pixel found, return None for pattern details
    if pattern_start_index == -1:
        return None, -1, 0, None

    # Find the length and sequence of the pattern starting from pattern_start_index
    for j in range(pattern_start_index, len(grid)):
        if grid[j] == pattern_color:
            pattern_length += 1
            pattern_sequence.append(grid[j])
        else:
            # Stop when the color changes or grid ends
            break

    # Convert pattern sequence to numpy array for easier slicing later
    return pattern_color, pattern_start_index, pattern_length, np.array(pattern_sequence)

def transform(input_grid_str):
    """
    Transforms the input grid string based on the pattern replication rule.

    Args:
        input_grid_str (str): A space-separated string of integers representing the input grid row.

    Returns:
        str: A space-separated string of integers representing the transformed output grid row.
    """
    # --- Input Parsing ---
    try:
        # Convert the space-separated string input into a numpy array of integers
        input_grid = np.array([int(x) for x in input_grid_str.split()], dtype=int)
    except ValueError:
        # Handle potential errors like empty string or non-integer values
        return "" # Return empty string for invalid input format

    if len(input_grid) == 0:
        return "" # Return empty string if input grid is empty

    grid_width = len(input_grid)

    # --- Pattern Identification ---
    # Find the first contiguous block of non-background color
    pattern_color, pattern_start_index, pattern_length, pattern_sequence = find_first_pattern(input_grid)

    # If no pattern is found (e.g., all zeros) or the pattern has zero length,
    # return the original grid string unchanged.
    if pattern_color is None or pattern_length == 0:
        return " ".join(map(str, input_grid))

    # --- Transformation ---
    # Initialize the output grid as a copy of the input grid.
    # Modifications will be made to this copy.
    output_grid = input_grid.copy()

    # Define the starting point for scanning for markers.
    # Scan begins immediately after the identified pattern ends.
    scan_start_index = pattern_start_index + pattern_length

    # Iterate through the *original* input grid from the scan start index
    for i in range(scan_start_index, grid_width):
        # Check if the pixel at the current index `i` matches the pattern's color
        if input_grid[i] == pattern_color:
            # This pixel is a marker. Calculate where the replacement should start.
            # The replacement starts one position *before* the marker index.
            start_replace = i - 1

            # Basic sanity check: Ensure the replacement start index is valid.
            # (Should always be >= 0 given scan_start_index logic, but good practice)
            if start_replace < 0:
                continue # Should not happen in this task's logic

            # Calculate the theoretical end index for the replacement (exclusive)
            # end_replace = start_replace + pattern_length

            # Determine the actual portion of the pattern sequence to insert,
            # respecting the grid boundary. Calculate how many elements fit.
            effective_pattern_length = min(pattern_length, grid_width - start_replace)

            # Get the sub-sequence of the pattern that will actually be inserted
            pattern_to_insert = pattern_sequence[:effective_pattern_length]

            # Perform the replacement in the output grid if there's a valid slice to insert
            if effective_pattern_length > 0:
                # Replace the slice in output_grid from start_replace up to
                # start_replace + effective_pattern_length with the pattern_to_insert.
                output_grid[start_replace : start_replace + effective_pattern_length] = pattern_to_insert

    # --- Output Formatting ---
    # Convert the final transformed numpy array back to a space-separated string
    output_grid_str = " ".join(map(str, output_grid))
    return output_grid_str