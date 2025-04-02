"""
Processes the input grid row by row. For each row:
1. Identifies all contiguous blocks (objects) of non-white pixels.
2. Determines the largest object in the row, designating it as the 'pattern' for that row.
3. Finds all single-pixel objects within the same row that share the same color as the row's pattern.
4. Creates a copy of the row.
5. Replaces each identified single-pixel object in the copied row with a copy of the pattern, ensuring the pattern is centered over the original pixel's position.
6. Handles boundary conditions: if placing the pattern causes it to extend beyond the row's edges, the pattern is clipped accordingly.
7. The original pattern object location remains unchanged unless it is overwritten by a replacement centered on a different target pixel.
8. Returns a new grid composed of these potentially modified rows, having the same dimensions as the input grid.
"""

import numpy as np
import math

def find_objects_1d(grid_1d):
    """
    Finds contiguous blocks of non-white pixels in a 1D NumPy array (a row).

    Args:
        grid_1d: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size', 'start', 'end'. Returns an empty list
        if the input is empty or contains only background pixels (color 0).
    """
    if grid_1d is None or grid_1d.size == 0:
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
                # No need to set in_object=True, it already is.
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
    Applies the row-wise pattern replacement transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # --- Input Validation and Initialization ---
    if not isinstance(input_grid, list) or not input_grid:
        return [] 
    if not all(isinstance(row, list) for row in input_grid):
         # Handle cases where input is not list of lists
         # Return input unmodified as a safe default, though error might be better
         return input_grid 

    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy() # Create a copy to modify
    height, width = input_np.shape

    # --- Process Each Row Independently ---
    for r in range(height):
        row_np = input_np[r, :] # Get the current row from the original input
        
        # Handle empty rows within the grid
        if row_np.size == 0:
            continue 

        # --- Find Objects in the Current Row ---
        objects = find_objects_1d(row_np)

        # If no non-white objects exist in this row, skip to the next row
        if not objects:
            continue

        # --- Identify Pattern and Targets for the Row ---
        # Use max with a default value in case objects is empty (safety check)
        pattern_object_info = max(objects, key=lambda obj: obj['size'], default=None)
        
        # This check is redundant due to the 'if not objects' check above, but safe
        if pattern_object_info is None:
            continue # Should not happen if objects list is not empty

        pattern_color = pattern_object_info['color']
        pattern_size = pattern_object_info['size']
        pattern_start = pattern_object_info['start']
        pattern_end = pattern_object_info['end']

        # Extract the actual pixel sequence of the pattern from the original row
        # Ensure indices are within bounds (should be guaranteed by find_objects_1d)
        if pattern_start >= 0 and pattern_end < width:
             pattern_sequence = row_np[pattern_start : pattern_end + 1]
        else:
             # Handle potential error case if find_objects_1d returned invalid indices
             continue # Skip this row if pattern indices are bad


        # Identify target objects: single pixels (size 1) with the same color as the pattern
        target_objects_indices = [
            obj['start'] for obj in objects
            if obj['size'] == 1 and obj['color'] == pattern_color
        ]

        # --- Perform Replacements in the Output Row ---
        # Note: Replacements are done on output_np[r, :]
        for target_index in target_objects_indices:
            # Calculate the ideal start index for placing the pattern so it's centered
            start_index = target_index - math.floor(pattern_size / 2)
            # Calculate the ideal end index (exclusive) for slicing
            end_index = start_index + pattern_size

            # --- Boundary Condition Handling (Clipping) ---
            # Determine the actual slice of the output row to modify (destination)
            dest_start = max(0, start_index)
            dest_end = min(width, end_index)

            # Determine the corresponding slice of the pattern sequence to use (source)
            src_start = max(0, -start_index) 
            src_end = pattern_size - max(0, end_index - width)
            
            # Ensure the calculated slices are valid before attempting replacement
            if dest_start < dest_end and src_start < src_end and src_end <= pattern_sequence.size:
                 # Ensure the source slice doesn't exceed the pattern sequence length
                effective_src_end = min(src_end, src_start + (dest_end - dest_start))

                if src_start < effective_src_end:
                    # Place the appropriate (potentially clipped) part of the pattern sequence
                    # into the corresponding row of the output grid
                    output_np[r, dest_start:dest_end] = pattern_sequence[src_start:effective_src_end]

    # --- Format Output ---
    # Convert the final NumPy array back to a list of lists
    return output_np.tolist()