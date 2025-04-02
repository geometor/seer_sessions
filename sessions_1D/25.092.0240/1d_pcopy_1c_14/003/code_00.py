"""
Identify the largest contiguous block of non-white pixels (the 'pattern') in the first row of the input grid.
Find all single non-white pixels in that row that have the same color as the pattern.
Replace each of these single pixels with a copy of the pattern, centering the pattern over the original pixel's position. Handle boundary conditions where the pattern might extend beyond the grid edges.
Other pixels, including the original pattern object location (unless overwritten by another replacement), remain unchanged.
Return the modified first row within a list-of-lists structure.
"""

import numpy as np
import math

def find_objects_1d(grid_1d):
    """
    Finds contiguous blocks of non-white pixels in a 1D grid (NumPy array).

    Args:
        grid_1d: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size', 'start', 'end'. Returns an empty list
        if the input is empty or contains only background pixels.
    """
    if grid_1d is None or len(grid_1d) == 0:
        return []

    objects = []
    in_object = False
    current_object = {}
    for i, pixel in enumerate(grid_1d):
        pixel_val = pixel.item() # Extract scalar value for comparison
        if pixel_val != 0 and not in_object: # Start of a new non-white object
            in_object = True
            current_object = {'color': pixel_val, 'size': 1, 'start': i, 'end': i}
        elif pixel_val != 0 and in_object: # Continuing an object
            if pixel_val == current_object['color']: # Same color, extend object
                current_object['size'] += 1
                current_object['end'] = i
            else: # Different non-white color, end previous object, start new one
                objects.append(current_object)
                current_object = {'color': pixel_val, 'size': 1, 'start': i, 'end': i}
        elif pixel_val == 0 and in_object: # End of an object (hit white pixel)
            in_object = False
            objects.append(current_object)
            current_object = {}
        # If pixel is 0 and not in_object, do nothing

    # If the grid ends while inside an object, add the last object
    if in_object:
        objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the described pattern replacement rule,
    operating only on the first row.

    Args:
        input_grid: A list containing list(s) representing the grid rows.
                    Expected format: [[row1_data], [row2_data], ...] or just [[row1_data]].

    Returns:
        A list containing a single list representing the transformed first row,
        or the original input if input is invalid or no transformation is applicable.
    """
    # --- Input Validation ---
    if not isinstance(input_grid, list) or not input_grid:
        # Handle empty input list []
        return []
    if not isinstance(input_grid[0], list):
         # Handle cases where input is not list of lists, e.g. [1, 2, 3]
         # Depending on strictness, could raise error or return input
         return input_grid # Or maybe [[ ]] or [] ? Let's return input for now.
    
    # Handle empty first row [[]]
    if not input_grid[0]:
        return [[]]

    # --- Select and Prepare Data ---
    # Select the first row for processing
    grid_1d_list = input_grid[0]
    # Convert to NumPy array for easier processing
    grid_np = np.array(grid_1d_list, dtype=int)
    # Create a copy to modify for the output
    output_grid_np = grid_np.copy()
    grid_len = len(grid_np)

    # --- Find Objects ---
    # Find all non-white objects in the 1D grid
    objects = find_objects_1d(grid_np)

    # If no non-white objects exist, return the original first row (formatted)
    if not objects:
        return [output_grid_np.tolist()]

    # --- Identify Pattern and Targets ---
    # Identify the pattern object (the one with the largest size)
    # Use max with a default value in case objects is empty (though checked above)
    pattern_object_info = max(objects, key=lambda obj: obj['size'], default=None)
    
    # This check is redundant due to the 'if not objects' check above, but safe
    if pattern_object_info is None:
         return [output_grid_np.tolist()]

    pattern_color = pattern_object_info['color']
    pattern_size = pattern_object_info['size']
    pattern_start = pattern_object_info['start']
    pattern_end = pattern_object_info['end']

    # Extract the actual pixel sequence of the pattern from the original input grid
    pattern_sequence = grid_np[pattern_start : pattern_end + 1]

    # Identify target objects: single pixels (size 1) with the same color as the pattern
    target_objects_indices = [
        obj['start'] for obj in objects
        if obj['size'] == 1 and obj['color'] == pattern_color
    ]

    # --- Perform Replacements ---
    # Perform the replacement for each target object
    for target_index in target_objects_indices:
        # Calculate the ideal start index for placing the pattern so it's centered
        # The center pixel of the pattern (at index floor(pattern_size / 2) within the pattern)
        # should align with the target_index.
        start_index = target_index - math.floor(pattern_size / 2)

        # Calculate the ideal end index (exclusive) for slicing
        end_index = start_index + pattern_size

        # --- Boundary Condition Handling ---
        # Determine the actual slice of the output grid to modify (destination)
        dest_start = max(0, start_index)
        dest_end = min(grid_len, end_index)

        # Determine the corresponding slice of the pattern sequence to use (source)
        # Adjust source start if pattern placement starts before the grid (start_index < 0)
        src_start = max(0, -start_index)
        # Adjust source end if pattern placement ends after the grid (end_index > grid_len)
        src_end = pattern_size - max(0, end_index - grid_len)
        # --- End Boundary Handling ---

        # Ensure the calculated slices are valid before attempting replacement
        # (dest_start < dest_end) checks if there's any overlap with the grid
        # (src_start < src_end) checks if the calculated source slice is valid
        if dest_start < dest_end and src_start < src_end:
            # Place the appropriate (potentially clipped) part of the pattern sequence
            # into the output grid
            output_grid_np[dest_start:dest_end] = pattern_sequence[src_start:src_end]

    # --- Format Output ---
    # Return the modified grid in the required list-of-lists format
    return [output_grid_np.tolist()]