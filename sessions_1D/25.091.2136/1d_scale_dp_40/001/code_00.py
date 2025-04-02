import numpy as np

"""
Transformation rule:
1. Find the orange pixel (color 7) in the 1D input array.
2. Look backwards from the position just before the orange pixel. Identify the contiguous sequence of white pixels (color 0) immediately preceding the orange pixel.
3. Determine the 'fill color' which is the color of the pixel immediately preceding this sequence of white pixels.
4. Replace the identified sequence of white pixels with the 'fill color'.
5. Keep all other pixels unchanged.
"""

def find_last_occurrence(arr, value):
    """Finds the index of the last occurrence of a value in a list."""
    try:
        # Reverse the list, find the first index, and adjust for original list length
        return len(arr) - 1 - arr[::-1].index(value)
    except ValueError:
        return -1 # Not found

def transform(input_grid):
    """
    Applies the transformation rule to fill white pixels between a color block
    and an orange marker with that color.

    Args:
        input_grid (list): A 1D list representing the input pixel array.

    Returns:
        list: A 1D list representing the transformed pixel array.
    """
    # Ensure input is treated as a 1D list
    if isinstance(input_grid, np.ndarray):
        # Flatten if it's a numpy array, handle potential >1D cases
        input_list = input_grid.flatten().tolist()
    elif isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         # Handle case of list of lists (e.g., [[1, 2, 3]])
        input_list = input_grid[0]
    else:
        input_list = list(input_grid) # Assume it's already a 1D iterable

    # Initialize output_grid as a copy of the input
    output_list = list(input_list)
    
    # 1. Find the index of the orange pixel (marker)
    try:
        # Assuming there's only one orange pixel or we care about the first one
        # Based on examples, there seems to be only one relevant orange marker
        orange_index = input_list.index(7) 
    except ValueError:
        # If no orange pixel is found, return the original grid copy
        return output_list

    # 2. Find the sequence of white pixels preceding the orange pixel
    fill_end_index = orange_index  # The sequence ends just before the orange pixel
    current_index = orange_index - 1

    # Iterate backwards while the pixel is white and index is valid
    while current_index >= 0 and input_list[current_index] == 0:
        current_index -= 1

    # The sequence of white pixels starts at the index after the last non-white pixel found
    fill_start_index = current_index + 1
    
    # Check if any white pixels were actually found between a preceding color and orange
    if fill_start_index >= fill_end_index:
        # No white pixels to fill, return the copy
        return output_list

    # 3. Determine the fill color (the color at current_index)
    # Check if current_index is valid (i.e., we didn't fall off the beginning)
    if current_index < 0:
        # This case shouldn't happen if the pattern holds (color -> white -> orange)
        # but handle defensively: maybe no fill color found before white sequence
         return output_list # Or potentially raise an error, depending on requirements
        
    fill_color = input_list[current_index]

    # 4. Replace the identified white pixels with the fill color in the output list
    for i in range(fill_start_index, fill_end_index):
         # Double check we are only replacing 0s (though the backward scan ensures this)
         if output_list[i] == 0:
            output_list[i] = fill_color

    # 5. Return the modified output list
    return output_list