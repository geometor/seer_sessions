import numpy as np

"""
Transforms a 1D input grid based on the following rules:
1. Create an output array of the same size as the input array, filled entirely with the background color (white, 0).
2. Identify the contiguous block of pixels in the input array that represent the "main object" (i.e., are neither white (0) nor magenta (6)). Record its color, starting index, and length.
3. Identify the index of the single "marker object" pixel (magenta, 6) in the input array. Record its index.
4. Calculate the new starting index for the main object by adding 2 to its original starting index.
5. Place the main object (using its recorded color and length) into the output array starting at the calculated new index. Ensure the placement respects the array boundaries; if the object extends beyond the end of the array, only place the part that fits.
6. Place the marker object (magenta, 6) into the output array at its original index. This placement occurs regardless of whether it overwrites the background or part of the main object already placed.
7. Return the modified output array.
"""

def find_main_object(grid):
    """
    Finds the first contiguous block of non-white (0), non-magenta (6) color.

    Args:
        grid (np.array): The 1D input grid.

    Returns:
        tuple: (color, start_index, length) of the main object,
               or (-1, -1, 0) if not found.
    """
    color = -1
    start_index = -1
    length = 0
    in_object = False
    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 6: # Found a potential start or continuation
            if not in_object: # Start of a new object
                color = pixel
                start_index = i
                length = 1
                in_object = True
            elif pixel == color: # Continue the current object
                 length += 1
            else: # Different non-background/marker color, means end of current object
                 break
        elif in_object: # Found background (0) or marker (6) after being in an object
            # End of the object
            break
            
    # If no object was ever found
    if start_index == -1:
        return -1, -1, 0
        
    return color, start_index, length

def find_marker_object(grid, marker_color=6):
    """
    Finds the index of the first occurrence of the marker pixel color.

    Args:
        grid (np.array): The 1D input grid.
        marker_color (int): The color of the marker object to find. Default is 6 (magenta).

    Returns:
        int: The index of the marker object, or -1 if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return -1 # Marker not found


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure input is a numpy array for easier slicing and manipulation
    grid = np.array(input_grid)
    grid_size = len(grid)

    # 1. Initialize output_grid with background color (0)
    output_grid = np.zeros(grid_size, dtype=int)

    # 2. Identify the main object
    main_color, main_start_index, main_length = find_main_object(grid)

    # 3. Identify the marker object (magenta, 6)
    marker_index = find_marker_object(grid, marker_color=6)

    # Proceed only if both objects are found in the input
    if main_start_index != -1 and marker_index != -1:
        # 4. Calculate the new start index for the main object
        new_main_start_index = main_start_index + 2

        # 5. Place the main object in the output grid, handling boundaries
        # Check if the new start index is within the grid bounds
        if new_main_start_index < grid_size:
            # Calculate the effective length that fits within the grid
            placeable_length = min(main_length, grid_size - new_main_start_index)
            # Calculate the end index for slicing
            end_index = new_main_start_index + placeable_length
            # Assign the main object's color to the calculated slice
            output_grid[new_main_start_index:end_index] = main_color

        # 6. Place the marker object in the output grid at its original index
        # Check bounds just in case, though marker_index should be valid if found != -1
        if 0 <= marker_index < grid_size:
            output_grid[marker_index] = 6 # Magenta color

    # 7. Return the modified output grid as a standard Python list
    return output_grid.tolist()