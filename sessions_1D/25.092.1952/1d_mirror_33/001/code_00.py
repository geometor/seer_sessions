"""
Reflects a contiguous block of non-white, non-maroon pixels across a single maroon pivot pixel in a 1D grid (single row), maintaining the separation distance.

1.  Find the index of the maroon pixel (9), the pivot.
2.  Find the contiguous block of non-white (0) and non-maroon pixels. Record its color, start index, and end index.
3.  Calculate the distance (number of white pixels) between the block and the pivot.
4.  Determine if the block is to the left or right of the pivot.
5.  Calculate the new starting position for the block on the opposite side of the pivot, maintaining the distance.
6.  Create an output grid filled with white (0).
7.  Place the pivot pixel (9) at its original position in the output grid.
8.  Place the colored block at its calculated new position in the output grid.
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index of the pivot pixel (9)."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i
    return -1 # Should not happen based on task description

def find_object(grid_1d, pivot_index):
    """Finds the start index, end index, and color of the movable object."""
    object_color = -1
    object_start = -1
    object_end = -1
    in_object = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 9: # Found a pixel of the object
            if not in_object:
                object_color = pixel
                object_start = i
                in_object = True
            object_end = i # Keep updating end index while in object
        elif in_object: # Just exited the object
            break # Stop searching once the object is found and passed

    if object_start == -1: # Handle case where object might be at the very end
        # Re-scan if not found in the first pass (e.g., object ends at grid end)
        # This simple loop actually covers this, but explicit check might be needed
        # for more complex cases. For this task, the above loop should suffice.
        pass

    return object_start, object_end, object_color


def transform(input_grid):
    """
    Transforms the input grid by reflecting the colored object across the pivot.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the transformed 1D output grid.
    """
    # Ensure input is treated as a 1D list/array
    if isinstance(input_grid[0], list): # Handle potential [[...]] format
         grid_1d = np.array(input_grid[0])
    else:
         grid_1d = np.array(input_grid) # Assume already flat list

    grid_size = len(grid_1d)
    output_grid = np.zeros(grid_size, dtype=int) # Initialize with white (0)

    # 1. Find the pivot
    pivot_index = find_pivot(grid_1d)
    if pivot_index == -1:
        # Handle error: Pivot not found (though examples guarantee one)
        return input_grid # Or raise an error

    # 2. Place the pivot in the output
    output_grid[pivot_index] = 9

    # 3. Find the object
    object_start, object_end, object_color = find_object(grid_1d, pivot_index)
    if object_start == -1:
         # Handle error: Object not found (though examples guarantee one)
         return output_grid.tolist() # Return grid with only pivot

    object_length = object_end - object_start + 1

    # 4. Calculate distance and determine relative position
    distance = 0
    is_left = False
    if object_end < pivot_index: # Object is to the left
        is_left = True
        distance = pivot_index - object_end - 1
    else: # Object is to the right
        is_left = False
        distance = object_start - pivot_index - 1

    # Ensure distance is non-negative (can be 0 if adjacent)
    distance = max(0, distance)

    # 5. Calculate new position
    new_object_start = -1
    if is_left:
        # Move to the right
        new_object_start = pivot_index + distance + 1
    else:
        # Move to the left
        new_object_start = pivot_index - distance - object_length

    # 6. Place the object in the output grid
    new_object_end = new_object_start + object_length
    if 0 <= new_object_start < grid_size and 0 <= new_object_end <= grid_size:
        output_grid[new_object_start:new_object_end] = object_color
    else:
        # Handle error: Calculated position is out of bounds
        # This shouldn't happen if input follows the pattern
        print(f"Warning: Calculated object position out of bounds.")
        print(f"Pivot: {pivot_index}, OldStart: {object_start}, OldEnd: {object_end}, Dist: {distance}, Len: {object_length}, NewStart: {new_object_start}")


    # Return as a flat list, matching input/output format
    return output_grid.tolist()