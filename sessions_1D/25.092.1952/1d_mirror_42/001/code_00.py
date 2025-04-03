import numpy as np
from typing import List, Tuple, Optional

# Define colors for clarity
WHITE = 0
MAROON = 9

"""
Transforms a 1D grid based on the following rules:
1. Finds a single 'pivot' pixel (maroon, 9) and a single contiguous 'object' block of another color (non-white, non-maroon).
2. The pivot pixel's position remains unchanged in the output.
3. The object block is moved to the opposite side of the pivot pixel.
4. The distance (number of white pixels) between the object and the pivot is preserved on the new side.
5. All other pixels in the output grid are set to the background color (white, 0).
"""

def find_pixel(grid: List[int], color: int) -> Optional[int]:
    """Finds the index of the first occurrence of a given color."""
    try:
        return grid.index(color)
    except ValueError:
        return None

def find_object(grid: List[int], exclude_colors: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of pixels whose color is not in exclude_colors.
    Returns: Tuple of (start_index, end_index, color) or None if not found.
    """
    start_index = -1
    object_color = -1
    for i, pixel in enumerate(grid):
        if pixel not in exclude_colors:
            if start_index == -1: # Start of a potential object
                start_index = i
                object_color = pixel
            elif pixel != object_color: # End of the object (different color found)
                 # This case shouldn't happen based on task description (only one object)
                 # but good to handle. We assume the first block is *the* object.
                 return (start_index, i - 1, object_color)
        elif start_index != -1: # End of the object (excluded color found)
            return (start_index, i - 1, object_color)

    # Handle case where object goes to the end of the grid
    if start_index != -1:
        return (start_index, len(grid) - 1, object_color)

    return None # No object found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Input is assumed to be a 1xN grid (represented as a list of lists).
    """
    # Since ARC grids are 2D, but this task uses 1D, flatten the input
    # Handle potential numpy array input
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.flatten().tolist()
    elif isinstance(input_grid, list) and len(input_grid) == 1:
         input_list = input_grid[0]
    else:
         # Fallback or raise error if format is unexpected
         # For this specific task, assume it's a flat list if not NxM np array
         # or handle error more robustly depending on expected variations
         try:
            input_list = list(input_grid) # try casting if it looks 1D-like
            if any(isinstance(el, list) for el in input_list): # Check if it's actually nested
                 raise ValueError("Input grid format not recognized as 1D for this task.")
         except TypeError:
             raise ValueError("Input grid format not recognized as 1D for this task.")


    grid_size = len(input_list)

    # 1. Initialize the output grid with the background color (white, 0).
    output_list = [WHITE] * grid_size

    # 2. Locate the pivot (maroon pixel) and place it in the output.
    pivot_index = find_pixel(input_list, MAROON)
    if pivot_index is None:
        # Handle error: Maroon pixel not found (though examples guarantee it)
        # For robustness, maybe return input or raise error
        print("Warning: Maroon pivot pixel not found.")
        # Returning input as a safe default for now
        # Reshape back to 1xN list of lists
        return [output_list] # Return initialized grid

    output_list[pivot_index] = MAROON

    # 3. Identify the object (contiguous block of non-white, non-maroon).
    object_info = find_object(input_list, [WHITE, MAROON])
    if object_info is None:
        # Handle error: Object not found
        print("Warning: Movable object not found.")
         # Reshape back to 1xN list of lists
        return [output_list] # Return grid with only pivot placed

    obj_start, obj_end, obj_color = object_info
    obj_len = obj_end - obj_start + 1

    # 4. Determine if the object is left or right of the pivot.
    # 5. Calculate the gap size.
    gap_size = 0
    is_left = False
    if obj_end < pivot_index:
        is_left = True
        # Calculate gap: pixels between object end and pivot start
        gap_size = pivot_index - (obj_end + 1)
    elif obj_start > pivot_index:
        is_left = False
        # Calculate gap: pixels between pivot end and object start
        gap_size = obj_start - (pivot_index + 1)
    else:
        # This case (object overlapping pivot) shouldn't occur based on examples
        print("Warning: Object overlaps with pivot.")
        # Reshape back to 1xN list of lists
        return [output_list]


    # 6. Calculate the new object position.
    new_obj_start = -1
    new_obj_end = -1
    if is_left:
        # Object was left, move it to the right
        new_obj_start = pivot_index + 1 + gap_size
        new_obj_end = new_obj_start + obj_len - 1
    else:
        # Object was right, move it to the left
        new_obj_end = pivot_index - 1 - gap_size
        new_obj_start = new_obj_end - obj_len + 1

    # Check bounds to prevent errors if logic leads to out-of-bounds placement
    if new_obj_start < 0 or new_obj_end >= grid_size:
        print(f"Warning: Calculated new object position ({new_obj_start}-{new_obj_end}) is out of bounds for grid size {grid_size}.")
        # Reshape back to 1xN list of lists
        return [output_list] # Return grid with only pivot

    # 7. Place the object in the output grid.
    for i in range(new_obj_start, new_obj_end + 1):
        output_list[i] = obj_color

    # Reshape back to 1xN list of lists format expected by ARC
    return [output_list]
