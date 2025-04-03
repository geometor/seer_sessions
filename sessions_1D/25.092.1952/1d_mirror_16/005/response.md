```python
import numpy as np

"""
Identify the maroon pivot (9). Find the contiguous colored block and the white gap to its left. 
Create a new grid. Place the pivot at its original position. Calculate the right gap size: 
if the block started at index 0, the right gap equals the left gap; otherwise, the right gap 
is the left gap plus one. Place the colored block to the right of the pivot, separated by 
this calculated right gap. Fill remaining space with white.
"""


def find_pivot(grid_np):
    """Finds the index of the pivot color (9). Returns -1 if not found."""
    pivot_indices = np.where(grid_np == 9)[0]
    if len(pivot_indices) == 1:
        return pivot_indices[0]
    else:
        # Handle cases where the pivot is not found or multiple pivots exist.
        # Based on examples, a single pivot should exist.
        return -1

def find_object_and_left_gap(grid_np, pivot_index):
    """
    Finds the object (contiguous non-white, non-pivot block) and the gap 
    to the left of the pivot.
    Returns the object pixels (list), object start index, and the left gap size.
    Returns (None, -1, left_gap_size) if no valid object is found.
    """
    object_pixels = []
    object_start_index = -1
    left_gap_size = 0

    # 1. Calculate left_gap_size by scanning left from pivot
    current_index = pivot_index - 1
    while current_index >= 0 and grid_np[current_index] == 0:
        left_gap_size += 1
        current_index -= 1

    # 2. Find the object
    # current_index is now at the potential last pixel of the object, or < 0
    object_found = False
    if current_index >= 0:
        object_color = grid_np[current_index]
        # Check if the color is valid (not white 0, not pivot 9)
        if object_color != 0 and object_color != 9:
            # Scan left to find the start of the object and collect pixels
            obj_idx = current_index
            while obj_idx >= 0 and grid_np[obj_idx] == object_color:
                object_pixels.insert(0, grid_np[obj_idx]) # Prepend to keep order
                object_start_index = obj_idx
                obj_idx -= 1
            object_found = True

    if not object_found:
        # Return the calculated gap size even if no object is found
        return None, -1, left_gap_size
    else:
        return object_pixels, object_start_index, left_gap_size

def transform(input_grid):
    """
    Applies the pivot-mirror transformation with conditional gap logic.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid)
    input_len = len(input_np)

    # Initialize output_grid with white pixels (0)
    output_grid = np.zeros(input_len, dtype=int)

    # Locate the pivot
    pivot_index = find_pivot(input_np)

    # Handle case where pivot is not found (though unlikely based on examples)
    if pivot_index == -1:
        print("Warning: Pivot (9) not found in input.")
        return output_grid.tolist() # Return empty grid

    # Place the pivot in the output grid
    # Check index validity just in case, though find_pivot should ensure it's within bounds if found
    if 0 <= pivot_index < input_len:
        output_grid[pivot_index] = 9
    else:
        # This case should ideally not be reached if find_pivot works correctly
        print("Error: Invalid pivot index calculated.")
        return np.zeros(input_len, dtype=int).tolist() # Return empty grid on error

    # Find the object block and the gap to the left of the pivot
    movable_object_pixels, object_start_index, left_gap_size = find_object_and_left_gap(input_np, pivot_index)

    # Calculate the size of the gap on the right side based on the condition
    # The condition checks if an object was found AND it started at index 0
    starts_with_object = (movable_object_pixels is not None and object_start_index == 0)
    right_gap_size = left_gap_size if starts_with_object else left_gap_size + 1

    # Place the object in the output grid if one was found
    if movable_object_pixels is not None:
        object_len = len(movable_object_pixels)
        # Calculate the starting position for the object in the output grid
        output_object_start_index = pivot_index + 1 + right_gap_size

        # Place the object pixels into the output grid, checking boundaries
        for i in range(object_len):
            output_index = output_object_start_index + i
            # Check if the index is within the output grid bounds
            if 0 <= output_index < input_len:
                output_grid[output_index] = movable_object_pixels[i]
            else:
                # Object placement goes out of bounds, stop placing further pixels
                # print(f"Warning: Object placement truncated at index {output_index}.")
                break

    # The output_grid is already filled with 0s for background and the right gap.
    # Convert the numpy array back to a list for the final return format.
    return output_grid.tolist()

```