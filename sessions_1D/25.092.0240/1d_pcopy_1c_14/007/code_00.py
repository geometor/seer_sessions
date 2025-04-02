import numpy as np
import math

"""
Processes the input grid row by row. For each row:
1. Identifies all contiguous horizontal blocks (objects) of non-white pixels.
2. Determines the largest object in the row based on width, designating it as the 'pattern' for that row. If there's a tie for the largest size, the one appearing earliest (leftmost start index) is chosen.
3. Finds all single-pixel objects (width=1) within the same row that share the same color as the row's pattern.
4. Creates a copy of the row to store modifications.
5. Replaces each identified single-pixel object in the copied row with a copy of the pattern, ensuring the pattern is centered over the original pixel's position.
6. Handles boundary conditions: if placing the pattern causes it to extend beyond the row's edges, the pattern is clipped accordingly so only the overlapping part is written.
7. The original pattern object location remains unchanged in the input but can be overwritten in the output if a target replacement overlaps its position.
8. Returns a new grid composed of these potentially modified rows, having the same dimensions as the input grid. If a row has no non-white objects, or no single-pixel targets matching the pattern color, it remains unchanged in the output.
"""

def find_objects_1d(grid_1d):
    """
    Finds contiguous blocks of non-white pixels in a 1D NumPy array (a row).

    Args:
        grid_1d: A 1D NumPy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        with keys: 'color', 'size' (width), 'start' (column index), 'end' (column index). 
        Returns an empty list if the input row is empty or contains only 
        background pixels (color 0).
    """
    if grid_1d is None or grid_1d.size == 0:
        return []

    objects = []
    in_object = False
    current_object = {}
    for i, pixel in enumerate(grid_1d):
        # Ensure pixel is a standard Python int for comparisons
        pixel_val = pixel.item() 
        
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
                in_object = True # Still in an object (the new one)
        elif pixel_val == 0 and in_object: # End of an object (hit white pixel)
            in_object = False
            objects.append(current_object)
            current_object = {}
        # If pixel is 0 and not in_object, do nothing

    # If the row ends while inside an object, add the last object
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
        return [] # Handle empty input list
    if not all(isinstance(row, list) for row in input_grid):
         # Handle cases where input is not list of lists (e.g., list of ints)
         return input_grid # Return input unmodified as a safe default

    try:
        # Convert input to NumPy array for efficient processing
        input_np = np.array(input_grid, dtype=int)
    except ValueError:
        # Handle potential error if rows have different lengths (ragged array)
        # Returning original might be safest without more specs
        return input_grid 
        
    output_np = input_np.copy() # Create a copy to modify for the output
    
    # Handle empty grid (e.g., [[]])
    if input_np.size == 0:
       # If input was [[]], numpy might make shape (1,0). 
       # Return [[]] to match potential expectation.
       if len(input_grid) == 1 and len(input_grid[0]) == 0:
           return [[]]
       # Otherwise return empty list for input like []
       return []
       
    height, width = input_np.shape
    
    # Handle grid with width 0 (e.g. [[], []])
    if width == 0:
        return [[] for _ in range(height)] # Return list of empty lists


    # --- Process Each Row Independently ---
    for r in range(height):
        # Extract the current row from the original input
        # This ensures subsequent pattern searches use the unmodified row
        row_np_original = input_np[r, :] 
        
        # --- Find Objects in the Current Row ---
        objects = find_objects_1d(row_np_original)

        # If no non-white objects exist in this row, skip to the next row
        # The output row already contains the original row data from the initial copy
        if not objects:
            continue

        # --- Identify Pattern and Targets for the Row ---
        # Find the object(s) with the maximum size
        max_size = 0
        for obj in objects:
            if obj['size'] > max_size:
                max_size = obj['size']
        
        # Filter to get all objects with max_size
        largest_objects = [obj for obj in objects if obj['size'] == max_size]

        # If multiple largest objects exist, choose the one with the smallest 'start' index
        # (This handles ties consistently)
        if not largest_objects: # Should not happen if objects is not empty
             continue 
        pattern_object_info = min(largest_objects, key=lambda obj: obj['start'])

        pattern_color = pattern_object_info['color']
        pattern_size = pattern_object_info['size']
        pattern_start = pattern_object_info['start']
        pattern_end = pattern_object_info['end']

        # Extract the actual pixel sequence of the pattern from the original row
        # Check bounds just in case, though find_objects should be correct
        if 0 <= pattern_start <= pattern_end < width:
             pattern_sequence = row_np_original[pattern_start : pattern_end + 1]
        else:
             # Should not happen with correct find_objects_1d
             continue # Skip row if pattern indices are invalid

        # Identify target objects: single pixels (size 1) with the same color as the pattern
        target_objects_indices = [
            obj['start'] for obj in objects
            if obj['size'] == 1 and obj['color'] == pattern_color
        ]
        
        # If no targets found, no changes needed for this row
        if not target_objects_indices:
            continue

        # --- Perform Replacements in the Output Row ---
        # Operate on the corresponding row in the output_np array
        row_to_modify = output_np[r, :]
        
        for target_index in target_objects_indices:
            # Calculate the ideal start column for placing the pattern, centered on target_index
            # math.floor is used for centering consistency, especially with even pattern sizes
            start_col = target_index - math.floor(pattern_size / 2)
            
            # Calculate the ideal end column (exclusive)
            end_col = start_col + pattern_size

            # --- Boundary Condition Handling (Clipping) ---
            # Determine the actual slice of the output row to modify (destination)
            dest_start = max(0, start_col)
            dest_end = min(width, end_col)

            # Determine the corresponding slice of the pattern sequence to use (source)
            # src_start is how many pixels to skip from the beginning of pattern_sequence
            src_start = max(0, -start_col) 
            # src_end is the index in pattern_sequence corresponding to dest_end
            # It's calculated based on how much the pattern hangs off the right edge
            src_end = pattern_size - max(0, end_col - width)
            
            # Ensure the calculated slices are valid and represent a non-empty segment
            if dest_start < dest_end and src_start < src_end:
                # Get the actual segment of the pattern to place
                pattern_segment = pattern_sequence[src_start:src_end]
                
                # Check if the lengths match (they should if logic is correct)
                if len(pattern_segment) == (dest_end - dest_start):
                     # Place the potentially clipped part of the pattern sequence
                     # into the corresponding row of the output grid
                     row_to_modify[dest_start:dest_end] = pattern_segment
                # else: Optional: add error handling/logging if lengths mismatch


    # --- Format Output ---
    # Convert the final NumPy array back to a list of lists
    return output_np.tolist()