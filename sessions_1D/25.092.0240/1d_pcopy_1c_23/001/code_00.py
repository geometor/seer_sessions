import numpy as np
import logging

# Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
Transformation Rule Description:

1.  Identify the single non-white color present in the input row.
2.  Locate all contiguous horizontal segments (objects) of this non-white color, noting their starting position and length in order of appearance.
3.  Determine the maximum length (`max_len`) among all identified segments.
4.  Create a "template segment" consisting of `max_len` pixels of the identified non-white color.
5.  Initialize an output row of the same size as the input, filled with the background color (white, 0).
6.  Iterate through the located objects based on their order of appearance (index `i`):
    a.  Determine the target starting position (`target_start`) in the output row:
        *   If it's the first object (`i == 0`), `target_start` is the object's original starting position.
        *   If it's not the first object (`i > 0`), `target_start` is the object's original starting position minus 1.
    b.  Calculate the portion of the template segment to write, ensuring it fits within the grid boundaries starting from `target_start`.
    c.  Write this portion of the template segment into the output row at the calculated position (`target_start`).
7.  Return the resulting output row.
"""

def find_objects_1d(grid_1d, color):
    """
    Finds contiguous segments (objects) of a given color in a 1D numpy array.

    Args:
        grid_1d (np.array): The 1D input grid (single row).
        color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'start' (index) and 'length'. Returns an empty list
              if no objects of the specified color are found.
    """
    objects = []
    in_object = False
    start_index = -1
    # logging.debug(f"Searching for color {color} in grid: {grid_1d}")
    for i, pixel in enumerate(grid_1d):
        if pixel == color and not in_object:
            # Start of a new object
            in_object = True
            start_index = i
            # logging.debug(f"Found start of object at index {i}")
        elif pixel != color and in_object:
            # End of an object (transition from color to non-color)
            in_object = False
            length = i - start_index
            objects.append({'start': start_index, 'length': length})
            # logging.debug(f"Found end of object. Start: {start_index}, Length: {length}")
            start_index = -1 # Reset start index
            
    # Check if the grid ends with an object
    if in_object:
        length = len(grid_1d) - start_index
        objects.append({'start': start_index, 'length': length})
        # logging.debug(f"Found end of object at end of grid. Start: {start_index}, Length: {length}")
        
    # logging.info(f"Found {len(objects)} objects: {objects}")
    return objects

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid_list (list): A list containing a single list representing the input row. 
                               Example: [[0, 0, 5, 5, 5, 0, 0, 0, 5, 0, ...]]

    Returns:
        list: A list containing a single list representing the transformed output row.
              Example: [[0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, ...]]
    """
    # Ensure input is a list containing one list (the row)
    if not isinstance(input_grid_list, list) or len(input_grid_list) != 1 or not isinstance(input_grid_list[0], list):
        # logging.error("Invalid input format. Expected a list containing a single list.")
        return [] # Or raise an error

    # Convert input list to a 1D numpy array
    input_grid = np.array(input_grid_list[0], dtype=int)
    grid_len = len(input_grid)
    # logging.info(f"Input grid (len {grid_len}): {input_grid}")

    # 1. Identify the non-white color
    non_white_color = -1
    for pixel in input_grid:
        if pixel != 0:
            non_white_color = pixel
            break

    # If no non-white color found or grid is empty, return a copy of the original grid
    if non_white_color == -1 or grid_len == 0:
        # logging.info("No non-white color found or grid empty. Returning original grid.")
        return [input_grid.tolist()] # Return as list of lists

    # logging.info(f"Identified non-white color: {non_white_color}")

    # 2. Locate all objects of this color
    objects = find_objects_1d(input_grid, non_white_color)

    # Handle case with no objects of the found color
    if not objects:
        # logging.info(f"No objects found for color {non_white_color}. Returning original grid.")
        return [input_grid.tolist()]

    # 3. Determine the maximum length
    max_length = 0
    for obj in objects:
        if obj['length'] > max_length:
            max_length = obj['length']
    
    if max_length == 0: # Should not happen if objects were found, but safeguard
         # logging.warning("Max length is 0, though objects were found. Returning original grid.")
         return [input_grid.tolist()]
         
    # logging.info(f"Maximum object length: {max_length}")

    # 4. Define the template segment
    template_segment = np.full(max_length, non_white_color, dtype=int)
    # logging.debug(f"Template segment: {template_segment}")

    # 5. Create output grid initialized with background color (0)
    output_grid = np.zeros(grid_len, dtype=int)
    # logging.debug(f"Initialized output grid: {output_grid}")

    # 6. Iterate through objects and place template segment
    for i, obj in enumerate(objects):
        original_start = obj['start']
        
        # a. Determine target start position
        if i == 0:
            target_start = original_start
            # logging.debug(f"Object {i} (first): original_start={original_start}, target_start={target_start}")
        else:
            target_start = original_start - 1
            # logging.debug(f"Object {i}: original_start={original_start}, target_start={target_start}")

        # Ensure target_start is not negative
        if target_start < 0:
            # logging.warning(f"Calculated target_start {target_start} is negative. Clamping to 0.")
            target_start = 0
            
        # b. Calculate target end position (exclusive)
        target_end = min(target_start + max_length, grid_len)
        # logging.debug(f"Calculated target_end (exclusive): {target_end}")

        # c. Calculate actual length to copy from template
        copy_length = target_end - target_start
        # logging.debug(f"Calculated copy_length: {copy_length}")

        # d. Write the template segment portion to the output grid
        if copy_length > 0:
            # logging.debug(f"Writing template[:{copy_length}] to output[{target_start}:{target_end}]")
            output_grid[target_start:target_end] = template_segment[:copy_length]
            # logging.debug(f"Output grid after writing object {i}: {output_grid}")
        # else:
            # logging.debug(f"Skipping write for object {i} as copy_length is not positive.")

    # 7. Return the modified grid as a list of lists
    # logging.info(f"Final output grid: {output_grid}")
    return [output_grid.tolist()]