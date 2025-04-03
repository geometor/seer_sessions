import numpy as np

"""
The transformation identifies a single maroon pivot (9). It finds the contiguous block 
of a single non-white, non-maroon color located to the left of the pivot, possibly 
separated by a gap of white pixels (0). The size of this 'left gap' is measured.

An output grid of the same size is created, filled with white (0). The pivot (9) is 
placed at its original index. 

A 'right gap' size is calculated: if the identified colored block started at index 0 
in the input, the 'right gap' size equals the 'left gap' size. Otherwise (if the block 
started after index 0, or if no block was found), the 'right gap' size is the 
'left gap' size plus one.

Finally, the identified colored block (if found) is placed in the output grid, starting 
immediately after this calculated 'right gap' (i.e., starting at index: 
pivot_index + 1 + right_gap_size). All other positions remain white (0).
"""

def find_pivot(grid_np):
    """Finds the index of the pivot color (9). Returns -1 if not found."""
    # Use np.where to find indices where the value is 9
    pivot_indices = np.where(grid_np == 9)[0]
    # Expect exactly one pivot based on examples
    if len(pivot_indices) == 1:
        return int(pivot_indices[0]) # Return the index as an integer
    else:
        # Return -1 if zero or more than one pivot is found
        return -1

def find_object_and_left_gap(grid_np, pivot_index):
    """
    Finds the object (contiguous non-white, non-pivot block) and the gap 
    to the left of the pivot.
    Returns the object pixels (list), object start index, and the left gap size.
    Returns (None, -1, left_gap_size) if no valid object is found adjacent to the gap.
    """
    object_pixels = []
    object_start_index = -1
    left_gap_size = 0

    # 1. Calculate left_gap_size by scanning left from the pivot
    current_index = pivot_index - 1
    while current_index >= 0 and grid_np[current_index] == 0:
        left_gap_size += 1
        current_index -= 1

    # 2. Find the object immediately left of the calculated gap
    # current_index is now at the potential last pixel of the object, or < 0
    object_found = False
    if current_index >= 0:
        # Get the color of the potential object pixel
        object_color = grid_np[current_index]
        # Check if the color is valid (not white 0, not pivot 9)
        if object_color != 0 and object_color != 9:
            # Scan left to find the full extent of the object and collect its pixels
            obj_idx = current_index
            while obj_idx >= 0 and grid_np[obj_idx] == object_color:
                # Prepend pixels to maintain the correct order
                object_pixels.insert(0, grid_np[obj_idx]) 
                object_start_index = obj_idx # Update start index as we move left
                obj_idx -= 1
            object_found = True # Mark that a valid object was found

    # Return results based on whether an object was found
    if not object_found:
        # Return the calculated gap size even if no object is found
        return None, -1, left_gap_size
    else:
        # Return the object details and the gap size
        return object_pixels, object_start_index, left_gap_size

def transform(input_grid):
    """
    Applies the pivot-mirror transformation with conditional gap logic.
    """
    # Convert input list to a numpy array for efficient processing
    input_np = np.array(input_grid)
    input_len = len(input_np)

    # Initialize output_grid as a numpy array of the same size, filled with 0s (white)
    output_grid = np.zeros(input_len, dtype=int)

    # Locate the pivot (maroon pixel, 9)
    pivot_index = find_pivot(input_np)

    # Handle case where pivot is not found (though unlikely based on examples)
    if pivot_index == -1:
        # print("Warning: Pivot (9) not found in input.") # Optional warning
        return output_grid.tolist() # Return the empty grid as a list

    # Place the pivot in the output grid at its original position
    # Check index validity just in case
    if 0 <= pivot_index < input_len:
        output_grid[pivot_index] = 9
    else:
        # This case should ideally not be reached if find_pivot works correctly
        # print("Error: Invalid pivot index calculated.") # Optional error message
        return np.zeros(input_len, dtype=int).tolist() # Return empty grid on error

    # Find the movable object block and the size of the gap to the left of the pivot
    movable_object_pixels, object_start_index, left_gap_size = find_object_and_left_gap(input_np, pivot_index)

    # Calculate the size of the gap to be placed on the right side based on the conditional rule
    # The condition checks if an object was found AND it started at index 0
    starts_at_index_zero = (movable_object_pixels is not None and object_start_index == 0)
    right_gap_size = left_gap_size if starts_at_index_zero else left_gap_size + 1

    # Place the object in the output grid if one was found
    if movable_object_pixels is not None:
        object_len = len(movable_object_pixels)
        # Calculate the starting position for the object in the output grid
        # It starts after the pivot (index + 1) and after the right gap
        output_object_start_index = pivot_index + 1 + right_gap_size

        # Place the object pixels into the output grid, ensuring they stay within bounds
        for i in range(object_len):
            output_index = output_object_start_index + i
            # Check if the calculated index is within the grid's boundaries
            if 0 <= output_index < input_len:
                output_grid[output_index] = movable_object_pixels[i]
            else:
                # Object placement goes out of bounds, stop placing further pixels
                # This prevents errors and implicitly truncates the object if needed.
                # print(f"Warning: Object placement truncated at index {output_index}.") # Optional warning
                break

    # The output_grid already contains the pivot and the moved object (if any).
    # The rest is filled with 0s (white), correctly representing the background and gaps.
    
    # Convert the numpy array back to a list for the standard ARC output format
    return output_grid.tolist()