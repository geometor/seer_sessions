import numpy as np
import math

"""
Transforms a 1xN grid by identifying two non-white objects: a single pixel and a 
multi-pixel horizontal block. The single pixel is expanded into a new horizontal 
block of the same color, centered at the single pixel's original position. The 
size (width) of this new block is equal to the size (width) of the original 
multi-pixel block. The original multi-pixel block remains unchanged in the output. 
The transformation assumes the input grid has exactly one row.
"""

def find_objects_1d(row_data):
    """
    Identifies contiguous blocks of non-zero pixels (objects) in a 1D numpy array.

    Args:
        row_data: A 1D numpy array representing a row of the grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its 'color', 'start' (column index), 'end' (column index), 
        and 'size'. Returns an empty list if no non-zero pixels are found.
    """
    objects = []
    in_object = False
    current_object = {}
    row_len = len(row_data)

    for i, pixel in enumerate(row_data):
        is_non_zero = pixel != 0
        
        if is_non_zero and not in_object:
            # Start of a new object
            in_object = True
            current_object = {'color': pixel, 'start': i, 'size': 1}
        elif is_non_zero and in_object:
            # Continuation of the current object
            if pixel == current_object['color']:
                current_object['size'] += 1
            else:
                # Different color encountered, end previous object and start new one
                current_object['end'] = i - 1
                objects.append(current_object)
                # Start the new object
                current_object = {'color': pixel, 'start': i, 'size': 1}
                in_object = True # Still in an object (the new one)
        elif not is_non_zero and in_object:
            # End of the current object (hit background)
            in_object = False
            current_object['end'] = i - 1
            objects.append(current_object)
            current_object = {} # Reset

    # Handle object that extends exactly to the end of the row
    if in_object:
        current_object['end'] = row_len - 1
        objects.append(current_object)
        
    # Post-process to ensure all objects have an 'end' index, 
    # especially single-pixel ones.
    for obj in objects:
        if 'end' not in obj:
             obj['end'] = obj['start']
             
    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid. 
                    Expected to have shape (1, N).

    Returns:
        A 2D numpy array representing the transformed output grid. Returns a 
        copy of the input if the assumptions (1 row, specific objects) aren't met.
    """
    # Check if input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
        print("Error: Input must be a 2D NumPy array.")
        return np.copy(input_grid) if isinstance(input_grid, np.ndarray) else np.array([])

    # Get grid dimensions
    height, width = input_grid.shape

    # Assumption check: Grid must have exactly one row based on examples
    if height != 1:
        # print(f"Warning: Expected grid height 1, found {height}. Returning copy.")
        return np.copy(input_grid)

    # Initialize output_grid as a deep copy of the input
    output_grid = np.copy(input_grid)
    
    # Extract the first (and only) row for analysis
    row_data = input_grid[0]

    # 1. Identify all contiguous blocks of non-zero pixels in the row
    objects = find_objects_1d(row_data)

    # 2. Expect exactly two objects: one single-pixel, one multi-pixel
    if len(objects) != 2:
        # Return original grid if assumption is violated
        # print(f"Warning: Expected 2 objects, found {len(objects)}. Returning copy.")
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
    #    print("Warning: Could not find both a single-pixel and multi-pixel object. Returning copy.")
       return output_grid

    # 4. Extract properties needed for transformation
    target_color = single_pixel_object['color']
    # Position P is the column index of the single pixel
    target_position = single_pixel_object['start'] 
    # Size S is the width of the reference object
    reference_size = multi_pixel_object['size']

    # 5. Calculate the start and end column indices for the new block
    # Center the new block of size 'reference_size' at 'target_position'
    offset = math.floor(reference_size / 2)
    new_start_col = target_position - offset
    # The block includes 'reference_size' pixels starting from 'new_start_col'
    new_end_col = new_start_col + reference_size - 1 

    # 6. Modify the output grid's first row: Fill the pixels for the new block
    # Iterate through the calculated column range for the new block
    for j in range(new_start_col, new_end_col + 1):
        # Ensure the column index is within the grid boundaries before modification
        if 0 <= j < width:
            output_grid[0, j] = target_color
            
    # The original multi-pixel block is preserved because we started with a copy
    # and only overwrote pixels in the area of the new block. Overlap is handled
    # implicitly as the original block's pixels would be overwritten if the new
    # block expands into its space (though this doesn't happen in the examples).

    return output_grid