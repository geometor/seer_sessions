import numpy as np
from typing import List, Dict, Tuple, Optional

"""
Transformation Rule Description:

1.  The input grid is always a single row (1D).
2.  Identify the single non-white color (value > 0) present in the input row. If no non-white color exists, return the input unchanged.
3.  Locate all contiguous horizontal segments (objects) composed of this non-white color. Record the starting position (column index) and length of each segment in the order they appear. If no objects are found, return the input unchanged.
4.  Determine the maximum length (`max_len`) among all identified segments.
5.  Create a "template segment" which is a 1D array (or list) of length `max_len`, filled with the identified non-white color.
6.  Initialize an output row of the same size as the input, filled entirely with the background color (white, 0).
7.  Iterate through the list of identified objects based on their order of appearance (using index `i`). For each object:
    a.  Retrieve its original starting position (`original_start`).
    b.  Calculate the target starting position (`target_start`) in the output row:
        *   If it's the first object (`i == 0`), `target_start` is equal to `original_start`.
        *   If it's not the first object (`i > 0`), `target_start` is equal to `original_start - 1`.
    c.  Ensure `target_start` is not negative. If it is, clamp it to 0.
    d.  Calculate the target ending position (exclusive) in the output grid: `target_end = min(target_start + max_len, grid_length)`.
    e.  Calculate the actual number of pixels to copy from the template: `copy_length = target_end - target_start`.
    f.  If `copy_length` is greater than 0, copy the first `copy_length` pixels from the `template_segment` into the `output_grid` starting at index `target_start` and ending at index `target_end - 1`. Overwrite any previous values in that range.
8.  Return the resulting output row, formatted as a list containing a single list (e.g., [[...row elements...]]).
"""

def find_objects_1d(grid_1d: np.ndarray, color: int) -> List[Dict[str, int]]:
    """
    Finds contiguous segments (objects) of a given color in a 1D numpy array.

    Args:
        grid_1d (np.ndarray): The 1D input grid (single row).
        color (int): The color of the objects to find.

    Returns:
        List[Dict[str, int]]: A list of dictionaries, where each dictionary 
                               represents an object and contains 'start' (index) 
                               and 'length'. Returns an empty list if no objects 
                               of the specified color are found.
    """
    objects = []
    in_object = False
    start_index = -1
    for i, pixel in enumerate(grid_1d):
        if pixel == color and not in_object:
            # Start of a new object
            in_object = True
            start_index = i
        elif pixel != color and in_object:
            # End of an object (transition from color to non-color)
            in_object = False
            length = i - start_index
            objects.append({'start': start_index, 'length': length})
            start_index = -1 # Reset start index
            
    # Check if the grid ends with an object
    if in_object:
        length = len(grid_1d) - start_index
        objects.append({'start': start_index, 'length': length})
        
    return objects

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (List[List[int]]): A list containing a single list 
                                       representing the input row. 
                                       Example: [[0, 0, 5, 5, 5, 0, ...]]

    Returns:
        List[List[int]]: A list containing a single list representing 
                         the transformed output row.
    """
    # Ensure input is valid and convert to numpy array
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # Handle potential numpy array input from testing harness if needed
        if isinstance(input_grid, np.ndarray) and input_grid.ndim == 1:
            input_row_np = input_grid.astype(int)
        elif isinstance(input_grid, np.ndarray) and input_grid.ndim == 2 and input_grid.shape[0] == 1:
             input_row_np = input_grid[0].astype(int)
        else:
            # Invalid format
            # Consider raising an error or returning input depending on expected behavior
            return input_grid # Or raise ValueError("Invalid input format")
    else:
        input_row_np = np.array(input_grid[0], dtype=int)
        
    grid_len = len(input_row_np)

    # 1. Identify the non-white color
    non_white_color: Optional[int] = None
    for pixel in input_row_np:
        if pixel != 0:
            non_white_color = int(pixel) # Ensure it's standard int
            break

    # If no non-white color found or grid is empty, return the original grid
    # formatted correctly as list of lists.
    if non_white_color is None or grid_len == 0:
        return [input_row_np.tolist()]

    # 2. Locate all objects of this color
    objects = find_objects_1d(input_row_np, non_white_color)

    # Handle case with no objects found
    if not objects:
        return [input_row_np.tolist()]

    # 3. Determine the maximum length
    max_length = 0
    for obj in objects:
        max_length = max(max_length, obj['length'])
    
    # If max_length is somehow 0 (e.g., empty objects found?), return original
    if max_length == 0: 
         return [input_row_np.tolist()]
         
    # 4. Define the template segment
    template_segment = np.full(max_length, non_white_color, dtype=int)

    # 5. Create output grid initialized with background color (0)
    output_grid_np = np.zeros(grid_len, dtype=int)

    # 6. Iterate through objects and place template segment
    for i, obj in enumerate(objects):
        original_start = obj['start']
        
        # a. Determine target start position
        target_start: int
        if i == 0:
            target_start = original_start
        else:
            target_start = original_start - 1

        # b. Clamp target_start to 0 if it became negative
        target_start = max(0, target_start)
            
        # c. Calculate target end position (exclusive)
        target_end = min(target_start + max_length, grid_len)

        # d. Calculate actual length to copy from template
        copy_length = target_end - target_start

        # e. Write the template segment portion to the output grid
        if copy_length > 0:
            # Ensure slicing the template doesn't go out of bounds 
            # (shouldn't happen if max_length > 0 and copy_length > 0)
            template_portion = template_segment[:copy_length]
            output_grid_np[target_start:target_end] = template_portion

    # 7. Return the modified grid as a list of lists
    return [output_grid_np.tolist()]