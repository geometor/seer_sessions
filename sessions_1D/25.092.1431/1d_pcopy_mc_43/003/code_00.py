import math
import copy

"""
Transforms a 1D grid by identifying two non-white objects: a single pixel and a 
multi-pixel block. The single pixel is expanded into a new block of the same 
color, centered at the single pixel's original position. The size of this new 
block is equal to the size of the original multi-pixel block. The original 
multi-pixel block remains unchanged in the output.
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
        is_non_white = pixel != 0 # Use standard integer comparison
        
        if is_non_white and not in_object:
            # Start of a new object
            in_object = True
            current_object = {'color': pixel, 'start': i, 'size': 1}
        elif is_non_white and in_object:
            # Continuation of the current object
            if pixel == current_object['color']:
                current_object['size'] += 1
            else:
                # Different color encountered, end previous object and start new one
                current_object['end'] = i - 1
                objects.append(current_object)
                current_object = {'color': pixel, 'start': i, 'size': 1}
                in_object = True # Still in an object (the new one)
        elif not is_non_white and in_object:
            # End of the current object (hit background)
            in_object = False
            current_object['end'] = i - 1
            objects.append(current_object)
            current_object = {} # Reset for safety

    # Handle object that extends exactly to the end of the grid
    if in_object:
        current_object['end'] = grid_len - 1
        objects.append(current_object)
        
    # Post-process to add 'end' index for single-pixel objects found
    for obj in objects:
        if 'end' not in obj:
             obj['end'] = obj['start']
             
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of integers representing the 1D input grid.

    Returns:
        A list of integers representing the 1D output grid.
    """
    # initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    grid_len = len(input_grid)

    # 1. Identify all contiguous blocks of non-white pixels
    objects = find_objects(input_grid)

    # 2. Expect exactly two objects: one single-pixel, one multi-pixel
    if len(objects) != 2:
        # Return original grid if assumption is violated (as per examples)
        # Consider logging a warning in a real scenario
        return output_grid 

    # 3. Find the single-pixel ('target') and multi-pixel ('reference') objects
    single_pixel_object = None
    multi_pixel_object = None
    for obj in objects:
        if obj['size'] == 1:
            single_pixel_object = obj
        elif obj['size'] > 1:
            multi_pixel_object = obj

    # Check if both types were correctly identified
    if single_pixel_object is None or multi_pixel_object is None:
       # Return original grid if assumption is violated
        return output_grid

    # 4. Extract properties needed for transformation
    target_color = single_pixel_object['color']
    target_position = single_pixel_object['start'] # Index of the single pixel
    reference_size = multi_pixel_object['size']

    # 5. Calculate the start and end indices for the new block
    # Center the new block of size 'reference_size' at 'target_position'
    offset = math.floor(reference_size / 2)
    new_start_index = target_position - offset
    # The block includes 'reference_size' pixels starting from 'new_start_index'
    new_end_index = new_start_index + reference_size - 1 

    # 6. Modify the output grid: Fill the pixels for the new block
    # Iterate through the calculated range for the new block
    for i in range(new_start_index, new_end_index + 1):
        # Ensure the index is within the grid boundaries before changing the pixel
        if 0 <= i < grid_len:
            output_grid[i] = target_color
            
    # The original multi-pixel block is preserved because we started with a copy
    # and only overwrite pixels in the area of the new block.

    return output_grid