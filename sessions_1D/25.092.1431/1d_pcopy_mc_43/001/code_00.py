import math
import copy

"""
Transforms a 1D grid by expanding a single non-white pixel into a block.
The size of the new block is determined by the size of the other non-white 
block present in the input grid. The new block retains the color of the 
original single pixel and is centered at its position. The original multi-pixel 
block remains unchanged.
"""

def find_objects(grid):
    """
    Identifies contiguous blocks of non-white pixels (objects) in a 1D grid.

    Args:
        grid: A list of integers representing the 1D grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'color', 'start', 'end', and 'size'. Returns an
        empty list if no non-white pixels are found.
    """
    objects = []
    in_object = False
    current_object = {}
    grid_len = len(grid)

    for i, pixel in enumerate(grid):
        is_non_white = pixel != 0
        
        if is_non_white and not in_object:
            # Start of a new object
            in_object = True
            current_object = {'color': pixel, 'start': i, 'size': 1}
        elif is_non_white and in_object:
            # Continuation of the current object
            if pixel == current_object['color']:
                current_object['size'] += 1
            else:
                # Different color encountered, end previous object and start new
                current_object['end'] = i - 1
                objects.append(current_object)
                current_object = {'color': pixel, 'start': i, 'size': 1}
        elif not is_non_white and in_object:
            # End of the current object
            in_object = False
            current_object['end'] = i - 1
            objects.append(current_object)
            current_object = {}

    # Handle object that extends to the end of the grid
    if in_object:
        current_object['end'] = grid_len - 1
        objects.append(current_object)
        
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the 1D output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = copy.deepcopy(input_grid)
    grid_len = len(input_grid)

    # 1. & 2. Scan the input grid to identify all contiguous blocks of non-white pixels.
    objects = find_objects(input_grid)

    # Expect exactly two objects based on the examples
    if len(objects) != 2:
        # Handle unexpected cases, though based on provided examples, 
        # this shouldn't happen. Returning input might be a safe default.
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning original grid.")
        return output_grid 

    # 3. & 4. Identify the single-pixel object and the multi-pixel object.
    single_pixel_object = None
    multi_pixel_object = None
    for obj in objects:
        if obj['size'] == 1:
            single_pixel_object = obj
        elif obj['size'] > 1:
            multi_pixel_object = obj

    # Check if both types of objects were found
    if single_pixel_object is None or multi_pixel_object is None:
        print("Warning: Could not find both a single-pixel and a multi-pixel object. Returning original grid.")
        return output_grid

    # Record properties
    C = single_pixel_object['color']
    P = single_pixel_object['start'] # For a single pixel, start == end
    S = multi_pixel_object['size']

    # 5. Calculate the start index for the new block
    start_index = P - math.floor(S / 2)
    
    # 6. Calculate the end index for the new block
    # The block has size S, so it spans S indices.
    # If start_index is the first index, the last index is start_index + S - 1.
    end_index = start_index + S - 1 

    # 7. Modify the output grid: Fill the pixels with color C.
    # Ensure indices are within bounds
    effective_start = max(0, start_index)
    effective_end = min(grid_len - 1, end_index)
    
    for i in range(effective_start, effective_end + 1):
        output_grid[i] = C
        
    return output_grid