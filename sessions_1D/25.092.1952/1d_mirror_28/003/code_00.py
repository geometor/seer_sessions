"""
Identify the single maroon (9) pixel (pivot) and the contiguous block of non-white, non-maroon pixels (object) in the input 1D grid. Reflect the object across the pivot, maintaining the original distance (number of white pixels) between the object and the pivot. The pivot remains stationary, and the original location of the object becomes white (0).
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index of the pivot pixel (maroon, 9)."""
    pivot_indices = np.where(grid_1d == 9)[0]
    if len(pivot_indices) > 0:
        return pivot_indices[0]
    return -1 # Should not happen based on examples

def find_object(grid_1d):
    """Finds the start index, end index, color, and length of the movable object."""
    object_indices = np.where((grid_1d != 0) & (grid_1d != 9))[0]
    if len(object_indices) == 0:
        return -1, -1, -1, 0 # Object not found

    start_index = object_indices[0]
    end_index = object_indices[-1]
    
    # Verify contiguity: check if all indices between start and end are present
    # and that the color is consistent
    object_color = grid_1d[start_index]
    is_contiguous = True
    for i in range(start_index, end_index + 1):
        if grid_1d[i] != object_color:
            is_contiguous = False
            break
            
    if is_contiguous and len(object_indices) == (end_index - start_index + 1):
        length = end_index - start_index + 1
        return start_index, end_index, object_color, length
    else:
        # This handles cases where non-0/9 pixels might not form a single contiguous block
        # or have varying colors within the block, though not present in examples.
        print(f"Warning: Non-contiguous or multi-colored object detected at indices {object_indices}")
        # For simplicity based on examples, let's still return the first block found
        # A more robust solution might need clarification on how to handle multiple objects.
        # Let's assume the first contiguous block IS the object.
        
        # Re-scan to find the first contiguous block
        current_start = -1
        current_color = -1
        first_block = None # (start, end, color, length)
        
        for i, pixel in enumerate(grid_1d):
             if pixel != 0 and pixel != 9:
                 if current_start == -1: # Start of a potential block
                     current_start = i
                     current_color = pixel
                 elif pixel != current_color: # Color changed, previous block ended
                      if first_block is None:
                          first_block = (current_start, i-1, grid_1d[current_start], (i-1)-current_start + 1)
                      current_start = i # Start new block
                      current_color = pixel
             elif current_start != -1: # End of the block (found 0 or 9)
                 if first_block is None:
                      first_block = (current_start, i-1, current_color, (i-1)-current_start + 1)
                 current_start = -1 # Reset block tracking
        
        # Handle block ending at the grid edge
        if current_start != -1 and first_block is None:
             first_block = (current_start, len(grid_1d)-1, current_color, (len(grid_1d)-1)-current_start + 1)

        if first_block:
             return first_block
        else: # No valid object found
             return -1, -1, -1, 0
                 


def calculate_gap(obj_start, obj_end, pivot_index):
    """Calculates the gap size between the object and the pivot."""
    if obj_end < pivot_index: # Object is to the left
        return pivot_index - obj_end - 1
    elif obj_start > pivot_index: # Object is to the right
        return obj_start - pivot_index - 1
    else: # Should not happen if object and pivot don't overlap
        return -1 

def transform(input_grid):
    """
    Moves a contiguous block of colored pixels from one side of a stationary 
    maroon (9) pixel (pivot) to the other side, preserving the gap size.
    """
    # Ensure input is treated as a list of lists, get the first (only) row
    if not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        raise ValueError("Input grid must be a list of lists.")
    
    grid_1d = np.array(input_grid[0], dtype=int)
    grid_length = len(grid_1d)

    # Initialize output_grid as a 1D array of zeros (white)
    output_grid_1d = np.zeros(grid_length, dtype=int)

    # 1. Identify the pivot point (maroon pixel)
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
         print("Error: Pivot (9) not found.")
         return input_grid # Return original grid if pivot missing

    # Place pivot in output
    output_grid_1d[pivot_index] = 9

    # 2. Identify the movable object
    obj_start, obj_end, obj_color, obj_length = find_object(grid_1d)
    if obj_start == -1:
        print("Warning: Movable object not found. Returning grid with only pivot.")
        # Return grid with just the pivot placed
        output_grid = [output_grid_1d.tolist()]
        return output_grid

    # 3. Calculate the gap size in the input grid
    input_gap_size = calculate_gap(obj_start, obj_end, pivot_index)
    if input_gap_size < 0:
        print("Error: Could not determine gap between object and pivot.")
        return input_grid # Or handle error appropriately

    # 4. Determine new position based on reflection and preserved gap
    if obj_end < pivot_index: # Object was to the left, move to the right
        new_start_index = pivot_index + 1 + input_gap_size
    else: # Object was to the right, move to the left
        new_start_index = pivot_index - 1 - input_gap_size - obj_length + 1 # Calculate start based on where end should be

    new_end_index = new_start_index + obj_length - 1

    # 5. Place the movable object in the output grid at the new location
    # Check bounds before placing
    if 0 <= new_start_index < grid_length and 0 <= new_end_index < grid_length:
         output_grid_1d[new_start_index : new_end_index + 1] = obj_color
    else:
        # Handle case where object goes out of bounds (optional based on task constraints)
        print(f"Warning: New object placement ({new_start_index}-{new_end_index}) out of bounds for grid length {grid_length}.")
        # Decide how to handle: truncate? error? place partially? 
        # For now, we simply won't place it if it's fully out of bounds, 
        # or numpy slicing might handle partial placement implicitly if start/end are adjusted.
        # Let's explicitly clip indices to stay within bounds if any part overlaps.
        clip_start = max(0, new_start_index)
        clip_end = min(grid_length -1, new_end_index)
        offset_start = clip_start - new_start_index # How much the object start is shifted due to left clipping
        
        if clip_start <= clip_end : # Check if any part is within bounds after clipping
             # Create the object array and slice the part that fits
             object_segment = np.full(obj_length, obj_color, dtype=int)
             place_segment = object_segment[offset_start : offset_start + (clip_end - clip_start + 1)]
             output_grid_1d[clip_start : clip_end + 1] = place_segment


    # Convert back to list of lists format for ARC
    output_grid = [output_grid_1d.tolist()]

    return output_grid