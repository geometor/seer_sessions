import numpy as np
import collections

"""
Identify all contiguous groups (objects) of the non-background color in the input grid (treated as 1D).
Determine the size (length) of each object.
Find the object with the largest size.
Create an output grid of the same size as the input, filled with the background color.
Copy only the pixels corresponding to the largest object into the output grid at their original positions.
"""

def find_objects_1d(grid_1d, primary_color):
    """
    Finds contiguous blocks of the primary_color in a 1D list.

    Args:
        grid_1d (list): The 1D input grid (list of integers).
        primary_color (int): The color to find objects of.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and has 'start', 'end', 'color', and 'size' keys.
              Returns an empty list if no objects are found.
    """
    objects = []
    current_object = None
    for i, color in enumerate(grid_1d):
        if color == primary_color:
            # If we find the primary color, start or extend the current object
            if current_object is None:
                # Start a new object
                current_object = {'start': i, 'end': i, 'color': color}
            else:
                # Extend the current object
                current_object['end'] = i
        else:
            # If we find a different color, and we were tracking an object,
            # finalize the previous object
            if current_object is not None:
                current_object['size'] = current_object['end'] - current_object['start'] + 1
                objects.append(current_object)
                current_object = None # Reset for the next potential object

    # After the loop, check if we were still tracking an object
    if current_object is not None:
        current_object['size'] = current_object['end'] - current_object['start'] + 1
        objects.append(current_object)

    return objects

def transform(input_grid):
    """
    Identifies the largest contiguous block of the non-background color in a 1D input grid
    and returns a new grid containing only that block, with the rest as background.

    Args:
        input_grid (list): A 1D list representing the input grid.

    Returns:
        list: A 1D list representing the output grid.
    """
    # Convert input to a list if it's a numpy array (often the case in ARC)
    if isinstance(input_grid, np.ndarray):
        # Check if it's effectively 1D (1xN or Nx1) and flatten
        if input_grid.shape[0] == 1 or input_grid.shape[1] == 1:
            grid_list = input_grid.flatten().tolist()
        else:
            # Handle unexpected 2D input - return input or raise error?
            # For this specific task based on examples, we expect 1D.
            # Let's assume it's already flattened or represents a single row/column.
            # If it's multi-row/col and not flat, this logic might fail.
            # We'll proceed assuming it can be treated as 1D.
            grid_list = input_grid.flatten().tolist()
    else:
        grid_list = list(input_grid) # Ensure it's a list

    if not grid_list:
        return []

    # Determine background and primary colors
    counts = collections.Counter(grid_list)
    background_color = 0 # Default assumption for ARC
    primary_color = -1
    
    # Find the most frequent color, assume it's background if it's 0 or covers most area
    # Find the non-background color
    most_common = counts.most_common()
    if most_common[0][0] == 0:
        background_color = 0
        if len(most_common) > 1:
            primary_color = most_common[1][0]
    elif len(most_common) > 0 : # If 0 is not the most common, find the single non-zero color
         non_zeros = [c for c in counts if c != 0]
         if len(non_zeros) == 1:
             primary_color = non_zeros[0]
             # Decide background based on frequency if 0 exists
             if 0 in counts:
                 background_color = 0
             else: # Case with no zeros - pick least frequent as primary? Or most frequent as background?
                  # Based on examples, 0 is always background.
                  # If no 0, this case is undefined by examples. Let's default background to most frequent.
                  background_color = most_common[0][0]
                  if len(most_common) > 1:
                      primary_color = most_common[1][0] # This might be wrong if multiple non-background colors exist equally
                  else: # Only one color exists
                      primary_color = -1 # No distinct primary color



    # Handle case where only one color exists or no clear primary color found
    if primary_color == -1:
        # If only background color exists, return as is (or all background?)
        # Let's return a grid of background color
         return [background_color] * len(grid_list)


    # Find all objects of the primary color
    objects = find_objects_1d(grid_list, primary_color)

    # If no objects of the primary color are found, return the background grid
    if not objects:
        return [background_color] * len(grid_list)

    # Find the largest object
    largest_object = max(objects, key=lambda obj: obj['size'])

    # Initialize output_grid with the background color
    output_grid = [background_color] * len(grid_list)

    # Copy the largest object to the output grid
    start = largest_object['start']
    end = largest_object['end']
    color = largest_object['color']
    for i in range(start, end + 1):
        output_grid[i] = color

    return output_grid